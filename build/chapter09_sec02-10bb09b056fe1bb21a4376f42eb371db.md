---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 9.2 Wie implementiere ich ein physikalisches Modell in Python?

Wir kennen jetzt die Kräfte: Hangabtrieb, Normalkraft, Haftreibung,
Gleitreibung. Wir wissen, wann das Objekt stehen bleibt und wann es sich
bewegt. In Kapitel 8 haben wir bereits eine Euler-Cromer-Schleife gebaut,
in der die Kugel mit einer konstanten Beschleunigung glitt. Jetzt ersetzen
wir diese vereinfachte Beschleunigung durch ein echtes Kraftmodell mit
Reibung und Zustandsübergang.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können den Zustandsübergang von Haftreibung zu Gleitreibung als
  `if`/`else`-Konstrukt in Python implementieren.
* [ ] Sie können die Nettokraft und Beschleunigung für den gleitenden
  Zustand berechnen und in die Euler-Cromer-Schleife aus Kapitel 8
  einbauen.
* [ ] Sie können das Modell für den translatorischen Pfad (schiefe Ebene)
  und den rotatorischen Pfad (drehendes Objekt unter Drehmoment) parallel
  implementieren.
* [ ] Sie können das Simulationsergebnis mit einer analytischen Lösung
  vergleichen und die Abweichung durch die Euler-Cromer-Methode einschätzen.
```

## Vom Kraftdiagramm zum Code

In Abschnitt 9.1 haben wir das Kraftdiagramm aufgestellt. Jetzt übersetzen
wir es Schritt für Schritt in Python.

### Wie berechnen wir die Kräfte?

Als erster Schritt definieren wir alle Parameter und berechnen die
zeitunabhängigen Kräfte einmalig vor der Schleife. Kräfte, die sich während
der Simulation nicht ändern (Normalkraft, maximale Haftreibung, Gleitreibung),
gehören nicht in die Schleife:

```{code-cell} python
import math

# Objektparameter
m     = 0.1                    # Masse in kg
G     = 9.81                   # Erdbeschleunigung in m/s²
THETA = math.radians(20)       # Neigungswinkel

# Reibungskoeffizienten
MU_H = 0.35                    # Haftreibungskoeffizient (Static Friction)
MU_G = 0.25                    # Gleitreibungskoeffizient (Kinetic Friction)

# Kräfte (zeitunabhängig)
F_N        = m * G * math.cos(THETA)
F_H        = m * G * math.sin(THETA)
F_HAFT_MAX = MU_H * F_N
F_GLEIT    = MU_G * F_N

print(f"F_N        = {F_N:.4f} N")
print(f"F_H        = {F_H:.4f} N")
print(f"F_Haft,max = {F_HAFT_MAX:.4f} N")
print(f"Bewegt sich das Objekt? {'Ja' if F_H > F_HAFT_MAX else 'Nein'}")
```

### Wie modellieren wir den Übergang von Haften zu Gleiten?

Das Herzstück des Modells ist der Zustandsübergang. Wir verwalten ihn mit
einer booleschen Variable `gleitet`, die angibt, in welchem Zustand sich das
Objekt gerade befindet:

```{code-cell} python
import math

m, G    = 0.1, 9.81
THETA   = math.radians(20)
MU_H, MU_G = 0.35, 0.25

F_N        = m * G * math.cos(THETA)
F_H        = m * G * math.sin(THETA)
F_HAFT_MAX = MU_H * F_N
F_GLEIT    = MU_G * F_N

# Anfangszustand
gleitet         = False
geschwindigkeit = 0.0

# Zustandsübergang prüfen
if not gleitet and F_H > F_HAFT_MAX:
    gleitet = True
    print("Haftreibung überwunden – Objekt beginnt zu gleiten.")

# Beschleunigung berechnen
if gleitet:
    a = (F_H - F_GLEIT) / m
else:
    a = 0.0

print(f"Beschleunigung: {a:.4f} m/s²")
```

*Warum setzen wir `gleitet` nicht einfach direkt auf `True`?*

Weil der Zustand während der Simulation wechseln kann. Das Objekt kann stehen,
dann zu gleiten beginnen und, wenn die Bahn flacher wird, theoretisch wieder
zum Stillstand kommen. Die Variable `gleitet` verfolgt diesen Zustand über
alle Zeitschritte der Schleife hinweg.

### Wie bauen wir die vollständige Schleife?

Jetzt fügen wir den Zustandsübergang in die Euler-Cromer-Schleife ein. Die
Reihenfolge ist dieselbe wie in Kapitel 8: erst Geschwindigkeit aktualisieren,
dann Position:

```{code-cell} python
import math
import pandas as pd
import plotly.express as px

# Parameter
m, G        = 0.1, 9.81
THETA       = math.radians(20)
MU_H, MU_G  = 0.35, 0.25
BAHNLAENGE  = 1.2
KUGELRADIUS = 0.04
S_EFF       = BAHNLAENGE - 2 * KUGELRADIUS
dt          = 0.005

# Kräfte
F_N        = m * G * math.cos(THETA)
F_H        = m * G * math.sin(THETA)
F_HAFT_MAX = MU_H * F_N
F_GLEIT    = MU_G * F_N

# Anfangszustand
x               = 0.0
geschwindigkeit = 0.0
gleitet         = False
t               = 0.0
ergebnis        = []

while x < S_EFF:
    # Zustandsübergang: Haftreibung → Gleitreibung
    if not gleitet and F_H > F_HAFT_MAX:
        gleitet = True

    # Beschleunigung
    if gleitet:
        a = (F_H - F_GLEIT) / m
    else:
        a = 0.0

    # Euler-Cromer-Schritt: erst Geschwindigkeit, dann Position
    geschwindigkeit += a * dt
    x               += geschwindigkeit * dt
    t               += dt

    ergebnis.append({
        "Zeit (s)":            round(t, 4),
        "Position (m)":        round(x, 5),
        "Geschwindigkeit (m/s)": round(geschwindigkeit, 5),
        "Zustand":             "Gleiten" if gleitet else "Haften"
    })

df = pd.DataFrame(ergebnis)

fig = px.line(
    df, x="Zeit (s)", y="Geschwindigkeit (m/s)",
    color="Zustand",
    title=f"Geschwindigkeit der Kugel (θ={math.degrees(THETA):.0f}°, "
          f"μ_H={MU_H}, μ_G={MU_G})"
)
fig.show()

print(f"Bewegungszeit:      {t:.4f} s")
print(f"Endgeschwindigkeit: {geschwindigkeit:.4f} m/s")
```

```{admonition} Mini-Übung
:class: tip
Setzen Sie `MU_H = 0.15`. Was beobachten Sie am Kurvenverlauf? Erklären Sie,
warum der Zustand "Haften" nun nicht mehr auftritt.
```

````{admonition} Lösung
:class: tip
:class: dropdown
Bei `MU_H = 0.15` gilt `F_Haft,max = 0.15 · F_N < F_H`, also ist die maximale
Haftreibungskraft kleiner als die Hangabtriebskraft. Das Objekt beginnt sofort
zu gleiten, ohne jemals im Haft-Zustand zu sein. Die Kurve startet daher sofort
mit konstanter Beschleunigung, ohne einen flachen Anfangsabschnitt.
````

## Wie überprüfen wir das Modell analytisch?

Für eine gleichmäßig beschleunigte Bewegung, bei der das Objekt sofort gleitet,
gibt es eine exakte analytische Lösung. Wir vergleichen sie mit dem
Simulationsergebnis, um den Diskretisierungsfehler der Euler-Cromer-Methode zu
beurteilen:

```{code-cell} python
import math

G, THETA, MU_G = 9.81, math.radians(20), 0.25
S_EFF          = 1.2 - 2 * 0.04   # BAHNLAENGE - 2 * KUGELRADIUS

a_analytisch = G * (math.sin(THETA) - MU_G * math.cos(THETA))
t_analytisch = math.sqrt(2 * S_EFF / a_analytisch)
v_analytisch = a_analytisch * t_analytisch

print(f"Analytische Beschleunigung:     {a_analytisch:.4f} m/s²")
print(f"Analytische Bewegungszeit:      {t_analytisch:.4f} s")
print(f"Analytische Endgeschwindigkeit: {v_analytisch:.4f} m/s")
```

Bei `dt = 0.005 s` sollte die Abweichung zur Simulation unter 0.5 % liegen.
In Kapitel 10 werden wir sehen, wie wir diesen Wert durch Parameteranpassung
an echte Messungen kalibrieren.

## Wie sieht der rotatorische Pfad aus?

Für Objekte, die sich um eine feste Achse drehen (Fahrradkurbel, Zahnrad),
ist die Struktur identisch mit dem translatorischen Pfad. Nur die
Zustandsgrößen wechseln:

### Wie lauten die Parameter des rotatorischen Modells?

Statt Masse und Kraft verwenden wir Trägheitsmoment und Drehmoment:

```{code-cell} python
import math

# Rotatorische Parameter
I         = 0.003    # Trägheitsmoment in kg·m² (als gegebener Parameter)
M_ANTRIEB = 0.08     # Antriebsdrehmoment in N·m
MU_ROT    = 0.08     # Vereinfachter Reibungskoeffizient

# Reibungsdrehmoment (analog zu F_GLEIT = μ_G · F_N)
M_REIB     = MU_ROT * M_ANTRIEB
M_HAFT_MAX = 1.2 * M_REIB     # Haftmoment etwas größer als Gleitmoment

print(f"Antriebsdrehmoment: {M_ANTRIEB:.4f} N·m")
print(f"Reibungsdrehmoment: {M_REIB:.4f} N·m")
print(f"Nettodrehmoment:    {M_ANTRIEB - M_REIB:.4f} N·m")
```

```{admonition} Hinweis: Trägheitsmoment als Parameter
:class: note
Das Trägheitsmoment I hängt von der Massenverteilung des Objekts ab und ist
für komplexe Geometrien aufwändig zu berechnen. Für Kapitel 9 entnehmen wir
I einer Tabelle oder messen es experimentell. Typische Werte:

| Körper | Trägheitsmoment |
| ------ | --------------- |
| Vollzylinder (Radius r, Masse m) | I = ½ · m · r² |
| Hohlzylinder (Radien r₁, r₂) | I = ½ · m · (r₁² + r₂²) |
| Dünner Stab (Länge L, um Mittelpunkt) | I = 1/12 · m · L² |
```

### Wie sieht die rotatorische Schleife aus?

```{code-cell} python
import math
import pandas as pd
import plotly.express as px

I, M_ANTRIEB, MU_ROT = 0.003, 0.08, 0.08
M_REIB     = MU_ROT * M_ANTRIEB
M_HAFT_MAX = 1.2 * M_REIB
THETA_ZIEL = 4 * math.pi   # zwei volle Umdrehungen
dt         = 0.005

dreht  = False
omega  = 0.0     # Winkelgeschwindigkeit in rad/s
theta  = 0.0     # Winkel in Radiant
t      = 0.0
ergebnis = []

while theta < THETA_ZIEL:
    # Zustandsübergang
    if not dreht and M_ANTRIEB > M_HAFT_MAX:
        dreht = True

    # Winkelbeschleunigung
    if dreht:
        alpha = (M_ANTRIEB - M_REIB) / I
    else:
        alpha = 0.0

    # Euler-Cromer-Schritt: erst Winkelgeschwindigkeit, dann Winkel
    omega += alpha * dt
    theta += omega * dt
    t     += dt

    ergebnis.append({
        "Zeit (s)":                      round(t, 4),
        "Winkelgeschwindigkeit (rad/s)":  round(omega, 4),
        "Zustand":                        "Dreht" if dreht else "Haftend"
    })

df = pd.DataFrame(ergebnis)
fig = px.line(df, x="Zeit (s)", y="Winkelgeschwindigkeit (rad/s)",
              color="Zustand",
              title="Winkelgeschwindigkeit der Kurbel über die Zeit")
fig.show()

print(f"Zeit für zwei Umdrehungen: {t:.3f} s")
print(f"Enddrehzahl:               {omega / (2*math.pi) * 60:.1f} U/min")
```

```{admonition} Mini-Übung
:class: tip
Vergleichen Sie die Struktur der rotatorischen Schleife mit der
translatorischen Schleife weiter oben. Benennen Sie die vier direkten
Entsprechungen zwischen den Variablen und Parametern beider Pfade.
```

````{admonition} Lösung
:class: tip
:class: dropdown
| Translatorisch | Rotatorisch |
| -------------- | ----------- |
| `m` (Masse) | `I` (Trägheitsmoment) |
| `F_H - F_GLEIT` (Nettokraft) | `M_ANTRIEB - M_REIB` (Nettodrehmoment) |
| `geschwindigkeit` | `omega` (Winkelgeschwindigkeit) |
| `x` (Position) | `theta` (Winkel) |

Der Euler-Cromer-Schritt ist in beiden Fällen strukturell identisch:

```python
# Translation:                  # Rotation:
a   = F / m                     alpha  = M / I
v   += a     * dt               omega  += alpha * dt
x   += v     * dt               theta  += omega * dt
```
````

## Zusammenfassung und Ausblick

In diesem Abschnitt haben wir das Kraftmodell aus Abschnitt 9.1 in Python
übersetzt. Das zentrale Werkzeug ist der Zustandsübergang von Haftreibung zu
Gleitreibung als `if`/`else`-Konstrukt: Solange die Hangabtriebskraft die
maximale Haftreibungskraft nicht übersteigt, ist die Beschleunigung null.
Sobald sie es tut, wechseln wir in den Gleitzustand und berechnen die
Nettokraft. Der rotatorische Pfad für Objekte wie Kurbeln und Zahnräder folgt
derselben Struktur mit Drehmoment statt Kraft und Trägheitsmoment statt Masse.

Im nächsten Abschnitt verbinden wir dieses Physikmodell mit Ursina: Die Kugel
bewegt sich mit korrekter Reibungsphysik auf einer animierten Rampe,
Kräftepfeile aktualisieren sich in Echtzeit und eine Textanzeige zeigt den
aktuellen Zustand (Haften oder Gleiten).
