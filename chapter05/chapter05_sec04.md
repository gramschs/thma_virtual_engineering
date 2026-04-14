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
TODO
````

---

````{admonition} Übung 5.2 (✩✩)
:class: tip
**Konvergenzverlauf interpretieren**

Ein ICP-Lauf auf zwei Scans desselben Maschinenbauteils liefert folgende
Protokollzeilen:

| Iteration | RMS-Fehler (mm) | Δ RMS (mm) |
| --------- | --------------- | ---------- |
| 1         | 4.832           | –          |
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
TODO
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
   nebeneinander (Plotly), farblich unterschieden nach "Globales Minimum
   erreicht".
2. Bestimmen Sie den kritischen Schwellenwert des initialen RMS-Fehlers,
   oberhalb dessen ICP in einem lokalen Minimum stecken bleibt.
3. Leiten Sie eine praktische Empfehlung ab: Wie gut muss eine manuelle
   Vorausrichtung mindestens sein, bevor man ICP startet?
````

````{admonition} Lösung
:class: tip
:class: dropdown
TODO
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
