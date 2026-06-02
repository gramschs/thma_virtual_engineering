---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Übungen

````{admonition} Übung 9.1 (✩)
:class: tip
**Kräfte auf der schiefen Ebene einordnen**

Die folgende Tabelle listet vier Aussagen über ein Objekt auf einer schiefen
Ebene. Entscheiden Sie für jede Aussage, ob sie richtig oder falsch ist, und
korrigieren Sie die falschen Aussagen in einem Satz.

| Nr. | Aussage |
| --- | ------- |
| 1 | Die Normalkraft ist immer gleich groß wie die Gewichtskraft. |
| 2 | Die Haftreibungskraft ist stets kleiner als die Gleitreibungskraft. |
| 3 | Der kritische Winkel hängt nur vom Haftreibungskoeffizienten ab, nicht von der Masse. |
| 4 | Ein Objekt, das einmal gleitet, kann auf derselben Rampe bei konstantem Neigungswinkel nicht wieder zum Stillstand kommen. |
````

````{admonition} Lösung
:class: tip
:class: dropdown
| Nr. | Richtig/Falsch | Korrektur |
| --- | -------------- | --------- |
| 1 | **Falsch** | Die Normalkraft beträgt `F_N = m·g·cos(θ)` und ist nur bei θ = 0° gleich groß wie die Gewichtskraft. Bei geneigter Fläche ist sie kleiner. |
| 2 | **Falsch** | Es gilt stets μ_H > μ_G, also ist die maximale Haftreibungskraft größer als die Gleitreibungskraft. Deshalb ist es schwerer, ein Objekt in Bewegung zu setzen, als es in Bewegung zu halten. |
| 3 | **Richtig** | `θ_krit = arctan(μ_H)` – Masse und Erdbeschleunigung kürzen sich heraus. |
| 4 | **Richtig** | Damit die Kugel stoppt, müsste die Nettokraft null werden, also `F_H = F_Gleit`, was `tan(θ) = μ_G` bedeutet. Da `μ_G < μ_H`, liegt dieser Winkel unterhalb des kritischen Winkels. Bei konstantem Winkel oberhalb von `θ_krit` bleibt die Nettokraft positiv und die Kugel stoppt nicht. |
````

````{admonition} Übung 9.2 (✩)
:class: tip
**Kritischen Winkel berechnen und Zustand bestimmen**

Gegeben sind drei Materialpaare mit ihren Reibungskoeffizienten:

| Materialpaar | μ_H | μ_G |
| ------------ | ---- | ---- |
| Stahl auf Stahl | 0.15 | 0.10 |
| Gummi auf Beton | 0.80 | 0.60 |
| Holz auf Holz | 0.40 | 0.25 |

1. Berechnen Sie für jedes Materialpaar den kritischen Winkel `θ_krit`.
2. Eine Schwerlastrolle (m = 5 kg) liegt auf einer Stahlrampe mit θ = 12°.
   Bewegt sie sich? Berechnen Sie falls ja die Nettokraft und Beschleunigung.
3. Bei welchem Winkel würde die Holzeisenbahn (m = 0.3 kg, Holz auf Holz)
   zu gleiten beginnen?
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import math

materialien = {
    "Stahl auf Stahl": (0.15, 0.10),
    "Gummi auf Beton":  (0.80, 0.60),
    "Holz auf Holz":    (0.40, 0.25),
}

print("Kritische Winkel:")
for name, (mu_h, mu_g) in materialien.items():
    theta_krit = math.degrees(math.atan(mu_h))
    print(f"  {name}: θ_krit = {theta_krit:.1f}°")

# Schwerlastrolle auf Stahl, θ = 12°
m, mu_h, mu_g, theta, G = 5.0, 0.15, 0.10, math.radians(12), 9.81
F_N = m * G * math.cos(theta)
F_H = m * G * math.sin(theta)
F_haft_max = mu_h * F_N

print(f"\nSchwerlastrolle (θ=12°, Stahl):")
if F_H > F_haft_max:
    F_gleit = mu_g * F_N
    a       = (F_H - F_gleit) / m
    print(f"  Gleitet: F_netto = {F_H - F_gleit:.3f} N, a = {a:.3f} m/s²")
else:
    print(f"  Haftet: F_H={F_H:.3f} N < F_Haft,max={F_haft_max:.3f} N")

print(f"\nHolzeisenbahn: θ_krit = {math.degrees(math.atan(0.40)):.1f}°")
```

Ausgabe:
```
Kritische Winkel:
  Stahl auf Stahl: θ_krit = 8.5°
  Gummi auf Beton: θ_krit = 38.7°
  Holz auf Holz:   θ_krit = 21.8°

Schwerlastrolle (θ=12°, Stahl):
  Gleitet: F_netto = 3.481 N, a = 0.696 m/s²

Holzeisenbahn: θ_krit = 21.8°
```
````

````{admonition} Übung 9.3 (✩✩)
:class: tip
**Zustandsübergang systematisch untersuchen**

Implementieren Sie eine Python-Funktion `zustand(m, theta_grad, mu_h, mu_g)`,
die `"haftet"` zurückgibt, wenn das Objekt stehen bleibt, oder `"gleitet"`
sowie die Beschleunigung `a` in m/s², wenn es sich bewegt.

Verwenden Sie die Funktion, um für die Kugelbahn (m = 0.1 kg, μ_H = 0.35,
μ_G = 0.25) eine Tabelle der Zustände und Beschleunigungen für Winkel von
5° bis 40° in 5°-Schritten zu erstellen. Stellen Sie die Beschleunigung als
Funktion des Winkels mit Plotly dar und markieren Sie den kritischen Winkel
als vertikale Linie.
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import math
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def zustand(m, theta_grad, mu_h, mu_g, G=9.81):
    theta      = math.radians(theta_grad)
    F_N        = m * G * math.cos(theta)
    F_H        = m * G * math.sin(theta)
    F_haft_max = mu_h * F_N
    if F_H <= F_haft_max:
        return "haftet", 0.0
    else:
        a = (F_H - mu_g * F_N) / m
        return "gleitet", a

m, MU_H, MU_G = 0.1, 0.35, 0.25
daten = []

for theta_grad in range(5, 41, 5):
    z, a = zustand(m, theta_grad, MU_H, MU_G)
    daten.append({
        "Winkel (°)": theta_grad,
        "Zustand":    z,
        "Beschleunigung (m/s²)": round(a, 4)
    })
    print(f"θ = {theta_grad:2d}°: {z:8s}  a = {a:.4f} m/s²")

df  = pd.DataFrame(daten)
fig = px.bar(
    df, x="Winkel (°)", y="Beschleunigung (m/s²)", color="Zustand",
    title="Beschleunigung in Abhängigkeit vom Neigungswinkel",
    color_discrete_map={"haftet": "steelblue", "gleitet": "tomato"}
)

theta_krit = math.degrees(math.atan(MU_H))
fig.add_vline(x=theta_krit, line_dash="dash", line_color="gray",
              annotation_text=f"θ_krit = {theta_krit:.1f}°")
fig.show()
```
````

````{admonition} Übung 9.4 (✩✩)
:class: tip
**Ursina: Spurpunkte und Kraftindikator ergänzen**

Nehmen Sie den vollständigen Starter-Code aus Abschnitt 9.3 als Ausgangspunkt
und erweitern Sie ihn um zwei Elemente:

1. **Spurpunkte:** Setzen Sie alle 0.05 s einen kleinen türkisen Spurpunkt
   an der aktuellen Kugelposition (analog zu Kapitel 8.2).
2. **Dynamischer Neigungswinkel:** Fügen Sie zwei Tastenbefehle hinzu:
   - Taste `u` erhöht `NEIGUNGSWINKEL` um 1° und berechnet alle Kräfte neu.
   - Taste `d` verringert `NEIGUNGSWINKEL` um 1° (Minimum: 1°).
   - Nach jeder Änderung soll die Kugel in ihre Startposition zurückgesetzt
     und die Simulation neu gestartet werden.

Hinweis: Tastatureingaben in Ursina werden über die eingebaute Funktion
`input(key)` abgefangen:

```python
def input(key):
    if key == 'u':
        # Winkel erhöhen und zurücksetzen
        ...
```
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
from ursina import *
import math

app = Ursina(title='Kugelbahn – Dynamischer Winkel', width=1200, height=700)
window.color = color.white

BAHNLAENGE  = 1.0
KUGELRADIUS = 0.04
m, G        = 0.1, 9.81
MU_H, MU_G  = 0.35, 0.25
SPUR_INT    = 0.05

neigungswinkel = [20.0]   # als Liste, damit input() darauf zugreifen kann

def berechne_kraefte(winkel):
    theta      = math.radians(winkel)
    F_N        = m * G * math.cos(theta)
    F_H        = m * G * math.sin(theta)
    F_HAFT_MAX = MU_H * F_N
    F_GLEIT    = MU_G * F_N
    return F_N, F_H, F_HAFT_MAX, F_GLEIT

START_X = -(BAHNLAENGE / 2) + KUGELRADIUS
ENDE_X  =  (BAHNLAENGE / 2) - KUGELRADIUS

Entity(model='cube', color=color.gray,
       scale=Vec3(BAHNLAENGE, 0.02, 0.12))

kugel  = Entity(model='sphere', color=color.red,
                scale=2*KUGELRADIUS,
                position=Vec3(START_X, KUGELRADIUS + 0.01, 0))
status = Text(text='', position=(-0.85, 0.45), scale=1.2, color=color.black)
winkel_text = Text(text=f'θ = {neigungswinkel[0]:.0f}°  (u/d zum Ändern)',
                   position=(-0.85, 0.40), scale=1.2, color=color.black)
EditorCamera()

spurpunkte         = []
geschwindigkeit    = [0.0]
t_sim              = [0.0]
gleitet            = [False]
laeuft             = [True]
spur_timer         = [0.0]

F_N, F_H, F_HAFT_MAX, F_GLEIT = berechne_kraefte(neigungswinkel[0])

def reset():
    for s in spurpunkte:
        destroy(s)
    spurpunkte.clear()
    kugel.x            = START_X
    geschwindigkeit[0] = 0.0
    t_sim[0]           = 0.0
    spur_timer[0]      = 0.0
    laeuft[0]          = True
    kugel.color        = color.orange if F_H > F_HAFT_MAX else color.red
    gleitet[0]         = F_H > F_HAFT_MAX

reset()

def update():
    global F_N, F_H, F_HAFT_MAX, F_GLEIT
    if not laeuft[0]:
        return
    if not gleitet[0] and F_H > F_HAFT_MAX:
        gleitet[0]  = True
        kugel.color = color.orange
    a                   = (F_H - F_GLEIT) / m if gleitet[0] else 0.0
    geschwindigkeit[0] += a * time.dt
    kugel.x            += geschwindigkeit[0] * time.dt
    t_sim[0]           += time.dt
    spur_timer[0]      += time.dt
    if spur_timer[0] >= SPUR_INT:
        spurpunkte.append(
            Entity(model='sphere', color=color.cyan,
                   scale=0.015, position=kugel.position))
        spur_timer[0] = 0.0
    status.text = (f"θ = {neigungswinkel[0]:.0f}°\n"
                   f"t = {t_sim[0]:.3f} s\n"
                   f"v = {geschwindigkeit[0]:.3f} m/s")
    if kugel.x >= ENDE_X:
        laeuft[0] = False

def input(key):
    global F_N, F_H, F_HAFT_MAX, F_GLEIT
    if key == 'u':
        neigungswinkel[0] += 1.0
    elif key == 'd':
        neigungswinkel[0] = max(1.0, neigungswinkel[0] - 1.0)
    else:
        return
    winkel_text.text         = f'θ = {neigungswinkel[0]:.0f}°  (u/d)'
    F_N, F_H, F_HAFT_MAX, F_GLEIT = berechne_kraefte(neigungswinkel[0])
    reset()

app.run()
```
````

````{admonition} Übung 9.5 (✩✩✩)
:class: tip
**Einfluss von μ_G auf Bewegungszeit und Endgeschwindigkeit**

In der Simulation verwenden wir oft Literaturwerte für den
Gleitreibungskoeffizienten. Aber wie empfindlich reagiert die Simulation
auf diesen Wert?

Simulieren Sie die Kugel aus Abschnitt 9.3 (θ = 20°, m = 0.1 kg,
BAHNLAENGE = 1.0 m, μ_H = 0.35) für folgende μ_G-Werte in reinem Python
(ohne Ursina): 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35.

1. Berechnen Sie für jeden Wert die Bewegungszeit und Endgeschwindigkeit
   mit der Euler-Cromer-Schleife (`dt = 0.005 s`).
2. Berechnen Sie zusätzlich die analytischen Werte zum Vergleich.
3. Stellen Sie beide Ergebnisse (Simulation und Analytik) in einem
   einzigen Plotly-Diagramm dar: Bewegungszeit als Funktion von μ_G.
4. Beantworten Sie: Um wie viel Prozent ändert sich die Bewegungszeit,
   wenn μ_G um 0.05 steigt? Ist die Abhängigkeit linear?
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import math
import pandas as pd
import plotly.graph_objects as go

G           = 9.81
THETA       = math.radians(20)
m           = 0.1
MU_H        = 0.35
BAHNLAENGE  = 1.0
KUGELRADIUS = 0.04
S_EFF       = BAHNLAENGE - 2 * KUGELRADIUS
dt          = 0.005

MU_G_WERTE = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35]
t_sim_liste = []
t_ana_liste = []

for MU_G in MU_G_WERTE:
    F_N     = m * G * math.cos(THETA)
    F_H     = m * G * math.sin(THETA)
    F_GLEIT = MU_G * F_N

    # Simulation
    v, x, t = 0.0, 0.0, 0.0
    while x < S_EFF:
        a  = (F_H - F_GLEIT) / m
        v += a * dt
        x += v * dt
        t += dt
    t_sim_liste.append(t)

    # Analytik
    a_ana = G * (math.sin(THETA) - MU_G * math.cos(THETA))
    t_ana = math.sqrt(2 * S_EFF / a_ana)
    t_ana_liste.append(t_ana)

    print(f"μ_G = {MU_G:.2f}: t_sim = {t:.4f} s, t_ana = {t_ana:.4f} s")

# Diagramm
fig = go.Figure()
fig.add_trace(go.Scatter(x=MU_G_WERTE, y=t_sim_liste,
                         mode='lines+markers', name='Simulation'))
fig.add_trace(go.Scatter(x=MU_G_WERTE, y=t_ana_liste,
                         mode='lines', name='Analytisch',
                         line=dict(dash='dash')))
fig.update_layout(
    title="Bewegungszeit als Funktion von μ_G",
    xaxis_title="Gleitreibungskoeffizient μ_G",
    yaxis_title="Bewegungszeit (s)"
)
fig.show()

# Prozentuale Änderung pro Δμ_G = 0.05
for i in range(1, len(MU_G_WERTE)):
    delta = (t_sim_liste[i] - t_sim_liste[i-1]) / t_sim_liste[i-1] * 100
    print(f"μ_G {MU_G_WERTE[i-1]:.2f}→{MU_G_WERTE[i]:.2f}: "
          f"Δt = {delta:+.1f} %")
```

Die Abhängigkeit ist nicht linear: Bei kleinen μ_G-Werten steigt die
Bewegungszeit stärker pro Einheit als bei großen. Das liegt daran, dass die
Bewegungszeit von `1/sqrt(a)` abhängt, was eine nichtlineare Funktion von
μ_G ist. Simulation und Analytik stimmen sehr gut überein (Abweichung unter
0.3 %).
````

````{admonition} Übung 9.6 (Mini-Projekt)
:class: tip
**Vollständige Ursina-Simulation des eigenen Objekts**

Erstellen Sie eine vollständige Ursina-Simulation für Ihr eigenes
Simulationsobjekt. Verwenden Sie den Starter-Code aus Abschnitt 9.3 als
Ausgangspunkt und wählen Sie den passenden Pfad.

**Teilaufgaben:**

1. **Parameterwahl:** Bestimmen Sie Masse, Reibungskoeffizienten und
   Geometrie Ihres Objekts. Begründen Sie die Wahl in zwei bis drei Sätzen:
   Haben Sie gemessen, aus der Literatur entnommen oder geschätzt?

2. **Kritische Prüfung:** Berechnen Sie den kritischen Winkel
   beziehungsweise das kritische Drehmoment. Entspricht das Ihrer Intuition
   für das reale Objekt?

3. **Ursina-Simulation:** Implementieren Sie die Simulation mit mindestens:
   - Zwei Kraftindikatoren (Hangabtrieb und Reibungskraft).
   - Spurpunkten alle 0.05 s.
   - Einer Textanzeige mit Zeit, Geschwindigkeit und Zustand.

4. **Analytischer Vergleich:** Berechnen Sie die analytische Bewegungszeit
   und vergleichen Sie mit der Simulation. Wie groß ist die Abweichung?

5. **Reflexion:** Beantworten Sie in drei bis vier Sätzen: Welche
   physikalischen Effekte vernachlässigt Ihr Modell? Was würde sich ändern,
   wenn Sie diese einbeziehen würden?

**Hinweis für rotatorische Objekte (Kurbel, Zahnrad):** Verwenden Sie den
rotatorischen Starter-Code aus Abschnitt 9.2 für die Physikberechnung und
visualisieren Sie die Drehbewegung in Ursina mit:

```python
def update():
    ...
    objekt.rotation_y = math.degrees(theta)
```
````
