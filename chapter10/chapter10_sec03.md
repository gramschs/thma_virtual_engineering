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
    """Berechnet Segmentlängen und lokale Neigungswinkel."""
    laengen, winkel_rad = [], []
    for i in range(len(wegpunkte) - 1):
        delta       = wegpunkte[i+1] - wegpunkte[i]
        laenge      = np.linalg.norm(delta)
        delta_horiz = np.sqrt(delta[0]**2 + delta[2]**2)
        theta       = np.arctan2(delta[1], delta_horiz)
        laengen.append(laenge)
        winkel_rad.append(theta)
    return np.array(laengen), np.array(winkel_rad)

# Wegpunkte (aus CloudCompare exportiert oder manuell definiert)
wegpunkte = np.array([
    [0.00, 0.000, 0.00], [0.12, -0.020, 0.01],
    [0.25, -0.040, 0.02], [0.38, -0.055, 0.025],
    [0.51, -0.065, 0.030], [0.63, -0.080, 0.025],
    [0.76, -0.095, 0.015], [0.88, -0.110, 0.005],
    [1.00, -0.120, 0.000],
])

laengen, winkel_rad = bahn_aus_wegpunkten(wegpunkte)

# Physikparameter
m    = 0.1      # Masse in kg
G    = 9.81     # Erdbeschleunigung in m/s²
MU_H = 0.30     # Haftreibungskoeffizient
MU_G = 0.20     # Gleitreibungskoeffizient

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
import numpy as np
import math

# (Wegpunkte und laengen/winkel_rad wie oben definiert)

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
Stillstand – aber nur, wenn sie auch langsam genug ist. Eine Kugel, die
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
import numpy as np
import math

def bahn_aus_wegpunkten(wegpunkte):
    laengen, winkel_rad = [], []
    for i in range(len(wegpunkte) - 1):
        delta       = wegpunkte[i+1] - wegpunkte[i]
        laenge      = np.linalg.norm(delta)
        delta_horiz = np.sqrt(delta[0]**2 + delta[2]**2)
        theta       = np.arctan2(delta[1], delta_horiz)
        laengen.append(laenge)
        winkel_rad.append(theta)
    return np.array(laengen), np.array(winkel_rad)

wegpunkte = np.array([
    [0.00, 0.000, 0.00], [0.12, -0.020, 0.01],
    [0.25, -0.040, 0.02], [0.38, -0.055, 0.025],
    [0.51, -0.065, 0.030], [0.63, -0.080, 0.025],
    [0.76, -0.095, 0.015], [0.88, -0.110, 0.005],
    [1.00, -0.120, 0.000],
])
laengen, winkel_rad = bahn_aus_wegpunkten(wegpunkte)

m, G, MU_H, MU_G = 0.1, 9.81, 0.30, 0.20
dt = 0.005

# Anfangszustand
v_aktuell = 0.0
t_gesamt  = 0.0
gleitet   = False

# Ergebnislisten
t_verlauf = [0.0]
v_verlauf = [0.0]
s_verlauf = [0.0]
s_gesamt  = 0.0

# Äußere Schleife: über alle Segmente
for seg_idx in range(len(laengen)):
    theta    = winkel_rad[seg_idx]
    L        = laengen[seg_idx]
    F_N      = m * G * math.cos(theta)
    F_H      = m * G * math.sin(theta)
    F_haft   = MU_H * F_N
    F_gleit  = MU_G  * F_N

    # Zustandscheck beim Segmenteintritt
    if v_aktuell > 1e-6 or abs(F_H) > F_haft:
        gleitet = True

    s_seg = 0.0   # zurückgelegte Distanz im aktuellen Segment

    # Innere Schleife: Euler-Cromer-Schritte im Segment
    while s_seg < L:
        if gleitet:
            a = (-F_H - F_gleit) / m   # Gefälle: F_H negativ, Reibung bremst
        else:
            a = 0.0

        # Euler-Cromer-Schritt: erst Geschwindigkeit, dann Position
        v_aktuell += a * dt
        if v_aktuell < 0:
            v_aktuell = 0.0

        s_seg    += v_aktuell * dt
        s_gesamt += v_aktuell * dt
        t_gesamt += dt

        t_verlauf.append(t_gesamt)
        v_verlauf.append(v_aktuell)
        s_verlauf.append(s_gesamt)

print(f"Bewegungszeit:      {t_gesamt:.4f} s")
print(f"Endgeschwindigkeit: {v_aktuell:.4f} m/s")
print(f"Gesamtstrecke:      {s_gesamt:.4f} m")
```

```{admonition} Warum ist die Reihenfolge in der inneren Schleife wichtig?
:class: note
Der Zustandscheck (`gleitet`) findet einmalig beim Segmenteintritt statt. Die
Geschwindigkeit `v_aktuell` und die zurückgelegte Distanz `s_seg` innerhalb
des Segments werden in jedem Zeitschritt aktualisiert. Die Geschwindigkeit am
Ende des Segments ist gleichzeitig die Anfangsgeschwindigkeit des nächsten –
das ist die nahtlose Weitergabe, die eine korrekte segmentübergreifende Physik
gewährleistet.
```

## Schritt 4: Ergebnis mit Messung vergleichen

Wir stellen die simulierte Geschwindigkeit als Funktion der Zeit dar und
markieren den Messwert aus Abschnitt 10.2 als vertikale Linie:

```{code-cell} python
import plotly.graph_objects as go

T_MESSUNG = 1.51   # s – aus Stoppuhr (Abschnitt 10.2)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=t_verlauf, y=v_verlauf,
    mode='lines', name='Simulation',
    line=dict(color='royalblue', width=2)
))
fig.add_vline(
    x=T_MESSUNG, line_dash='dash', line_color='tomato',
    annotation_text=f'Messung: {T_MESSUNG} s'
)
fig.add_vline(
    x=t_gesamt, line_dash='dot', line_color='royalblue',
    annotation_text=f'Simulation: {t_gesamt:.3f} s'
)

fig.update_layout(
    title='Segmentweise Simulation: Geschwindigkeit über Zeit',
    xaxis_title='Zeit (s)',
    yaxis_title='Geschwindigkeit (m/s)'
)
fig.show()

delta_rel = (t_gesamt - T_MESSUNG) / T_MESSUNG * 100
print(f"Relative Abweichung: {delta_rel:+.2f} %")
```

## Schritt 5: μ_G durch Kalibrierung bestimmen

*Warum stimmt die Simulation nicht sofort mit der Messung überein?*

Der Reibungskoeffizient aus der Literatur ist eine Näherung. Wir können ihn
durch Kalibrierung an unserem Messwert verbessern: Wir suchen das μ_G, das
die simulierte Bewegungszeit dem Messwert am nächsten bringt.

```{code-cell} python
import numpy as np
import math

def simuliere(wegpunkte, m, G, MU_H, MU_G, dt=0.005):
    """Gibt die Bewegungszeit zurück."""
    laengen, winkel_rad = bahn_aus_wegpunkten(wegpunkte)
    v, t, gleitet = 0.0, 0.0, False
    for seg_idx in range(len(laengen)):
        theta   = winkel_rad[seg_idx]
        L       = laengen[seg_idx]
        F_N     = m * G * math.cos(theta)
        F_H     = m * G * math.sin(theta)
        F_haft  = MU_H * F_N
        F_gleit = MU_G  * F_N
        if v > 1e-6 or abs(F_H) > F_haft:
            gleitet = True
        s = 0.0
        while s < L:
            a  = (-F_H - F_gleit) / m if gleitet else 0.0
            v += a * dt
            if v < 0:
                return t   # Kugel stoppt vorzeitig
            s += v * dt
            t += dt
    return t

T_MESSUNG = 1.51

# Bisektionsverfahren: μ_G auf vier Dezimalstellen genau bestimmen
mu_lo, mu_hi = 0.05, 0.45
for _ in range(40):
    mu_mid  = (mu_lo + mu_hi) / 2
    t_mid   = simuliere(wegpunkte, m, G, MU_H, mu_mid)
    if t_mid < T_MESSUNG:
        mu_lo = mu_mid   # zu wenig Reibung → Bewegungszeit zu kurz
    else:
        mu_hi = mu_mid

t_kalibriert = simuliere(wegpunkte, m, G, MU_H, mu_mid)
print(f"Kalibriertes μ_G:    {mu_mid:.4f}")
print(f"Simulationszeit:     {t_kalibriert:.5f} s")
print(f"Messung:             {T_MESSUNG:.5f} s")
print(f"Restabweichung:      {abs(t_kalibriert - T_MESSUNG) / T_MESSUNG * 100:.4f} %")
```

```{admonition} Mini-Übung
:class: tip
Verändern Sie `MU_G` manuell von 0.10 auf 0.35 in Schritten von 0.05 und
tragen Sie die simulierte Bewegungszeit in einer Tabelle ein. Vergleichen
Sie diese mit dem kalibrierten Wert aus der Bisektion. Entspricht der
kalibrierte Wert einem der Schritte, oder liegt er zwischen zwei
Tabellenwerten?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import pandas as pd

T_MESSUNG = 1.51
daten     = []

for mu_g in np.arange(0.10, 0.40, 0.05):
    t = simuliere(wegpunkte, m, G, MU_H, round(mu_g, 2))
    abw = (t - T_MESSUNG) / T_MESSUNG * 100
    daten.append({"μ_G": round(mu_g, 2),
                  "t_sim (s)": round(t, 4),
                  "Δ (%)": round(abw, 2)})

df = pd.DataFrame(daten)
print(df.to_string(index=False))
```

Der kalibrierte Wert liegt fast immer zwischen zwei Tabelleneinträgen, weil
die Schrittweite von 0.05 zu grob ist, um den Messwert exakt zu treffen.
Die Bisektion bestimmt μ_G auf vier Dezimalstellen – weit feiner als jede
manuelle Tabelle.
````

## Zusammenfassung und Ausblick

In diesem Abschnitt haben wir die vollständige segmentweise Simulation
implementiert. Die Funktion `bahn_aus_wegpunkten` liefert Längen und Winkel
aller Segmente; die doppelte Euler-Cromer-Schleife verarbeitet sie
nacheinander und gibt die Geschwindigkeit nahtlos von Segment zu Segment
weiter. Der Vergleich mit dem Messwert zeigt, dass der Reibungskoeffizient
der wichtigste Stellhebel für die Genauigkeit ist. Das Bisektionsverfahren
bestimmt ihn auf vier Dezimalstellen in weniger als 40 Iterationen.

Im nächsten Abschnitt verlassen wir die reine Zahlenebene und bringen die
Simulation zum Leuchten: Ursina lädt das echte `.obj`-Mesh der Kugelbahn und
spielt die soeben berechnete Trajektorie als 3D-Animation ab.
