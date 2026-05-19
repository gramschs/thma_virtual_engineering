---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 10.4 Ursina: Das echte Mesh in Bewegung

In Abschnitt 10.3 hat die Kugel eine Bahn aus Zylindern durchlaufen – eine
saubere Simulation, aber kein besonders eindrucksvoller Anblick. Das bereinigte
Mesh unserer Kugelbahn, das wir in Kapitel 4 bis 6 mit CloudCompare aufbereitet
haben, liegt als `.obj`-Datei vor. Warum nicht die Kugel direkt auf dem echten
Modell rollen lassen? Genau das ermöglicht **Ursina**: Wir laden das Mesh als
3D-Kulisse, platzieren die Kugel darauf und spielen die in Abschnitt 10.3
berechnete Trajektorie als Animation ab.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können Ursina installieren und eine einfache 3D-Szene mit einer
  Entity aufbauen.
* [ ] Sie können ein `.obj`-Mesh aus CloudCompare in Ursina laden, skalieren
  und korrekt ausrichten.
* [ ] Sie können eine vorberechnete Trajektorie als Liste von Positionen und
  Zeitstempeln in Ursinas `update()`-Loop abspielen.
* [ ] Sie können den Unterschied zwischen Physik-Loop und Render-Loop
  erklären und begründen, warum wir beide trennen.
```

## Warum Ursina statt VPython?

VPython ist für interaktive Physikdemonstrationen ausgelegt – es hat eine
einfache API und läuft im Browser. Ursina ist eine vollwertige
Python-Game-Engine, die auf Panda3D aufbaut. Der entscheidende Unterschied für
unsere Zwecke: Ursina kann beliebige 3D-Modelle laden, darunter genau das
`.obj`-Mesh, das unsere Kugelbahn beschreibt. Die Visualisierung sieht dadurch
deutlich realistischer aus.

*Bedeutet das, dass wir die Physik in Ursina neu schreiben müssen?*

Nein – und das ist ein wichtiges Konzept. Wir **trennen Physik und Darstellung**:
Die Physikberechnung führen wir wie in Abschnitt 10.3 als reines Python-Skript
durch und speichern die Trajektorie als Liste von Positionen. Ursina spielt
diese Trajektorie dann als Animation ab. Die Engine muss nichts von der Physik
wissen.

## Schritt 1: Ursina installieren

```{admonition} Installation
:class: note
```
pip install ursina
```

Ursina benötigt Python 3.12 oder neuer. Die Installation zieht automatisch
Panda3D als Abhängigkeit mit. Auf manchen Systemen ist außerdem `pip install
pillow` nötig, falls Texturen nicht geladen werden.

Optionale Abhängigkeit für das automatische Konvertieren von `.blend`-Dateien:
Blender muss lokal installiert sein – Ursina findet es automatisch.
```

Ein minimales Ursina-Programm hat immer dieselbe Grundstruktur:

```{code-cell} python
# Minimales Ursina-Beispiel (lokal ausführen, nicht im Notebook):
# from ursina import *
#
# app = Ursina()
#
# wuerfel = Entity(model='cube', color=color.orange, scale=2)
#
# def update():
#     wuerfel.rotation_y += 1   # dreht sich jede Frame um 1°
#
# app.run()   # öffnet das Fenster und startet den Loop
```

```{admonition} Hinweis: Ursina läuft nicht im Jupyter Notebook
:class: note
Ursina öffnet ein eigenständiges Desktop-Fenster und kann nicht in einem
Jupyter Notebook ausgeführt werden. Die Code-Zellen in diesem Abschnitt sind
als Vorlagen gedacht, die in einer separaten `.py`-Datei gespeichert und
direkt mit Python gestartet werden:

```
python kugelbahn_ursina.py
```

Im Jupyter Book sind sie als ausführbarer Code dargestellt, der kopiert und
lokal verwendet werden kann.
```

## Schritt 2: Physik vorberechnen und Trajektorie speichern

Bevor wir Ursina starten, berechnen wir die vollständige Trajektorie mit dem
Modell aus Abschnitt 10.3. Das Ergebnis ist eine Liste von Positionen im
3D-Raum und den zugehörigen Zeitstempeln.

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


def simuliere_trajektorie(wegpunkte, m=0.1, G=9.81, MU_H=0.30,
                          MU_G=0.20, dt=0.005):
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

        F_N     = m * G * math.cos(theta)
        F_H     = m * G * math.sin(theta)
        F_haft  = MU_H * F_N
        F_gleit = MU_G * F_N

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

            pos_3d = start + richtung * min(s_seg, L)
            trajektorie.append((t_gesamt, pos_3d.copy()))

    return trajektorie


# Beispielwegpunkte (in der Praxis: aus CloudCompare-CSV laden)
wegpunkte = np.array([
    [0.00, 0.000, 0.00], [0.12, -0.020, 0.01],
    [0.25, -0.040, 0.02], [0.38, -0.055, 0.025],
    [0.51, -0.065, 0.030], [0.63, -0.080, 0.025],
    [0.76, -0.095, 0.015], [0.88, -0.110, 0.005],
    [1.00, -0.120, 0.000],
])

trajektorie = simuliere_trajektorie(wegpunkte)

print(f"Trajektorie berechnet: {len(trajektorie)} Punkte")
print(f"Rollzeit:              {trajektorie[-1][0]:.4f} s")
print(f"Startposition:         {trajektorie[0][1]}")
print(f"Endposition:           {trajektorie[-1][1]}")
```

## Schritt 3: Das Mesh und die Kugel in Ursina

Jetzt öffnen wir Ursina, laden das Mesh und platzieren die Kugel auf dem
Startpunkt der Trajektorie. Die `.obj`-Datei aus CloudCompare legen wir in
denselben Ordner wie das Python-Skript.

```{code-cell} python
# Datei: kugelbahn_ursina.py
# Lokal ausführen mit: python kugelbahn_ursina.py

from ursina import *
import numpy as np
import math

# ----------------------------------------------------------------
# Trajektorie vorberechnen (Funktion aus dem Abschnitt oben)
# ----------------------------------------------------------------
# [bahn_aus_wegpunkten und simuliere_trajektorie hier einfügen]
# ...

wegpunkte = np.array([
    [0.00, 0.000, 0.00], [0.12, -0.020, 0.01],
    [0.25, -0.040, 0.02], [0.38, -0.055, 0.025],
    [0.51, -0.065, 0.030], [0.63, -0.080, 0.025],
    [0.76, -0.095, 0.015], [0.88, -0.110, 0.005],
    [1.00, -0.120, 0.000],
])
trajektorie = simuliere_trajektorie(wegpunkte)

# ----------------------------------------------------------------
# Ursina-Szene
# ----------------------------------------------------------------
app = Ursina(title="Kugelbahn – Ursina", borderless=False)

# Kugelbahn-Mesh laden
# Die .obj-Datei stammt aus CloudCompare (bereinigtes Mesh aus Kapitel 4–6)
# Falls keine eigene Datei vorhanden: 'cube' als Platzhalter verwenden
kugelbahn = Entity(
    model     = 'kugelbahn_bereinigt.obj',   # Pfad zur .obj-Datei
    color     = color.gray,
    scale     = 1,                            # Mesh ist bereits in Metern
    position  = (0, 0, 0),
    # rotation_x = -90  # Falls das Mesh z-up exportiert wurde, hier korrigieren
)

# Kugel
kugel = Entity(
    model    = 'sphere',
    color    = color.red,
    scale    = 0.03,    # Radius 0.015 m → scale 0.03
    position = Vec3(*trajektorie[0][1])
)

# Kamera: EditorCamera erlaubt Mausnavigation (Drehen, Zoomen, Verschieben)
EditorCamera()

# Hintergrundfläche
window.color = color.white
```

```{admonition} Tipp: Mesh korrekt ausrichten
:class: note
CloudCompare exportiert Meshes standardmäßig in einem rechtshändigen
Koordinatensystem mit z-up. Ursina erwartet y-up. Falls das Mesh nach dem
Laden auf der Seite liegt, hilft `kugelbahn.rotation_x = -90`. Falls es
zu groß oder zu klein erscheint, `kugelbahn.scale = 100` ausprobieren (wenn
das Mesh in Millimetern exportiert wurde).
```

## Schritt 4: Trajektorie abspielen

Im `update()`-Loop suchen wir für die aktuelle Simulationszeit den nächstgelegenen
Trajektoriepunkt und setzen die Kugelposition entsprechend. Wir verwenden
`time.dt` – Ursinas eingebaute Zeitdifferenz zwischen zwei Frames – um die
Simulationszeit voranzurücken.

```{code-cell} python
# Fortsetzung von kugelbahn_ursina.py

# Trajektorie als NumPy-Array für schnelle Suche
traj_t   = np.array([p[0] for p in trajektorie])
traj_pos = np.array([p[1] for p in trajektorie])

# Simulationszustand
sim_zeit   = 0.0
laeuft     = True
ROLLZEIT   = traj_t[-1]

def update():
    global sim_zeit, laeuft

    if not laeuft:
        return

    sim_zeit += time.dt

    if sim_zeit >= ROLLZEIT:
        sim_zeit = ROLLZEIT
        laeuft   = False

    # Nächstgelegenen Trajektoriepunkt suchen
    idx          = np.searchsorted(traj_t, sim_zeit)
    idx          = min(idx, len(traj_pos) - 1)
    kugel.position = Vec3(*traj_pos[idx])

app.run()
```

## Schritt 5: Szene aufwerten

Ursina bietet mit wenigen Zeilen deutlich bessere Visualisierungsmöglichkeiten
als VPython. Hier sind drei einfache Verbesserungen:

```{code-cell} python
# Verbesserungen (in die Szene vor app.run() einfügen):

# 1. Beleuchtung
licht = DirectionalLight(shadows=True)
licht.look_at(Vec3(1, -1, -1))
AmbientLight(color=color.rgba(100, 100, 100, 0.1))

# 2. Spur der Kugel (als wachsende Linie)
spur_punkte = []

def update():
    global sim_zeit, laeuft

    if not laeuft:
        return

    sim_zeit  += time.dt
    sim_zeit   = min(sim_zeit, ROLLZEIT)
    laeuft     = sim_zeit < ROLLZEIT

    idx            = np.searchsorted(traj_t, sim_zeit)
    idx            = min(idx, len(traj_pos) - 1)
    pos            = Vec3(*traj_pos[idx])
    kugel.position = pos

    # Spur: kleine Kugeln an jedem 50. Frame
    if int(sim_zeit / time.dt) % 50 == 0:
        Entity(model='sphere', color=color.cyan,
               scale=0.008, position=pos)

# 3. Tastatur: R zum Neustarten
def input(key):
    global sim_zeit, laeuft
    if key == 'r':
        sim_zeit = 0.0
        laeuft   = True
        kugel.position = Vec3(*traj_pos[0])
        print("Simulation neugestartet.")
```

```{admonition} Mini-Übung
:class: tip
Erweitern Sie die Szene um eine `Text`-Anzeige, die die aktuelle
Simulationszeit und Geschwindigkeit in Echtzeit anzeigt. Verwenden Sie
dazu Ursinas eingebautes `Text`-Objekt:

```python
anzeige = Text(text="t = 0.000 s", position=(-0.7, 0.45), scale=1.5)
```

Aktualisieren Sie `anzeige.text` im `update()`-Loop mit der aktuellen
Simulationszeit und der interpolierten Geschwindigkeit.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
from ursina import *
import numpy as np

# [Trajektorie und Szene wie oben aufgebaut]

traj_t   = np.array([p[0] for p in trajektorie])
traj_pos = np.array([p[1] for p in trajektorie])

# Geschwindigkeit aus Differenzquotient vorberechnen
traj_v = np.zeros(len(traj_t))
for i in range(1, len(traj_t)):
    dp = np.linalg.norm(traj_pos[i] - traj_pos[i-1])
    dt = traj_t[i] - traj_t[i-1]
    traj_v[i] = dp / dt if dt > 0 else 0.0

anzeige = Text(
    text     = "t = 0.000 s | v = 0.000 m/s",
    position = (-0.85, 0.45),
    scale    = 1.5,
    color    = color.black
)

sim_zeit = 0.0
laeuft   = True

def update():
    global sim_zeit, laeuft
    if not laeuft:
        return
    sim_zeit          += time.dt
    sim_zeit           = min(sim_zeit, traj_t[-1])
    laeuft             = sim_zeit < traj_t[-1]
    idx                = min(np.searchsorted(traj_t, sim_zeit), len(traj_pos)-1)
    kugel.position     = Vec3(*traj_pos[idx])
    anzeige.text       = (f"t = {sim_zeit:.3f} s | "
                          f"v = {traj_v[idx]:.3f} m/s")

app.run()
```
````

## VPython und Ursina im Vergleich

Nach dem Durcharbeiten beider Abschnitte lässt sich der Unterschied klar
benennen:

| | VPython / Trinket | Ursina |
|---|---|---|
| **Stärke** | Einfache API, läuft im Browser | Echte Meshes, professionelle Optik |
| **Physikloop** | `while True: rate(N)` | `def update():` automatisch |
| **Modelle laden** | Nur Grundkörper | `.obj`, `.gltf`, `.blend` |
| **Installation** | Trinket: keine | `pip install ursina` |
| **Jupyter** | Ja (vpython-Paket) | Nein (Desktop-Fenster) |
| **Empfehlung** | Physik verstehen, schnell iterieren | Finale Präsentation, echtes Mesh |

## Zusammenfassung und Ausblick

In diesem Abschnitt haben wir Ursina als Visualisierungsebene über der
Physiksimulation aus Abschnitt 10.3 gelegt. Das Schlüsselkonzept ist die
Trennung von Physik und Darstellung: Die Trajektorie wird einmal berechnet
und als Liste gespeichert; Ursina spielt sie framegenau ab, ohne die Physik
zu kennen. Das echte `.obj`-Mesh der Kugelbahn dient dabei als Kulisse und
schließt den Kreis: Dasselbe Objekt, das wir in Kapitel 2 fotografiert, in
Kapitel 3 rekonstruiert, in Kapitel 4 bis 6 bereinigt und in Kapitel 7
gedruckt haben, rollt jetzt auch digital auf seinem eigenen Modell.

Im nächsten Abschnitt warten die Übungen zu Kapitel 10 – darunter ein
Mini-Projekt, in dem Sie die vollständige Pipeline von der Wegpunktvorbereitung
über die Simulation bis zum Ursina-Rendering auf Ihr eigenes Objekt anwenden.
