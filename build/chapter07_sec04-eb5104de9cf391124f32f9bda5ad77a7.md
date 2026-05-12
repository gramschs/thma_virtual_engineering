---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Übungen

```{admonition} Übung 7.1 (✩)
:class: tip
**Parameter für drei Anforderungsprofile wählen**

Drei Ingenieurinnen drucken dasselbe Bauteil für drei verschiedene Zwecke.
Jede hat andere Anforderungen:

| Profil | Zweck | Wichtigstes Kriterium |
| ------ | ----- | --------------------- |
| A | Erste schnelle Funktionsprüfung | Kurze Druckzeit |
| B | Präsentationsmodell für einen Messestand | Glatte Oberfläche |
| C | Mechanisch belastetes Ersatzteil | Hohe Festigkeit |

Die folgende Tabelle listet vier Parametersätze. Weisen Sie jedem Profil
(A, B, C) den passenden Parametersatz zu und begründen Sie Ihre Wahl jeweils
in einem Satz. Ein Parametersatz bleibt übrig.

| Satz | Schichthöhe | Fülldichte | Druckgeschwindigkeit |
| ---- | ----------- | ---------- | -------------------- |
| 1 | 0.30 mm | 15 % | 70 mm/s |
| 2 | 0.10 mm | 20 % | 30 mm/s |
| 3 | 0.20 mm | 55 % | 45 mm/s |
| 4 | 0.15 mm | 20 % | 45 mm/s |
```

````{admonition} Lösung
:class: tip
:class: dropdown
**Profil A → Satz 1** (0.30 mm / 15 % / 70 mm/s): Die große Schichthöhe
reduziert die Schichtenanzahl und damit die Druckzeit am stärksten. Die
geringe Fülldichte und die hohe Druckgeschwindigkeit verstärken diesen
Effekt. Die Oberflächenqualität ist zweitrangig.

**Profil B → Satz 2** (0.10 mm / 20 % / 30 mm/s): Eine sehr feine
Schichthöhe erzeugt die glatteste Oberfläche, weil der Treppeneffekt an
Kurven und schrägen Flächen minimal ist. Die niedrige Druckgeschwindigkeit
unterstützt die Qualität der Außenwand.

**Profil C → Satz 3** (0.20 mm / 55 % / 45 mm/s): Die hohe Fülldichte
erhöht die Materialstärke im Inneren und damit die Biegefestigkeit und
Druckfestigkeit des Bauteils. Schichthöhe und Geschwindigkeit sind ein
ausgewogener Kompromiss.

**Übrig bleibt Satz 4**: Dieser Satz entspricht dem Ausgangspunkt für die
Kugelbahn aus Abschnitt 7.1 und 7.3 und ist ein guter Allround-Kompromiss,
aber keines der drei spezifischen Profile trifft er am besten.
````

---

````{admonition} Übung 7.2 (✩✩)
:class: tip
**Drei Druckfehler diagnostizieren**

Drei Kollegen beschreiben ihre Druckergebnisse. Identifizieren Sie jeweils
den Druckfehler aus Abschnitt 7.2, nennen Sie die wahrscheinlichste Ursache
in den Druckparametern und schlagen Sie eine konkrete Korrekturmaßnahme vor.

**Beschreibung 1:**
Die Kugelbahn liegt nach dem Druck vollständig auf der Druckplatte, aber
zwei der vier Ecken haben sich um etwa 2 mm nach oben gewölbt. Gedruckt
wurde mit PLA bei 50 °C Betttemperatur und 60 mm/s für die erste Schicht.

**Beschreibung 2:**
Die Führungsrille sieht von oben einwandfrei aus. Beim Blick von unten durch
einen Lichtspalt erkennt man jedoch, dass zwischen den Außenwänden der
Rille schmale Lücken klaffen, durch die Licht fällt. Die Drucktemperatur
lag bei 195 °C, die Druckgeschwindigkeit bei 75 mm/s.

**Beschreibung 3:**
Das Objekt hat eine saubere Außenwand und sitzt gut auf der Platte. Zwischen
zwei getrennt gedruckten Bögen der Führungsrille hängen jedoch feine
Kunststofffäden. Gedruckt wurde bei 220 °C; der Filamentrückzug war im Slicer
auf 0.5 mm eingestellt.
````

````{admonition} Lösung
:class: tip
:class: dropdown
**Beschreibung 1: Warping**

Ursache: Die Betttemperatur von 50 °C ist für PLA zu niedrig. Das Material
kühlt an den Ecken schnell ab und zieht sich zusammen, bevor die Haftung
zur Druckplatte stabil genug ist. Die hohe erste-Schicht-Geschwindigkeit
von 60 mm/s gibt dem Material zusätzlich wenig Zeit, sich mit der
Druckplattenoberfläche zu verbinden.

Korrekturmaßnahme: Betttemperatur auf 60 bis 65 °C erhöhen.
Erste-Schicht-Geschwindigkeit auf 20 mm/s senken. Falls das Problem
bestehen bleibt, Druckplattenoberfläche mit Isopropanol reinigen.

**Beschreibung 2: Unterextrusion**

Ursache: Die Kombination aus 195 °C (unteres Ende des PLA-Bereichs) und
75 mm/s (hohe Geschwindigkeit) führt dazu, dass die Nozzle schneller
bewegt wird, als das Material bei dieser Temperatur fließen kann. Das
Ergebnis ist zu wenig Material pro Extrusionsstrecke, was sich als Lücken
zwischen den Wand-Bahnen zeigt.

Korrekturmaßnahme: Drucktemperatur auf 205 bis 210 °C erhöhen oder
Druckgeschwindigkeit auf 45 bis 50 mm/s senken. Beide Maßnahmen zusammen
sind noch wirkungsvoller.

**Beschreibung 3: Stringing**

Ursache: 220 °C liegt am oberen Ende des PLA-Temperaturbereichs und macht
das Material sehr dünnflüssig. Ein Filamentrückzug von 0.5 mm ist zu kurz, um
den Druckabfall in der Nozzle bei einem Travel-Move vollständig
auszugleichen. Das flüssige Material tritt daher während des Travel-Moves
aus der Nozzle aus und zieht Fäden.

Korrekturmaßnahme: Drucktemperatur auf 205 bis 210 °C senken. Retraktion
auf 1.5 bis 2.0 mm erhöhen (für direkt angetriebene Systeme) beziehungsweise
auf 4 bis 6 mm (für Bowden-Extruder). Im Slicer zusätzlich
"Avoid crossing perimeters" aktivieren, um Travel-Moves über den Spalt
zwischen den Bögen zu vermeiden.
````

---

````{admonition} Übung 7.3 (✩✩✩)
:class: tip
**Parameterstudie: Druckzeit und Oberflächenqualität modellieren**

Der Einfluss der Schichthöhe auf Druckzeit und Oberflächenqualität lässt sich
mit einem vereinfachten Modell quantifizieren.

**Modell:**
Wir nehmen an, dass die Druckzeit $t$ proportional zur Anzahl der Schichten
$n$ ist:

\begin{equation*}
t = n \cdot t_\text{Schicht}, \quad n = \frac{H}{h}
\end{equation*}

mit der Objekthöhe $H = 80$ mm, der Schichthöhe $h$ und der mittleren Zeit
pro Schicht $t_\text{Schicht} = 42$ s.

Die sichtbare Stufenhöhe an einer schrägen Fläche (Treppeneffekt) bei einem
Überhangwinkel $\alpha = 40°$ zur Vertikalen berechnet sich näherungsweise als:

\begin{equation*}
s = h \cdot \tan(\alpha)
\end{equation*}

**Aufgabe:** Berechnen Sie für Schichthöhen von 0.05 mm bis 0.35 mm in
Schritten von 0.02 mm jeweils die Druckzeit in Stunden und die Stufenhöhe
in mm. Stellen Sie beide Größen als Diagramm über der Schichthöhe dar und
markieren Sie den empfohlenen Wert von 0.15 mm. Beantworten Sie anschließend
die Fragen 4 und 5.

Lösen Sie die Aufgabe mit **Weg 1** (Tabellenkalkulation) oder **Weg 2**
(Python):

---

**Weg 1: Tabellenkalkulation** (Excel, LibreOffice Calc, Numbers oder vergleichbar)

Legen Sie ein neues Tabellenblatt an. Zeile 1 enthält Spaltenüberschriften,
die Daten beginnen in Zeile 2.

| Spalte | Überschrift | Inhalt / Formel ab Zeile 2 |
| ------ | ----------- | -------------------------- |
| A | Schichthöhe (mm) | 0.05 in A2, dann `=A2+0.02` in A3 usw. bis 0.35 |
| B | Anzahl Schichten | `=80/A2` |
| C | Druckzeit (h) | `=B2*42/3600` |
| D | Stufenhöhe (mm) | `=A2*TAN(RADIANS(40))` |

Ziehen Sie alle Formeln bis zur letzten Zeile (Schichthöhe 0.35 mm) nach
unten. Das ergibt 16 Datenzeilen. Erstellen Sie dann zwei Liniendiagramme:
Spalte C über Spalte A und Spalte D über Spalte A. Markieren Sie in beiden
Diagrammen die Spalte, die $h = 0.15$ mm entspricht, farblich oder fügen
Sie eine Hilfslinie ein.

---

**Weg 2: Python**

```{code-cell} python
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---- Objekt- und Prozessparameter ----
OBJECT_HEIGHT_MM   = 80.0   # Höhe der Kugelbahn in mm
TIME_PER_LAYER_S   = 42.0   # mittlere Zeit pro Schicht in Sekunden
OVERHANG_ANGLE_DEG = 40.0   # typischer Überhangwinkel der Führungsrille

LAYER_HEIGHTS = np.arange(0.05, 0.37, 0.02)  # 0.05, 0.07, ..., 0.35

# ---- Aufgabe 1 ----
# Berechnen Sie als Arrays:
#   - layer_count:    Anzahl der Schichten
#   - print_time_h:   Druckzeit in Stunden
#   - step_height_mm: Stufenhöhe in mm (Winkel zuerst in Bogenmaß umrechnen)

# layer_count    = ...
# print_time_h   = ...
# step_height_mm = ...

# ---- Aufgabe 2 ----
# Erstellen Sie zwei Subplots nebeneinander:
#   links:  Druckzeit (h) über Schichthöhe (mm)
#   rechts: Stufenhöhe (mm) über Schichthöhe (mm)
# Markieren Sie h = 0.15 mm in beiden Subplots mit add_vline.

# ---- Aufgabe 3 ----
# Berechnen und drucken Sie: Um welchen Faktor steigt die Druckzeit,
# wenn wir von 0.35 mm auf 0.05 mm wechseln?
```

---

**Fragen (für beide Wege):**

4. Bei welcher Schichthöhe liegt die Druckzeit erstmals unter 4 Stunden?
   Lesen Sie den Wert aus Ihrem Diagramm oder Ihrer Tabelle ab.
5. Welche Schichthöhe ist maximal zulässig, damit die Stufenhöhe an der
   Führungsrille unter 0.15 mm bleibt? Berechnen Sie den Wert analytisch
   aus der Formel.
````

````{admonition} Lösung
:class: tip
:class: dropdown
**Weg 1: Tabellenkalkulation**

Die fertige Tabelle (Auszug, gerundete Werte):

| Schichthöhe (mm) | Anzahl Schichten | Druckzeit (h) | Stufenhöhe (mm) |
| ---------------- | ---------------- | ------------- | --------------- |
| 0.05 | 1600 | 18.67 | 0.042 |
| 0.07 | 1143 | 13.33 | 0.059 |
| 0.09 | 889 | 10.37 | 0.076 |
| 0.11 | 727 | 8.48 | 0.092 |
| 0.13 | 615 | 7.17 | 0.109 |
| 0.15 | 533 | 6.22 | 0.126 |
| 0.17 | 471 | 5.49 | 0.143 |
| 0.19 | 421 | 4.91 | 0.159 |
| 0.21 | 381 | 4.44 | 0.176 |
| 0.23 | 348 | 4.06 | 0.193 |
| 0.25 | 320 | 3.73 | 0.210 |
| 0.27 | 296 | 3.45 | 0.227 |
| 0.29 | 276 | 3.22 | 0.243 |
| 0.31 | 258 | 3.01 | 0.260 |
| 0.33 | 242 | 2.83 | 0.277 |
| 0.35 | 229 | 2.67 | 0.294 |

Die Druckzeit sinkt von 18.67 h (0.05 mm) auf 2.67 h (0.35 mm). Die
Stufenhöhe steigt linear von 0.042 mm auf 0.294 mm. Der Wert bei 0.15 mm
ist in beiden Spalten gut ablesbar und dient als Referenz.

---

**Weg 2: Python-Lösung**

```python
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

OBJECT_HEIGHT_MM   = 80.0
TIME_PER_LAYER_S   = 42.0
OVERHANG_ANGLE_DEG = 40.0

LAYER_HEIGHTS = np.arange(0.05, 0.37, 0.02)

# Aufgabe 1
layer_count    = OBJECT_HEIGHT_MM / LAYER_HEIGHTS
print_time_h   = layer_count * TIME_PER_LAYER_S / 3600
step_height_mm = LAYER_HEIGHTS * np.tan(np.deg2rad(OVERHANG_ANGLE_DEG))

# Aufgabe 2
fig = make_subplots(rows=1, cols=2,
    subplot_titles=["Druckzeit (h)", "Stufenhöhe am Überhang (mm)"])
fig.add_trace(go.Scatter(x=LAYER_HEIGHTS, y=print_time_h,
    mode="lines+markers", line=dict(color="steelblue"), name="Druckzeit"),
    row=1, col=1)
fig.add_trace(go.Scatter(x=LAYER_HEIGHTS, y=step_height_mm,
    mode="lines+markers", line=dict(color="firebrick"), name="Stufenhöhe"),
    row=1, col=2)
for col in [1, 2]:
    fig.add_vline(x=0.15, line_dash="dot", line_color="gray",
                  annotation_text="0.15 mm", row=1, col=col)
fig.update_xaxes(title_text="Schichthöhe (mm)")
fig.update_layout(title="Parameterstudie Schichthöhe", showlegend=False)
fig.show()

# Aufgabe 3
faktor = print_time_h[0] / print_time_h[-1]
print(f"Zeitverhältnis 0.05 mm / 0.35 mm: {faktor:.1f}×")
```

Das Zeitverhältnis beträgt 0.35 / 0.05 = **7×**: Eine Schichthöhe von
0.05 mm dauert siebenmal so lang wie 0.35 mm.

---

**Frage 4:** Die Druckzeit liegt erstmals unter 4 Stunden bei einer
Schichthöhe von etwa **0.25 mm** (Tabelle: 3.73 h; die Zeile 0.23 mm liegt
mit 4.06 h noch knapp darüber).

**Frage 5:** Gesucht ist $h$ mit $s \leq 0.15$ mm:

\begin{equation*}
h \leq \frac{s}{\tan(\alpha)} = \frac{0.15}{\tan(40°)} = \frac{0.15}{0.839} \approx 0.179 \text{ mm}
\end{equation*}

Eine Schichthöhe von maximal **0.18 mm** hält die Stufenhöhe unter 0.15 mm.
Der empfohlene Wert von 0.15 mm liegt mit $0.15 \cdot 0.839 \approx
0.126$ mm sicher darunter und ist damit gut begründet.
````

---

````{admonition} Übung 7.4 (Mini-Projekt)
:class: tip
**Eigenes Projekt slicen, dokumentieren und bewerten**

Führen Sie den vollständigen Slicer-Workflow aus Abschnitt 7.3 auf Ihrem
eigenen bereinigten Mesh durch und dokumentieren Sie jeden Schritt.

**Teil 1: Slicen mit empfohlenen Parametern**

Importieren Sie Ihr Mesh in den Slicer Ihrer Wahl (PrusaSlicer oder Cura)
und führen Sie Schritt 1 bis 5 aus Abschnitt 7.3 durch. Notieren Sie:

- Welche Mesh-Fehler hat der Slicer gemeldet?
- Welche Druckorientierung haben Sie gewählt, und warum?
- Druckzeit und Materialgewicht mit den empfohlenen Parametern.
- Eine auffällige Stelle in der Layer-Vorschau (Stützstruktur, langer
  Travel-Move) mit Screenshot und kurzer Erläuterung.

**Teil 2: Parameterstudie mit zwei Varianten**

Erstellen Sie zwei weitere G-Code-Dateien, in denen Sie je einen Parameter
gezielt verändern:

- Variante 1: Schichthöhe auf 0.30 mm erhöhen (alle anderen Parameter gleich)
- Variante 2: Fülldichte auf 50 % erhöhen (alle anderen Parameter gleich)

Tragen Sie die Ergebnisse in die folgende Tabelle ein:

| Variante | Schichthöhe | Fülldichte | Druckzeit | Materialgewicht |
| -------- | ----------- | ---------- | --------- | --------------- |
| Basis (7.3) | 0.15 mm | 20 % | | |
| Variante 1 | 0.30 mm | 20 % | | |
| Variante 2 | 0.15 mm | 50 % | | |

**Teil 3: Auswertung und Reflexion**

Beantworten Sie die folgenden Fragen auf Basis Ihrer Tabelle:

1. Um welchen Faktor hat sich die Druckzeit zwischen Basis und Variante 1
   verändert? Stimmt dieser Faktor mit der Modellvorhersage aus Übung 7.3
   überein?
2. Welche Variante würden Sie für einen ersten realen Druck der Kugelbahn
   wählen, und welche für eine finale Präsentation? Begründen Sie Ihre
   Entscheidung.
3. Nennen Sie einen Druckfehler aus Abschnitt 7.2, der bei Variante 1
   wahrscheinlicher ist als bei der Basis-Variante, und erklären Sie warum.

*Optionale Erweiterung:* Drucken Sie eine der drei Varianten tatsächlich
aus. Vergleichen Sie die tatsächliche Druckzeit mit der Slicer-Schätzung
und die Oberflächenqualität zwischen Basis und Variante 1.
````
