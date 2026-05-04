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

---

## Tool-Stack (ausschließlich Open Source)

| Tool | Zweck | Betriebssystem |
| ---- | ----- | -------------- |
| **Meshroom** | Photogrammetrie: Fotos → Mesh | Windows, Linux |
| **CloudCompare** | Punktwolke bereinigen, Registration, Abweichungsanalyse | Windows, Linux, macOS |
| **PrusaSlicer** | Slicing: Mesh → 3D-Druckdatei (alternativ: Cura) | Windows, Linux, macOS |
| **Python / VPython** | Simulation der Kugelbahn | plattformunabhängig |

**Wichtig:** macOS-Nutzer können Meshroom nicht nativ nutzen → ab Kapitel 4
arbeiten alle Studierenden mit demselben exportierten Mesh.

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

### Seitenstruktur

Jede Sektion folgt dieser festen Abfolge:

1. **H1-Titel** (`# Titel der Sektion`)
2. **3-4 einleitende Sätze**: kein Inhaltsverzeichnis, kein "In diesem Kapitel lernen wir ...", sondern ein konkretes Szenario oder eine Problemstellung, die Neugier weckt und den Abschnitt in den Gesamtworkflow einordnet.
3. **`## Lernziele`** mit der Lernziel-Box
4. Inhaltliche Unterabschnitte
5. **`## Zusammenfassung und Ausblick`**

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

### Nummerierte Übungen (Schwierigkeitsgrad mit Sternen)

Admonition-Blöcke werden grundsätzlich mit **drei Backticks** (` ``` `) geöffnet
und geschlossen. **Vier Backticks** (` ```` `) sind nur dann erforderlich, wenn
der Block einen eingebetteten Fenced Code Block enthält (` ```python ... ``` `),
da MyST sonst den inneren Block als Abschluss des äußeren interpretiert.

Drei Backticks (Normalfall, kein eingebetteter Code):

```{admonition} Übung X.Y (✩)
:class: tip
Aufgabentext hier.
```

```{admonition} Lösung
:class: tip
:class: dropdown
Lösungstext hier.
```

Vier Backticks (nur wenn die Lösung einen ```python-Block enthält):

```{admonition} Übung X.Y (✩✩)
:class: tip
Aufgabentext hier.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
# Musterlösung hier
```
````

Schwierigkeitsgrade:

```markdown
```{admonition} Übung X.Y (✩)             ← einfach
```{admonition} Übung X.Y (✩✩)            ← mittel
```{admonition} Übung X.Y (✩✩✩)           ← schwer
```{admonition} Übung X.Y (Mini-Projekt)  ← umfangreich
```

### Eingebettete YouTube-Videos

```markdown
```{dropdown} Video "Titel" von Quelle
<iframe width="560" height="315" src="https://www.youtube.com/embed/VIDEO_ID"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen></iframe>
```

### Markdown-Tabellen

Tabellen werden im **compact-Stil** gesetzt: In der Trennzeile steht auf beiden
Seiten der Striche je ein Leerzeichen. Die Variante ohne Leerzeichen (`|---|`)
ist nicht erlaubt, da sie die Linter-Warnung MD060 auslöst.

```markdown
| Spalte 1 | Spalte 2 | Spalte 3 |
| -------- | -------- | -------- |
| Inhalt   | Inhalt   | Inhalt   |
```

### Abschluss jeder Sektion

Jede Sektion endet mit:

```markdown
## Zusammenfassung und Ausblick

Kurzer Rückblick auf die Inhalte und Vorschau auf das nächste Kapitel.
```

---

## TikZ-Abbildungen

Alle Abbildungen werden als eigenständige `standalone`-Dokumente in LaTeX
erstellt, nach SVG exportiert und über eine `{figure}`-Direktive in die
MyST-Markdown-Quelldatei eingebunden. Die Kompilierung erfolgt mit `lualatex`.

### Präambel-Vorlage

Jede TikZ-Datei verwendet ausnahmslos die folgende Präambel:

```latex
\documentclass[11pt]{standalone}
\usepackage{amssymb}
\usepackage{amsmath}
\usepackage[no-math]{fontspec}
\usepackage{unicode-math}
\setmainfont{Libertinus Sans}
\setsansfont{Libertinus Sans}
\setmathfont{Libertinus Math}
\usepackage{pgf,xcolor}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, backgrounds}
\usepackage{pgfplots}
\pgfplotsset{compat=newest}
\usepackage{pifont}
```

`pgfplots` wird in jeder Datei eingebunden, auch wenn die Abbildung nur
reines TikZ verwendet, damit die Präambel über alle Dateien identisch bleibt.

Die Präambel darf bei Bedarf erweitert werden.

### Schrift

Die Abbildungen verwenden **Libertinus Sans** als Textschrift und
**Libertinus Math** als Mathematikschrift. Libertinus Sans passt als
serifenlose Schrift zum Standard-Theme von Jupyter Book; Libertinus Math
stellt sicher, dass Formeln in Abbildungen auch in späteren Kapiteln
korrekt gesetzt werden. Das Paket `\usepackage{libertinus}` wird nicht
mehr verwendet, da die Schriften nun explizit über `fontspec` und
`unicode-math` konfiguriert werden. Keine anderen Schriftfamilien verwenden
(insbesondere nicht TeX Gyre Heros oder Computer Modern).

### Farbpalette

Alle sieben Farben werden in jeder Datei definiert, auch wenn nur eine
Teilmenge verwendet wird:

```latex
\definecolor{my_darkgray}{HTML}{484949}
\definecolor{my_lightgray}{HTML}{F3F4F4}
\definecolor{my_darkblue}{HTML}{005A94}
\definecolor{my_lightblue}{HTML}{CCDEE9}
\definecolor{my_yellow}{HTML}{FFEC7F}
\definecolor{my_red}{HTML}{E60000}
\definecolor{my_orange}{HTML}{E87846}
```

Keine ad-hoc-Farbnamen einführen. Alle Farben kommen ausnahmslos aus
dieser Palette.

**Zweifarbige Abbildungen (Standardfall):** `my_darkblue` für das primäre
Element (Konturlinie, Hauptkurve, dominante Region) und `my_lightblue` für
das sekundäre Element (Füllung, Hintergrundregion, zweite Kurve).

**Dreifarbige Funktionsgraphen:** `my_darkblue` für die erste Kurve,
`my_red` für die zweite, `my_orange` für die dritte. `my_yellow` nicht für
Kurvenlinien verwenden (zu wenig Kontrast). `my_yellow` ist für
hervorgehobene Füllregionen reserviert.

**Text und Annotationen:** `my_darkgray` für sekundäre Labels.
`my_darkblue` für Labels, die mathematische oder technische Objekte
bezeichnen.

### Hintergrundpanel

Jede Abbildung hat ein explizites Hintergrundpanel mit `my_lightgray`.
Dies gewährleistet korrekte Darstellung in hellen und dunklen
Browser-Themes:

```latex
\begin{tikzpicture}[
    show background rectangle,
    background rectangle/.style={fill=my_lightgray, rounded corners=8pt},
    inner frame sep=0.8cm
]
```

`inner frame sep=0.3cm` nur für breite, flache Abbildungen (zum Beispiel
Zahlenstrahlen). In allen anderen Fällen `0.8cm`.

### Achsenstil für Funktionsgraphen (pgfplots)

```latex
\begin{axis}[
    axis lines = center,
    xlabel = {$x$},
    ylabel = {$y$},
    grid = both,
    axis equal,
    axis line style={thick},
]
```

`axis equal` nur weglassen, wenn das natürliche Seitenverhältnis der
Funktion den Graphen unleserlich macht. Die Ausnahme mit einem Kommentar
dokumentieren. Alle Kurven:

```latex
\addplot[draw=my_darkblue, samples=300, ultra thick, domain=a:b]{ ... };
```

### Legenden

Bei mehr als einer Kurve eine Legende einfügen:

```latex
legend pos=north west,
legend style={font=\small},
legend cell align=left,
```

`\addlegendentry{...}` direkt nach dem jeweiligen `\addplot`-Aufruf.

### Schematische Diagramme und technische Abbildungen

Für Diagramme ohne Koordinatenachsen (annotierte Skizzen, Konzeptdiagramme,
Mehrpanel-Vergleiche) gelten folgende Ergänzungen zur allgemeinen Farbpalette.

**Annotationspfeil:** Beschriftungspfeile verwenden einheitlich den
Stealth-Pfeilkopf in `my_darkgray`. Die Stil-Definition gehört in das
optionale Argument der `tikzpicture`-Umgebung:

```latex
annotation/.style={draw=my_darkgray, thick, -{Stealth[length=7pt, width=5pt]}}
```

Labels neben Annotationspfeilen: `font=\small, text=my_darkgray`.

**Mehrpanel-Layout:** Panels werden mit `\begin{scope}[xshift=...]`
nebeneinander gesetzt. Der Abstand zwischen zwei Panels beträgt mindestens
`1cm`. Vertikale Trennlinien zwischen Panels sind nicht erforderlich.

**Panel-Untertitel:** Jedes Panel erhält einen Titel direkt unterhalb des
Inhalts, zentriert:

```latex
\node[font=\small\bfseries, text=my_darkgray, anchor=north] at (...) {...};
```

**Hervorgehobene Elemente:**

- Fläche oder Füllregion: `fill=my_yellow`
- Linienelement (Kante, Achse): `draw=my_orange, ultra thick`
- Knotenpunkt: `fill=my_orange` mit weißem Rand (`draw=my_lightgray, thick`)

**Bewertungssymbole:** ✓ und ✗ werden über das Paket `pifont` gesetzt
(bereits in der Präambel). `\ding{51}` für ✓, `\ding{55}` für ✗.
Unicode-Zeichen dürfen in Kommentaren erscheinen, aber nicht im ausführbaren
LaTeX-Code. `font=\large\bfseries`. ✓ in `my_darkblue`, ✗ in `my_red`.

### Einbindung in MyST Markdown

SVG-Dateien werden im Unterordner `bilder/` abgelegt und mit der
`{figure}`-Direktive eingebunden:

````markdown
```{figure} bilder/dateiname.svg
:alt: Kurze Beschreibung für Screenreader
:align: center

Darstellung von [was die Abbildung zeigt].
(Quelle: eigene Abbildung; Lizenz [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0))
```
````

Den beschreibenden Teil der Bildunterschrift auf einen Satz begrenzen.
Keine Informationen wiederholen, die bereits im umgebenden Fließtext stehen.

### Dateinamen

Dateinamen beschreibend, in Kleinbuchstaben mit Unterstrichen, ohne
Kapitel- oder Sektionsnummer. Das Sprachkürzel `_DE` oder `_EN` nur
anhängen, wenn zwei Sprachversionen derselben Abbildung existieren.

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
- Englische Fachbegriffe, die im deutschen Satz als Nomen verwendet werden,
  werden großgeschrieben, auch wenn sie aus mehreren Wörtern bestehen
  (zum Beispiel: Watertight Mesh, Non-Manifold Edges, Triangle Mesh, Sparse
  Point Cloud). Das gilt auch für englische Nomen in Klammern als
  Übersetzungsangabe (zum Beispiel: `(englisch: "Holes")`).
  Wird ein englisches Wort hingegen als Prädikatsadjektiv verwendet, bleibt
  es klein (zum Beispiel: "das Mesh ist nicht watertight").
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

## Qualitätscheckliste vor dem Abliefern

Vor dem Ausgeben einer Sektion prüfen:

- [ ] YAML-Header vorhanden?
- [ ] Nach dem H1-Titel 3-4 einleitende Sätze vorhanden (konkretes Szenario,
  kein "In diesem Kapitel ...")?
- [ ] Einleitung beginnt mit einem konkreten Szenario oder Problem, nicht mit
  einer Definition?
- [ ] Lernziele mit `* [ ]` formatiert.
- [ ] Unterabschnittsüberschriften als Fragen oder natürliche Aussagen
  formuliert?
- [ ] Prinzip "Erst Beispiel, dann abstrakt" eingehalten?
- [ ] Mindestens eine rhetorische Frage im Fließtext, kursiv gesetzt?
- [ ] Mindestens ein Rückverweis auf eine frühere Sektion?
- [ ] Mindestens ein konkreter Vorwärtsverweis auf ein späteres Thema?
- [ ] Kein Gedankenstrich im Fließtext?
- [ ] Englische Fachbegriffe, die als Nomen verwendet werden, großgeschrieben?
- [ ] Kein `d.h.` oder `z.B.` mitten im Satz?
- [ ] Wir-Perspektive im Fließtext, Sie-Anrede nur in den Lernzielen?
- [ ] YouTube-Videos direkt nach dem jeweiligen Unterabschnitt eingebettet,
  nicht am Ende der Sektion gesammelt?
- [ ] Tabellen im compact-Stil gesetzt (Leerzeichen in der Trennzeile: `| ---
  |`)?
- [ ] Mini-Übungen mit Lösungs-Dropdown versehen?
- [ ] Zusammenfassung mit konkretem Ausblick auf die nächste Sektion?
- [ ] TikZ-Abbildungen: Präambel identisch mit Vorlage, alle 7 Farben definiert?
- [ ] TikZ-Abbildungen: Hintergrundpanel mit `my_lightgray` gesetzt?
- [ ] TikZ-Abbildungen: Nur Farben aus der definierten Palette verwendet?
- [ ] TikZ-Abbildungen: `{figure}`-Direktive mit `alt`-Text und Lizenzangabe?
