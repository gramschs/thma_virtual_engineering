---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 10.4 Ursina: Das echte Mesh in Bewegung

In Abschnitt 10.3 haben wir die Simulation als Liste von Zeitstempeln und
Geschwindigkeiten berechnet. Aber eine Tabelle voller Zahlen ist kein
überzeugendes Ergebnis. Das bereinigte Mesh unserer Kugelbahn, das wir in
den Kapiteln 4 bis 6 mit CloudCompare aufbereitet haben, wartet als
`.obj`-Datei auf uns. Jetzt laden wir es in Ursina, setzen die Kugel auf
das echte Modell und spielen die berechnete Trajektorie als 3D-Animation ab.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können erklären, warum Physikberechnung und Visualisierung in
  getrennten Schritten implementiert werden, und den Vorteil dieser Trennung
  benennen.
* [ ] Sie können eine vorberechnete Trajektorie als Liste von Positionen und
  Zeitstempeln speichern.
* [ ] Sie können ein `.obj`-Mesh aus CloudCompare in Ursina laden, skalieren
  und korrekt ausrichten.
* [ ] Sie können die Trajektorie mit `np.searchsorted` framegenau in der
  `update()`-Schleife abspielen.
```

## Warum trennen wir Physik und Darstellung?

In Kapitel 9 haben wir Physik und Ursina direkt kombiniert: Die
`update()`-Schleife berechnete die Physik und bewegte die Kugel gleichzeitig.
Das funktioniert gut für eine einfache gerade Rampe. Für die vollständige
segmentweise Simulation aus Abschnitt 10.3 wäre dieser Ansatz jedoch
problematisch.

*Warum?*

Die segmentweise Schleife in 10.3 läuft mit einem festen Zeitschritt von
0.005 s. Ursinas `update()`-Schleife läuft mit der Framerate des Rechners,
typischerweise 60 fps, was `time.dt ≈ 0.017 s` ergibt. Diese unterschiedlichen
Zeitskalen würden die Physik ungenau machen.

Die saubere Lösung ist die Trennung: Wir berechnen die gesamte Trajektorie
einmalig in reinem Python mit festem Zeitschritt, speichern sie als Liste und
lassen Ursina diese Liste framegenau abspielen. Die Physik ist damit
unabhängig vom Rechner, und Ursina kümmert sich nur um die Darstellung.

## Schritt 1: Trajektorie vorberechnen

Wir erweitern die Simulationsfunktion aus Abschnitt 10.3 so, dass sie nicht
nur die Endwerte, sondern die vollständige 3D-Position in jedem Zeitschritt
zurückgibt:

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


def simuliere_trajektorie(wegpunkte, m=0.1, G=9.81,
                           MU_H=0.30, MU_G=0.20, dt=0.005):
    """
    Berechnet die vollständige Trajektorie als Liste von (Zeit, 3D-Position).

    Rückgabe:
        trajektorie : list of (t, np.array([x, y, z]))
    """
    laengen, winkel_rad = bahn_aus_wegpunkten(wegpunkte)
    trajektorie = [(0.0, wegpunkte[0].copy())]

    v_aktuell = 0.0
    t_gesamt  = 0.0
    gleitet   = False

    for seg_idx in range(len(laengen)):
        theta    = winkel_rad[seg_idx]
        L        = laengen[seg_idx]
        start    = wegpunkte[seg_idx]
        richtung = (wegpunkte[seg_idx + 1] - start) / L
        F_N      = m * G * math.cos(theta)
        F_H      = m * G * math.sin(theta)
        F_haft   = MU_H * F_N
        F_gleit  = MU_G  * F_N

        if v_aktuell > 1e-6 or abs(F_H) > F_haft:
            gleitet = True

        s_seg = 0.0
        while s_seg < L:
            a          = (-F_H - F_gleit) / m if gleitet else 0.0
            v_aktuell += a * dt
            if v_aktuell < 0:
                v_aktuell = 0.0
            s_seg    += v_aktuell * dt
            t_gesamt += dt
            pos_3d    = start + richtung * min(s_seg, L)
            trajektorie.append((t_gesamt, pos_3d.copy()))

    return trajektorie


# Wegpunkte aus Abschnitt 10.1
wegpunkte = np.array([
    [0.00, 0.000, 0.00], [0.12, -0.020, 0.01],
    [0.25, -0.040, 0.02], [0.38, -0.055, 0.025],
    [0.51, -0.065, 0.030], [0.63, -0.080, 0.025],
    [0.76, -0.095, 0.015], [0.88, -0.110, 0.005],
    [1.00, -0.120, 0.000],
])

trajektorie = simuliere_trajektorie(wegpunkte)

print(f"Trajektorie berechnet: {len(trajektorie)} Punkte")
print(f"Bewegungszeit:         {trajektorie[-1][0]:.4f} s")
print(f"Startposition:         {trajektorie[0][1]}")
print(f"Endposition:           {trajektorie[-1][1]}")
```

## Schritt 2: Trajektorie für die Wiedergabe aufbereiten

Für eine schnelle Positionssuche nach Zeit wandeln wir die Liste in
NumPy-Arrays um:

```{code-cell} python
import numpy as np

# Zeitstempel und Positionen als NumPy-Arrays
traj_t   = np.array([p[0] for p in trajektorie])
traj_pos = np.array([p[1] for p in trajektorie])

# Geschwindigkeit aus Differenzquotient vorberechnen
traj_v = np.zeros(len(traj_t))
for i in range(1, len(traj_t)):
    dp        = np.linalg.norm(traj_pos[i] - traj_pos[i-1])
    dt_i      = traj_t[i] - traj_t[i-1]
    traj_v[i] = dp / dt_i if dt_i > 0 else 0.0

print(f"Maximale Geschwindigkeit: {traj_v.max():.3f} m/s")
print(f"Zeitauflösung:            {np.mean(np.diff(traj_t)):.5f} s")
```

## Schritt 3: Das Mesh und die Kugel in Ursina laden

Jetzt öffnen wir Ursina, laden das Mesh und platzieren die Kugel am
Startpunkt der Trajektorie. Die `.obj`-Datei aus CloudCompare legen wir in
denselben Ordner wie das Python-Skript.

```{admonition} Hinweis: Datei als .py-Skript ausführen
:class: note
Dieser Abschnitt enthält Ursina-Code. Alles zusammen in eine Datei kopieren,
zum Beispiel `kugelbahn_10.py`, und mit `python kugelbahn_10.py` starten.
```

```{code-cell} python
# Datei: kugelbahn_10.py  –  Schritte 1 und 2 oben einfügen, dann:

from ursina import *
import numpy as np
import math

# --- Trajektorie berechnen (Schritte 1 und 2 aus diesem Abschnitt) ---
# [bahn_aus_wegpunkten, simuliere_trajektorie, wegpunkte, traj_t, traj_pos, traj_v]
# hier einfügen ...

# --- Szene ---
app = Ursina(title='Kugelbahn – Vollständige Simulation', width=1200, height=700)
window.color = color.white

# Kugelbahn-Mesh laden
# Die .obj-Datei stammt aus CloudCompare (Kapitel 4–6)
kugelbahn = Entity(
    model    = 'kugelbahn_bereinigt',   # Dateiname ohne .obj
    color    = color.gray,
    scale    = 1,                        # Mesh ist bereits in Metern
    position = (0, 0, 0)
)
```

```{admonition} Mesh korrekt ausrichten
:class: note
CloudCompare exportiert Meshes standardmäßig mit z-up-Koordinatensystem.
Ursina erwartet y-up. Falls das Mesh nach dem Laden auf der Seite liegt,
hilft `kugelbahn.rotation_x = -90`. Falls es zu groß oder zu klein erscheint,
war das Mesh möglicherweise in Millimetern exportiert: dann `scale = 0.001`
setzen.
```

## Schritt 4: Kugel und Anzeige einrichten

```{code-cell} python
# (Fortsetzung von kugelbahn_10.py)

# Kugel am Startpunkt der Trajektorie
kugel = Entity(
    model    = 'sphere',
    color    = color.red,
    scale    = 0.03,                         # entspricht Radius 0.015 m
    position = Vec3(*traj_pos[0])
)

# Kamera für freie Navigation
EditorCamera()

# Statusanzeige
anzeige = Text(
    text     = 't = 0.000 s | v = 0.000 m/s',
    position = (-0.85, 0.45),
    scale    = 1.2,
    color    = color.black
)
```

## Schritt 5: Trajektorie in der update()-Schleife abspielen

Die `update()`-Schleife sucht für die aktuelle Simulationszeit den
nächstgelegenen Trajektoriepunkt mit `np.searchsorted` und setzt die
Kugelposition:

```{code-cell} python
# (Fortsetzung von kugelbahn_10.py)

sim_zeit = 0.0
laeuft   = True
ROLLZEIT = traj_t[-1]

def update():
    global sim_zeit, laeuft

    if not laeuft:
        return

    sim_zeit += time.dt
    if sim_zeit >= ROLLZEIT:
        sim_zeit = ROLLZEIT
        laeuft   = False

    # Nächstgelegenen Trajektoriepunkt suchen
    idx            = min(np.searchsorted(traj_t, sim_zeit), len(traj_pos) - 1)
    kugel.position = Vec3(*traj_pos[idx])

    anzeige.text = f't = {sim_zeit:.3f} s | v = {traj_v[idx]:.3f} m/s'
```

```{admonition} Wie funktioniert np.searchsorted?
:class: note
`np.searchsorted(traj_t, sim_zeit)` gibt den Index zurück, an dem
`sim_zeit` in das sortierte Array `traj_t` eingefügt werden müsste, damit
es sortiert bleibt. Das ist der Index des nächsten Trajektoriepunkts nach
der aktuellen Simulationszeit – in O(log n) und damit sehr schnell, auch
bei langen Trajektorien.
```

## Schritt 6: Das vollständige Skript

Hier alles zusammen als lauffähige Datei:

```{code-cell} python
# kugelbahn_10.py – vollständiges Skript

from ursina import *
import numpy as np
import math

# --- Physik: Trajektorie berechnen ---

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

def simuliere_trajektorie(wegpunkte, m=0.1, G=9.81,
                           MU_H=0.30, MU_G=0.20, dt=0.005):
    laengen, winkel_rad = bahn_aus_wegpunkten(wegpunkte)
    trajektorie = [(0.0, wegpunkte[0].copy())]
    v, t, gleitet = 0.0, 0.0, False
    for seg_idx in range(len(laengen)):
        theta    = winkel_rad[seg_idx]
        L        = laengen[seg_idx]
        start    = wegpunkte[seg_idx]
        richtung = (wegpunkte[seg_idx + 1] - start) / L
        F_N      = m * G * math.cos(theta)
        F_H      = m * G * math.sin(theta)
        F_gleit  = MU_G * F_N
        if v > 1e-6 or abs(F_H) > MU_H * F_N:
            gleitet = True
        s = 0.0
        while s < L:
            a  = (-F_H - F_gleit) / m if gleitet else 0.0
            v += a * dt
            if v < 0:
                v = 0.0
            s += v * dt
            t += dt
            trajektorie.append((t, (start + richtung * min(s, L)).copy()))
    return trajektorie

wegpunkte = np.array([
    [0.00, 0.000, 0.00], [0.12, -0.020, 0.01],
    [0.25, -0.040, 0.02], [0.38, -0.055, 0.025],
    [0.51, -0.065, 0.030], [0.63, -0.080, 0.025],
    [0.76, -0.095, 0.015], [0.88, -0.110, 0.005],
    [1.00, -0.120, 0.000],
])

trajektorie = simuliere_trajektorie(wegpunkte)
traj_t      = np.array([p[0] for p in trajektorie])
traj_pos    = np.array([p[1] for p in trajektorie])
traj_v      = np.zeros(len(traj_t))
for i in range(1, len(traj_t)):
    dp         = np.linalg.norm(traj_pos[i] - traj_pos[i-1])
    dt_i       = traj_t[i] - traj_t[i-1]
    traj_v[i]  = dp / dt_i if dt_i > 0 else 0.0

# --- Ursina: Szene und Wiedergabe ---

app = Ursina(title='Kugelbahn – Vollständige Simulation',
             width=1200, height=700)
window.color = color.white

kugelbahn = Entity(
    model    = 'kugelbahn_bereinigt',
    color    = color.gray,
    scale    = 1,
    position = (0, 0, 0)
)

kugel = Entity(
    model    = 'sphere',
    color    = color.red,
    scale    = 0.03,
    position = Vec3(*traj_pos[0])
)

anzeige = Text(
    text     = '',
    position = (-0.85, 0.45),
    scale    = 1.2,
    color    = color.black
)

EditorCamera()

sim_zeit = 0.0
laeuft   = True
ROLLZEIT = traj_t[-1]

def update():
    global sim_zeit, laeuft
    if not laeuft:
        return
    sim_zeit       += time.dt
    sim_zeit        = min(sim_zeit, ROLLZEIT)
    laeuft          = sim_zeit < ROLLZEIT
    idx             = min(np.searchsorted(traj_t, sim_zeit), len(traj_pos)-1)
    kugel.position  = Vec3(*traj_pos[idx])
    anzeige.text    = f't = {sim_zeit:.3f} s | v = {traj_v[idx]:.3f} m/s'

def input(key):
    global sim_zeit, laeuft
    if key == 'r':                   # R zum Neustarten
        sim_zeit       = 0.0
        laeuft         = True
        kugel.position = Vec3(*traj_pos[0])

app.run()
```

```{admonition} Checkliste: Was prüfen wir nach dem ersten Lauf?
:class: note
* **Mesh sichtbar:** Die Kugelbahn erscheint im Fenster.
* **Mesh korrekt ausgerichtet:** Falls auf der Seite: `rotation_x = -90`.
* **Kugel startet am richtigen Punkt:** Erster Wegpunkt ist der Startpunkt.
* **Bewegungsrichtung stimmt:** Die Kugel bewegt sich von Start nach Ende.
* **Anzeige läuft:** Zeit und Geschwindigkeit werden aktualisiert.
* **Neustart funktioniert:** Taste R setzt die Simulation zurück.
```

```{admonition} Mini-Übung
:class: tip
Erweitern Sie das Skript um Spurpunkte: Setzen Sie alle 0.05 s eine kleine
türkise Kugel an der aktuellen Position. Verwenden Sie dazu einen
`spur_timer`-Mechanismus wie in Kapitel 8.2.

Beobachten Sie: Sind die Abstände zwischen den Spurpunkten gleichmäßig?
Was sagt eine ungleichmäßige Verteilung über die Geschwindigkeit der Kugel
auf verschiedenen Bahnabschnitten aus?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
# In der update()-Schleife ergänzen:
spur_timer = 0.0   # als globale Variable vor update() definieren
SPUR_INT   = 0.05

def update():
    global sim_zeit, laeuft, spur_timer
    if not laeuft:
        return
    sim_zeit   += time.dt
    sim_zeit    = min(sim_zeit, ROLLZEIT)
    laeuft      = sim_zeit < ROLLZEIT
    idx         = min(np.searchsorted(traj_t, sim_zeit), len(traj_pos)-1)
    kugel.position = Vec3(*traj_pos[idx])

    spur_timer += time.dt
    if spur_timer >= SPUR_INT:
        Entity(model='sphere', color=color.cyan,
               scale=0.01, position=kugel.position)
        spur_timer = 0.0

    anzeige.text = f't = {sim_zeit:.3f} s | v = {traj_v[idx]:.3f} m/s'
```

Ungleichmäßige Abstände zwischen Spurpunkten zeigen, dass die Kugel auf
steilen Abschnitten schneller ist: In denselben 0.05 s legt sie dort mehr
Weg zurück. Das ist eine visuelle Bestätigung der Physik aus Abschnitt 10.3.
````

## Zusammenfassung und Ausblick

In diesem Abschnitt haben wir die Trennung von Physik und Darstellung
konsequent umgesetzt: Die Trajektorie wird einmalig mit festem Zeitschritt
berechnet und als NumPy-Array gespeichert; Ursina spielt sie framegenau ab,
ohne die Physik zu kennen. Das echte `.obj`-Mesh der Kugelbahn dient dabei
als Kulisse und schließt den Kreis des gesamten Workflows: Dasselbe Objekt,
das wir in Kapitel 2 fotografiert, in Kapitel 3 rekonstruiert, in den Kapiteln
4 bis 6 bereinigt und in Kapitel 7 gedruckt haben, rollt jetzt als rote Kugel
auf seinem eigenen digitalen Modell.

Im nächsten Abschnitt warten die Übungen zu Kapitel 10, darunter ein
Mini-Projekt, das die vollständige Pipeline von der Wegpunktaufnahme bis zur
Ursina-Animation auf das eigene Objekt anwendet.
