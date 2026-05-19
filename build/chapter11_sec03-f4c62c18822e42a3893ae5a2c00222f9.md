---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Übungen

Die Übungen in diesem Kapitel unterscheiden sich von allen vorherigen: Es
gibt keine Berechnungen und keinen Code. Stattdessen sind es Schreibaufgaben,
die direkt auf den Projektbericht vorbereiten. Jede Aufgabe entspricht einem
Abschnitt, der im Bericht erwartet wird. Die Musterlösungen zeigen, wie ein
gut formulierter Abschnitt aussieht – nicht als Text zum Abschreiben, sondern
als Maßstab für das eigene Schreiben.

````{admonition} Übung 11.1 (✩)
:class: tip
**Den Workflow zusammenfassen**

Schreiben Sie einen zusammenhängenden Absatz (fünf bis sieben Sätze), der
den gesamten Workflow Ihres Projekts beschreibt. Der Absatz soll:

- Mit dem Objekt und der Motivation beginnen ("Untersucht wurde...").
- Die vier Hauptphasen nennen (Digitalisierung, Bereinigung, Druck,
  Simulation).
- Die verwendeten Werkzeuge benennen.
- Mit dem Ziel der Validierung abschließen.

Schreiben Sie den Absatz so, dass jemand, der den Kurs nicht kennt, den
Workflow nach dem Lesen grob verstanden hat.
````

````{admonition} Musterlösung
:class: tip
:class: dropdown
*Untersucht wurde eine Kugelbahn aus PLA-Kunststoff mit einer Länge von
95 cm und einem Neigungswinkel von ca. 18°. Ziel des Projekts war die
Digitalisierung, der 3D-Druck und die physikalische Simulation des Objekts.
Im ersten Schritt wurde das Objekt mit einer Smartphone-Kamera fotografiert
(68 Aufnahmen) und mit der Photogrammetrie-Software Meshroom zu einem
dreidimensionalen Mesh rekonstruiert. Das Mesh wurde anschließend mit
CloudCompare bereinigt: Hintergrundgeometrie wurde manuell entfernt,
Ausreißer durch einen statistischen Filter gefiltert und die Oberfläche
durch Laplacian Smoothing geglättet. Das bereinigte Mesh wurde in PrusaSlicer
in G-Code überführt und auf einem FDM-Drucker gedruckt. Auf Basis der
Wegpunkte aus CloudCompare wurde eine segmentweise Euler-Simulation in Python
und VPython implementiert, die Rollzeit und Geschwindigkeitsverlauf der Kugel
vorhersagt. Die Simulation wurde durch Stoppuhrmessungen (8 Wiederholungen)
validiert.*
````

````{admonition} Übung 11.2 (✩)
:class: tip
**Ergebnisse präzise berichten**

Betrachten Sie die folgenden vier Ergebnissätze. Jeder beschreibt dasselbe
Ergebnis – aber auf unterschiedlichem Qualitätsniveau. Ordnen Sie sie von
schwächster (1) zu stärkster (4) Formulierung und begründen Sie Ihre
Reihenfolge in je einem Satz.

**Satz A:**
"Die Abweichungsanalyse zeigte, dass die meisten Bereiche des Meshs im
grünen Bereich lagen."

**Satz B:**
"Die Cloud-to-Mesh-Distanzanalyse ergab eine mittlere Abweichung von
0.31 mm mit einer Standardabweichung von 0.18 mm. 94.7 % der Vertices
lagen innerhalb der Toleranz von ±0.5 mm."

**Satz C:**
"Die Simulation sagte eine Rollzeit von 1.43 s voraus. Gemessen wurden
im Mittel 1.51 s bei einer Standardabweichung von 0.03 s, was einer
relativen Abweichung von −5.3 % entspricht."

**Satz D:**
"Das Modell funktionierte gut und die Ergebnisse stimmten mit den
Erwartungen überein."
````

````{admonition} Lösung
:class: tip
:class: dropdown
Reihenfolge: **D < A < B ≈ C**

**D (schwächste):** Völlig ohne Zahlen, ohne Werkzeugbezug, ohne
Aussagekraft. "Gut" und "Erwartungen" sind nicht messbar.

**A:** Immerhin ein konkretes Werkzeug genannt (Abweichungsanalyse), aber
"grüner Bereich" ist keine quantitative Aussage. Keine Zahlen, keine
Einheiten.

**B und C (gleichwertig stark):** Beide nennen ein konkretes Verfahren,
konkrete Zahlenwerte mit Einheiten, eine statistische Kennzahl (Stabw., rel.
Abweichung) und eine Referenzgröße (Toleranz, Messmittelwert). Das ist das
Niveau, das ein guter Bericht durchgehend erreichen sollte.
````

````{admonition} Übung 11.3 (✩✩)
:class: tip
**Einen Methodenabschnitt schreiben**

Schreiben Sie für einen der folgenden Schritte Ihres Projekts einen
Methodenabschnitt von etwa acht bis zehn Sätzen. Ein guter
Methodenabschnitt ist so formuliert, dass eine andere Person den Schritt
anhand Ihrer Beschreibung reproduzieren könnte.

Wählen Sie einen der folgenden Schritte:

- **Option A:** Die Fotoaufnahme für Meshroom (Kapitel 2).
- **Option B:** Die Mesh-Bereinigung in CloudCompare (Kapitel 4).
- **Option C:** Die segmentweise Simulation in Python (Kapitel 10).

Ihr Text soll enthalten:
- Welches Werkzeug verwendet wurde (Name und Version, falls bekannt).
- Welche Eingabedaten verwendet wurden.
- Welche Parameter gewählt wurden und warum.
- Welche Ausgabe erzeugt wurde.
- Welche Qualitätssicherungsschritte durchgeführt wurden.
````

````{admonition} Musterlösung (Option C: segmentweise Simulation)
:class: tip
:class: dropdown
*Die Simulation der Rollbewegung wurde als segmentweiser Euler-Algorithmus
in Python 3.12 implementiert. Als Grundlage diente eine Wegpunktliste mit
neun Punkten, die manuell mit dem Werkzeug "Point Picking" in CloudCompare
2.13 entlang der Mittellinie der Führungsrille aufgenommen und als
CSV-Datei exportiert wurde. Aus den Wegpunkten wurden mit der Funktion
`bahn_aus_wegpunkten` acht Segmentlängen und lokale Neigungswinkel berechnet.
Die Masse der Kugel wurde zu m = 85 g bestimmt (gemessen mit einer
Küchenwaage, Auflösung 1 g). Für den Haftreibungskoeffizienten wurde der
Literaturwert μ_H = 0.22 für Stahl auf PLA verwendet; der
Gleitreibungskoeffizient μ_G = 0.16 wurde durch Kalibrierung an der
Messung bestimmt (Bisektionsverfahren, Konvergenzkriterium: |t_sim − t_mess|
< 0.001 s). Der Zeitschritt wurde auf dt = 0.005 s gesetzt, was bei den
vorliegenden Geschwindigkeiten einem Numerikfehler von unter 0.3 %
entspricht (geprüft durch Halbierung des Zeitschritts). Als Ausgabe wurden
Rollzeit, Endgeschwindigkeit und der vollständige Zeitverlauf von Position
und Geschwindigkeit gespeichert. Die Simulation wurde in VPython 7.6
visualisiert und auf korrekte Bewegungsrichtung und plausible
Größenordnungen geprüft.*
````

````{admonition} Übung 11.4 (✩✩)
:class: tip
**Grenzen des Modells benennen**

Jedes Modell hat Grenzen. In einem guten Bericht werden sie explizit
benannt – nicht als Entschuldigung für Abweichungen, sondern als Zeichen
kritischen Denkens.

Schreiben Sie einen Absatz (sechs bis acht Sätze) über die Grenzen
Ihres Simulationsmodells. Der Absatz soll:

- Mindestens drei konkrete Modellannahmen benennen, die vom realen
  Verhalten abweichen.
- Für jede Annahme einschätzen, in welche Richtung sie die Simulation
  verzerrt (zu schnell / zu langsam / unbekannt).
- Mindestens eine Annahme quantifizieren (wie groß ist ihr Beitrag
  zur Abweichung?).
- Einen Ausblick geben, wie das Modell verbessert werden könnte.
````

````{admonition} Musterlösung
:class: tip
:class: dropdown
*Das Simulationsmodell basiert auf drei vereinfachenden Annahmen, die zu
systematischen Abweichungen führen. Erstens wurde die Kugel als Punktmasse
behandelt, wodurch die Rotationsenergie vernachlässigt wird. Für eine
solide Vollkugel beträgt dieser Anteil 2/7 der kinetischen Gesamtenergie,
was die Beschleunigung um den Faktor 5/7 reduziert. Die Simulation
überschätzt daher die Rollgeschwindigkeit um ca. 18 % (√(7/5) ≈ 1.18)
und unterschätzt die Rollzeit um denselben Betrag. Zweitens wurde der
Reibungskoeffizient als über die gesamte Bahn konstant angenommen. In
der Realität variiert er mit der lokalen Oberflächenrauheit, der
Normalspannung und der Gleitgeschwindigkeit; die Richtung dieser
Abweichung ist schwer vorherzusagen. Drittens wurde die Bahngeometrie
durch neun Wegpunkte stückweise linear approximiert, wodurch Kurven
und Übergänge zu Knicken werden. Dies hat geringe Auswirkungen auf die
Rollzeit, aber möglicherweise sichtbare Auswirkungen auf die Trajektorie
in der Visualisierung. Eine Verbesserung des Modells könnte durch
Berücksichtigung des Trägheitsmoments (Faktor 5/7 in der Beschleunigung),
eine Kalibrierung des ortsabhängigen Reibungskoeffizienten aus Phyphox-
Daten und eine feinere Wegpunktauflösung erzielt werden.*
````

````{admonition} Übung 11.5 (✩✩✩)
:class: tip
**Peer Review: Einen Diskussionsabschnitt bewerten**

Lesen Sie den folgenden Diskussionsabschnitt aus einem fiktiven Bericht
und bewerten Sie ihn anhand von vier Kriterien. Geben Sie für jedes
Kriterium eine Note von 1 (sehr gut) bis 4 (nicht ausreichend) und
begründen Sie Ihre Bewertung in je zwei Sätzen. Formulieren Sie
anschließend einen verbesserten Abschnitt.

**Zu bewertender Text:**

> "Die Simulation hat gut funktioniert. Die Rollzeit wurde berechnet und
> mit der echten Rollzeit verglichen. Es gab eine kleine Abweichung, die
> wahrscheinlich an der Reibung liegt. Insgesamt war die Simulation
> erfolgreich und das Modell ist für praktische Zwecke geeignet."

**Bewertungskriterien:**
1. Quantitative Aussagen (werden Zahlen und Einheiten genannt?)
2. Begründungstiefe (werden Ursachen erklärt, nicht nur benannt?)
3. Kritische Reflexion (werden Grenzen des Modells anerkannt?)
4. Wissenschaftliche Sprache (präzise Fachbegriffe, kein Umgangssprachliches?)
````

````{admonition} Lösung
:class: tip
:class: dropdown
**Bewertung:**

1. **Quantitative Aussagen: 4 (nicht ausreichend).** Kein einziger Zahlenwert
   wird genannt. Weder Rollzeit, noch Abweichung, noch Reibungskoeffizient.
   "Kleine Abweichung" ist keine messbare Aussage.

2. **Begründungstiefe: 4 (nicht ausreichend).** "Liegt wahrscheinlich an der
   Reibung" ist keine Begründung. Es wird nicht erklärt, welcher
   Reibungseffekt gemeint ist, ob Haft- oder Gleitreibung, und in welche
   Richtung der Fehler zeigt.

3. **Kritische Reflexion: 3 (ausreichend).** Es wird immerhin anerkannt, dass
   eine Abweichung existiert. Aber die Formulierung "insgesamt erfolgreich"
   ohne Einschränkung lässt keine kritische Auseinandersetzung erkennen.

4. **Wissenschaftliche Sprache: 3 (ausreichend).** "Hat gut funktioniert" und
   "war erfolgreich" sind umgangssprachliche Bewertungen ohne
   Aussagekraft. Fachbegriffe wie Validierung, Euler-Methode oder MAE fehlen
   vollständig.

**Verbesserter Text:**

*Die simulierte Rollzeit von 1.43 s liegt um 5.3 % unterhalb des
Messmittelwerts von 1.51 ± 0.03 s (8 Messungen, Stoppuhr). Die Simulation
unterschätzt die Rollzeit systematisch, was auf die Vernachlässigung der
Rotationsenergie zurückzuführen ist: Da die Kugel als Punktmasse modelliert
wurde, wird der Energieanteil der Eigenrotation (2/7 der kinetischen
Gesamtenergie) nicht berücksichtigt. Der theoretische Korrekturfaktor
√(7/5) ≈ 1.18 erklärt einen systematischen Fehler von ca. 18 %, der die
tatsächlich gemessene Abweichung von 5.3 % übersteigt. Der verbleibende
Unterschied lässt sich durch die Kalibrierung des Gleitreibungskoeffizienten
erklären: Der kalibrierte Wert μ_G = 0.27 weicht vom Literaturwert 0.20 ab,
was die Bremswirkung erhöht und die simulierte Rollzeit auf 1.48 s anhebt
(Abweichung: 2.0 %). Für den vorliegenden Zweck – eine erste Auslegung
der Rollzeit mit Smartphone-Fotogrammetrie und Stoppuhrmessung – ist diese
Genauigkeit ausreichend.*
````

````{admonition} Übung 11.6 (Mini-Projekt)
:class: tip
**Den vollständigen Diskussionsteil schreiben**

Schreiben Sie den vollständigen Diskussionsteil Ihrer Projektarbeit. Der
Text soll 300 bis 500 Wörter umfassen und folgende Struktur haben:

**1. Zusammenfassung der Ergebnisse (ca. 80 Wörter)**
Welche Hauptergebnisse hat das Projekt geliefert? Nennen Sie die wichtigsten
Zahlen aus allen vier Phasen (Digitalisierung, Bereinigung, Simulation,
Validierung).

**2. Bewertung der Simulationsqualität (ca. 150 Wörter)**
Wie gut stimmt die Simulation mit der Messung überein? Benennen Sie die
relative Abweichung, das dominante Fehlerursachenpaar und quantifizieren
Sie den wichtigsten Effekt.

**3. Grenzen des Modells (ca. 100 Wörter)**
Welche drei Annahmen haben den größten Einfluss auf die Genauigkeit?
Wie würde eine Verbesserung dieser Annahmen das Modell verändern?

**4. Einordnung und Ausblick (ca. 80 Wörter)**
Ist das Modell für seinen Zweck ausreichend genau? Welcher nächste Schritt
würde die Simulation am stärksten verbessern – mehr Wegpunkte, ein
verbessertes Physikmodell oder eine präzisere Messung des
Reibungskoeffizienten?

Verwenden Sie ausschließlich Ihre eigenen Zahlenwerte aus den Übungen der
Kapitel 6, 9 und 10. Kein Zahlenwert darf erfunden oder ohne Herkunftsangabe
verwendet werden.
````
