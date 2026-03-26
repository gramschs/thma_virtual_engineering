---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 1.2 Das Leitprojekt: Kugelbahn

In dieser Vorlesung arbeiten wir durchgängig an einem konkreten Leitprojekt:
der Digitalisierung, dem 3D-Druck und der Simulation einer Kugelbahn. Dieses
Kapitel stellt das Projekt vor, erklärt den Gesamtworkflow und zeigt, welche
Werkzeuge dabei zum Einsatz kommen. Außerdem erfahren wir, welche Kriterien ein
Objekt erfüllen muss, das wir zusätzlich selbst fotografieren und digitalisieren.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie kennen den Gesamtworkflow des Leitprojekts von der Fotoaufnahme bis
  zur Simulation.
* [ ] Sie wissen, welche vier Werkzeuge im Tool-Stack eingesetzt werden und
  welche Aufgabe jedes Werkzeug übernimmt.
* [ ] Sie kennen den bereitgestellten Musterdatensatz und wissen, wie er
  verwendet wird.
* [ ] Sie können ein geeignetes eigenes Objekt für die Photogrammetrie auswählen
  und Ihre Wahl begründen.
```

## Der Gesamtworkflow

Das Leitprojekt folgt einem durchgängigen Workflow, der alle wesentlichen
Methoden des Virtual Engineering und Reverse Engineering verbindet. Der rote
Faden der Vorlesung lässt sich in fünf Schritte zusammenfassen:

```
Fotos aufnehmen → Mesh erzeugen → Mesh bereinigen → drucken      → simulieren
   (Meshroom)      (Meshroom)     (CloudCompare)    (PrusaSlicer)   (VPython)
```

Jeder dieser Schritte entspricht einer Phase der Vorlesung und wird in den
folgenden Wochen schrittweise erarbeitet. Am Präsenztag am Ende der Vorlesung
werden alle Ergebnisse zusammengeführt: Die simulierte Kugelbahn wird mit der
gedruckten, realen Kugelbahn verglichen.

## Welche Werkzeuge setzen wir ein?

Für das gesamte Projekt setzen wir ausschließlich Open-Source-Werkzeuge ein.
Das hat zwei Vorteile: Die Werkzeuge sind kostenlos verfügbar und können nach
der Vorlesung ohne Lizenzkosten weiter genutzt werden.

**Meshroom** ist eine Software für Photogrammetrie. Aus einer Serie von Fotos,
die ein Objekt aus verschiedenen Winkeln zeigen, berechnet Meshroom automatisch
eine dreidimensionale Punktwolke und ein Mesh. Die zugrundeliegende Technologie
heißt *Structure from Motion* (SfM) und *Multi-View Stereo* (MVS), die wir in
Kapitel 2 genauer kennenlernen werden. Meshroom ist für Windows und Linux
verfügbar.

```{admonition} Hinweis für macOS-Nutzer
:class: warning
Meshroom ist offiziell nicht für macOS verfügbar, da es eine NVIDIA-GPU mit
CUDA-Unterstützung benötigt, die in aktuellen Apple-Geräten nicht vorhanden ist.
Für macOS-Nutzer steht der Musterdatensatz zur Verfügung, der bereits alle
Meshroom-Ergebnisse enthält. Ab Kapitel 4 (CloudCompare) arbeiten alle
Studierenden mit demselben Datensatz.
```

**CloudCompare** ist ein Werkzeug zur Verarbeitung und Analyse von Punktwolken
und Meshes. Es ermöglicht das Filtern, Glätten und Reparieren von Scandaten
sowie den Vergleich eines gescannten Modells mit einer Referenzgeometrie.
CloudCompare läuft auf Windows, Linux und macOS.

**PrusaSlicer** ist ein Slicer für den 3D-Druck. Er wandelt ein Mesh (zum
Beispiel eine .stl-Datei) in eine druckfertige Datei um, die der 3D-Drucker
verarbeiten kann. Dabei werden Parameter wie Schichthöhe, Fülldichte und
Stützstrukturen festgelegt. PrusaSlicer läuft auf Windows, Linux und macOS.

```{admonition} Hinweis zur Tool-Wahl
:class: tip
In dieser Vorlesung wird bevorzugt PrusaSlicer verwendet. Als Alternative
ist auch Cura vollständig geeignet, da beide Slicer die gleichen
Grundfunktionen bieten. Wenn Sie bereits Erfahrung mit einem der beiden haben,
können Sie dieses einsetzen. Screenshots und Anleitungen im Material beziehen
sich auf PrusaSlicer; die entsprechenden Funktionen sind in Cura analog zu
finden.
```

**VPython** ist eine Python-Bibliothek für 3D-Visualisierung und
Physiksimulation. Sie wurde speziell für die Lehre entwickelt und erlaubt es,
physikalische Vorgänge wie die Bewegung einer Kugel auf einer Bahn direkt im
Browser zu simulieren und zu visualisieren. Grundlegende Python-Kenntnisse
werden vorausgesetzt; VPython selbst wird ab Kapitel 9 eingeführt.

## Was enthält der Musterdatensatz?

Für das Leitprojekt steht ein vorgefertigter Foto-Datensatz der Kugelbahn zur
Verfügung. Dieser Datensatz wurde unter kontrollierten Bedingungen aufgenommen
und enthält alle Fotos, die für eine vollständige Meshroom-Rekonstruktion
benötigt werden.

Der Musterdatensatz enthält die originalen Fotos der Kugelbahn (ca. 80
Aufnahmen), das fertige Meshroom-Ergebnis mit Punktwolke und Mesh sowie ein
bereinigtes CloudCompare-Projekt.

*Warum brauchen wir überhaupt einen Musterdatensatz?* Photogrammetrie hängt
stark von der Aufnahmequalität ab. Glänzende Oberflächen, schlechte Beleuchtung
oder zu wenige Fotos führen zu unvollständigen Modellen. Der Musterdatensatz
stellt sicher, dass alle Studierenden, unabhängig von der Qualität ihrer eigenen
Aufnahmen, mit denselben Ausgangsdaten weiterarbeiten können. Er dient als
gemeinsame Referenz für alle nachfolgenden Schritte.

## Wie wählen wir ein geeignetes eigenes Objekt aus?

Parallel zum Musterdatensatz fotografieren wir in Kapitel 2 ein eigenes Objekt.
Diese Aufgabe dient dazu, die Herausforderungen der Photogrammetrie selbst zu
erleben: Nicht jedes Objekt eignet sich gleich gut, und die Aufnahmetechnik hat
einen großen Einfluss auf das Ergebnis.

Ein gut geeignetes Objekt für die Photogrammetrie hat eine matte, texturierte
Oberfläche (zum Beispiel Holz, Beton oder rauen Kunststoff), eine kompakte,
handliche Größe von etwa 10 bis 30 cm sowie ausreichend viele verschiedene
Details und Merkmale. Weniger geeignet sind glänzende oder spiegelnde
Oberflächen, transparente Materialien, sehr gleichförmige strukturlose Flächen
sowie sehr große oder sehr kleine Objekte.

```{admonition} Mini-Übung
:class: tip
Wählen Sie ein eigenes Objekt aus Ihrem Alltag oder dem Maschinenbaustudium für
die Photogrammetrie-Aufgabe in Kapitel 2. Beschreiben Sie Ihre Wahl in drei bis
vier Sätzen:

- Was ist das Objekt?
- Warum eignet es sich gut für die Photogrammetrie?
- Welche Schwierigkeiten könnten auftreten?
```

````{admonition} Lösung
:class: tip
:class: dropdown
Beispiellösung für ein Pleuel aus dem Maschinenbaulabor:

Das Objekt ist ein Pleuel aus Aluminium, wie es in Verbrennungsmotoren eingesetzt
wird, um die Kurbelwelle mit dem Kolben zu verbinden. Es eignet sich gut für die
Photogrammetrie, weil es eine klare, dreidimensionale Form mit gut erkennbaren
Kanten und Bohrungen hat, die dem Algorithmus viele Merkmalspunkte bietet. Die
Oberfläche ist durch die Bearbeitung leicht matt und diffus reflektierend, was
Reflexionen reduziert. Als mögliche Schwierigkeit könnte die glatte, bearbeitete
Fläche an den Lageraugen problematisch sein; hier könnte ein Hauch Kreide-Spray
helfen.

Andere gut geeignete Objekte sind zum Beispiel ein Zahnrad, ein
Motorblock-Ausschnitt, eine alte Schraube oder ein Stein mit rauer Oberfläche.
````

## Vorschau auf den weiteren Verlauf

Die folgende Tabelle gibt einen Überblick, in welcher Woche welcher
Workflow-Schritt erarbeitet wird:

| Kapitel | Thema | Werkzeug |
|---------|-------|----------|
| 1–2 | Grundlagen, Photogrammetrie, Fotoaufnahme | Meshroom |
| 3 | Mesh erzeugen und beurteilen | Meshroom |
| 4–6 | Punktwolke bereinigen, Registration, Abweichungsanalyse | CloudCompare |
| 7–8 | 3D-Druck vorbereiten und auswerten | PrusaSlicer / Cura |
| 9–11 | Simulation der Kugelbahn | Python / VPython |
| 12–13 | Zusammenführung, Präsenztag | alle Werkzeuge |

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir das Leitprojekt der Vorlesung kennengelernt: die
Digitalisierung, den 3D-Druck und die Simulation einer Kugelbahn. Der
Gesamtworkflow führt von der Fotoaufnahme über die Mesh-Erzeugung und
-Bereinigung zum 3D-Druck und schließlich zur physikalischen Simulation. Alle
vier Werkzeuge (Meshroom, CloudCompare, PrusaSlicer und VPython) sind Open
Source und kostenlos verfügbar. Im nächsten Kapitel tauchen wir in die
Grundlagen der Photogrammetrie ein und verstehen, wie ein Computer aus einer
Serie gewöhnlicher Fotos ein dreidimensionales Modell berechnen kann.
