---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 1.1 Virtual Engineering und Digitale Zwillinge

Moderne Produkte entstehen heute nicht mehr allein am Reißbrett oder in der
Werkstatt. Bevor ein Bauteil überhaupt gefertigt wird, existiert es bereits als
vollständiges digitales Modell, simuliert, getestet und optimiert. Dieses
Kapitel führt in die grundlegenden Konzepte des Virtual Engineering ein und
erklärt, warum der Digitale Zwilling zum zentralen Werkzeug der modernen
Produktentwicklung geworden ist.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können den Begriff **Virtual Engineering** erklären und von
  klassischen Entwicklungsmethoden abgrenzen.
* [ ] Sie kennen das Konzept des **Digitalen Zwillings** und können seine drei
  Kernkomponenten benennen.
* [ ] Sie können den Begriff **Digital First** erläutern und auf den
  Produktlebenszyklus anwenden.
* [ ] Sie können mindestens drei Anwendungsfelder des Virtual Engineering im
  Maschinenbau nennen.
```

## Was versteht man unter Virtual Engineering?

**Virtual Engineering** bezeichnet den Einsatz digitaler Methoden und Werkzeuge
in allen Phasen der Produktentwicklung, von der ersten Idee bis zum Ende der
Produktlebensdauer. Ziel ist es, reale Objekte, Prozesse und Systeme so
vollständig digital abzubilden, dass Entscheidungen auf Basis virtueller Modelle
getroffen werden können, bevor physische Prototypen gebaut oder
Produktionsanlagen eingerichtet werden.

Der Begriff umfasst ein breites Spektrum an Technologien und Methoden, darunter
Simulation (FEM, CFD, Mehrkörpersimulation), 3D-Scanning und Reverse
Engineering, virtuelle Prototypen und Digitale Zwillinge sowie KI-gestützte
Optimierung und generatives Design.

Im Gegensatz zur klassischen Produktentwicklung, bei der physische Prototypen
teuer und zeitaufwendig gebaut und getestet werden, erlaubt Virtual Engineering
eine frühe Fehlererkennung und iterative Verbesserung im digitalen Raum.
Fehler, die im digitalen Modell entdeckt werden, kosten einen Bruchteil dessen,
was eine Korrektur am physischen Bauteil kosten würde. In Kapitel 12 werden
wir sehen, wie wir genau diesen Gedanken auf unsere Kugelbahn anwenden und den
gesamten Entwicklungsweg vom Foto bis zur Simulation als einen einzigen
digitalen Workflow verstehen.

## Was ist ein Digitaler Zwilling?

Stellen wir uns vor, eine Gasturbine in einem Kraftwerk läuft rund um die Uhr.
Irgendwann verschleißen die Schaufeln, die Effizienz sinkt. Um einen Ausfall zu
vermeiden, müsste man die Turbine regelmäßig abschalten und prüfen. Das ist
teuer und zeitaufwendig. *Was wäre, wenn wir die Turbine jederzeit im Blick
hätten, ohne sie anzuhalten?*

Genau das ermöglicht ein Digitaler Zwilling. Ein **Digitaler Zwilling**
(englisch: *Digital Twin*) ist eine digitale Repräsentation eines physischen
Objekts, Prozesses oder Systems. Der Begriff wurde maßgeblich von Michael
Grieves geprägt und hat sich in der Industrie als Schlüsseltechnologie
etabliert.

Ein vollständiger Digitaler Zwilling besteht aus drei Kernkomponenten:

1. Das physische Objekt: das reale Bauteil oder System in der realen Welt
2. Das digitale Modell: die virtuelle Repräsentation mit Geometrie,
   Materialeigenschaften und Verhaltensbeschreibung
3. Die Datenverbindung: der bidirektionale Datenaustausch zwischen
   physischem Objekt und digitalem Modell

```{admonition} Mini-Übung
:class: tip
Überlegen Sie: Welche der drei Kernkomponenten eines Digitalen Zwillings ist
Ihrer Meinung nach am schwierigsten umzusetzen, und warum? Notieren Sie Ihre
Überlegung in zwei bis drei Sätzen.
```

````{admonition} Lösung
:class: tip
:class: dropdown
Es gibt keine eindeutig richtige Antwort. Am häufigsten wird die
Datenverbindung als schwierigste Komponente genannt, weil sie eine
funktionierende Sensorik am physischen Objekt, eine zuverlässige
Datenübertragung und eine kontinuierliche Aktualisierung des digitalen Modells
in Echtzeit erfordert. Ein digitales Modell und ein physisches Objekt existieren
verhältnismäßig einfach nebeneinander. Erst die bidirektionale, lebendige
Verbindung zwischen beiden macht aus einem CAD-Modell einen echten Digitalen
Zwilling. Andere Argumente, etwa dass das digitale Modell am schwierigsten ist,
weil es alle physikalischen Eigenschaften korrekt abbilden muss, sind ebenfalls
gut begründbar.
````

Die Verbindung zwischen realem Objekt und digitalem Modell ist dabei
entscheidend. Ein einfaches CAD-Modell ist noch kein Digitaler Zwilling. Erst
wenn das Modell mit realen Messdaten gespeist wird und Rückschlüsse auf das
physische Objekt erlaubt, spricht man von einem echten Digitalen Zwilling.

In der Praxis unterscheidet man oft zwischen dem **Digital Twin Prototype
(DTP)**, bei dem das digitale Modell existiert, bevor das physische Objekt
gebaut wird, und der **Digital Twin Instance (DTI)**, bei der das Modell ein
konkretes, bereits existierendes Objekt über seinen gesamten Lebenszyklus
begleitet.

## Wie verändert Digital First den Produktlebenszyklus?

Das Konzept **Digital First** beschreibt einen Ansatz, bei dem das digitale
Modell am Anfang der Produktentwicklung steht, nicht am Ende. Statt ein
physisches Objekt zu bauen und anschließend zu digitalisieren, wird das Produkt
zuerst vollständig digital entwickelt, simuliert und optimiert.

Der klassische Produktlebenszyklus verlief vereinfacht wie folgt:

```code
Idee → Skizze → physischer Prototyp → Test → Korrektur → Serienproduktion
```

Im Digital-First-Ansatz sieht der Ablauf anders aus:

```code
Idee → digitales Modell → Simulation → Optimierung → (physischer Prototyp) → Serienproduktion
```

Der physische Prototyp wird damit seltener und später gebaut. In manchen Fällen
entfällt er ganz. Das spart Zeit, Material und Kosten und ermöglicht eine
nachhaltigere Produktentwicklung.

```{admonition} Mini-Übung
:class: tip
Recherchieren Sie ein konkretes Industriebeispiel, in dem ein Unternehmen einen
Digitalen Zwilling einsetzt. Beschreiben Sie in drei bis vier Sätzen:

- Was ist das physische Objekt?
- Was enthält das digitale Modell?
- Welchen Nutzen bringt der Digitale Zwilling in diesem Fall?
```

````{admonition} Lösung
:class: tip
:class: dropdown
Beispiel: Siemens und die digitale Gasturbine

Das physische Objekt ist eine Gasturbine, die in einem Kraftwerk Strom erzeugt.
Das digitale Modell enthält die vollständige Geometrie der Turbine, ihre
Materialeigenschaften und ein thermodynamisches Simulationsmodell, das das
Verhalten unter verschiedenen Betriebsbedingungen vorhersagt. Die Datenverbindung
wird über Sensoren hergestellt, die kontinuierlich Temperatur, Druck und
Schwingungen messen und an das digitale Modell übermitteln. Der Nutzen besteht
darin, dass Wartungsintervalle vorausschauend geplant werden können und
ungeplante Ausfälle vermieden werden, was die Betriebskosten erheblich senkt.

Andere Beispiele sind ebenfalls korrekt, zum Beispiel BMW (Fahrzeugentwicklung),
Airbus (Flugzeugwartung) oder Schindler (Aufzugsüberwachung).
````

## Wo wird Virtual Engineering eingesetzt?

Virtual Engineering ist heute in nahezu allen Bereichen des Maschinenbaus
präsent. In der Produktentwicklung und Konstruktion ermöglichen virtuelle
Prototypen es, Entwürfe frühzeitig auf Festigkeit, Schwingungsverhalten oder
Strömungseigenschaften zu prüfen. In der Fertigung erlauben Digitale Zwillinge
von Produktionsanlagen die Simulation ganzer Fertigungslinien, bevor diese
physisch aufgebaut werden. In der Qualitätssicherung können gescannte Bauteile
mit ihren CAD-Referenzmodellen verglichen und Fertigungsabweichungen exakt
quantifiziert werden, ein Thema, das wir in Kapitel 5 mit CloudCompare selbst
durchführen werden. Im Betrieb schließlich können Digitale Zwillinge genutzt
werden, um Ausfälle vorherzusagen und Wartungsintervalle zu optimieren, was
unter dem Begriff *Predictive Maintenance* bekannt ist.

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir die grundlegenden Konzepte des Virtual Engineering
kennengelernt. Virtual Engineering umfasst alle digitalen Methoden, die in der
Produktentwicklung eingesetzt werden. Der Digitale Zwilling verbindet das
physische Objekt mit seinem digitalen Abbild über eine bidirektionale
Datenverbindung. Der Digital-First-Ansatz stellt das digitale Modell an den
Anfang des Produktlebenszyklus. Im nächsten Abschnitt lernen wir das
Leitprojekt dieser Vorlesung kennen: die Digitalisierung, den 3D-Druck und die
Simulation einer Kugelbahn, an der wir alle diese Konzepte Schritt für Schritt
in die Praxis umsetzen werden.
