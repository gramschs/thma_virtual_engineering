# Instruktionen: Vorlesungsmaterial Virtual Engineering

## Kontext

Dieses Projekt enthält das Vorlesungsmaterial für das Modul **Virtual Engineering**
an der Technischen Hochschule Mannheim (Prof. Dr. Simone Gramsch).
Das Material wird mit **MyST Markdown** erstellt und ist für **Jupyter Book** konzipiert.

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

```
Fotos aufnehmen → Mesh erzeugen → bereinigen → drucken       → simulieren → vergleichen
   (Meshroom)      (Meshroom)    (CloudCompare) (PrusaSlicer)  (VPython)   (Präsenztag)
```

**Musterdatensatz:** Studierende erhalten einen vorgefertigten Foto-Datensatz der
Kugelbahn (Option 3: eigenes Objekt fotografieren + Musterdatensatz nutzen).

---

## Tool-Stack (ausschließlich Open Source)

| Tool | Zweck | Betriebssystem |
|------|-------|----------------|
| **Meshroom** | Photogrammetrie: Fotos → Mesh | Windows, Linux |
| **CloudCompare** | Punktwolke bereinigen, Registration, Abweichungsanalyse | Windows, Linux, macOS |
| **PrusaSlicer** | Slicing: Mesh → 3D-Druckdatei (alternativ: Cura) | Windows, Linux, macOS |
| **Python / VPython** | Simulation der Kugelbahn | plattformunabhängig |

**Wichtig:** macOS-Nutzer können Meshroom nicht nativ nutzen → Musterdatensatz
als Workaround bereitstellen.

---

## Vorlesungsgliederung (13 Wochen)

| Phase | Wochen | Inhalt | Tool |
|-------|--------|--------|------|
| 1 | 1–2 | Grundlagen, Photogrammetrie, Aufnahme | Meshroom |
| 2 | 3–6 | Reverse Engineering, Punktwolken, Qualitätssicherung | CloudCompare |
| 3 | 7–8 | 3D-Druck, Slicing, Auswertung | PrusaSlicer |
| 4 | 9–11 | Simulation mit Python/VPython | VPython |
| 5 | 12–13 | Zusammenführung, Präsenztag | alle Tools |

---

## Dateistruktur eines Kapitels

Die Dateistruktur ist flexibel und richtet sich nach dem Inhalt der Woche:

**Theorie-Wochen** (z. B. Woche 1, 12): 3 Dateien

```
chapterXX_sec01.md   → Theorieteil 1
chapterXX_sec02.md   → Theorieteil 2
chapterXX_sec03.md   → Übungen
```

**Tool-Wochen** (z. B. Wochen 2–11): 4 Dateien

```
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

```markdown
## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Lernziel 1
* [ ] Lernziel 2
```
```

### Ausführbare Code-Zellen

```markdown
```{code-cell} python
# Python-Code hier
print("Beispiel")
```
```

### Mini-Übungen (innerhalb der Theorieteile)

```markdown
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
```

### Nummerierte Übungen (sec03, Schwierigkeitsgrad mit Sternen)

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
- Variablennamen sind **sprechend und auf Deutsch** (z. B. `temperatur_C`, `zeit_s`)
- Einheiten werden im Variablennamen kodiert (z. B. `_C` für Celsius, `_s` für Sekunden)

### Konstanten
- Konstanten werden in **GROSSBUCHSTABEN** geschrieben (z. B. `KRITISCHE_TEMPERATUR_C = 300`)

### Code-Kommentare
- Code wird mit **EVA-Kommentaren** strukturiert:
  ```python
  # Eingabe
  # Verarbeitung
  # Ausgabe
  ```

### Visualisierung
- Standardmäßig wird **Plotly Express** (`import plotly.express as px`) für Diagramme verwendet

### Sprache
- Alle Materialien sind auf **Deutsch**
- Fachbegriffe auf Englisch werden beim ersten Auftreten erklärt
- In den **Lernzielen** wird die Studierenden mit **Sie** angesprochen
  (z. B. "Sie können ... erklären")
- In den **übrigen Lehrtexten** wird die gemeinsame Perspektive mit **wir**
  verwendet (z. B. "In diesem Kapitel haben wir ... kennengelernt")

---

## Aufgabenstruktur (sec03)

Jede Übungsdatei folgt diesem Muster:

1. Einfache Verständnisaufgaben (✩) – Konzepte anwenden
2. Mittelschwere Aufgaben (✩✩) – Kombination von Konzepten
3. Schwere Aufgaben (✩✩✩) – Transfer, Analyse, Reflexion
4. Mini-Projekt – umfangreichere, offene Aufgabe mit optionaler Erweiterung

Lösungen sind immer als aufklappbare Dropdowns eingebettet.

---

## Synchron-/Asynchron-Kennzeichnung

Aufgaben und Aktivitäten werden im Material wie folgt gekennzeichnet:

- **Asynchron:** Lernvideos, Tutorials, Aufgaben, Foren (80 %)
- **Synchron:** Online-Session ~45 min, Q&A, Zwischenpräsentationen (20 %)

---

## Referenzmaterial

- **Modulhandbuch:** `Modulhandbuch_VirtualEngineering.pdf`
- **Beispielkapitel Python:** `chapter04_sec01.md`, `chapter04_sec02.md`, `chapter04_sec03.md`
- **Vorlesungsgliederung:** siehe Gesprächsprotokoll im Projekt

---

## Hinweise für die Materialerstellung

- **Just-in-time:** Material muss nicht vollständig vorab fertig sein; 1–2 Wochen Vorlauf reicht
- **Forschendes Lernen:** Transparenz kommunizieren – Workflow wird gemeinsam erarbeitet
- **Starter-Code:** Für VPython-Aufgaben immer einen Grundgerüst-Code bereitstellen
- **YouTube-Tutorials:** Für Tool-Einführungen (CloudCompare, Meshroom) können englische
  Tutorials verlinkt werden, statt eigene Videos zu erstellen
