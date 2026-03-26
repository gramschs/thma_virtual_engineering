---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 2.1 Grundlagen der Photogrammetrie

Wie kann ein Computer aus einer Sammlung gewöhnlicher Fotos ein
dreidimensionales Modell berechnen? Diese Frage steht im Mittelpunkt dieses
Kapitels. Wir schauen uns an, welche mathematischen und algorithmischen
Prinzipien dahinter stecken, und verstehen damit auch, warum manche Objekte
sich gut für die Photogrammetrie eignen und andere nicht.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können das Prinzip der Photogrammetrie erklären und von anderen
  3D-Erfassungsmethoden abgrenzen.
* [ ] Sie können die beiden Hauptschritte Structure from Motion und
  Multi-View Stereo beschreiben und ihre jeweilige Ausgabe benennen.
* [ ] Sie kennen den Unterschied zwischen einer Punktwolke und einem Mesh
  und können erklären, wie eine Punktwolke in ein Mesh umgewandelt wird.
* [ ] Sie können begründen, warum texturreiche, matte Oberflächen für die
  Photogrammetrie besser geeignet sind als glänzende oder strukturlose.
```

## Was ist Photogrammetrie?

**Photogrammetrie** bezeichnet die Methode, aus zweidimensionalen Fotos
dreidimensionale Informationen über ein Objekt oder eine Szene zu gewinnen.
Der Begriff setzt sich aus dem griechischen *photos* (Licht), *gramma*
(Aufzeichnung) und *metron* (Maß) zusammen.

Das Grundprinzip ist dasselbe wie das menschliche räumliche Sehen: Wenn wir
ein Objekt mit beiden Augen betrachten, sehen jedes Auge das Objekt aus einem
leicht anderen Winkel. Aus diesen zwei leicht unterschiedlichen Bildern
berechnet unser Gehirn automatisch Tiefe und Entfernung. Die Photogrammetrie
nutzt dasselbe Prinzip, nur mit vielen Fotos aus vielen verschiedenen Winkeln
statt mit zwei Augen.

Moderne Photogrammetrie-Software wie Meshroom kombiniert zwei aufeinander
aufbauende Algorithmen: **Structure from Motion (SfM)** und
**Multi-View Stereo (MVS)**.

## Structure from Motion (SfM)

Der erste Schritt heißt **Structure from Motion (SfM)**, auf Deutsch etwa
"Struktur aus Bewegung". Ziel ist es, aus den Fotos zwei Dinge gleichzeitig
zu berechnen: die Position der Kamera bei jeder Aufnahme und eine erste grobe
Punktwolke des Objekts.

*Wie funktioniert das?*

SfM arbeitet in mehreren Teilschritten:

1. Merkmalsextraktion: Aus jedem Foto werden markante Punkte extrahiert,
sogenannte **Keypoints** oder Merkmalspunkte. Das sind Stellen im Bild, die sich
klar von ihrer Umgebung abheben, zum Beispiel Ecken, Kanten oder besondere
Texturmuster. Der bekannteste Algorithmus dafür heißt SIFT (**Scale-Invariant
Feature Transform**).

2. Merkmalszuordnung: Anschließend sucht der Algorithmus nach denselben
Merkmalspunkten in verschiedenen Fotos. Wenn ein markanter Punkt auf Foto 1
und auf Foto 3 zu sehen ist, wird er als derselbe Punkt identifiziert und
zugeordnet.

3. Kameraposition berechnen: Aus der Zuordnung gemeinsamer Merkmalspunkte
in mehreren Fotos kann die relative Position und Ausrichtung der Kamera bei
jeder Aufnahme berechnet werden. Gleichzeitig entstehen die ersten
dreidimensionalen Koordinaten dieser Merkmalspunkte. Das Ergebnis ist eine
**dünn besetzte Punktwolke** (englisch: *sparse point cloud*) mit einigen
tausend bis zehntausend Punkten.

```{admonition} Mini-Übung
:class: tip
Stellen Sie sich vor, Sie fotografieren eine Kugelbahn von zwei Seiten.
Auf beiden Fotos ist eine markante Verschraubung sichtbar.

Überlegen Sie: Welche Information benötigt der SfM-Algorithmus mindestens,
um aus diesen zwei Fotos die Position der Verschraubung im Raum zu berechnen?
Notieren Sie Ihre Überlegung in zwei bis drei Sätzen.
```

````{admonition} Lösung
:class: tip
:class: dropdown
Der Algorithmus benötigt mindestens die Position desselben Merkmalspunkts
(der Verschraubung) in beiden Fotos sowie die relative Lage der beiden
Kameras zueinander (oder er berechnet beides gleichzeitig). Aus den zwei
unterschiedlichen Blickwinkeln auf denselben Punkt im Raum lässt sich durch
Triangulation die dreidimensionale Position berechnen, ähnlich wie beim
menschlichen Sehen mit zwei Augen.
````

## Multi-View Stereo (MVS)

Die dünn besetzte Punktwolke aus SfM enthält nur wenige tausend Punkte und
reicht nicht aus, um ein detailliertes 3D-Modell zu erzeugen. Hier setzt
*Multi-View Stereo* (MVS) an.

MVS nutzt die bekannten Kamerapositionen aus SfM und analysiert die Fotos
nun deutlich tiefer. Für jeden Bildbereich wird berechnet, wo sich die
entsprechende Oberfläche im Raum befinden muss, damit sie auf allen Fotos,
auf denen sie sichtbar ist, an der richtigen Stelle erscheint. Das Ergebnis
ist eine **dicht besetzte Punktwolke** (englisch: *dense point cloud*) mit
Millionen von Punkten, die die Oberfläche des Objekts sehr detailliert
beschreibt.

## Von der Punktwolke zum Mesh

Eine Punktwolke beschreibt eine Oberfläche als Menge von Punkten im
dreidimensionalen Raum. Sie enthält jedoch keine Informationen darüber,
wie diese Punkte miteinander verbunden sind. Um eine geschlossene, druckbare
oder simulierbare Oberfläche zu erhalten, wird die Punktwolke in ein
**Mesh** umgewandelt.

Ein Mesh besteht aus **Dreiecken** (englisch: *triangles*), die jeweils drei
benachbarte Punkte der Punktwolke verbinden. Die Gesamtheit dieser Dreiecke
bildet ein zusammenhängendes Dreiecksnetz, das die Oberfläche des Objekts
beschreibt. Dieser Schritt heißt **Meshing** oder **Polygonisierung**.

Der Übergang von der Punktwolke zum Mesh ist in Meshroom automatisiert. Im
Ergebnis erhalten wir eine Datei im Format **.obj** oder **.ply**, die das
vollständige Dreiecksnetz enthält.

```{admonition} Mini-Übung
:class: tip
Eine dicht besetzte Punktwolke enthält zum Beispiel 5 Millionen Punkte.

Erklären Sie in zwei bis drei Sätzen, warum eine Punktwolke allein nicht
ausreicht, um ein Objekt zu drucken, und was das Mesh zusätzlich liefert.
```

````{admonition} Lösung
:class: tip
:class: dropdown
Eine Punktwolke beschreibt nur einzelne Punkte im Raum, aber keine
geschlossene Oberfläche. Ein 3D-Drucker benötigt jedoch ein wasserdichtes,
zusammenhängendes Netz von Flächen, um zu wissen, welcher Bereich des Raums
zum Objekt gehört und welcher nicht. Das Mesh liefert genau das: Es verbindet
die Punkte zu Dreiecken und erzeugt damit eine geschlossene Hülle, die den
Körper vollständig beschreibt.
````

## Warum Textur und Mattheit so wichtig sind

SfM kann nur dann Merkmalspunkte finden und zuordnen, wenn die Oberfläche
genug visuelle Informationen enthält. Daraus ergeben sich zwei praktische
Anforderungen an das Aufnahmeobjekt.

Textur: Eine strukturlose, einfarbige Fläche, zum Beispiel eine weiße Wand,
liefert dem Algorithmus kaum Merkmalspunkte. Es gibt nichts Markantes, das
von einem Foto zum nächsten wiedererkannt werden könnte. Objekte mit
ausgeprägter Textur, zum Beispiel Holzmaserung, Rost oder Gravuren, liefern dagegen
viele stabile Merkmalspunkte.

Mattheit: Glänzende Oberflächen verändern ihr Erscheinungsbild stark,
wenn sich der Aufnahmewinkel ändert. Ein Reflexionspunkt, der auf Foto 1 an
einer bestimmten Stelle sichtbar ist, erscheint auf Foto 2 an einer anderen
Stelle, weil er von der veränderten Kameraposition anders reflektiert wird.
Der Algorithmus interpretiert das fälschlicherweise als zwei verschiedene
Punkte, was zu Fehlern in der Rekonstruktion führt.

Als praktischer Workaround in der Industrie und in der Forschung wird
**Mattierungsspray** (englisch: *scanning spray*) verwendet. Es legt einen
feinen, gleichmäßigen, matten Film auf die Oberfläche, der nach dem Scan
wieder entfernt werden kann.

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir das Grundprinzip der Photogrammetrie
kennengelernt. Structure from Motion berechnet gleichzeitig die
Kamerapositionen und eine erste dünn besetzte Punktwolke. Multi-View Stereo
verfeinert das Ergebnis zu einer dicht besetzten Punktwolke, die anschließend
in ein Mesh umgewandelt wird. Texturreiche und matte Oberflächen sind
Voraussetzung für eine gute Rekonstruktion. Im nächsten Abschnitt schauen
wir uns an, wie wir selbst gute Fotos für die Photogrammetrie aufnehmen.
