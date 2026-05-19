---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 8.1 Was ist Ursina, und wie funktioniert es?

Wir haben unsere Kugelbahn digitalisiert, bereinigt und gedruckt. Jetzt wollen
wir sie zum Leben erwecken: eine Kugel soll die Bahn digital hinunterrollen.
Dafür brauchen wir ein Werkzeug, das dreidimensionale Objekte in Echtzeit
darstellen und animieren kann. Dieses Werkzeug heißt **Ursina**, eine
Python-Bibliothek für interaktive 3D-Anwendungen, die auf der bewährten
Spiele-Engine Panda3D aufbaut.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können Ursina installieren und ein einfaches Python-Skript mit
  einer 3D-Szene erstellen und ausführen.
* [ ] Sie können die grundlegende Programmstruktur von Ursina erklären:
  `app = Ursina()`, `Entity`, `def update()`, `app.run()`.
* [ ] Sie können das dreidimensionale Koordinatensystem von Ursina beschreiben
  und einfache Objekte (Kugel, Quader, Zylinder) mit Position, Farbe und
  Größe erzeugen.
* [ ] Sie können die Szene mit der `EditorCamera` interaktiv erkunden.
* [ ] Sie kennen den Unterschied zwischen Ursina und einem Jupyter Notebook
  und können erklären, warum Ursina-Skripte als eigenständige `.py`-Dateien
  ausgeführt werden.
```

## Warum Ursina?

In einem Python-Skript können wir Zahlen berechnen und in der Konsole ausgeben.
Was uns fehlt, ist die Möglichkeit, diese Zahlen als Bewegung im Raum
darzustellen. *Warum ist das so wichtig?*

Ein typischer Fehler in physikalischen Simulationen ist ein falsches Vorzeichen
in der Kraftberechnung. Numerisch ist das Ergebnis eine Zahl; ohne
Visualisierung bemerken wir den Fehler vielleicht erst nach langem Suchen. Mit
Ursina sehen wir sofort, wenn die Kugel nach oben statt nach unten
beschleunigt.

Ursina kombiniert dabei zwei Stärken: die Einfachheit von Python und die
Leistungsfähigkeit einer echten 3D-Engine. Wir können das bereinigte Mesh
unserer Kugelbahn aus Kapitel 4 bis 6 direkt als `.obj`-Datei laden und die
simulierte Kugel auf dem echten Modell rollen lassen. Das werden wir in
Kapitel 10 tun. Die Grundbausteine dafür erarbeiten wir in diesem Kapitel.

In Kapitel 9 werden wir sehen, wie wir Kräfte und Reibung in die Simulation
einbauen, sodass die Kugel nicht nur animiert ist, sondern sich physikalisch
korrekt verhält.

## Installation

````{admonition} Ursina installieren
:class: warning
```code
pip install ursina==6.1.2
```

Wir verwenden Version 6.1.2, die auf allen gängigen Betriebssystemen stabil
läuft. Die Installation zieht Panda3D automatisch als Abhängigkeit mit.

**macOS:** Beim ersten Start erscheinen GLSL-Warnungen in der Konsole. Diese
sind nicht-fatal und können ignoriert werden, solange das Fenster sich öffnet
und die Animation läuft.
````

## Das erste Ursina-Programm

Jedes Ursina-Skript folgt derselben Grundstruktur. Hier ist das
kleinstmögliche lauffähige Beispiel:

```{code-cell} python
:tags: [skip-execution]
from ursina import *

app = Ursina()

wuerfel = Entity(model='cube', color=color.orange)

def update():
    wuerfel.rotation_y += 1

app.run()
```

Vier Zeilen genügen für eine animierte 3D-Szene. Schauen wir uns die
Bestandteile genauer an.

### Wie starte ich die Anwendung?

Diese Zeile öffnet das Anwendungsfenster und initialisiert die 3D-Engine.
Sie steht immer an erster Stelle, vor allen Entities und Funktionen.

### Was ist eine Entity?

Alles, was in der Szene sichtbar ist, ist eine **Entity**, ein Objekt mit
Eigenschaften wie Position, Größe, Farbe und Modell. Der Parameter `model`
gibt die Form an (`'cube'`, `'sphere'`, `'cylinder'`), `color` die Farbe.

### Was bewirkt update()?

Diese Funktion wird von Ursina automatisch in jedem Frame aufgerufen,
typischerweise 60 Mal pro Sekunde. Alles, was sich bewegen oder verändern
soll, kommt hierher. Die Variable `time.dt` enthält die Zeit in Sekunden,
die seit dem letzten Frame vergangen ist. Sie ist das Ursina-Äquivalent
zum Zeitschritt `dt` aus der Physik.

### Wofür steht "app.run()"?

Diese Zeile startet die Hauptschleife und muss immer am Ende stehen. Das Skript
hält an dieser Stelle an, bis das Fenster geschlossen wird.

## Das Koordinatensystem

Ursina verwendet ein rechtshändiges Koordinatensystem:

- **x** zeigt nach rechts
- **y** zeigt nach oben
- **z** zeigt aus dem Bildschirm heraus (in Richtung der betrachtenden Person)

Für unsere Kugelbahn bedeutet das: Die Bahn verläuft hauptsächlich entlang
der x-Achse, die Schwerkraft wirkt in die negative y-Richtung, und die Breite
der Führungsrille erstreckt sich in z-Richtung.

Alle Positionen werden mit `Vec3(x, y, z)` angegeben:

```python
from ursina import *

app = Ursina()
window.color = color.white

# Drei Kugeln entlang der x-Achse
Entity(model='sphere', color=color.red,
       position=Vec3(-2, 0, 0), scale=0.4)
Entity(model='sphere', color=color.green,
       position=Vec3( 0, 0, 0), scale=0.4)
Entity(model='sphere', color=color.blue,
       position=Vec3( 2, 0, 0), scale=0.4)

EditorCamera()
app.run()
```

```{admonition} Navigation mit EditorCamera
:class: note
Nach dem Öffnen einmal ins Fenster klicken, damit es den Fokus bekommt:

- **Rechte Maustaste + Ziehen:** Szene drehen
- **Scrollrad:** Zoom
- **Mittlere Maustaste + Ziehen:** Szene verschieben
```

## Welche Grundobjekte kennt Ursina?

### Wie erstelle ich eine Kugel?

```python
from ursina import *

app = Ursina()
window.color = color.white

kugel = Entity(
    model    = 'sphere',
    color    = color.red,
    scale    = 0.1,           # Durchmesser in Metern (Radius = 0.05 m)
    position = Vec3(0, 0, 0)
)

EditorCamera()
app.run()
```

```{admonition} Hinweis: scale ist der Durchmesser
:class: note
In Ursina hat ein Einheitsobjekt (`scale=1`) einen Durchmesser von 1. Für
eine Kugel mit Radius r setzen wir also `scale = 2 * r`. Das ist ein
wichtiger Unterschied zu VPython, wo `radius` direkt angegeben wird.
```

### Wie erstelle ich einen Quader?

```python
from ursina import *

app = Ursina()
window.color = color.white

rampe = Entity(
    model    = 'cube',
    color    = color.gray,
    scale    = Vec3(1.2, 0.02, 0.12),   # Länge x, Höhe y, Breite z in Metern
    position = Vec3(0, 0, 0)
)

EditorCamera()
app.run()
```

### Wie erstelle ich einen Zylinder?

```python
from ursina import *

app = Ursina()
window.color = color.white

# Liegender Zylinder entlang der x-Achse (rotation_z=90 dreht ihn)
schiene = Entity(
    model      = 'cylinder',
    color      = color.gray,
    scale      = Vec3(0.016, 1.0, 0.016),
    position   = Vec3(0, 0, 0),
    rotation_z = 90
)

EditorCamera()
app.run()
```

```{admonition} Mini-Übung
:class: tip
Erstellen Sie eine Szene mit drei Objekten:

1. Einen grauen Quader an `Vec3(0, 0, 0)` mit `scale=Vec3(1.0, 0.02, 0.15)`.
2. Eine rote Kugel an `Vec3(-0.4, 0.06, 0)` mit `scale=0.08`.
3. Einen blauen Zylinder an `Vec3(0, 0.5, 0)` mit `scale=Vec3(0.02, 1.0, 0.02)`.

Fügen Sie `EditorCamera()` hinzu und erkunden Sie die Szene.
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
from ursina import *

app = Ursina()
window.color = color.white

Entity(model='cube',   color=color.gray, scale=Vec3(1.0, 0.02, 0.15),
       position=Vec3(0, 0, 0))
Entity(model='sphere', color=color.red,  scale=0.08,
       position=Vec3(-0.4, 0.06, 0))
Entity(model='cylinder', color=color.blue, scale=Vec3(0.02, 1.0, 0.02),
       position=Vec3(0, 0.5, 0))

EditorCamera()
app.run()
```
````

## Wie stelle ich Farben und das Fenster ein?

Ursina kennt vordefinierte Farben (`color.red`, `color.green`, `color.blue`,
`color.orange`, `color.gray`, `color.white`, `color.black` und weitere) sowie
eigene RGB-Farben mit `color.rgb(r, g, b)`, wobei die Werte zwischen 0 und 1
liegen.

Das Fenster lässt sich beim Start konfigurieren:

```python
from ursina import *

app = Ursina(
    title  = 'Kugelbahn: Simulation',
    width  = 1200,
    height = 700
)

window.color = color.white

# Objekte...
Entity(model='sphere', color=color.red, scale=0.1)

EditorCamera()
app.run()
```

## Zusammenfassung und Ausblick

In diesem Abschnitt haben wir Ursina als 3D-Bibliothek für Python
kennengelernt. Jedes Skript besteht aus `app = Ursina()`, Entities mit Modell,
Farbe und Position, der `update()`-Funktion für Animationen und `app.run()`
zum Starten. Das Koordinatensystem ist rechtshändig mit y nach oben, Positionen
werden mit `Vec3(x, y, z)` angegeben, und `scale` gibt den Durchmesser an.
Mit `EditorCamera` lässt sich die Szene interaktiv erkunden.

Im nächsten Abschnitt bringen wir die Kugel zum Rollen: Wir lernen, wie die
`update()`-Funktion im Detail funktioniert, was `time.dt` bedeutet und wie wir
ein Objekt mit einer Geschwindigkeit durch den Raum bewegen.
