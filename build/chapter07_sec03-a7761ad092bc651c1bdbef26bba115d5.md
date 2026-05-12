---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 7.3 Vom Mesh zum optimierten G-Code: Schritt für Schritt

Wir haben in den Abschnitten 7.1 und 7.2 die Theorie erarbeitet: Was passiert
im FDM-Drucker, welche Parameter bestimmen das Ergebnis, und welche Fehler
entstehen, wenn Parameter falsch gewählt werden? Jetzt wenden wir das Gelernte
auf unser bereinigtes Kugelbahn-Mesh an. Am Ende dieses Abschnitts liegt eine
fertige G-Code-Datei vor, die wir direkt an den Drucker übergeben können.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können ein Mesh in den Slicer laden und grundlegende Mesh-Fehler
  anhand der Slicer-Rückmeldung identifizieren.
* [ ] Sie können das Modell der Kugelbahn im Slicer begründet ausrichten und
  die Konsequenzen der Orientierungswahl für Stützstrukturen und
  Oberflächenqualität erklären.
* [ ] Sie können die fünf Schlüsselparameter aus Abschnitt 7.1 im Slicer
  einstellen und ihre Einstellungen begründen.
* [ ] Sie können die Layer-Vorschau lesen und Risikostellen für Stringing und
  mangelhafte Stützstrukturen gezielt aufspüren.
* [ ] Sie können den G-Code exportieren und die Druckzeit- sowie
  Materialschätzung aus dem Slicer ablesen und bewerten.
```

## Schritt 1: Mesh laden und auf Fehler prüfen

Wir starten den Slicer (PrusaSlicer oder Cura) und importieren unsere bereinigte
`.ply`-Datei aus Abschnitt 4.3 über `File > Import > Import
STL/3MF/STEP/OBJ/AMF/...` beziehungsweise den entsprechenden Menüeintrag. Falls
der Slicer das PLY-Format nicht direkt unterstützt, exportieren wir das Mesh
zuvor in CloudCompare als `.obj` oder `.stl`.

Nach dem Import erscheint das Modell auf der virtuellen Druckplatte. Bevor wir
Parameter einstellen, prüfen wir, ob der Slicer Warnmeldungen anzeigt. Beide
gängigen Slicer melden automatisch, wenn das Mesh Probleme enthält.

**Mesh-Fehler erkennen:**
Häufige Warnungen sind "non-manifold edges" (Kanten, die zu mehr als zwei
Dreiecken gehören) und "holes in mesh" (Lücken in der Oberfläche). Kleine
Lücken entstehen fast immer in Photogrammetrie-Meshes, weil Meshroom nicht
garantiert, dass die rekonstruierte Oberfläche vollständig geschlossen ist. In
Abschnitt 4.3 haben wir das mit dem `trimesh`-Check bereits gesehen.

**Automatische Reparatur:**
Beide Slicer bieten eine automatische Reparaturfunktion an. In PrusaSlicer
erscheint beim Laden eines fehlerhaften Meshes ein Dialog, der die Reparatur
direkt anbietet. In Cura findet sich die Funktion unter `Extensions > Mesh
Tools > Fix Model`. Die Reparatur schließt kleine Lücken, indem fehlende
Dreiecke interpoliert werden. Für unsere Kugelbahn ist das ausreichend, solange
die Lücken klein und auf die Unterseite des Objekts begrenzt sind.

```{admonition} Tipp
:class: note
Falls der Slicer nach der automatischen Reparatur immer noch Fehler meldet,
lohnt es sich, das Mesh erneut in CloudCompare zu öffnen und dort über
`Edit > Mesh > Close Holes` gezielt die verbleibenden Lücken zu schließen.
Diese Funktion füllt Lücken bis zu einer einstellbaren Maximalgröße mit neuen
Dreiecken. Anschließend exportieren und neu importieren.
```

```{figure} pics/chap07_screenshot_prusaslicer01.png
:alt: Slicer-Fenster nach dem Import der Kugelbahn
:align: center

Slicer nach dem Import der Kugelbahn (Quelle: eigene Abbildung; Lizenz [CC BY-SA
4.0](https://creativecommons.org/licenses/by-sa/4.0))
```

## Schritt 2: Druckorientierung wählen

Das Modell liegt nach dem Import vielleicht in der Orientierung auf der
Druckplatte, in der es fotogrammiert wurde: also flach, mit der Unterseite der
Kugelbahn nach unten. Das ist ein Ausgangspunkt, aber nicht zwingend die beste
Druckorientierung.

*Warum ist die Druckorientierung eine der wichtigsten Entscheidungen im
gesamten Workflow?*

Sie bestimmt, an welchen Stellen Stützstrukturen entstehen, wie die
Schichtlinien im Verhältnis zur Führungsrille verlaufen und welche Flächen
mit der Druckplatte in Kontakt kommen und dadurch eine weniger gute
Oberfläche erhalten. Eine falsche Orientierungswahl kann trotz perfekter
Parameterwahl zu einem funktional schlechten Druck führen.

**Überhänge in der Vorschau prüfen:** Beide Slicer können Überhänge
(**Overhang**) farblich markieren, noch bevor wir slicen. In PrusaSlicer
aktivieren wir die Overhang-Darstellung über das Dropdown "View" in der Toolbar.
In Cura kann in der Vorschau ein Farbmodus für Überhänge gewählt werden, der
kritische Bereiche farblich hervorhebt. Rote beziehungsweise orange eingefärbte
Flächen zeigen Bereiche, die mehr als 45 Grad zur Vertikalen überhängen und
Stützstrukturen benötigen.

**Schritt 1 - Standardorientierung beurteilen:**
Wir drehen das Modell von allen Seiten und schätzen ab, wie viele
Stützstrukturen in der aktuellen Lage entstehen würden und ob kritische
Flächen davon betroffen sind.

**Schritt 2 - Alternative Orientierungen testen:**
Wir drehen das Modell um 90 Grad um die Längsachse und prüfen die
Overhang-Anzeige erneut. In vielen Fällen wandern Überhänge an kritischen
Stellen an eine unkritische Außenfläche. Wir wählen die Orientierung, bei der
kritische Stellen wie beispielsweise die Führungsrille am wenigsten
Stützstrukturen benötigen.

**Schritt 3 - Erste Schicht prüfen:**
In der gewählten Endorientierung prüfen wir, welche Fläche auf der Druckplatte
aufliegt. Idealerweise ist das eine möglichst große, ebene Fläche. Eine kleine
Auflagefläche erhöht das Warping-Risiko aus Abschnitt 7.2.

```{admonition} Mini-Übung
:class: tip
Wir drehen die Kugelbahn so, dass ihre Längsachse senkrecht zur Druckplatte
steht, also das Objekt hochkant gedruckt wird.

1. Welcher Vorteil ergibt sich für die Schichtorientierung im Verhältnis zur
   Führungsrille?
2. Welcher neue Nachteil entsteht bei dieser Orientierung?
```

````{admonition} Lösung
:class: tip
:class: dropdown
1. Wenn die Kugelbahn hochkant steht, verlaufen die Schichtlinien senkrecht
   zur Führungsrille. Das bedeutet, dass die Rille aus vielen dünnen
   horizontalen Schichten aufgebaut wird und ihre Querschnittsgeometrie
   schichtweise sehr genau wiedergegeben werden kann. Die Rollbahn der Kugel
   liegt damit auf gut verbundenen Schichtkanten und nicht auf einer
   Überhang-Fläche.

2. Das Objekt hat in hochkanter Lage eine sehr kleine Auflagefläche auf der
   Druckplatte, was das Warping-Risiko erheblich erhöht. Außerdem ist die
   Druckhöhe groß, sodass der Druckkopf weit über das Bett fährt und
   Vibrationen die Maßhaltigkeit der oberen Schichten beeinträchtigen
   können. In den meisten Fällen ist diese Orientierung deshalb keine
   gute Wahl.
````

## Schritt 3: Parameter einstellen

Wir haben die Druckorientierung festgelegt. Jetzt öffnen wir die
Druckeinstellungen des Slicers und setzen die fünf Schlüsselparameter aus
Abschnitt 7.1.

In PrusaSlicer finden sich die Parameter unter dem Reiter "Print Settings".
In Cura sind sie im rechten Panel unter "Print settings" mit aktivierter
"Custom"-Ansicht zugänglich.

**Schichthöhe: 0.15 mm**
Wir suchen den Eintrag "Layer height" beziehungsweise "Schichthöhe" und tragen
0.15 mm ein. Der Slicer aktualisiert daraufhin automatisch die geschätzte
Druckzeit, die wir unten in der Statusleiste ablesen können.

**Fülldichte: 20 %**
Wir setzen "Infill - Fill density" auf 20 Prozent. Als Füllmuster empfehlen sich
"Gyroid" oder "Grid": Beide sind für Prototypen stabil genug. Grid ist einfacher
zu slicen und spart etwas Rechenzeit.

**Drucktemperatur: 205 °C und Bett: 60 °C**
Unter "Filaments" beziehungsweise den Temperatureinstellungen tragen wir 205 °C
für die Nozzle und 60 °C für das Druckbett ein. Diese Werte gelten für PLA; für
andere Materialien passen wir sie entsprechend der Tabelle aus Abschnitt 7.1 an.

**Druckgeschwindigkeit: 45 mm/s**
Wir setzen die allgemeine "Print speed" auf 45 mm/s. Für die erste Schicht
(First layer speed) tragen wir 20 mm/s ein, um die Haftung auf der
Druckplatte zu verbessern.

**Stützstrukturen: aktiviert, nur wo nötig**
Wir aktivieren Supports und wählen "Support on build plate only" (PrusaSlicer)
beziehungsweise "Touching Buildplate" (Cura). Diese Option erzeugt
Stützstrukturen nur für Überhänge, die direkt bis zur Druckplatte reichen, und
reduziert Stützstrukturen im Inneren des Objekts. Wir sollten in der
Layer-Vorschau prüfen, ob trotzdem alle kritischen Überhänge ausreichend
gestützt sind.

## Schritt 4: Layer-Vorschau lesen und Problemstellen erkennen

Mit den eingestellten Parametern klicken wir auf "Slice now" beziehungsweise
"Slice" und warten, bis der Slicer den G-Code berechnet hat. Das dauert bei
unserer Kugelbahn je nach Rechner zwischen wenigen Sekunden und einer Minute.

Danach wechseln wir in die Layer-Vorschau. In PrusaSlicer klicken wir auf
"Preview" in der unteren Toolbar. In Cura erscheint die Vorschau automatisch
nach dem Slicen. Im Vorschaumodus können wir mit einem Schieberegler Schicht
für Schicht durch das gesamte Objekt blättern.

**Stützstrukturen kontrollieren:**
Wir blättern von der untersten Schicht nach oben und achten darauf, wo gelb
oder grau eingefärbte Stützstrukturen erscheinen. Berühren Stützstrukturen die
Unterseite der Führungsrille? Falls ja, prüfen wir, ob eine leichte
Nachkorrektur der Druckorientierung aus Schritt 2 diesen Kontakt vermeiden kann.

**Travel-Moves und Stringing-Risiko einschätzen:**
In PrusaSlicer lassen sich Travel-Moves als gestrichelte Linien anzeigen
(Farbmodus "Travel"). Lange Travel-Moves über die Führungsrille sind die
häufigste Ursache für Stringing. Wenn wir solche Bahnen sehen, überprüfen wir,
ob der Filamentrückzug (retraction) aktiv ist.

*Wie viele Travel-Moves über den Spalt der Führungsrille sind noch
akzeptabel?*

Das lässt sich nicht pauschal sagen. Als Faustregel gilt: Ein einzelner
kurzer Travel-Move (unter 5 mm) mit aktivem Filmentrückzug erzeugt selten
sichtbares Stringing. Mehrere lange Travel-Moves (über 15 mm) ohne Filamentrückzug
sind ein deutliches Warnsignal. In diesem Fall prüfen wir, ob eine andere
Slicing-Reihenfolge oder eine veränderte Seam-Position das Problem löst.

**Erste und letzte Schicht prüfen:**
Wir scrollen zur ersten Schicht und prüfen, ob die Auflagefläche gleichmäßig
und vollständig gedruckt wird. Dann springen wir zur letzten Schicht und
kontrollieren, ob die obere Deckfläche geschlossen und ohne Lücken dargestellt
ist.

```{admonition} Mini-Übung
:class: tip
Die Layer-Vorschau zeigt in Schicht 47 einen Travel-Move von 22 mm Länge
direkt über die Führungsrille. Die Einstellung des Filamentrückzugs ist auf 0.8 mm
gesetzt.

1. Warum ist dieser Travel-Move ein Stringing-Risiko, obwohl der Filamentrückzug
   aktiviert ist?
2. Nennen Sie zwei Maßnahmen im Slicer, die das Risiko ohne Neuausrichtung
   des Modells reduzieren.
```

````{admonition} Lösung
:class: tip
:class: dropdown
1. Ein Filamentrückzug von 0.8 mm ist für direkt angetriebene Extruder (Direct
   Drive) geeignet, für Bowden-Extruder jedoch meist zu kurz. Bei einem
   22 mm langen Travel-Move bleibt außerdem mehr Zeit für den Druckabfall
   in der Nozzle auszugleichen, was bei zu niedrigen Filamentrückzugslänge zu
   einem Materialaustritt führt. Zudem ist 205 °C für PLA am oberen
   Temperaturbereich: Das Material ist flüssig genug, um bei langen Moves
   trotz Filamentrückzug auszutreten.

2. Erstens: Filamentrückzugslänge auf 1.5 bis 2.0 mm erhöhen (bei Bowden-Extruder
   auf 4 bis 6 mm). Zweitens: Drucktemperatur um 5 bis 8 °C senken, damit
   das Material beim Travel-Move weniger fließfähig ist. Optional lässt sich
   auch "Avoid crossing perimeters" (PrusaSlicer) beziehungsweise "Combing"
   (Cura) aktivieren: Diese Funktion leitet Travel-Moves soweit möglich durch
   das Innere des Objekts und vermeidet damit Travel-Moves über offene
   Bereiche.
````

## Schritt 5: G-Code exportieren und Druckzeit ablesen

Die Layer-Vorschau sieht gut aus. Wir exportieren den G-Code über `File >
Export > Export G-code` beziehungsweise den "Save to disk"-Button in Cura. Als
Dateinamen wählen wir etwas Beschreibendes mit den wichtigsten Parametern,
zum Beispiel `kugelbahn_lh015_if20_205C.gcode`. Das erleichtert später die
Zuordnung, wenn mehrere G-Code-Dateien vorliegen.

**Druckzeit und Materialverbrauch ablesen:**
Vor dem Export zeigt der Slicer eine Schätzung der Druckzeit und des
Filamentverbrauchs. Diese Werte lesen wir ab und notieren sie. Typische Werte
für unsere Kugelbahn mit den gewählten Parametern:

| Kennwert | Typischer Wert | Bedeutung |
| -------- | -------------- | --------- |
| Druckzeit | 3 bis 5 Stunden | Abhängig von Modellgröße und Parametern |
| Filamentlänge | 8 bis 15 m | Abhängig von Fülldichte und Wandstärke |
| Filamentgewicht | 25 bis 45 g | Bei PLA: 1 g ≈ ca. 33 cm Filament |

**Kurzer Blick in den G-Code:**
Wir öffnen die exportierte `.gcode`-Datei in einem Texteditor. Die ersten
Zeilen enthalten Kommentare des Slicers mit den verwendeten Parametern:

```code
; generated by PrusaSlicer 2.8
; layer_height = 0.15
; infill_density = 20%
; nozzle_temperature = 205
```

Danach folgen die Initialisierungsbefehle (Aufheizen, Homing, Purge-Linie)
und schließlich die eigentlichen Druckbefehle. Das Format brauchen wir nicht
im Detail zu verstehen: Es reicht zu wissen, dass jede Zeile, die mit `G1`
beginnt, eine Bewegung der Nozzle beschreibt, und dass `;` Kommentarzeilen
einleitet, die der Drucker ignoriert.

```{admonition} Tipp
:class: note
Manche Drucker unterstützen nur G-Code-Dateien, die von einem bestimmten
Slicer-Profil erzeugt wurden. Falls der Drucker die Datei ablehnt oder
das Druckobjekt stark versetzt auf der Platte erscheint, lohnt sich ein
Blick in den Header des G-Code: Die erste `G28`-Zeile führt den Homing-
Vorgang durch. Fehlt sie, fährt der Druckkopf ohne definierte Ausgangsposition
los, was zu Fehldrucken und in seltenen Fällen zu Kollisionen führen kann.
```

Abschließend nehmen wir den exportierten G-Code anhand der folgenden
Checkliste ab:

```{admonition} Checkliste: G-Code vor dem Druck
:class: note
* **Mesh erfolgreich importiert und repariert:** Keine verbleibenden
  Fehler-Warnmeldungen im Slicer.
* **Druckorientierung gewählt:** Führungsrille möglichst frei von
  Stützstrukturen, ausreichend große Auflagefläche auf der Druckplatte.
* **Fünf Schlüsselparameter gesetzt:** Schichthöhe 0.15 mm, Fülldichte 20 %,
  Nozzle-Temperatur 205 °C, Druckgeschwindigkeit 45 mm/s, Supports aktiviert.
* **Layer-Vorschau geprüft:** Keine langen Travel-Moves ohne Filamentrückzug über
  die Führungsrille; Stützstrukturen an unkritischen Stellen.
* **Druckzeit und Materialverbrauch notiert.**
* **G-Code mit beschreibendem Dateinamen exportiert.**
```

```{dropdown} Video "PrusaSlicer für Anfänger" von Rico Quin
<iframe width="995" height="560" src="https://www.youtube.com/embed/5H2-DXWQe3s"
title="PrusaSlicer für Anfänger: Dein Leitfaden zum ersten 3D-Druck - Ein Grundlagentutorial
| Deutsch" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media;
gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin"
allowfullscreen></iframe>
```

> Playlist [Prusa Slicer Tutorials DE von JanTec](https://www.youtube.com/playlist?list=PLTER67VfmYO6I6BGR4JRaHOcPXCe0s7-Y)

## Zusammenfassung und Ausblick

In diesem Abschnitt haben wir die vollständige Slicer-Pipeline durchlaufen.
Wir haben das bereinigte Mesh importiert und automatisch repariert, die
Druckorientierung anhand der Overhang-Anzeige begründet gewählt, die fünf
Schlüsselparameter aus Abschnitt 7.1 konkret eingestellt und die Layer-Vorschau
genutzt, um Stringing-Risiken und problematische Stützstrukturen zu erkennen.
Am Ende steht ein G-Code mit bekannter Druckzeit und dokumentierten Parametern.

Im nächsten Abschnitt warten die Übungen zu Kapitel 7: Dort werden wir
Parameter systematisch variieren, die Auswirkungen auf Layer-Vorschau und
Druckzeit quantitativ erfassen und für eine veränderte Objektgeometrie eine
eigene begründete Parameterwahl entwickeln.
