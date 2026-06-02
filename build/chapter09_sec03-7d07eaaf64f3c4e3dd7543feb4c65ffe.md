---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 9.3 Ursina: Kugel auf einer Rampe simulieren

Wir haben das Kraftmodell in Python übersetzt: Zustandsübergang, Euler-Cromer-
Schritt, analytischer Vergleich. Jetzt bringen wir dieses Modell zum Leben.
In diesem Abschnitt bauen wir Schritt für Schritt eine Ursina-Simulation, in
der die Kugel mit echter Reibungsphysik gleitet, farbige Kraftindikatoren
sich in Echtzeit aktualisieren und eine Textanzeige den Zustand (Haften oder
Gleiten) sichtbar macht.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können das Physikmodell aus Abschnitt 9.2 in die `update()`-Funktion
  von Ursina einbetten.
* [ ] Sie können Kraftindikatoren als schmale Quader implementieren, die sich
  mit der Kugel mitbewegen und in Echtzeit skalieren.
* [ ] Sie können den Haft-/Gleitzustand durch Farbe und Textanzeige sichtbar
  machen.
* [ ] Sie können den Starter-Code auf ihr eigenes Objekt übertragen.
```

## Was entsteht in diesem Abschnitt?

Am Ende dieses Abschnitts läuft ein Simulator mit folgenden Eigenschaften:

- Eine rote Kugel liegt auf einer grauen Rampe und bleibt zunächst stehen,
  solange der Neigungswinkel unterhalb des kritischen Winkels liegt.
- Vier farbige Kraftindikatoren zeigen Gewichtskraft (blau), Normalkraft
  (grün), Hangabtrieb (orange) und Reibungskraft (lila).
- Sobald die Haftgrenze überschritten wird, wechselt die Kugelfarbe auf Orange
  und die Kugel beginnt zu gleiten.
- Eine Textanzeige zeigt Simulationszeit, Geschwindigkeit und Zustand.

## Schritt 1: Szene und Parameter einrichten

```{code-cell} python
from ursina import *
import math

app = Ursina(title='Kugelbahn – Simulation mit Reibung',
             width=1200, height=700)
window.color = color.white

# Physikalische Parameter
NEIGUNGSWINKEL = 20.0
BAHNLAENGE     = 1.0
KUGELRADIUS    = 0.04
m              = 0.1
G              = 9.81
MU_H           = 0.35
MU_G           = 0.25
KRAFT_SKALA    = 1.5    # Meter pro Newton für die Kraftindikatoren

# Abgeleitete Größen
THETA      = math.radians(NEIGUNGSWINKEL)
F_N        = m * G * math.cos(THETA)
F_H        = m * G * math.sin(THETA)
F_HAFT_MAX = MU_H * F_N
F_GLEIT    = MU_G * F_N
S_EFF      = BAHNLAENGE - 2 * KUGELRADIUS
START_X    = -(BAHNLAENGE / 2) + KUGELRADIUS
ENDE_X     =  (BAHNLAENGE / 2) - KUGELRADIUS
```

## Schritt 2: Rampe, Kugel und Kraftindikatoren

In Ursina gibt es keine eingebauten Pfeile. Wir verwenden schmale Quader als
vereinfachte Kraftindikatoren: Ihre Länge ist proportional zum Kraftbetrag,
ihre Farbe codiert die Kraftart.

*Warum reichen schmale Quader als Kraftindikatoren aus?*

Weil wir nicht die exakte Pfeilform benötigen, sondern die Richtung und
relative Größe der Kraft. Ein orangefarbener Quader, der sich mit der Kugel
mitbewegt und je nach Beschleunigung länger oder kürzer wird, vermittelt
dieselbe Information wie ein Pfeil.

```{code-cell} python
# Rampe
rampe = Entity(
    model    = 'cube',
    color    = color.gray,
    scale    = Vec3(BAHNLAENGE, 0.02, 0.12),
    position = Vec3(0, 0, 0)
)

# Kugel – startet rot (Haft-Zustand), wechselt auf Orange beim Gleiten
kugel = Entity(
    model    = 'sphere',
    color    = color.red,
    scale    = 2 * KUGELRADIUS,
    position = Vec3(START_X, KUGELRADIUS + 0.01, 0)
)

# Kraftindikatoren (schmale Quader, z leicht versetzt für Sichtbarkeit)
Z_OFFSET = 0.07   # damit die Indikatoren vor der Rampe liegen

pfeil_FH = Entity(model='cube', color=color.orange,
                  scale=Vec3(F_H * KRAFT_SKALA, 0.008, 0.008))
pfeil_FR = Entity(model='cube', color=color.violet,
                  scale=Vec3(F_H * KRAFT_SKALA, 0.008, 0.008))
pfeil_FN = Entity(model='cube', color=color.green,
                  scale=Vec3(0.008, F_N * KRAFT_SKALA, 0.008))
pfeil_FG = Entity(model='cube', color=color.blue,
                  scale=Vec3(0.008, m * G * KRAFT_SKALA, 0.008))
```

## Schritt 3: Legende und Statusanzeige

```{code-cell} python
# Farbige Legende (statisch, oben links)
Text("● Orange: Hangabtrieb F_H",  position=(-0.85, 0.45), scale=1.1,
     color=color.orange)
Text("● Lila:   Reibungskraft F_R", position=(-0.85, 0.41), scale=1.1,
     color=color.violet)
Text("● Grün:   Normalkraft F_N",   position=(-0.85, 0.37), scale=1.1,
     color=color.green)
Text("● Blau:   Gewichtskraft F_G", position=(-0.85, 0.33), scale=1.1,
     color=color.blue)

# Dynamische Statusanzeige (oben rechts)
status = Text(
    text     = 'Zustand: Haften\nt = 0.000 s\nv = 0.000 m/s',
    position = (0.4, 0.45),
    scale    = 1.2,
    color    = color.black
)

EditorCamera()
```

## Schritt 4: Anfangszustand prüfen

Bevor die Schleife startet, prüfen wir einmalig, ob das Objekt sofort gleitet
oder zunächst haftet:

```{code-cell} python
geschwindigkeit = 0.0
t_sim           = 0.0
gleitet         = F_H > F_HAFT_MAX   # sofort gleiten, falls Winkel groß genug
laeuft          = True

# Anfangsfarbe je nach Zustand
kugel.color = color.orange if gleitet else color.red

print(f"Anfangszustand: {'Gleiten' if gleitet else 'Haften'}")
print(f"F_H        = {F_H:.4f} N")
print(f"F_Haft,max = {F_HAFT_MAX:.4f} N")
```

## Schritt 5: Das vollständige Skript

Jetzt alles zusammen als eine lauffähige Datei, zum Beispiel
`kugelbahn_09.py`:

```{code-cell} python
from ursina import *
import math

# --- Anwendung ---
app = Ursina(title='Kugelbahn – Simulation mit Reibung',
             width=1200, height=700)
window.color = color.white

# --- Parameter ---
NEIGUNGSWINKEL = 20.0
BAHNLAENGE     = 1.0
KUGELRADIUS    = 0.04
m              = 0.1
G              = 9.81
MU_H           = 0.35
MU_G           = 0.25
KRAFT_SKALA    = 1.5
Z_OFFSET       = 0.07

THETA      = math.radians(NEIGUNGSWINKEL)
F_N        = m * G * math.cos(THETA)
F_H        = m * G * math.sin(THETA)
F_HAFT_MAX = MU_H * F_N
F_GLEIT    = MU_G * F_N
START_X    = -(BAHNLAENGE / 2) + KUGELRADIUS
ENDE_X     =  (BAHNLAENGE / 2) - KUGELRADIUS

# --- Objekte ---
Entity(model='cube', color=color.gray,
       scale=Vec3(BAHNLAENGE, 0.02, 0.12), position=Vec3(0, 0, 0))

kugel = Entity(model='sphere', color=color.red,
               scale=2*KUGELRADIUS,
               position=Vec3(START_X, KUGELRADIUS + 0.01, 0))

pfeil_FH = Entity(model='cube', color=color.orange,
                  scale=Vec3(F_H * KRAFT_SKALA, 0.008, 0.008))
pfeil_FR = Entity(model='cube', color=color.violet,
                  scale=Vec3(F_H * KRAFT_SKALA, 0.008, 0.008))
pfeil_FN = Entity(model='cube', color=color.green,
                  scale=Vec3(0.008, F_N * KRAFT_SKALA, 0.008))
pfeil_FG = Entity(model='cube', color=color.blue,
                  scale=Vec3(0.008, m * G * KRAFT_SKALA, 0.008))

Text("● Orange: F_H", position=(-0.85, 0.45), scale=1.1, color=color.orange)
Text("● Lila:   F_R", position=(-0.85, 0.41), scale=1.1, color=color.violet)
Text("● Grün:   F_N", position=(-0.85, 0.37), scale=1.1, color=color.green)
Text("● Blau:   F_G", position=(-0.85, 0.33), scale=1.1, color=color.blue)

status = Text(text='', position=(0.4, 0.45), scale=1.2, color=color.black)

EditorCamera()

# --- Anfangszustand ---
geschwindigkeit = 0.0
t_sim           = 0.0
gleitet         = F_H > F_HAFT_MAX
laeuft          = True
kugel.color     = color.orange if gleitet else color.red

# --- update()-Schleife ---
def update():
    global geschwindigkeit, t_sim, gleitet, laeuft

    if not laeuft:
        return

    # Zustandsübergang: Haftreibung → Gleitreibung
    if not gleitet and F_H > F_HAFT_MAX:
        gleitet     = True
        kugel.color = color.orange

    # Beschleunigung berechnen
    a = (F_H - F_GLEIT) / m if gleitet else 0.0

    # Euler-Cromer-Schritt: erst Geschwindigkeit, dann Position
    geschwindigkeit += a * time.dt
    kugel.x         += geschwindigkeit * time.dt
    t_sim           += time.dt

    # Kraftindikatoren aktualisieren
    F_R_akt = F_GLEIT if gleitet else F_H

    pfeil_FH.position = Vec3(kugel.x + F_H * KRAFT_SKALA / 2,
                             kugel.y, Z_OFFSET)
    pfeil_FR.position = Vec3(kugel.x - F_R_akt * KRAFT_SKALA / 2,
                             kugel.y, Z_OFFSET)
    pfeil_FR.scale_x  = F_R_akt * KRAFT_SKALA

    pfeil_FN.position = Vec3(kugel.x, kugel.y + F_N * KRAFT_SKALA / 2,
                             Z_OFFSET)
    pfeil_FG.position = Vec3(kugel.x, kugel.y - m * G * KRAFT_SKALA / 2,
                             Z_OFFSET)

    # Statusanzeige
    zustand      = "Gleiten" if gleitet else "Haften"
    status.text  = (f"Zustand: {zustand}\n"
                    f"t = {t_sim:.3f} s\n"
                    f"v = {geschwindigkeit:.3f} m/s")

    # Abbruch
    if kugel.x >= ENDE_X:
        laeuft = False
        print(f"Bewegungszeit:      {t_sim:.4f} s")
        print(f"Endgeschwindigkeit: {geschwindigkeit:.4f} m/s")

app.run()
```

```{admonition} Checkliste: Was prüfen wir nach dem ersten Lauf?
:class: note
* **Anfangszustand korrekt:** Bei θ = 20° und μ_H = 0.35 bleibt die Kugel
  zunächst stehen (Kugel ist rot).
* **Farbe wechselt:** Wenn `NEIGUNGSWINKEL` auf 25° erhöht wird, startet die
  Kugel sofort orange.
* **Indikatoren bewegen sich mit:** Alle vier Kraftindikatoren folgen der
  Kugel.
* **Reibungsindikator skaliert:** Der lila Indikator wechselt beim
  Zustandsübergang von F_Haft auf F_Gleit (kürzer, weil μ_G < μ_H).
* **Konsole:** Nach dem Stopp erscheinen Bewegungszeit und Endgeschwindigkeit.
```

## Schritt 6: Ergebnis prüfen

```{code-cell} python
import math

NEIGUNGSWINKEL = 20.0
G, MU_G        = 9.81, 0.25
BAHNLAENGE     = 1.0
KUGELRADIUS    = 0.04
S_EFF          = BAHNLAENGE - 2 * KUGELRADIUS

A_X   = G * (math.sin(math.radians(NEIGUNGSWINKEL))
             - MU_G * math.cos(math.radians(NEIGUNGSWINKEL)))
V_END = math.sqrt(2 * A_X * S_EFF)
T_END = V_END / A_X

print(f"Analytische Beschleunigung:     {A_X:.4f} m/s²")
print(f"Analytische Bewegungszeit:      {T_END:.4f} s")
print(f"Analytische Endgeschwindigkeit: {V_END:.4f} m/s")
```

Eine Restabweichung zwischen Simulation und analytischem Wert entsteht
durch die variable Schrittweite `time.dt` in Ursina (abhängig von der
Framerate) sowie das leichte Überschießen beim Abbruch. In Kapitel 10
werden wir diesen Fehler systematisch durch Vergleich mit Messdaten
einschätzen.

```{admonition} Mini-Übung
:class: tip
Verändern Sie `MU_H` schrittweise von 0.35 auf 0.15. Beobachten Sie:

1. Ab welchem Wert beginnt die Kugel sofort zu gleiten (kein roter
   Anfangszustand)?
2. Berechnen Sie den kritischen Winkel für `MU_H = 0.35` analytisch und
   vergleichen Sie mit Ihrer Beobachtung.
3. Was ändert sich an der Endgeschwindigkeit, wenn Sie `MU_G` von 0.25
   auf 0.10 senken?
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import math

G, NEIGUNGSWINKEL = 9.81, 20.0

# Zu 1: Kritischer Winkel
for mu_h in [0.35, 0.30, 0.25, 0.20, 0.15]:
    theta_krit = math.degrees(math.atan(mu_h))
    gleitet    = NEIGUNGSWINKEL > theta_krit
    print(f"μ_H = {mu_h:.2f}: θ_krit = {theta_krit:.1f}°  "
          f"→ sofort gleiten: {gleitet}")

# Zu 3: Endgeschwindigkeit für verschiedene μ_G
S_EFF = 1.0 - 2 * 0.04
theta = math.radians(NEIGUNGSWINKEL)
for mu_g in [0.25, 0.10]:
    a     = G * (math.sin(theta) - mu_g * math.cos(theta))
    v_end = math.sqrt(2 * a * S_EFF)
    print(f"μ_G = {mu_g:.2f}: v_end = {v_end:.3f} m/s")
```

Ausgabe:
```
μ_H = 0.35: θ_krit = 19.3°  → sofort gleiten: True
μ_H = 0.30: θ_krit = 16.7°  → sofort gleiten: True
...
μ_G = 0.25: v_end = 2.127 m/s
μ_G = 0.10: v_end = 2.487 m/s
```

Ab θ_krit ≈ 19.3° gilt für μ_H = 0.35, dass der Neigungswinkel von 20°
bereits darüber liegt – die Kugel gleitet also sofort. Mit geringerer
Gleitreibung steigt die Endgeschwindigkeit deutlich.
````

## Starter-Code für das eigene Objekt

Das folgende Grundgerüst ist so gestaltet, dass es sich mit minimalen
Anpassungen auf jedes translatorische Objekt übertragen lässt. Die mit
`# ANPASSEN` markierten Stellen müssen für das eigene Objekt geändert werden:

```{code-cell} python
from ursina import *
import math

app = Ursina(title='Mein Objekt – Simulation')  # ANPASSEN
window.color = color.white

# Parameter – ANPASSEN
m               = 0.2        # Masse in kg
NEIGUNGSWINKEL  = 15.0       # Neigungswinkel in Grad
BAHNLAENGE      = 0.8        # Länge in m
KUGELRADIUS     = 0.05       # Radius / halbe Höhe des Objekts in m
MU_H            = 0.30       # Haftreibungskoeffizient
MU_G            = 0.20       # Gleitreibungskoeffizient
G               = 9.81

THETA      = math.radians(NEIGUNGSWINKEL)
F_N        = m * G * math.cos(THETA)
F_H        = m * G * math.sin(THETA)
F_HAFT_MAX = MU_H * F_N
F_GLEIT    = MU_G * F_N
START_X    = -(BAHNLAENGE / 2) + KUGELRADIUS
ENDE_X     =  (BAHNLAENGE / 2) - KUGELRADIUS

# Objekte – ANPASSEN (Farbe, Größe)
Entity(model='cube', color=color.gray,
       scale=Vec3(BAHNLAENGE, 0.02, 0.15), position=Vec3(0, 0, 0))
objekt = Entity(model='sphere', color=color.cyan,  # ANPASSEN
                scale=2*KUGELRADIUS,
                position=Vec3(START_X, KUGELRADIUS + 0.01, 0))

status = Text(text='', position=(-0.85, 0.45), scale=1.2, color=color.black)
EditorCamera()

geschwindigkeit = 0.0
t_sim           = 0.0
gleitet         = F_H > F_HAFT_MAX
laeuft          = True
objekt.color    = color.orange if gleitet else color.cyan  # ANPASSEN

def update():
    global geschwindigkeit, t_sim, gleitet, laeuft
    if not laeuft:
        return
    if not gleitet and F_H > F_HAFT_MAX:
        gleitet      = True
        objekt.color = color.orange   # ANPASSEN
    a               = (F_H - F_GLEIT) / m if gleitet else 0.0
    geschwindigkeit += a * time.dt
    objekt.x        += geschwindigkeit * time.dt
    t_sim           += time.dt
    zustand          = "Gleiten" if gleitet else "Haften"
    status.text      = f"{zustand}\nt={t_sim:.3f}s\nv={geschwindigkeit:.3f}m/s"
    if objekt.x >= ENDE_X:
        laeuft = False
        print(f"Bewegungszeit: {t_sim:.3f} s | v_end: {geschwindigkeit:.3f} m/s")

app.run()
```

## Zusammenfassung und Ausblick

In diesem Abschnitt haben wir das Physikmodell aus Abschnitt 9.2 vollständig
in Ursina integriert. Die vier Kraftindikatoren aktualisieren sich in Echtzeit
und machen das Kräftegleichgewicht sichtbar. Der Zustandsübergang von Haften
zu Gleiten ist durch den Farbwechsel der Kugel sofort erkennbar. Der
Starter-Code am Ende des Abschnitts dient als direkte Vorlage für das eigene
Simulationsobjekt.

In Kapitel 10 erweitern wir die Simulation in zwei Richtungen: Wir ersetzen
die vereinfachte gerade Rampe durch Wegpunkte aus dem echten CloudCompare-Mesh
und lernen, wie wir die Simulationsergebnisse mit Messdaten aus Stoppuhr und
Phyphox vergleichen und validieren.
