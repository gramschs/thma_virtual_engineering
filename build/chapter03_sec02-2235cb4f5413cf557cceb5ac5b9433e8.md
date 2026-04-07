---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Wie interpretiere ich das Meshroom-Ergebnis?

Meshroom hat die Pipeline durchlaufen, und im 3D-Viewer erscheint das erste
Modell der Kugelbahn. Doch was genau bedeuten die grünen und roten
Kamerasymbole? Warum ist die dichte Punktwolke an manchen Stellen auffällig
dünn, und weshalb sieht die Textur stellenweise wie ein unscharfer Fleck aus?
Die Qualitätskriterien aus Abschnitt 3.1 liefern jetzt den Maßstab, um diese
Fragen zu beantworten.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können die dünn besetzte und die dicht besetzte Punktwolke in Meshroom
  qualitativ beurteilen.
* [ ] Sie können anhand der Kamerapositions-Heatmap einschätzen, welche Bereiche
  des Modells gut und welche schlecht rekonstruiert wurden.
* [ ] Sie können erklären, wie Textur auf ein Mesh projiziert wird, und Merkmale
  schlechter Texturierung benennen.
* [ ] Sie können mindestens vier typische Fehlermuster in Meshroom-Ergebnissen
  benennen und deren Ursachen erklären.
```

## Was bedeutet ein erfolgreicher Pipeline-Durchlauf?

Meshroom zeigt uns nach einem erfolgreichen Durchlauf den grünen Haken an allen
Knoten der Pipeline. Das bedeutet: Alle Berechnungsschritte wurden fehlerfrei
abgeschlossen. Doch was bedeuten die Farben in der Punktwolke, warum sind manche
Kamerasymbole grün und andere gelb, und weshalb sieht die Textur auf dem Mesh
stellenweise wie ein unscharfer Fleck aus?

*Ein fehlerfreier Algorithmus-Durchlauf ist nicht dasselbe wie ein gutes Ergebnis.*

Die Qualität des Meshes hängt nicht davon ab, ob Meshroom "durchgelaufen" ist,
sondern davon, wie gut die Eingabefotos die Geometrie des Objekts abgedeckt
haben. In Abschnitt 3.1 haben wir gelernt, welche Qualitätskriterien ein gutes
Mesh auszeichnen. Jetzt lernen wir, wie wir diese Kriterien direkt an der
Meshroom-Ausgabe ablesen können.

## Was verrät die dünn besetzte Punktwolke?

Der erste sichtbare Schritt in der Meshroom-Pipeline ist die **dünn besetzte
Punktwolke** (englisch: "Sparse Point Cloud"). Sie entsteht im Knoten
"FeatureExtraction" und "StructureFromMotion" (SfM) und enthält typischerweise
einige zehntausend Punkte, also deutlich weniger als das spätere dichte Mesh,
aber ausreichend, um die Rekonstruktionsqualität früh zu beurteilen.

Die dünn besetzte Punktwolke zeigt uns zwei Dinge gleichzeitig: die grobe
Geometrie des Objekts und die rekonstruierten Kamerapositionen. Jede Kamera wird
als kleines Pyramidensymbol dargestellt. Die Farbe dieser Symbole ist der erste
wichtige Qualitätsindikator:

* **Grüne Kameras**: Die Kameraposition wurde mit hoher Konfidenz rekonstruiert.
  Das Foto hat viele übereinstimmende Feature-Punkte mit seinen Nachbaraufnahmen
  geliefert.
* **Gelbe Kameras**: Die Rekonstruktion war weniger sicher, meistens wegen zu
  geringer Überlappung oder schlechter Textur in diesem Bereich.
* **Rote oder fehlende Kameras**: Meshroom konnte diese Fotos nicht in die
  Rekonstruktion einbinden. Sie liefern keinen Beitrag zum Mesh.

*Was tun wir, wenn viele Kameras rot sind?*

Rote Kameras weisen fast immer auf einen Fehler beim Fotografieren hin: zu
wenige überlappende Aufnahmen, zu glatte Oberflächen ohne Textur oder starke
Beleuchtungsunterschiede zwischen den Fotos. Die Lösung liegt nicht in Meshroom,
sondern im Aufnahmeschritt, ein wichtiger Grund, warum wir in Kapitel 2 so viel
Sorgfalt auf die Aufnahmestrategie verwendet haben.

Neben den Kamerapositionen zeigt uns die dünn besetzte Punktwolke auch, welche
Bereiche des Objekts überhaupt rekonstruiert werden konnten. Bereiche, in denen
die Punktwolke auffällig leer ist, werden sehr wahrscheinlich auch im finalen
Mesh Lücken aufweisen.

```{admonition} Mini-Übung
:class: tip
Sie öffnen ein Meshroom-Projekt und sehen in der dünn besetzten Punktwolke: Von
80 Fotos wurden 72 als grüne Kameras rekonstruiert. Die restlichen 8 sind rot,
allesamt Aufnahmen der Unterseite der Kugelbahn.

1. Was erwarten Sie für das finale Mesh an der Unterseite des Objekts?
2. Welche Maßnahme hätte das Problem bereits beim Fotografieren verhindern
   können?
```

````{admonition} Lösung
:class: tip
:class: dropdown
1. An der Unterseite der Kugelbahn sind Lücken im Mesh zu erwarten, da Meshroom
   keine Kamerasichten für diesen Bereich rekonstruieren konnte. Ohne Kamerapositions-
   information fehlen dem SfM-Algorithmus die nötigen Tiefeninformationen.

2. Mehr Überlappungsaufnahmen von der Unterseite hätten das Problem verhindert.
   Praktisch: Das Objekt auf einem Drehteller oder einem Stativ positionieren,
   sodass Aufnahmen aus verschiedenen Höhenwinkeln (auch von unten) möglich sind.
````

## Was verrät die dicht besetzte Punktwolke?

Nach dem SfM-Schritt berechnet Meshroom die **dicht besetzte Punktwolke**
(englisch: "Dense Point Cloud") im Knoten "DepthMap" und "Meshing". Sie enthält
oft mehrere Millionen Punkte und liefert die Grundlage für das eigentliche Mesh.

Die dichte Punktwolke beurteilen wir anhand von drei Merkmalen:

1. **Dichte**: Gut beleuchtete und texturreiche Bereiche erzeugen eine dichte
   Punktwolke. Glatte, einfarbige oder reflektierende Oberflächen (bei unserer
   Kugelbahn zum Beispiel glänzende Metallteile) erzeugen kaum Punkte, weil der
   Stereo-Matching-Algorithmus dort keine stabilen Korrespondenzen findet.
2. **Rauschen**: Selbst in gut rekonstruierten Bereichen streuen einzelne Punkte
   leicht um die wahre Oberfläche. Dieses Rauschen ist normal und unvermeidlich.
   Problematisch wird es, wenn ganze Bereiche weit von der tatsächlichen
   Oberfläche abweichen.
3. **Lücken**: Stellen in der dichten Punktwolke ohne Punkte werden im späteren
   Mesh zu Lücken, genau wie wir es in Abschnitt 3.1 besprochen haben.

## Wie entsteht die Textur, und woran erkenne ich eine schlechte Texturierung?

Das finale Mesh ist zunächst farblos: Es kennt nur Geometrie. Im letzten Schritt
der Pipeline projiziert Meshroom die Originalfotos auf die Oberfläche und
erzeugt so eine **Textur**, eine Art fotografisches "Tapetenmuster", das auf das
Mesh geklebt wird.

*Aber wie entscheidet Meshroom, welches Foto für welchen Bereich der Oberfläche
verwendet wird?*

Für jeden Bereich des Meshes wählt Meshroom die Kameraansicht, aus der dieser
Bereich am besten sichtbar war: möglichst frontal, möglichst scharf, möglichst
wenig verdeckt. Anschließend wird der Bildausschnitt auf das Mesh projiziert und
in einer Textur-Datei (einem regulären Bild im `.png`-Format) gespeichert.

Schlechte Texturierung erkennen wir an mehreren Merkmalen:

* **Unscharfe Bereiche**: Meshroom musste auf ein Foto ausweichen, das den
  Bereich nur aus großer Entfernung oder aus einem ungünstigen Winkel zeigte.
* **Farbsprünge (Seams)**: An den Grenzen zwischen zwei Texturkacheln sind
  Helligkeits- oder Farbunterschiede sichtbar, weil zwei Fotos unter
  unterschiedlichen Beleuchtungsbedingungen aufgenommen wurden.
* **Verzerrte Textur**: Wenn das Mesh in diesem Bereich eine schlechte Geometrie
  hat, passt die projizierte Textur nicht zur Form, und das Ergebnis sieht aus
  wie ein krumm aufgeklebtes Etikett.

## Welche Fehlermuster treten typischerweise auf?

Die folgende Tabelle fasst die häufigsten Fehlerbilder zusammen, die wir in
Meshroom-Ergebnissen sehen, und erklärt ihre wahrscheinliche Ursache.

| Fehlermuster | Erscheinungsbild | Wahrscheinliche Ursache |
| ------------ | ---------------- | ----------------------- |
| **Lücken** | Fehlende Flächen, durch die man "hindurchsehen" kann | Zu wenige Fotos aus diesem Winkel; glatte oder verdeckte Oberfläche |
| **Doppelgeometrie** | Zwei sich überlappende Schichten an derselben Stelle | Fehlerhafte Kameraregistrierung; das Objekt wurde während der Aufnahme bewegt |
| **Hintergrundgeometrie** | Flache Fläche unter dem Objekt; Wände, Tisch, Hintergrundobjekte im Mesh | Hintergrund war auf allen Fotos sichtbar und wurde mitrekonstruiert |
| **Schwimmende Artefakte** | Isolierte Dreiecks-Wolken ohne Verbindung zum Objekt | Reflexionen, Glanzlichter oder Bewegungsunschärfe in einzelnen Fotos |
| **Spikes** | Einzelne Vertices, die spitz aus der Oberfläche herausragen | Messrauschen in der Tiefenkarte; häufig an Kanten oder glänzenden Bereichen |
| **Schlechte Textur** | Unschärfe, Farbsprünge, verzerrte Muster auf der Oberfläche | Beleuchtungsunterschiede zwischen Fotos; ungünstige Kamerawinkel |

Diese Fehlermuster werden in den Kapiteln 4 bis 6 systematisch mit CloudCompare
behoben. Dort lernen wir, Hintergrundgeometrie zu entfernen, Lücken zu schließen
und das Mesh zu glätten.

```{admonition} Mini-Übung
:class: tip
Sie öffnen das Meshroom-Ergebnis der Kugelbahn und stellen fest: Die
Führungsschiene sieht auf den ersten Blick gut aus, aber direkt neben ihr
"schwebt" ein dünnes, halbdurchsichtiges Dreiecks-Fragment in der Luft.

1. Um welches Fehlermuster handelt es sich?
2. Was war die wahrscheinliche Ursache?
3. Können Sie dieses Problem durch eine andere Einstellung in Meshroom beheben,
   oder brauchen Sie dafür ein anderes Werkzeug?
```

```{admonition} Lösung
:class: tip
:class: dropdown
1. Es handelt sich um einen schwimmenden Artefakt (Floating Fragment), ein
   isoliertes Dreiecks-Fragment ohne Verbindung zur Hauptgeometrie.

2. Wahrscheinliche Ursache: Die glänzende Oberfläche der Führungsschiene hat
   Reflexionen erzeugt, die Meshroom als eigenständige 3D-Struktur interpretiert
   hat. Alternativ könnte Bewegungsunschärfe in einem Foto zu falschen
   Tiefenwerten geführt haben.

3. In Meshroom selbst lässt sich das Problem kaum beheben, denn der Algorithmus
   hat die verfügbaren Fotos korrekt verarbeitet. Das Fragment muss in
   CloudCompare manuell selektiert und gelöscht werden.
```

## Zusammenfassung und Ausblick

In diesem Abschnitt haben wir gelernt, wie wir die Ausgabe der Meshroom-Pipeline
systematisch interpretieren. Die dünn besetzte Punktwolke zeigt uns, welche
Fotos erfolgreich eingebunden wurden. Die dichte Punktwolke gibt Aufschluss über
Dichte, Rauschen und Lücken. Die Textur verrät, ob die Fotos qualitativ
ausreichend waren. Und eine strukturierte Tabelle typischer Fehlermuster hilft
uns, Probleme schnell zu diagnostizieren.

Im nächsten Abschnitt arbeiten wir praktisch: Wir laden den Musterdatensatz,
passen Parameter an und exportieren das Mesh, damit alle mit demselben,
dokumentierten Ausgangspunkt in die CloudCompare-Phase starten.
