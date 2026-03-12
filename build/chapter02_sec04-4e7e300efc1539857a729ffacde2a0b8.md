---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Übungen

````{admonition} Übung 2.1 (✩)
:class: tip
Ordnen Sie die folgenden Schritte der Meshroom-Pipeline in die richtige
Reihenfolge und beschreiben Sie das Ergebnis jedes Schritts in einem Satz.

**Schritte (in falscher Reihenfolge):**
- Meshing
- FeatureExtraction
- StructureFromMotion
- Texturing
- FeatureMatching
- DepthMap
````

````{admonition} Lösung
:class: tip
:class: dropdown
Richtige Reihenfolge:

1. **FeatureExtraction:** Aus jedem Foto werden markante Merkmalspunkte
   extrahiert.
2. **FeatureMatching:** Dieselben Merkmalspunkte werden in verschiedenen Fotos
   einander zugeordnet.
3. **StructureFromMotion:** Aus den zugeordneten Merkmalspunkten werden die
   Kamerapositionen und eine dünn besetzte Punktwolke berechnet.
4. **DepthMap:** Für jedes Foto wird eine Tiefenkarte berechnet, die die
   Entfernung jedes Bildpunkts zur Kamera beschreibt.
5. **Meshing:** Aus den Tiefenkarten wird eine dicht besetzte Punktwolke
   erzeugt und zu einem Dreiecksnetz (Mesh) verbunden.
6. **Texturing:** Die Originalfotos werden auf das Mesh projiziert, um eine
   farbige Textur zu erzeugen.
````

````{admonition} Übung 2.2 (✩)
:class: tip
Gegeben sind folgende Beschreibungen von Aufnahmesituationen. Entscheiden Sie
für jede, ob sie für die Photogrammetrie **geeignet**, **bedingt geeignet**
oder **nicht geeignet** ist, und begründen Sie Ihre Entscheidung in einem Satz.

1. Ein Zahnrad aus Grauguss, fotografiert bei gleichmäßiger Raumbeleuchtung
   auf einem grauen Tuch.
2. Eine polierte Edelstahlwelle, fotografiert im direkten Sonnenlicht.
3. Ein Kunststoff-Gehäuse mit aufgedrucktem Schriftzug, fotografiert bei
   bewölktem Tageslicht.
4. Ein Glaskolben aus dem Chemielabor, fotografiert auf weißem Papier.
5. Ein alter Ziegelstein, fotografiert mit konstantem ISO-Wert bei
   Neonbeleuchtung.
````

````{admonition} Lösung
:class: tip
:class: dropdown
1. **Geeignet:** Grauguss ist matt und texturiert, gleichmäßige Beleuchtung
   und neutraler Hintergrund sind ideal.
2. **Nicht geeignet:** Polierter Edelstahl ist stark reflektierend, direkte
   Sonne erzeugt harte Schatten und wandernde Reflexionen.
3. **Bedingt geeignet:** Der Schriftzug liefert gute Merkmalspunkte, aber
   glatte Kunststoffflächen ohne Aufdruck können problematisch sein.
   Mattierungsspray kann helfen.
4. **Nicht geeignet:** Glas ist transparent und reflektierend, der Algorithmus
   findet keine stabilen Merkmalspunkte.
5. **Geeignet:** Ziegelstein hat eine ausgeprägte, matte Textur; konstanter
   ISO-Wert und gleichmäßige Neonbeleuchtung sind gut geeignet.
````

````{admonition} Übung 2.3 (✩✩)
:class: tip
Sie haben 45 Fotos eines Maschinenbauteils aufgenommen und in Meshroom
geladen. Die Pipeline läuft durch, aber das resultierende Mesh hat folgende
Probleme:

- Die Unterseite des Bauteils fehlt vollständig.
- An zwei Seiten gibt es große Lücken.
- Im Hintergrund ist eine flächige Geometrie zu sehen.
- Eine glänzende Fläche ist unregelmäßig und mit Artefakten übersät.

Benennen Sie für jedes der vier Probleme die wahrscheinlichste Ursache und
eine konkrete Maßnahme, mit der Sie das Problem bei einer neuen Aufnahme
beheben würden.
````

````{admonition} Lösung
:class: tip
:class: dropdown
**Unterseite fehlt vollständig:**
Ursache: Die Unterseite wurde nicht fotografiert, weil das Bauteil auf einer
Unterlage lag. Maßnahme: Das Bauteil auf einem dünnen Stab oder einem
Klebestreifen erhöhen und auch von unten fotografieren, oder das Bauteil
einmal umdrehen und eine zweite Aufnahmesession durchführen.

**Lücken an zwei Seiten:**
Ursache: Zu wenige Fotos aus diesen Richtungen oder zu wenig Überlappung.
Maßnahme: Die Aufnahmestrategie anpassen und in den betroffenen Bereichen mehr
Fotos mit kleinerem Winkelabstand aufnehmen.

**Flächige Geometrie im Hintergrund:**
Ursache: Der Hintergrund war zu strukturreich (z. B. Tisch mit Holzmaserung)
und wurde vom Algorithmus mitrekonstruiert. Maßnahme: Das Bauteil auf einen
einfarbigen, strukturlosen Untergrund stellen, z. B. auf ein einfarbiges
Tuch oder Papier.

**Artefakte auf der glänzenden Fläche:**
Ursache: Die glänzende Oberfläche erzeugt wandernde Reflexionen, die der
Algorithmus nicht stabil zuordnen kann. Maßnahme: Die glänzende Fläche vor
der Aufnahme mit Mattierungsspray behandeln.
````

````{admonition} Übung 2.4 (✩✩✩)
:class: tip
Vergleichen Sie die Photogrammetrie mit dem Verfahren der
**Structured-Light-Projektion** (strukturiertes Licht), das in industriellen
Messgeräten wie dem GOM ATOS eingesetzt wird, anhand der folgenden Kriterien:

- Messprinzip (wie wird die 3D-Information gewonnen?)
- Anforderungen an die Oberfläche
- Typische Messunsicherheit
- Kosten der Ausrüstung
- Portabilität

Formulieren Sie abschließend eine Empfehlung: In welchen Situationen würden
Sie als Ingenieurin oder Ingenieur welches Verfahren einsetzen? Begründen Sie
Ihre Antwort mit mindestens drei Kriterien.
````

````{admonition} Lösung
:class: tip
:class: dropdown
| Kriterium | Photogrammetrie | Structured-Light |
|-----------|----------------|-----------------|
| Messprinzip | Triangulation aus Merkmalspunkten in überlappenden Fotos | Projektion bekannter Lichtmuster; Auswertung der Verzerrung durch Kamera |
| Oberflächenanforderung | Matt, texturiert; glänzende Flächen problematisch | Gut geeignet für glänzende Flächen; spezielle Modi verfügbar |
| Messunsicherheit | 0,5 bis 5 mm (stark abhängig von Aufnahme) | 0,01 bis 0,1 mm (Präzisionsniveau) |
| Kosten | Gering (Smartphone + kostenlose Software) | Hoch (ab ca. 20.000 bis 200.000 Euro) |
| Portabilität | Hoch (Smartphone ist immer dabei) | Mittel bis gering (schweres Gerät, oft stationär) |

**Empfehlung:**
Photogrammetrie empfiehlt sich, wenn ein schnelles, kostengünstiges Ergebnis
benötigt wird, keine Präzisionsmessung erforderlich ist und keine
kostenintensive Ausrüstung zur Verfügung steht, z. B. bei der Dokumentation
von Bestandsobjekten, bei einfachem Reverse Engineering oder in der Lehre.

Structured-Light ist die richtige Wahl in der industriellen Qualitätssicherung,
wenn Toleranzen im Zehntel-Millimeter-Bereich eingehalten werden müssen, z. B.
beim Abgleich gefertigter Bauteile mit CAD-Solldaten oder in der Automotive-
und Luft- und Raumfahrtindustrie.
````

````{admonition} Übung 2.5 (Mini-Projekt)
:class: tip
Führen Sie eine vollständige Photogrammetrie-Aufnahme Ihres eigenen Objekts
durch und verarbeiten Sie die Fotos in Meshroom zu einem Mesh.

**Teilaufgaben:**

1. **Vorbereitung:** Bereiten Sie das Objekt vor (ggf. mattieren), wählen Sie
   einen geeigneten Aufnahmeort und prüfen Sie Ihre Kameraeinstellungen.

2. **Aufnahme:** Fotografieren Sie das Objekt nach der Strategie aus Kapitel
   2.2 mit mindestens 60 Fotos in mindestens zwei Ebenen.

3. **Rekonstruktion:** Importieren Sie die Fotos in Meshroom und führen Sie die
   vollständige Pipeline aus.

4. **Dokumentation:** Erstellen Sie eine kurze Dokumentation (ca. 300 bis 400
   Wörter) mit folgenden Inhalten:
   - Aufnahmebedingungen (Beleuchtung, Hintergrund, Kameraeinstellungen)
   - Anzahl aufgenommener Fotos und Anzahl erfolgreich eingebundener Fotos
   - Screenshot des Meshroom-Ergebnisses im 3D Viewer
   - Qualitätsbewertung: Was ist gut gelungen, was nicht?
   - Mindestens zwei konkrete Verbesserungsmaßnahmen für eine zweite Aufnahme

*Optionale Erweiterung:* Führen Sie eine zweite Aufnahmesession mit
verbesserten Einstellungen durch und vergleichen Sie die beiden Ergebnisse.
Welche Maßnahme hat die größte Verbesserung gebracht?
````
