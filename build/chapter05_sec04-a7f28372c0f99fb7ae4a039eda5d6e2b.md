---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Übungen

````{admonition} Übung 5.1 (✩)
:class: tip
**Begriffe zuordnen**

Ordnen Sie jeden der folgenden Fachbegriffe der richtigen Beschreibung zu.

**Begriffe:** ICP, RMS-Fehler, Vorausrichtung, Lokales Minimum, Überlappungsgrad,
Starrkörpertransformation

**Beschreibungen:**
1. Maß für den mittleren quadratischen Abstand zwischen korrespondierenden
   Punkten zweier Meshes nach der Ausrichtung.
2. Anteil der Oberfläche, der in beiden Scans sichtbar und damit für die
   Ausrichtung nutzbar ist.
3. Transformation, die ein Mesh dreht und verschiebt, ohne seine Form oder
   Größe zu verändern.
4. Iterativer Algorithmus, der zwei Punktmengen durch wiederholtes Suchen
   nächster Nachbarn und Minimieren des Abstands ausrichtet.
5. Zustand, in dem der ICP-Algorithmus konvergiert ist, das Ergebnis aber
   nicht die global beste Ausrichtung darstellt.
6. Grobe manuelle oder halbautomatische Annäherung zweier Scans vor der
   feinen algorithmischen Ausrichtung.
````

````{admonition} Lösung
:class: tip
:class: dropdown
| Beschreibung | Begriff |
| ------------ | ------- |
| 1 | RMS-Fehler |
| 2 | Überlappungsgrad |
| 3 | Starrkörpertransformation |
| 4 | ICP |
| 5 | Lokales Minimum |
| 6 | Vorausrichtung |

**Zur Vertiefung:**

Der *RMS-Fehler* (Root Mean Square error) ist der zentrale Qualitätsmaßstab
nach einer Registration. Er gibt den quadratischen Mittelwert aller
Punkt-zu-Punkt-Abstände an und liegt in derselben Einheit wie die Koordinaten
des Meshes, also bei uns in Millimetern.

Der *Überlappungsgrad* ist besonders relevant, wenn zwei Scans nicht exakt
dieselbe Oberfläche zeigen. Ein zu hoch angesetzter Überlappungsgrad im
ICP-Dialog führt dazu, dass ICP Korrespondenzen zwischen Punkten sucht, die
gar nicht in beiden Meshes vorhanden sind, und damit systematisch falsche
Transformationen berechnet.

Die *Starrkörpertransformation* ist die fundamentale Einschränkung der
Registration: Wir erlauben ausschließlich Rotation und Translation, keine
Skalierung. Das ist sinnvoll, weil zwei Scans desselben Objekts dieselbe
physikalische Größe haben sollten. Kleine Unterschiede in den Boundingboxen
(wie in Abschnitt 5.3 beobachtet) sind Messfehler der Photogrammetrie, keine
echten Größenunterschiede des Objekts.
````

---

````{admonition} Übung 5.2 (✩✩)
:class: tip
**Konvergenzverlauf interpretieren**

Ein ICP-Lauf auf zwei Scans desselben Maschinenbauteils liefert folgende
Protokollzeilen:

| Iteration | RMS-Fehler (mm) | Δ RMS (mm) |
| --------- | --------------- | ---------- |
| 1         | 4.832           | -          |
| 5         | 1.204           | 3.628      |
| 10        | 0.387           | 0.817      |
| 20        | 0.291           | 0.096      |
| 50        | 0.288           | 0.003      |
| 100       | 0.288           | 0.000      |

1. Ab welcher Iteration ist der Algorithmus praktisch konvergiert? Begründen
   Sie Ihre Antwort anhand der Δ RMS-Spalte.
2. Wie bewerten Sie den finalen RMS-Fehler von 0.288 mm für eine
   Photogrammetrie-Aufnahme mit einem Smartphone? Ist das eine gute oder
   eine schlechte Registration?
3. Ein zweiter Versuch mit einer schlechteren Vorausrichtung liefert nach
   100 Iterationen einen RMS von 3.91 mm, der sich nicht mehr verändert.
   Was ist wahrscheinlich passiert?
````

````{admonition} Lösung
:class: tip
:class: dropdown
**Teilaufgabe 1: Ab welcher Iteration ist der Algorithmus konvergiert?**

Praktisch konvergiert ist der Algorithmus ab **Iteration 50**. In der
Δ RMS-Spalte beobachten wir folgende Entwicklung:

- Von Iteration 1 zu 5: Δ RMS = 3.628 mm. Sehr starke Verbesserung in der
  Anfangsphase. ICP korrigiert die grobe Versetzung aus der Vorausrichtung.
- Von Iteration 5 zu 10: Δ RMS = 0.817 mm. Weiterhin deutliche Verbesserung.
- Von Iteration 10 zu 20: Δ RMS = 0.096 mm. Die Verbesserung wird kleiner, aber
  noch spürbar.
- Von Iteration 20 zu 50: Δ RMS = 0.003 mm. Die Verbesserung über 30
  Iterationen hinweg beträgt nur noch 3 Mikrometer. Das liegt weit unterhalb
  der Messgenauigkeit unserer Photogrammetrie-Aufnahme.
- Von Iteration 50 zu 100: Δ RMS = 0.000 mm. Keine messbare Veränderung mehr.

Das formale Konvergenzkriterium (Δ RMS < $10^{-5}$) wäre spätestens bei
Iteration 100 erfüllt. Praktisch ist die Registration aber bereits nach
Iteration 50 abgeschlossen, weil Δ RMS = 0.003 mm für unsere Zwecke
vernachlässigbar ist.

**Teilaufgabe 2: Bewertung des finalen RMS-Fehlers**

Ein RMS-Fehler von 0.288 mm ist für eine Smartphone-Photogrammetrie-
Aufnahme **sehr gut**. Als Einordnung:

Die Photogrammetrie mit einem Smartphone erreicht bei einem handgroßen Objekt
(charakteristische Länge etwa 200 mm) unter guten Bedingungen eine relative
Genauigkeit von 0.1 bis 0.3 Prozent. 0.288 mm entspricht bei einem 200-mm-
Objekt einem relativen Fehler von 0.14 Prozent und liegt damit am unteren Ende
des erreichbaren Bereichs. Für die Qualitätssicherung unserer Kugelbahn in
Kapitel 6 ist dieser RMS-Fehler akzeptabel: Abweichungen in der
Abweichungsanalyse, die deutlich über 0.3 mm liegen, sind dann tatsächlichen
geometrischen Unterschieden zwischen den Scans zuzuschreiben und nicht dem
Registrationsfehler.

**Teilaufgabe 3: Was ist beim zweiten Versuch passiert?**

Ein RMS-Fehler von 3.91 mm, der sich nach 100 Iterationen nicht mehr
verändert, ist ein klassisches **lokales Minimum**. ICP hat konvergiert, aber
in eine geometrisch falsche Lösung. 

Was wahrscheinlich passiert ist: Die schlechtere Vorausrichtung hat dazu
geführt, dass ICP im ersten Iterationsschritt geometrisch sinnlose
Korrespondenzen gefunden hat, weil die Meshes zu weit voneinander entfernt
lagen. Die berechnete Transformation war daraufhin geometrisch falsch, aber
ICP hat sie angewendet und ist in der nächsten Iteration auf dasselbe Problem
gestoßen. Da jede Iteration auf der vorherigen aufbaut, hat sich ICP von der
korrekten Lösung entfernt und ist in einem Zustand "eingefroren", aus dem er
durch weitere Iterationen nicht mehr herauskommt.

Die Gegenmaßnahme ist, die Vorausrichtung zu verbessern, bis der initiale
RMS-Fehler unter etwa 6 bis 7 mm liegt, bevor ICP gestartet wird. In Übung
5.3 werden wir diesen kritischen Schwellenwert quantitativ bestimmen.
````

---

````{admonition} Übung 5.3 (✩✩✩)
:class: tip
**Parameterstudie: Vorausrichtungsqualität und ICP-Ergebnis**

In dieser Aufgabe untersuchen wir, wie stark die Qualität der Vorausrichtung
das finale ICP-Ergebnis beeinflusst. Wir arbeiten mit simulierten Daten.

**Gegebene Messwerte** (simuliert; ICP mit maximal 100 Iterationen,
Überlappungsgrad 80 %, Ausgangsfehler variiert durch unterschiedlich gute
Vorausrichtung):

| Initialer RMS (mm) | Finaler RMS (mm) | Iterationen bis Konvergenz | Globales Minimum erreicht |
| ------------------ | ---------------- | -------------------------- | ------------------------- |
| 0.8                | 0.29             | 18                         | Ja                        |
| 2.5                | 0.31             | 47                         | Ja                        |
| 5.1                | 0.30             | 89                         | Ja                        |
| 9.3                | 1.84             | 100                        | Nein                      |
| 15.7               | 4.12             | 100                        | Nein                      |

1. Visualisieren Sie initialen und finalen RMS-Fehler als Balkendiagramm
   nebeneinander (optional mit Python), farblich unterschieden nach "Globales Minimum
   erreicht".
2. Bestimmen Sie den kritischen Schwellenwert des initialen RMS-Fehlers,
   oberhalb dessen ICP in einem lokalen Minimum stecken bleibt.
3. Leiten Sie eine praktische Empfehlung ab: Wie gut muss eine manuelle
   Vorausrichtung mindestens sein, bevor man ICP startet?
````

````{admonition} Lösung
:class: tip
:class: dropdown
**Teilaufgabe 1: Visualisierung**

Hier ist eine Beispiellösung mit Python und Plotly Express.
```python
import plotly.express as px
import pandas as pd

# Rohdaten aus der Tabelle
INITIAL_RMS = [0.8, 2.5, 5.1, 9.3, 15.7]
FINAL_RMS   = [0.29, 0.31, 0.30, 1.84, 4.12]
GLOBAL_MIN  = ['Ja', 'Ja', 'Ja', 'Nein', 'Nein']

# Daten in das Long-Format für Plotly umwandeln
rows = []
for i, (init, final, gmin) in enumerate(zip(INITIAL_RMS, FINAL_RMS, GLOBAL_MIN)):
    rows.append({'Experiment': i + 1,
                 'RMS (mm)': init,
                 'Phase': 'Initialer RMS',
                 'Globales Minimum': gmin})
    rows.append({'Experiment': i + 1,
                 'RMS (mm)': final,
                 'Phase': 'Finaler RMS',
                 'Globales Minimum': gmin})

df = pd.DataFrame(rows)

fig = px.bar(
    df,
    x='Experiment',
    y='RMS (mm)',
    color='Globales Minimum',
    pattern_shape='Phase',
    barmode='group',
    title='ICP-Parameterstudie: Einfluss der Vorausrichtungsqualität',
    color_discrete_map={'Ja': '#1976D2', 'Nein': '#D32F2F'},
    labels={'Globales Minimum': 'Globales Minimum erreicht',
            'Phase': 'Messphase'}
)
fig.update_layout(
    xaxis_title='Experiment',
    yaxis_title='RMS-Fehler (mm)',
    legend_title_text='Legende'
)
fig.show()
```

Im Diagramm sind fünf Experimente nebeneinander dargestellt. Für jedes
Experiment erscheinen zwei Balken: einer für den initialen RMS-Fehler
(Balken mit Schraffur), einer für den finalen RMS-Fehler (einfarbiger
Balken). Blaue Balken zeigen Experimente, bei denen das globale Minimum
erreicht wurde; rote Balken zeigen lokale Minima.

Das Muster ist deutlich: Bei den ersten drei Experimenten (blau) ist der
finale RMS-Fehler etwa zehnmal kleiner als der initiale RMS-Fehler. Bei
den letzten beiden Experimenten (rot) bleibt der finale RMS-Fehler auf
sehr hohem Niveau, weit über dem der erfolgreichen Experimente.

**Teilaufgabe 2: Kritischer Schwellenwert**

Der kritische Schwellenwert liegt zwischen **5.1 mm und 9.3 mm**. Bei einem
initialen RMS-Fehler von 5.1 mm hat ICP noch das globale Minimum gefunden.
Bei 9.3 mm ist ICP in einem lokalen Minimum stecken geblieben.

Als konservativer Schwellenwert ergibt sich ein Wert von etwa **7 mm** als
Mitte des Intervalls. Da wir mit nur fünf Datenpunkten arbeiten und der
tatsächliche Schwellenwert von der Objektgeometrie und vom Überlappungsgrad
abhängt, empfehlen wir, diesen Wert nicht als feste Grenze, sondern als
Orientierungswert zu verstehen.

Interessant ist außerdem die Anzahl der Iterationen bis zur Konvergenz: Bei
einem initialen RMS von 5.1 mm braucht ICP bereits 89 Iterationen, also fast
das Maximum. Das ist ein Warnsignal: Wenn ICP nahe an der maximalen
Iterationsgrenze konvergiert, ist die Vorausrichtung wahrscheinlich schon zu
grob.

**Teilaufgabe 3: Praktische Empfehlung**

Eine manuelle Vorausrichtung sollte einen initialen RMS-Fehler von
**unter 6 mm** erreichen, bevor ICP gestartet wird. Das entspricht
einem konservativen Abstand zum empirisch bestimmten Schwellenwert von
7 mm und lässt einen Sicherheitspuffer, weil die Daten in dieser Aufgabe
simuliert sind und reale Objekte abweichen können.

Operativ bedeutet das: Wir beurteilen die Vorausrichtung im 3D Viewer, bevor
wir ICP starten. Wenn die Oberflächen der beiden Meshes im 3D Viewer grob
übereinanderliegen und an keiner Stelle eine sichtbare Versetzung von mehr als
einem Drittel der Objektausdehnung zeigen, ist die Vorausrichtung
wahrscheinlich gut genug. Ist die Versetzung größer, fügen wir weitere
Referenzpunktpaare hinzu oder verbessern die Position der bestehenden Paare.
````

---

````{admonition} Übung 5.4 (Mini-Projekt)
:class: tip
**Vollständige Registration zweier eigener Scans**

Führen Sie die vollständige Registration aus Abschnitt 5.3 auf zwei eigenen
Meshroom-Ergebnissen durch.

**Teilaufgaben:**

1. **Vorbereitung:** Laden Sie beide bereinigten Meshes aus Kapitel 4 in
   CloudCompare und dokumentieren Sie ihre Ausgangslage im 3D Viewer
   (Screenshot). Schätzen Sie den initialen Abstand zwischen beiden Meshes
   grob ab.

2. **Vorausrichtung:** Führen Sie die manuelle Vorausrichtung mit mindestens
   drei Referenzpunktpaaren durch. Notieren Sie, welche markanten Stellen des
   Objekts Sie als Referenzpunkte gewählt haben und warum.

3. **ICP:** Führen Sie die ICP-Registration durch und notieren Sie den
   RMS-Fehler vor und nach ICP sowie die Anzahl der Iterationen bis zur
   Konvergenz.

4. **Bewertung:** Vergleichen Sie Ihr Ergebnis mit dem in Übung 5.2
   analysierten Konvergenzverlauf. Ist Ihre Registration qualitativ gut?
   Was könnte den RMS-Fehler weiter senken?

5. **Dokumentation:** Erstellen Sie eine kurze Dokumentation (ca. 300 bis
   400 Wörter) mit Screenshots der Vorausrichtung, des ICP-Ergebnisses und
   einer tabellarischen Zusammenfassung der Kennzahlen.

*Optionale Erweiterung:* Wiederholen Sie die Registration mit einer
absichtlich schlechteren Vorausrichtung. Ab welchem initialen RMS-Fehler
beobachten Sie ein lokales Minimum? Vergleichen Sie Ihr empirisches Ergebnis
mit dem Schwellenwert aus Übung 5.3.
````
