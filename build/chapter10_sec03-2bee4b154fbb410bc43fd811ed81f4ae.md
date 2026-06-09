---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 10.3 Python: Segmentweise Simulation und Validierung

Wir haben die Wegpunkte der Bahn in Abschnitt 10.1 berechnet und die
Messwerkzeuge in Abschnitt 10.2 kennengelernt. Jetzt kommen beide Bausteine
zusammen. Die Euler-Cromer-Schleife aus Kapitel 9 verarbeitet in diesem
Abschnitt nicht mehr ein einziges gerades Segment, sondern wandert von
Wegpunkt zu Wegpunkt durch die gesamte Bahn. Das Ergebnis ist eine
Zeitreihe von Geschwindigkeit und Position, die wir direkt mit unseren
Messwerten vergleichen.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können einen segmentweisen Euler-Cromer-Loop implementieren, der
  die Geschwindigkeit nahtlos von einem Segment zum nächsten weitergibt.
* [ ] Sie können die Kräfte pro Segment aus dem lokalen Neigungswinkel
  berechnen und den Haft-/Gleitzustand segmentweise prüfen.
* [ ] Sie können das Simulationsergebnis mit einem Messwert aus Abschnitt
  10.2 vergleichen und die relative Abweichung berechnen.
* [ ] Sie können den Gleitreibungskoeffizienten durch Kalibrierung an einem
  Messwert bestimmen.
```

## Schritt 1: Geometrie und Parameter vorbereiten

Wir beginnen mit der Funktion `bahn_aus_wegpunkten` aus Abschnitt 10.1 und
den Physikparametern aus Kapitel 9. Alle Parameter stehen am Anfang des
Skripts als Konstanten:

```{code-cell} python
import numpy as np
import math

def bahn_aus_wegpunkten(wegpunkte):
    """Berechnet Segmentlängen und lokale Neigungswinkel.

    Annahme: Wegpunkte als (x, y, z) in m, z ist die Höhenkoordinate.
    """
    laengen, winkel_rad = [], []
    for i in range(len(wegpunkte) - 1):
        delta  = wegpunkte[i+1] - wegpunkte[i]
        laenge = np.linalg.norm(delta)
        # horizontale Distanz in der x-y-Ebene
        delta_horiz = np.sqrt(delta[0]**2 + delta[1]**2)
        # Neigung: z als Höhe
        theta = np.arctan2(delta[2], delta_horiz)
        laengen.append(laenge)
        winkel_rad.append(theta)
    return np.array(laengen), np.array(winkel_rad)

# Wegpunkte (aus CloudCompare exportiert oder manuell definiert)
# x: Bahnlänge, y: seitliche Lage, z: Höhe (negativ bergab)
wegpunkte = np.array([
    [0.00, 0.000,  0.000],
    [0.12, 0.010, -0.030],  # steil
    [0.25, 0.020, -0.050],  # flacher
    [0.38, 0.025, -0.065],
    [0.51, 0.030, -0.075],
    [0.63, 0.025, -0.090],
    [0.76, 0.015, -0.105],
    [0.88, 0.005, -0.115],
    [1.00, 0.000, -0.120],
])

laengen, winkel_rad = bahn_aus_wegpunkten(wegpunkte)

# Physikparameter
m    = 0.1      # Masse in kg
G    = 9.81     # Erdbeschleunigung in m/s²
MU_H = 0.20     # Haftreibungskoeffizient
MU_G = 0.15     # Gleitreibungskoeffizient
dt = 0.005 # Zeitschritt in s

print(f"Segmente:      {len(laengen)}")
print(f"Gesamtlänge:   {np.sum(laengen):.4f} m")
print(f"Winkelbereich: {np.degrees(winkel_rad.min()):.1f}° "
      f"bis {np.degrees(winkel_rad.max()):.1f}°")
```

## Schritt 2: Kräfte pro Segment berechnen

Für jedes Segment berechnen wir Normalkraft, Hangabtrieb, Haftgrenze und
Gleitreibung einmalig. Diese Werte sind innerhalb eines Segments konstant
und hängen nur vom lokalen Neigungswinkel ab:

```{code-cell} python
F_N_seg        = m * G * np.cos(winkel_rad)
F_H_seg        = m * G * np.sin(winkel_rad)
F_HAFT_MAX_seg = MU_H * F_N_seg
F_GLEIT_seg    = MU_G  * F_N_seg

print(f"{'Seg':>4} {'θ (°)':>7} {'F_H (N)':>9} "
      f"{'F_Haft,max (N)':>15} {'gleitet?':>10}")
for i in range(len(laengen)):
    gleitet = abs(F_H_seg[i]) > F_HAFT_MAX_seg[i]
    print(f"{i+1:>4} {np.degrees(winkel_rad[i]):>7.2f} "
          f"{F_H_seg[i]:>9.4f} {F_HAFT_MAX_seg[i]:>15.4f} "
          f"{'ja' if gleitet else 'nein':>10}")
```

*Was passiert, wenn ein Segment so flach ist, dass die Kugel dort nicht
gleitet?*

Wenn `|F_H| ≤ F_Haft,max`, bremst die Haftreibung die Kugel bis zum
Stillstand, aber nur, wenn sie auch langsam genug ist. Eine Kugel, die
bereits mit hoher Geschwindigkeit in ein flaches Segment eintritt, wird durch
die Gleitreibung abgebremst, kommt aber möglicherweise erst im nächsten
Segment zum Stillstand. Die segmentweise Schleife behandelt diesen Fall durch
die Geschwindigkeitsweitergabe zwischen Segmenten.

## Schritt 3: Die segmentweise Schleife

Das Kernstück der Simulation ist eine doppelte Schleife: Die äußere Schleife
iteriert über alle Segmente, die innere führt die Euler-Cromer-Schritte
innerhalb eines Segments durch. Die Geschwindigkeit wird nahtlos von einem
Segment zum nächsten weitergegeben:

```{code-cell} python
# Anfangszustand
v_aktuell = 0.0   # m/s (optional: kleiner Startstoß, z.B. 0.05)
t_gesamt  = 0.0
s_gesamt  = 0.0

t_verlauf = [0.0]
v_verlauf = [v_aktuell]
s_verlauf = [0.0]

stopped = False

# Äußere Schleife: über alle Segmente
for seg_idx, (L, theta) in enumerate(zip(laengen, winkel_rad), start=1):
    # Kräfte im aktuellen Segment
    F_N       = m * G * math.cos(theta)
    F_H       = m * G * math.sin(theta)   # kann negativ sein (Gefälle)
    F_H_along = -F_H                      # Betrag in Richtung "bergab" (>= 0)
    F_haft    = MU_H * F_N
    F_gleit   = MU_G * F_N

    # Prüfen, ob die Kugel in diesem Segment überhaupt losrollen kann
    if F_H_along <= F_haft and v_aktuell <= 1e-6:
        print(f"Kugel bleibt in Segment {seg_idx} stehen "
              f"(|F_H| <= F_Haft,max und v ≈ 0).")
        stopped = True
        break

    s_seg = 0.0  # zurückgelegte Distanz im aktuellen Segment

    # Innere Schleife: Euler-Cromer-Schritte im Segment
    while s_seg < L:
        # Wenn die Kugel (fast) steht und Haftung ausreicht, endet die Bewegung
        if v_aktuell <= 1e-6 and F_H_along <= F_haft:
            v_aktuell = 0.0
            stopped = True
            break

        # Gleitreibung entlang der Bahn (nur Bewegung bergab betrachtet)
        a = (F_H_along - F_gleit) / m

        # Euler-Cromer: erst Geschwindigkeit, dann Weg und Zeit
        v_aktuell += a * dt
        if v_aktuell < 0:
            v_aktuell = 0.0

        s_step   = v_aktuell * dt
        s_seg   += s_step
        s_gesamt += s_step
        t_gesamt += dt

        t_verlauf.append(t_gesamt)
        v_verlauf.append(v_aktuell)
        s_verlauf.append(s_gesamt)

    if stopped:
        break

print(f"Bewegungszeit:      {t_gesamt:.4f} s")
print(f"Endgeschwindigkeit: {v_aktuell:.4f} m/s")
print(f"Gesamtstrecke:      {s_gesamt:.4f} m")
```

```{admonition} Warum ist die Reihenfolge in der inneren Schleife wichtig?
:class: note
Der Zustandscheck (`gleitet`) findet einmalig beim Segmenteintritt statt. Die
Geschwindigkeit `v_aktuell` und die zurückgelegte Distanz `s_seg` innerhalb
des Segments werden in jedem Zeitschritt aktualisiert. Die Geschwindigkeit am
Ende des Segments ist gleichzeitig die Anfangsgeschwindigkeit des nächsten.
Das ist die nahtlose Weitergabe, die eine korrekte segmentübergreifende Physik
gewährleistet.
```
