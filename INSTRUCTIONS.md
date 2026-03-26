# Instruktionen: Vorlesungsmaterial Virtual Engineering

## Kontext

Dieses Projekt enthält das Vorlesungsmaterial für das Modul **Virtual
Engineering** an der Technischen Hochschule Mannheim (Prof. Dr. Simone Gramsch).
Das Material wird mit **MyST Markdown** erstellt und ist für **Jupyter Book**
konzipiert.

---

## Lehrkonzept

- **Blended Learning:** 80 % asynchron, 20 % synchron (Online)
- **Dauer:** 13 Wochen + Präsenztag
- **Zielgruppe:** Masterstudierende Maschinenbau, 2. Semester
- **Grundlegende Python-Vorkenntnisse vorhanden**
- **Methodik:** Forschendes Lernen

### Leitprojekt: Kugelbahn

Der rote Faden aller Kapitel ist die Digitalisierung, der 3D-Druck und die
Simulation einer Kugelbahn:

```code
Fotos aufnehmen → Mesh erzeugen → bereinigen → drucken       → simulieren → vergleichen
   (Meshroom)      (Meshroom)    (CloudCompare) (PrusaSlicer)  (VPython)   (Präsenztag)
```

**Musterdatensatz:** Studierende erhalten einen vorgefertigten Foto-Datensatz
der Kugelbahn (Option 3: eigenes Objekt fotografieren + Musterdatensatz nutzen).

---

## Tool-Stack (ausschließlich Open Source)

| Tool | Zweck | Betriebssystem |
| ---- | ----- | -------------- |
| **Meshroom** | Photogrammetrie: Fotos → Mesh | Windows, Linux |
| **CloudCompare** | Punktwolke bereinigen, Registration, Abweichungsanalyse | Windows, Linux, macOS |
| **PrusaSlicer** | Slicing: Mesh → 3D-Druckdatei (alternativ: Cura) | Windows, Linux, macOS |
| **Python / VPython** | Simulation der Kugelbahn | plattformunabhängig |

**Wichtig:** macOS-Nutzer können Meshroom nicht nativ nutzen → Musterdatensatz
als Workaround bereitstellen.

---

## Vorlesungsgliederung (13 Wochen)

| Phase | Wochen | Inhalt | Tool |
| ----- | ------ | ------ | ---- |
| 1 | 1-2 | Grundlagen, Photogrammetrie, Aufnahme | Meshroom |
| 2 | 3-6 | Reverse Engineering, Punktwolken, Qualitätssicherung | CloudCompare |
| 3 | 7-8 | 3D-Druck, Slicing, Auswertung | PrusaSlicer |
| 4 | 9-11 | Simulation mit Python/VPython | VPython |
| 5 | 12-13 | Zusammenführung, Präsenztag | alle Tools |

---

## Dateistruktur eines Kapitels

Die Dateistruktur ist flexibel und richtet sich nach dem Inhalt der Woche:

**Theorie-Wochen** (z. B. Woche 1, 12): 3 Dateien

```code
chapterXX_sec01.md   → Theorieteil 1
chapterXX_sec02.md   → Theorieteil 2
chapterXX_sec03.md   → Übungen
```

**Tool-Wochen** (z. B. Wochen 2-11): 4 Dateien

```code
chapterXX_sec01.md   → Theorieteil 1
chapterXX_sec02.md   → Theorieteil 2
chapterXX_sec03.md   → Praxisteil: Tool-Tutorial / Schritt-für-Schritt-Anleitung
chapterXX_sec04.md   → Übungen
```

Dateien beginnen immer mit dem YAML-Header:

```yaml
---
kernelspec:
  name: python3
  display_name: 'Python 3'
---
```

---

## MyST-Formatkonventionen

### Lernziele (Beginn jeder Sektion)

````markdown
## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Lernziel 1
* [ ] Lernziel 2
```
````

### Ausführbare Code-Zellen

````markdown
```{code-cell} python
# Python-Code hier
print("Beispiel")
```
````

### Mini-Übungen (innerhalb der Theorieteile)

````markdown
```{admonition} Mini-Übung
:class: tip
Aufgabentext hier.
```

```{code-cell} python
# Code-Zelle

```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
# Musterlösung hier
```
````

````

### Nummerierte Übungen (Schwierigkeitsgrad mit Sternen)

```markdown
````{admonition} Übung X.Y (✩)        ← einfach
````{admonition} Übung X.Y (✩✩)       ← mittel
````{admonition} Übung X.Y (✩✩✩)      ← schwer
````{admonition} Übung X.Y (Mini-Projekt)  ← umfangreich
```

### Eingebettete YouTube-Videos

```markdown
```{dropdown} Video "Titel" von Quelle
<iframe width="560" height="315" src="https://www.youtube.com/embed/VIDEO_ID"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen></iframe>
```
```

### Abschluss jeder Sektion

Jede Sektion endet mit:

```markdown
## Zusammenfassung und Ausblick

Kurzer Rückblick auf die Inhalte und Vorschau auf das nächste Kapitel.
```

---

## Inhaltliche Konventionen

### Fachlicher Kontext
- Alle Beispiele und Aufgaben beziehen sich auf den **Maschinenbau**
- Leitthema ist stets die **Kugelbahn** oder verwandte Anwendungen
- Variablennamen sind **sprechend und auf Englisch** 

### Konstanten
- Konstanten werden in **GROSSBUCHSTABEN** geschrieben (z. B. `CRITICAL_TEMPERATURE = 300`)

### Visualisierung
- Standardmäßig wird **Plotly Express** (`import plotly.express as px`) für Diagramme verwendet

### Sprache
- Alle Materialien sind auf **Deutsch**
- Fachbegriffe auf Englisch werden beim ersten Auftreten erklärt
- In den **Lernzielen** wird die Studierenden mit **Sie** angesprochen
  (z. B. "Sie können ... erklären")
- In den **übrigen Lehrtexten** wird die gemeinsame Perspektive mit **wir**
  verwendet (z. B. "In diesem Kapitel haben wir ... kennengelernt")
- Kein `d.h.` oder `z.B.` mitten im Satz: entweder ausschreiben oder in
  Klammern setzen

### Rhetorische Fragen
- Rhetorische Fragen sind ausdrücklich erwünscht, um Aufmerksamkeit zu lenken
  und Spannung aufzubauen
- Rhetorische Fragen werden kursiv gesetzt:
  *Aber warum liefert Photogrammetrie bei glänzenden Oberflächen schlechte Ergebnisse?*

### Unterabschnittsüberschriften
- Überschriften sollen als Fragen oder kurze natürliche Aussagen formuliert
  werden, die ein Studierender natürlich stellen würde

Gute Beispiele:
- "Warum ist Textur so wichtig?"
- "Wie funktioniert Structure from Motion?"
- "Was leistet CloudCompare?"

Schlechte Beispiele (abstrakte Substantivphrasen):
- "Grundlagen der Photogrammetrie"
- "Anwendungsfelder"
- "Eigenschaften von Punktwolken"

### Prinzip: Erst Beispiel, dann abstrakt
Jedes neue Konzept wird nach folgendem Dreischritt eingeführt:

1. Konkretes Beispiel zuerst: Wir beschreiben ein praktisches Problem
   oder Phänomen in Alltagssprache (z. B. das glänzende Bauteil, das nicht
   rekonstruiert werden kann).
2. Informelle Beschreibung: Wir benennen das Muster oder den Grund dafür
   noch ohne formalen Begriff.
3. Begriff oder Erklärung: Erst jetzt führen wir den Fachbegriff oder
   die technische Erklärung ein.

### Rück- und Vorwärtsverweise
Jede Sektion soll enthalten:
- Mindestens einen Rückverweis auf ein Konzept aus einer früheren Sektion
- Mindestens einen Vorwärtsverweis auf ein späteres Thema

Gute Vorwärtsverweise sind konkret genug, um Neugier zu wecken, aber vage
genug, um die Antwort nicht vorwegzunehmen:

Gut: "In Kapitel 5 werden wir sehen, wie wir dieses Mesh mit dem
Original vergleichen und Abweichungen sichtbar machen können."

Schlecht: "Dies wird später behandelt."

### YouTube-Videos
- Videos werden direkt nach dem Unterabschnitt eingebettet, in dem das
  entsprechende Konzept eingeführt wurde, nicht am Ende der Sektion gesammelt
- Videos sind eine Vertiefung, kein Ersatz für den Fließtext
- Pro Sektion 1 bis 2 Videos
- Für Tool-Einführungen können englische YouTube-Tutorials verlinkt werden

---

## Aufgabenstruktur

Jede Übungsdatei folgt diesem Muster:

1. Einfache Verständnisaufgaben (✩) - Konzepte anwenden
2. Mittelschwere Aufgaben (✩✩) - Kombination von Konzepten
3. Schwere Aufgaben (✩✩✩) - Transfer, Analyse, Reflexion
4. Mini-Projekt - umfangreichere, offene Aufgabe mit optionaler Erweiterung

Lösungen sind immer als aufklappbare Dropdowns eingebettet.

---

## Referenzmaterial

- **Modulhandbuch:** `Modulhandbuch_VirtualEngineering.pdf`
- **Beispielkapitel Python:** `chapter04_sec01.md`, `chapter04_sec02.md`, `chapter04_sec03.md`
- **Vorlesungsgliederung:** siehe Gesprächsprotokoll im Projekt

---

## Hinweise für die Materialerstellung

- **Just-in-time:** Material muss nicht vollständig vorab fertig sein; 1-2 Wochen Vorlauf reicht
- **Forschendes Lernen:** Transparenz kommunizieren - Workflow wird gemeinsam erarbeitet
- **Starter-Code:** Für VPython-Aufgaben immer einen Grundgerüst-Code bereitstellen
- **YouTube-Tutorials:** Für Tool-Einführungen (CloudCompare, Meshroom) können englische
  Tutorials verlinkt werden, statt eigene Videos zu erstellen

---

## Qualitätscheckliste vor dem Abliefern

Vor dem Ausgeben einer Sektion prüfen:

- [ ] YAML-Header vorhanden?
- [ ] Einleitung beginnt mit einem konkreten Szenario oder Problem, nicht mit
  einer Definition?
- [ ] Lernziele mit `* [ ]` formatiert, unmittelbar nach dem H1-Titel?
- [ ] Unterabschnittsüberschriften als Fragen oder natürliche Aussagen formuliert?
- [ ] Prinzip "Erst Beispiel, dann abstrakt" eingehalten?
- [ ] Mindestens eine rhetorische Frage im Fließtext, kursiv gesetzt?
- [ ] Mindestens ein Rückverweis auf eine frühere Sektion?
- [ ] Mindestens ein konkreter Vorwärtsverweis auf ein späteres Thema?
- [ ] Kein Gedankenstrich im Fließtext?
- [ ] Kein `d.h.` oder `z.B.` mitten im Satz?
- [ ] Wir-Perspektive im Fließtext, Sie-Anrede nur in den Lernzielen?
- [ ] YouTube-Videos direkt nach dem jeweiligen Unterabschnitt eingebettet,
  nicht am Ende der Sektion gesammelt?
- [ ] Mini-Übungen mit Lösungs-Dropdown versehen?
- [ ] Zusammenfassung mit konkretem Ausblick auf die nächste Sektion?
