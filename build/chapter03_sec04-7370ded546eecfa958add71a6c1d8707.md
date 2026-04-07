---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Übungen

In diesen Übungen wenden wir die Konzepte aus Kapitel 3 an:
Mesh-Qualitätskriterien, Interpretation von Meshroom-Ergebnissen und den
Export-Workflow.

---

```{admonition} Übung 3.1 (✩)
:class: tip
**Begriffe zuordnen**

Ordnen Sie jeden der folgenden Fachbegriffe der richtigen Beschreibung zu.
Schreiben Sie die passende Zahl (1-6) neben den Begriff.

**Begriffe:** Vertex, Face, Watertight Mesh, Sparse Point Cloud, Dense Point
Cloud, Edge

**Beschreibungen:**
1. Verbindungslinie zwischen zwei Punkten im 3D-Raum; strukturiert die
   Oberfläche eines Meshes.
2. Dreieckige (oder polygonale) Fläche, die die sichtbare Oberfläche eines
   Meshes bildet.
3. Punktmenge mit mehreren Millionen Punkten, die als Grundlage für das
   Dreiecksmesh dient.
4. Punkt im dreidimensionalen Raum, definiert durch seine (x, y, z)-Koordinaten.
5. Mesh ohne Lücken und ohne Non-Manifold Kanten, das ein eindeutiges
   geschlossenes Volumen einschließt.
6. Erste Punktwolke aus dem Structure-from-Motion-Schritt mit typischerweise
   einigen zehntausend Punkten.
```

```{admonition} Lösung
:class: tip
:class: dropdown
Vertex              → 4

Face                → 2

Watertight Mesh     → 5

Sparse Point Cloud  → 6

Dense Point Cloud   → 3

Edge                → 1
```

---

```{admonition} Übung 3.2 (✩)
:class: tip
**Fehlermuster analysieren**

Betrachten Sie die folgende beschriebene Situation und beantworten Sie die Fragen.

**Situation:** Sie öffnen das Meshroom-Ergebnis eines Kommilitonen in der 3D-Vorschau.
Das Mesh der Kugelbahn sieht auf den ersten Blick vollständig aus. Beim Drehen des
Modells fallen Ihnen jedoch zwei Dinge auf:

- An der linken Seite der Führungsschiene ragt ein einzelner spitzer Vertex etwa
  2 cm aus der Oberfläche heraus.
- Unterhalb des gesamten Modells liegt eine flache, dünne Schicht Geometrie,
  etwa wie eine Bodenplatte, die aber nicht zur Kugelbahn gehört.

**Fragen:**

1. Benennen Sie für jede der beiden beobachteten Anomalien das Fehlermuster aus
   der Tabelle in Abschnitt 3.2.
2. Erklären Sie für jedes Fehlermuster kurz, wie es wahrscheinlich entstanden ist.
3. In welchem Werkzeug werden wir diese Fehler beheben, und in welchem Kapitel?
```

```{admonition} Lösung
:class: tip
:class: dropdown
1. Fehlermuster: Der spitze Vertex ist ein Spike (Ausreißer-Vertex). Die flache
   Schicht unter dem Objekt ist Hintergrundgeometrie.

2. Entstehung: Der Spike entstand, weil ein einzelner Tiefenwert in der DepthMap
   durch Rauschen oder eine Reflexion auf der Führungsschiene stark fehlerhaft
   war und Meshroom diesen Punkt trotzdem übernommen hat. Die
   Hintergrundgeometrie entstand, weil der Tisch oder die Unterlage, auf der die
   Kugelbahn stand, auf allen Fotos sichtbar war und von Meshroom als Teil der
   Szene mitrekonstruiert wurde.

3. Beide Fehler werden in CloudCompare behoben (Kapitel 4 bis 6). Die
   Hintergrundgeometrie lässt sich durch manuelle Selektion und Löschung
   entfernen. Spikes können durch Glättungsfilter oder manuelle Korrektur
   beseitigt werden.
```

---

```{admonition} Übung 3.3 (✩✩)
:class: tip
**Vergleich zweier Meshroom-Ergebnisse**

Sie haben zwei Meshroom-Rekonstruktionen vorliegen:

- **Mesh A**: Eigenes Objekt (ein Plastikgehäuse ohne Aufkleber, einfarbig grau,
  mit 40 Fotos aufgenommen). Meshroom meldet: 38/40 Kameras grün, 2 gelb.
  Das Mesh hat 320 000 Faces. `trimesh` gibt `Watertight: False` aus.

- **Mesh B**: Musterdatensatz Kugelbahn (70 Fotos). Meshroom meldet: 65/70 Kameras
  grün, 5 gelb. Das Mesh hat 560 000 Faces. `trimesh` gibt `Watertight: False` aus.

Vergleichen Sie beide Meshes anhand der vier Qualitätskriterien aus Abschnitt
3.1. Erstellen Sie dafür eine Vergleichstabelle und bewerten Sie jedes Kriterium
auf einer Skala von 1 (schlecht) bis 5 (sehr gut). Begründen Sie Ihre
Bewertungen kurz im Code-Kommentar.
```

```{admonition} Lösung
:class: tip
:class: dropdown
Die Bewertungen können je nach Argumentation variieren. Wichtig ist eine
konsistente Begründung, die auf den konkreten Angaben zur Aufnahmesituation
basiert.

Zentrale Beobachtungen: Mesh A leidet unter der einfarbig grauen Oberfläche, da
wenig Textur zu weniger stabilen Feature-Punkten, häufigeren Lücken und
schlechterer Wasserdichtheit führt. Mesh B profitiert von mehr Fotos und der
strukturierten Oberfläche der Kugelbahn; dafür ist die Szene komplexer und
enthält mehr potenzielle Artefaktquellen. Beide Meshes sind nicht watertight,
was der Normalfall nach Meshroom ist und in CloudCompare behoben wird.
```

---

````{admonition} Übung 3.4 (✩✩✩)
:class: tip
**Parametervariation: Auswirkung von `downscale` auf Mesh-Qualität und Rechenzeit**

In dieser Aufgabe analysieren wir, wie sich der Parameter `downscale` im Knoten
**DepthMap** auf das Rekonstruktionsergebnis auswirkt. Da wir Meshroom hier nicht
direkt ausführen, arbeiten wir mit simulierten Messdaten, die typische Ergebnisse
widerspiegeln.

**Gegebene Messwerte** (basierend auf dem Musterdatensatz, 70 Fotos):

| downscale | Rechenzeit (min) | Vertices | Faces | Mittlere Abweichung (mm) |
| --------- | ---------------- | -------- | ----- | ------------------------ |
| 1         | 240              | 850 000  | 1 680 000 | 0.31 |
| 2         | 58               | 510 000  | 1 020 000 | 0.47 |
| 4         | 14               | 210 000  | 415 000   | 0.89 |
| 8         | 4                | 72 000   | 143 000   | 1.95 |

**Aufgaben:**

1. Visualisieren Sie die Rechenzeit und die mittlere Abweichung als Funktion von
   `downscale` in einem Diagramm (Python oder Tabellenkalkulation) mit zwei Y-Achsen.
2. Berechnen Sie den "Effizienz-Quotienten": `Qualitätsgewinn / Rechenzeitgewinn`
   beim Schritt von `downscale=4` auf `downscale=2` (relativ zu `downscale=1`).
3. Begründen Sie: Welcher `downscale`-Wert wäre für einen ersten Qualitätscheck
   sinnvoll, und welcher für das finale Druckmodell?
````

````{admonition} Lösung
:class: tip
:class: dropdown
``` python
import plotly.graph_objects as go
import numpy as np

downscale     = [1, 2, 4, 8]
rechenzeit    = [240, 58, 14, 4]           # Minuten
abweichung    = [0.31, 0.47, 0.89, 1.95]  # mm

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=downscale, y=rechenzeit,
    name="Rechenzeit (min)",
    mode="lines+markers",
    marker=dict(size=10, color="#005A94"),
    line=dict(color="#005A94")
))

fig.add_trace(go.Scatter(
    x=downscale, y=abweichung,
    name="Mittlere Abweichung (mm)",
    mode="lines+markers",
    marker=dict(size=10, color="#E60000"),
    line=dict(color="#E60000"),
    yaxis="y2"
))

fig.update_layout(
    title="Auswirkung von 'downscale' auf Rechenzeit und Abweichung",
    xaxis=dict(title="downscale-Faktor", tickmode="array", tickvals=downscale),
    yaxis=dict(title="Rechenzeit (min)", color="#005A94"),
    yaxis2=dict(
        title="Mittlere Abweichung (mm)",
        overlaying="y",
        side="right",
        color="#E60000"
    ),
    legend=dict(x=0.5, y=1.1, orientation="h")
)

fig.show()

# Aufgabe 2: Effizienz-Quotient beim Schritt von downscale=4 auf downscale=2
# Qualitätsgewinn = Verbesserung der Abweichung relativ zu downscale=1
qualitaet_referenz = abweichung[0]  # downscale=1
qualitaet_4 = abweichung[2]         # downscale=4
qualitaet_2 = abweichung[1]         # downscale=2

qualitaetsgewinn = (qualitaet_4 - qualitaet_2) / qualitaet_referenz

# Rechenzeitgewinn relativ zum Referenzwert
rechenzeit_referenz = rechenzeit[0]
rechenzeitgewinn = (rechenzeit[2] - rechenzeit[1]) / rechenzeit_referenz

effizienz = qualitaetsgewinn / rechenzeitgewinn

print(f"Qualitätsgewinn (Abweichungsverbesserung):  {qualitaetsgewinn:.3f}")
print(f"Rechenzeitgewinn (relative Einsparung):     {rechenzeitgewinn:.3f}")
print(f"Effizienz-Quotient:                         {effizienz:.2f}")
```

Erwartete Ausgabe (Werte können je nach Berechnung leicht variieren):
Qualitätsgewinn:   (0.89 - 0.47) / 0.31 ≈ 1.355
# Rechenzeitgewinn:  (58 - 14) / 240 ≈ 0.183
# Effizienz-Quotient: ≈ 7.4

# Interpretation:
# Pro Einheit investierter Rechenzeit gewinnen wir beim Schritt von
# downscale=4 auf downscale=2 etwa 7.4-fach mehr Qualität zurück.
# Das ist ein sehr gutes Verhältnis.

# Frage 3: Empfehlung
# Erster Qualitätscheck: downscale=4 (14 Minuten, schnell beurteilbar)
# Finales Druckmodell:   downscale=1 oder downscale=2 (beste Qualität
#   bzw. guter Kompromiss aus Qualität und Wartezeit)
# downscale=8 ist nur für sehr schnelle Vorschauen geeignet;
# die Abweichung von fast 2 mm ist für die Kugelbahn-Simulation zu hoch.
```
````
