---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 9.1 Welche Kräfte wirken auf die Kugel?

Die Kugel liegt auf der geneigten Rampe. Wir haben in Kapitel 8 eine erste
Animation gebaut, in der sie beschleunigt und gleitet. Aber wir haben dabei
eine wichtige Frage übergangen: Bewegt sich die Kugel überhaupt? Jeder kennt
das Phänomen, dass ein Objekt auf einer leicht geneigten Fläche einfach liegen
bleibt, obwohl die Schwerkraft nach unten zieht. Offenbar gibt es eine Kraft,
die das verhindert.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können die vier wesentlichen Kräfte auf ein Objekt auf einer
  schiefen Ebene benennen, skizzieren und ihre Beträge berechnen:
  Gewichtskraft, Normalkraft, Hangabtriebskraft und Reibungskraft.
* [ ] Sie können den Unterschied zwischen Haftreibung und Gleitreibung
  erklären und die Bedingung formulieren, unter der ein Objekt von
  Haftreibung in Gleitreibung übergeht.
* [ ] Sie können die translatorischen Bewegungsgrößen (Kraft, Masse,
  Beschleunigung) den analogen rotatorischen Größen (Drehmoment,
  Trägheitsmoment, Winkelbeschleunigung) gegenüberstellen.
* [ ] Sie können für ihr eigenes Simulationsobjekt entscheiden, welcher
  Pfad (translatorisch oder rotatorisch) geeignet ist, und die relevanten
  Kräfte beziehungsweise Drehmomente benennen.
```

## Was hält die Kugel auf der Rampe?

Stellen wir uns vor, wir legen eine Kugel auf eine Rampe mit einem sehr kleinen
Neigungswinkel von 2°. Die Kugel bleibt liegen. Wir erhöhen den Winkel auf 5°.
Immer noch keine Bewegung. Erst ab einem bestimmten Winkel setzt die Kugel sich
in Bewegung.

*Warum bleibt die Kugel bei kleinen Winkeln liegen, obwohl die Schwerkraft
immer nach unten zieht?*

Die Antwort liegt in der **Reibungskraft** zwischen Kugel und Rampenoberfläche.
Um sie zu verstehen, müssen wir zunächst alle Kräfte kennen, die auf die Kugel
wirken.

## Die vier Kräfte auf der schiefen Ebene

Wir betrachten ein Objekt der Masse `m` auf einer Rampe mit dem
Neigungswinkel `θ`. Vier Kräfte bestimmen sein Verhalten.

### Was zieht nach unten?

Die **Gewichtskraft** (englisch: Weight Force) wirkt senkrecht nach unten
und hat den Betrag:

```code
F_G = m · g
```

mit der Erdbeschleunigung `g = 9.81 m/s²`. Sie ist die Ursache aller Bewegung
auf der Rampe, wirkt aber nicht direkt entlang der Bahn.

### Was hält das Objekt auf der Rampe?

Die **Normalkraft** (englisch: Normal Force) wirkt senkrecht zur
Rampenoberfläche und verhindert, dass das Objekt in die Rampe hineinfällt.
Ihr Betrag ergibt sich aus der Komponente der Gewichtskraft senkrecht zur
Rampe:

```code
F_N = m · g · cos(θ)
```

Bei einem flachen Winkel (θ ≈ 0°) ist `cos(θ) ≈ 1`, die Normalkraft entspricht
fast der vollen Gewichtskraft. Bei einem steilen Winkel nimmt sie ab, weil das
Objekt fast frei fällt.

### Was treibt das Objekt die Rampe hinunter?

Die **Hangabtriebskraft** ist die Komponente der Gewichtskraft entlang der
Rampe. Sie treibt das Objekt bergab:

```code
F_H = m · g · sin(θ)
```

Bei θ = 0° gibt es keinen Antrieb. Bei θ = 90° befindet sich das Objekt im
freien Fall.

```{code-cell} python
import math
import plotly.express as px
import pandas as pd

G = 9.81   # Erdbeschleunigung in m/s²
m = 0.1    # Masse in kg

winkel_grad = list(range(0, 91, 5))
daten = []

for theta_grad in winkel_grad:
    theta = math.radians(theta_grad)
    F_N   = m * G * math.cos(theta)
    F_H   = m * G * math.sin(theta)
    daten.append({"Winkel (°)": theta_grad, "Kraft (N)": round(F_N, 4),
                  "Typ": "Normalkraft F_N"})
    daten.append({"Winkel (°)": theta_grad, "Kraft (N)": round(F_H, 4),
                  "Typ": "Hangabtrieb F_H"})

df  = pd.DataFrame(daten)
fig = px.line(
    df, x="Winkel (°)", y="Kraft (N)", color="Typ",
    title=f"Normal- und Hangabtriebskraft als Funktion des Neigungswinkels "
          f"(m = {m} kg)"
)
fig.show()
```

*Bei welchem Winkel sind Normalkraft und Hangabtriebskraft gleich groß, und
was bedeutet das geometrisch?*

Bei 45° gilt `sin(45°) = cos(45°) ≈ 0.707`, beide Kräfte sind gleich groß.
Das entspricht genau der Diagonalen des Kräftedreiecks.

```{admonition} Mini-Übung
:class: tip
Berechnen Sie für eine Masse von 0.15 kg und einen Neigungswinkel von 20°
die Gewichtskraft `F_G`, die Normalkraft `F_N` und die Hangabtriebskraft
`F_H`. Überprüfen Sie mit Python, ob `F_N² + F_H² = F_G²` gilt.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import math

m     = 0.15
G     = 9.81
theta = math.radians(20)

F_G = m * G
F_N = m * G * math.cos(theta)
F_H = m * G * math.sin(theta)

print(f"F_G = {F_G:.4f} N")
print(f"F_N = {F_N:.4f} N")
print(f"F_H = {F_H:.4f} N")
print(f"Pythagoras-Check: F_N² + F_H² = {F_N**2 + F_H**2:.6f}")
print(f"F_G²                           = {F_G**2:.6f}")
```

Die kleine Abweichung im letzten Nachkommabereich ist ein Rundungsfehler.
Mathematisch gilt der Satz des Pythagoras exakt.
````

## Wann bewegt sich das Objekt?

Die Reibungskraft verhält sich in zwei grundlegend verschiedenen Zuständen
unterschiedlich. Diesen Unterschied müssen wir verstehen, bevor wir ihn in
Kapitel 9.2 in Code übersetzen.

### Was ist Haftreibung?

Solange das Objekt auf der Rampe ruht, wirkt die **Haftreibungskraft**
(englisch: Static Friction). Sie passt sich automatisch an die
Hangabtriebskraft an und hält das Objekt genau dort, wo es ist. Ihre Stärke
kann bis zu einem Maximalwert anwachsen:

```code
F_Haft,max = μ_H · F_N
```

Der dimensionslose Koeffizient `μ_H` heißt **Haftreibungskoeffizient**. Das
Objekt bleibt stehen, solange die Hangabtriebskraft kleiner ist als dieser
Maximalwert:

```code
F_H ≤ μ_H · F_N   →   Objekt bleibt stehen
```

### Was ist Gleitreibung?

Sobald `F_H > μ_H · F_N`, kann die Haftreibung die Hangabtriebskraft nicht
mehr kompensieren. Das Objekt beginnt zu gleiten. Ab diesem Moment wirkt die
**Gleitreibungskraft** (englisch: Kinetic Friction):

```code
F_Gleit = μ_G · F_N
```

Der **Gleitreibungskoeffizient** `μ_G` ist stets kleiner als `μ_H`. Das
erklärt ein bekanntes Phänomen: Es ist schwerer, ein Objekt in Bewegung zu
setzen, als es in Bewegung zu halten. Die resultierende Nettokraft und damit
die Beschleunigung sind:

```code
F_netto = F_H - F_Gleit = m · g · (sin(θ) - μ_G · cos(θ))
a       = F_netto / m   = g · (sin(θ) - μ_G · cos(θ))
```

```{admonition} Mini-Übung
:class: tip
Gegeben: `m = 0.1 kg`, `θ = 15°`, `μ_H = 0.35`, `μ_G = 0.25`.

1. Berechnen Sie `F_H` und `F_Haft,max`. Bewegt sich das Objekt?
2. Erhöhen Sie den Winkel auf 25°. Bewegt es sich jetzt?
3. Berechnen Sie für 25° die Nettokraft und die Beschleunigung.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import math

m    = 0.1
G    = 9.81
MU_H = 0.35
MU_G = 0.25

for theta_grad in [15, 25]:
    theta      = math.radians(theta_grad)
    F_N        = m * G * math.cos(theta)
    F_H        = m * G * math.sin(theta)
    F_haft_max = MU_H * F_N

    print(f"\nθ = {theta_grad}°")
    print(f"  F_H        = {F_H:.4f} N")
    print(f"  F_Haft,max = {F_haft_max:.4f} N")

    if F_H <= F_haft_max:
        print("  Objekt bleibt stehen (Haftreibung hält)")
    else:
        F_gleit = MU_G * F_N
        F_netto = F_H - F_gleit
        a       = F_netto / m
        print(f"  Objekt bewegt sich (Haftreibung überwunden)")
        print(f"  F_netto = {F_netto:.4f} N")
        print(f"  a       = {a:.4f} m/s²")
```
````

### Welchen Winkel braucht es zum Losrollen?

Es gibt genau einen Winkel, bei dem Haftreibung und Hangabtrieb im Gleichgewicht
sind. Wir setzen `F_H = F_Haft,max` und erhalten:

```code
tan(θ_krit) = μ_H   →   θ_krit = arctan(μ_H)
```

```{code-cell} python
import math

MU_H       = 0.35
THETA_KRIT = math.degrees(math.atan(MU_H))
print(f"Kritischer Winkel: {THETA_KRIT:.1f}°")
```

Unterhalb dieses Winkels bleibt das Objekt stets stehen, oberhalb setzt es
sich stets in Bewegung. Das ist ein nützlicher Schnelltest für die Praxis:
Wer den Haftreibungskoeffizienten eines Materials kennt, weiß sofort, ab
welcher Rampeneigung ein Objekt anfängt zu gleiten.

## Zwei Pfade: Translation und Rotation

Bisher haben wir ausschließlich über Translation gesprochen, also über das
Objekt, das sich geradlinig die Rampe entlang bewegt. Für Objekte, die sich
um eine feste Achse drehen (zum Beispiel eine Fahrradkurbel oder ein Zahnrad),
gelten analoge Gesetze mit anderen Größen.

Die folgende Tabelle zeigt die vollständige Analogie:

| Translatorisch | Symbol | Rotatorisch | Symbol |
| -------------- | ------ | ----------- | ------ |
| Masse | m | Trägheitsmoment | I |
| Kraft | F | Drehmoment | M |
| Beschleunigung | a | Winkelbeschleunigung | α |
| Geschwindigkeit | v | Winkelgeschwindigkeit | ω |
| Position | x | Winkel | θ |
| Newtons 2. Gesetz | F = m · a | Drehimpulssatz | M = I · α |

Der Euler-Cromer-Schritt sieht in beiden Fällen strukturell identisch aus:

```python
# Translatorisch:       # Rotatorisch:
v += a * dt             omega += alpha * dt
x += v * dt             theta += omega * dt
```

*Wozu brauchen wir das Trägheitsmoment I?*

Das Trägheitsmoment beschreibt, wie schwer es ist, ein Objekt in Rotation zu
versetzen, analog zur Masse bei der Translation. Ein massereicher, weit
ausgedehnter Körper (großes I) beschleunigt bei gleichem Drehmoment langsamer
als ein kompakter Körper (kleines I). Für Kapitel 9 behandeln wir I als
gegebenen Parameter, den wir aus Tabellen oder Messungen entnehmen.

```{admonition} Welchen Pfad wähle ich für mein Objekt?
:class: note
**Translatorischer Pfad:** Das Objekt bewegt sich geradlinig oder entlang
einer Kurve. Typische Objekte: rollende Kugel, Holzeisenbahn auf einem Gleis.

**Rotatorischer Pfad:** Das Objekt dreht sich um eine feste Achse. Typische
Objekte: Fahrradkurbel, Zahnrad, Pendel, Schwerlastrolle.

Manche Objekte kombinieren beide: Eine Rolle rollt (Translation des
Mittelpunkts und Rotation um die Achse). Für Kapitel 9 vereinfachen wir
und behandeln jedes Objekt als reinen Translations- oder Rotationsfall.
```

## Zusammenfassung und Ausblick

In diesem Abschnitt haben wir die vier Kräfte auf der schiefen Ebene
kennengelernt: Gewichtskraft, Normalkraft, Hangabtriebskraft und Reibungskraft.
Der entscheidende neue Begriff ist die Unterscheidung zwischen Haftreibung und
Gleitreibung. Solange die Hangabtriebskraft die maximale Haftreibungskraft
nicht übersteigt, bleibt das Objekt stehen. Sobald sie es tut, beginnt die
Bewegung mit Gleitreibung und wir können die Nettokraft und Beschleunigung
berechnen. Außerdem haben wir die Analogie zwischen Translation und Rotation
eingeführt, die es uns erlaubt, beide Typen von Simulationsobjekten mit
demselben Grundgerüst zu behandeln.

Im nächsten Abschnitt übersetzen wir dieses Kraftmodell in Python: Wir bauen
den Zustandsübergang von Haftreibung zu Gleitreibung als `if`/`else`-Konstrukt
und betten ihn in die Euler-Cromer-Schleife aus Kapitel 8 ein.
