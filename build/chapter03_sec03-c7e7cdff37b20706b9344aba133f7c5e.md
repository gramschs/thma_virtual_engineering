---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Meshroom: Pipeline steuern und Ergebnis exportieren

Die Meshroom-Pipeline lässt sich weit mehr steuern als mit einem einzigen Klick
auf "Start". An jedem Knoten können wir Parameter anpassen und einzelne
Berechnungsschritte gezielt wiederholen, ohne stundenlange Neuberechnungen in
Kauf zu nehmen. Wir laden außerdem gemeinsam den Musterdatensatz der Kugelbahn
und bereiten das Mesh für die Übergabe an CloudCompare vor. Die
Qualitätskriterien und Fehlermuster aus den vorigen Abschnitten sind dabei unser
Maßstab.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können relevante Parameter einzelner Knoten in der Meshroom-Pipeline benennen und deren Wirkung erläutern.
* [ ] Sie können einzelne Knoten der Pipeline gezielt neu starten, ohne die gesamte Berechnung zu wiederholen.
* [ ] Sie können den Musterdatensatz laden und das enthaltene Meshroom-Projekt korrekt öffnen.
* [ ] Sie können ein Mesh als `.obj` und als `.ply` exportieren und die Ordnerstruktur des Meshroom-Cache verstehen.
* [ ] Sie können anhand einer Qualitätscheckliste entscheiden, ob ein Mesh bereit für die Übergabe an CloudCompare ist.
```

## Mehr als nur "Play" drücken

Bisher haben wir Meshroom als Black Box behandelt: Fotos rein, Mesh raus. Doch
Meshroom bietet uns an jedem Knoten der Pipeline die Möglichkeit, Parameter
anzupassen, einzelne Schritte neu zu starten und das Ergebnis gezielt zu
verbessern, ohne die gesamte, mehrstündige Berechnung von vorn beginnen zu
müssen.

*Wann lohnt es sich, in die Parameter einzugreifen, und wann verschwendet man
damit nur Zeit?*

In diesem Abschnitt lernen wir, die Pipeline wie ein Werkzeug zu bedienen, nicht
nur wie einen Knopf. Wir schauen uns die Parameter an, die den größten Einfluss
auf Qualität und Rechenzeit haben, und üben dann gemeinsam am Musterdatensatz
der Kugelbahn. In den vorangegangenen Abschnitten haben wir gelernt, was ein
gutes Mesh ausmacht und wie wir Fehlermuster erkennen. Jetzt wenden wir dieses
Wissen konkret an.

## Welche Knoten-Parameter lohnt es sich zu kennen?

Die Meshroom-Pipeline besteht aus über einem Dutzend Knoten. Die meisten Standardwerte sind für typische Aufnahmen gut gewählt. Drei Knotenbereiche sind jedoch besonders relevant, wenn wir die Qualität des Ergebnisses gezielt steuern wollen.

### DepthMapFilter und Meshing: Wie dicht soll das Mesh sein?

Der Knoten **Meshing** bestimmt, wie fein das finale Dreiecksnetz aufgelöst wird. Der wichtigste Parameter lautet `maxInputPoints`: Er legt die maximale Anzahl an Punkten aus der dichten Punktwolke fest, die für das Meshing verwendet werden.

| Parameter | Standardwert | Niedrigerer Wert | Höherer Wert |
| --------- | ------------ | ---------------- | ------------ |
| `maxInputPoints` | 50 000 000 | Schneller, gröberes Mesh | Langsamer, feineres Mesh |
| `maxPoints` | 5 000 000 | Weniger Dreiecke | Mehr Dreiecke |

Für unsere Kugelbahn empfehlen wir für einen ersten Testdurchlauf reduzierte Werte (zum Beispiel `maxInputPoints = 10 000 000`), um schnell ein beurteilbares Ergebnis zu erhalten. Für das finale Mesh, das in den 3D-Druck gehen soll, erhöhen wir die Werte wieder.

### Texturing: Wie hoch soll die Texturauflösung sein?

Der Knoten **Texturing** erzeugt die Bilddateien, die als Textur auf das Mesh projiziert werden. Der Parameter `textureSide` legt die Seitenlänge dieser Texturbilder in Pixeln fest.

- `textureSide = 4096`: Standardauflösung, guter Kompromiss aus Qualität und Dateigröße.
- `textureSide = 8192`: Höhere Detailauflösung, deutlich größere Ausgabedatei.
- `textureSide = 2048`: Für schnelle Vorschauen ausreichend.

Für die Weiterverarbeitung in CloudCompare ist die Texturauflösung weniger kritisch, da wir dort hauptsächlich mit der Geometrie arbeiten. Für die abschließende Dokumentation und den Präsenztag lohnt sich jedoch die höhere Auflösung.

### DepthMap: Qualität vs. Rechenzeit

Der Knoten **DepthMap** ist rechnerisch der aufwendigste Schritt. Über den Parameter `downscale` können wir die Eingabebilder vor der Tiefenkarten-Berechnung verkleinern:

- `downscale = 1`: Volle Auflösung, maximale Qualität, sehr lange Rechenzeit.
- `downscale = 2`: Halbierte Auflösung, deutlich schneller, für die meisten Objekte ausreichend.
- `downscale = 4`: Für schnelle Testläufe, spürbar gröberes Ergebnis.

````{admonition} Mini-Übung
:class: tip
Sie starten einen Meshroom-Durchlauf mit dem Musterdatensatz auf einem Laptop ohne dedizierte GPU. Die Berechnung würde bei Standardparametern ca. 4 Stunden dauern.

Welche drei Parameter würden Sie anpassen, um die Rechenzeit auf unter eine Stunde zu reduzieren, und welche Qualitätseinbußen nehmen Sie dabei in Kauf?
````

````{admonition} Lösung
:class: tip
:class: dropdown
Sinnvolle Anpassungen für schnelle Testläufe:

1. DepthMap → `downscale = 4` (statt 1): Gröbere Tiefenkarten, weniger feine Details in der Punktwolke.
2. Meshing → `maxInputPoints = 5 000 000` (statt 50 000 000): Gröberes Mesh, feine Strukturen können verloren gehen.
3. Texturing → `textureSide = 2048` (statt 4096): Niedrigere Texturauflösung, Detailverlust in der Oberflächenfarbe.

Diese Einstellungen reichen für eine erste Beurteilung der Mesh-Qualität aus. Für das finale Modell sollten die Standardwerte (oder höher) verwendet werden.
````

## Wie starte ich einzelne Knoten neu?

Ein großer Vorteil von Meshroom ist das **inkrementelle Berechnen**: Wenn wir nur den Parameter `textureSide` ändern, müssen wir nicht die gesamte Pipeline von vorn starten, nur der Texturing-Knoten muss neu berechnet werden. Meshroom erkennt automatisch, welche Zwischenergebnisse noch gültig sind.

**Schritt für Schritt: Einzelnen Knoten neu starten**:

1. Rechtsklick auf den gewünschten Knoten im Pipeline-Editor.
2. Im Kontextmenü: **"Submit"** (neu berechnen) oder **"Force Recompute"** (auch
   wenn das Ergebnis scheinbar aktuell ist).
3. Den grünen "Start"-Button oben links drücken, um die Pipeline fortzusetzen.

**Wichtig:** Wenn wir einen frühen Knoten ändern (zum Beispiel DepthMap), werden automatisch alle nachgelagerten Knoten als "veraltet" markiert und müssen neu berechnet werden. Meshroom zeigt das durch ein orangefarbenes Warnsymbol an den betroffenen Knoten.

```{dropdown} Video "Meshroom: Recompute a single node" (englisch)
<iframe width="560" height="315" src="https://www.youtube.com/embed/v_O6tYKQEBA"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen></iframe>
```

## Den Musterdatensatz laden: Schritt für Schritt

Ab hier arbeiten alle Studierenden mit demselben vorgefertigten Datensatz. Das Meshroom-Projekt der Kugelbahn liegt als `.mg`-Projektdatei vor und enthält bereits alle Fotos sowie ein fertig berechnetes Mesh. Wir müssen also nicht neu berechnen, aber wir verstehen durch die vorherigen Abschnitte, wie das Ergebnis zustande kam.

**Voraussetzung:** Meshroom ist installiert (Windows oder Linux). macOS-Nutzer verwenden ausschließlich den Musterdatensatz, da Meshroom unter macOS nicht nativ unterstützt wird.

**Schritt 1: Musterdatensatz herunterladen**

Den Datensatz finden Sie im Kurs-Repository unter `datasets/kugelbahn_meshroom/`. Laden Sie den gesamten Ordner herunter und entpacken Sie ihn an einen Ort Ihrer Wahl (kein Leerzeichen im Pfad).

**Schritt 2: Meshroom starten und Projekt öffnen**

1. Meshroom starten (Doppelklick auf `Meshroom.exe` unter Windows).
2. Menü **File → Open Project** (Shortcut: `Ctrl + O`).
3. Die Datei `kugelbahn.mg` im entpackten Ordner auswählen und öffnen.
4. Meshroom lädt die Pipeline und alle bereits berechneten Zwischenergebnisse aus dem `MeshroomCache`-Unterordner.

**Schritt 3: Ergebnis im 3D-Viewer prüfen**

1. Im Pipeline-Editor den Knoten **Texturing** anklicken.
2. Im unteren Bereich erscheint das Ausgabeverzeichnis. Klicken Sie auf das Ordnersymbol, um den Cache-Pfad zu sehen.
3. Im 3D-Viewer (rechte Seite) sollte das texturierte Mesh der Kugelbahn sichtbar sein. Falls nicht: Doppelklick auf den Texturing-Knoten, um das Ergebnis zu laden.

**Schritt 4: Qualitätskontrolle durchführen**

Bevor wir exportieren, prüfen wir das Mesh anhand der Qualitätskriterien aus Abschnitt 3.1 und der Fehlermuster aus Abschnitt 3.2. Die vollständige Checkliste folgt am Ende dieses Abschnitts.

## Exportieren: Mesh als `.obj` und `.ply` sichern

Meshroom speichert das finale Mesh automatisch im `MeshroomCache`-Ordner. Dieser Pfad ist jedoch lang, kryptisch (er enthält Hashwerte) und nicht für die Weitergabe gedacht. Wir exportieren das Mesh deshalb in einen übersichtlichen Ausgabeordner.

**Ordnerstruktur des MeshroomCache verstehen**

```
MeshroomCache/
├── FeatureExtraction/
│   └── <hash>/                    ← Berechnete Feature-Punkte pro Foto
├── StructureFromMotion/
│   └── <hash>/                    ← Sparse Point Cloud + Kamerapositionen
├── DepthMap/
│   └── <hash>/                    ← Tiefenkarten pro Kamera
├── Meshing/
│   └── <hash>/
│       └── mesh.obj               ← Rohes Mesh (ohne Textur)
└── Texturing/
    └── <hash>/
        ├── texturedMesh.obj       ← Texturiertes Mesh (Hauptergebnis)
        ├── texturedMesh.mtl       ← Materialbeschreibung
        └── texture_*.png          ← Texturbilder
```

Der `<hash>`-Ordner enthält eine eindeutige Kennung des Berechnungszustands. Wenn wir Parameter ändern und neu berechnen, entsteht ein neuer Hash-Ordner, das alte Ergebnis bleibt erhalten.

**Mesh als `.obj` exportieren**

Die einfachste Methode: Den Ausgabeordner des Texturing-Knotens direkt kopieren.

1. Rechtsklick auf den Knoten **Texturing** → **"Open in File Explorer"**.
2. Den Inhalt des `<hash>`-Ordners (`.obj`, `.mtl`, alle `.png`-Dateien) in einen neuen Ordner `export/kugelbahn_mesh/` kopieren.
3. Sicherstellen, dass alle Dateien kopiert wurden: Ohne die `.png`-Texturdateien erscheint das Mesh in CloudCompare farblos.

**Mesh als `.ply` exportieren**

Meshroom erzeugt `.ply` nicht direkt als Texturing-Ausgabe. Wir konvertieren deshalb in Python:

```{code-cell} python
# Konvertierung von .obj nach .ply mit dem Paket trimesh
# Voraussetzung: pip install trimesh
import trimesh

OBJ_PATH = "export/kugelbahn_mesh/texturedMesh.obj"
PLY_PATH = "export/kugelbahn_mesh/kugelbahn.ply"

mesh = trimesh.load(OBJ_PATH)
mesh.export(PLY_PATH)

print(f"Mesh exportiert: {PLY_PATH}")
print(f"Vertices: {len(mesh.vertices)}")
print(f"Faces:    {len(mesh.faces)}")
print(f"Watertight: {mesh.is_watertight}")
```

Die `.ply`-Datei können wir anschließend direkt in CloudCompare öffnen. In Kapitel 4 werden wir damit arbeiten, um das Mesh zu bereinigen und mit einem Referenzmodell zu vergleichen.

````{admonition} Mini-Übung
:class: tip
Nach dem Export führen Sie das obige Python-Skript aus und erhalten folgende Ausgabe:

```
Vertices: 284 532
Faces:    569 041
Watertight: False
```

1. Was sagt uns `Watertight: False`?
2. Ist das ein Problem für die nächsten Schritte in CloudCompare?
3. Für welchen späteren Schritt wird `Watertight: True` zwingend benötigt?
````

````{admonition} Lösung
:class: tip
:class: dropdown
1. `Watertight: False` bedeutet, dass das Mesh nicht vollständig geschlossen ist: Es hat Lücken oder Non-Manifold Kanten und beschreibt kein eindeutiges Volumen.

2. Für die Arbeit in CloudCompare ist das kein unmittelbares Problem: Wir können das Mesh analysieren, bereinigen und glätten, auch wenn es noch nicht wasserdicht ist. CloudCompare arbeitet direkt mit der Geometrie, ohne ein geschlossenes Volumen vorauszusetzen.

3. `Watertight: True` wird für den 3D-Druck in PrusaSlicer benötigt. Der Slicer muss Innen und Außen eindeutig unterscheiden können. Deshalb reparieren wir das Mesh in CloudCompare (Kapitel 4 bis 6), bevor wir es an PrusaSlicer übergeben.
````

## Was überprüfen wir vor dem Export?

Bevor wir das Mesh an CloudCompare übergeben, prüfen wir folgende Punkte:

```{admonition} Checkliste: Mesh-Qualität vor dem Export
:class: attention
* [ ] **Kameraabdeckung**: Mindestens 90 % der Kameras wurden als grün (hohe Konfidenz) rekonstruiert.
* [ ] **Sparse Point Cloud**: Die Kugelbahn ist vollständig und ohne große Lücken in der dünn besetzten Punktwolke erkennbar.
* [ ] **Dense Point Cloud**: Keine auffälligen Bereiche mit extremem Rauschen oder fehlenden Punkten an funktionskritischen Stellen (Führungsrille).
* [ ] **Mesh-Vollständigkeit**: Keine sichtbaren Lücken an der Führungsschiene oder an anderen funktionalen Bereichen im 3D-Viewer.
* [ ] **Artefakte identifiziert**: Schwimmende Fragmente und Hintergrundgeometrie sind sichtbar und werden in CloudCompare entfernt.
* [ ] **Export vollständig**: `.obj`-Datei zusammen mit `.mtl` und allen `.png`-Texturdateien kopiert.
* [ ] **Python-Check durchgeführt**: Vertices- und Faces-Zahl plausibel (deutlich über 10 000); Watertight-Status dokumentiert.
```

## Zusammenfassung und Ausblick

In diesem Abschnitt haben wir gelernt, die Meshroom-Pipeline aktiv zu steuern: Wir kennen die wichtigsten Parameter in den Knoten DepthMap, Meshing und Texturing, wir können einzelne Knoten gezielt neu starten, und wir haben den Musterdatensatz der Kugelbahn geladen und exportiert.

Alle Studierenden arbeiten jetzt mit demselben Ausgangsmesh. In den Kapiteln 4 bis 6 beginnen wir mit CloudCompare: Wir entfernen Hintergrundgeometrie, bereinigen Artefakte und führen eine quantitative Abweichungsanalyse zwischen dem rekonstruierten Mesh und einem CAD-Referenzmodell durch.
