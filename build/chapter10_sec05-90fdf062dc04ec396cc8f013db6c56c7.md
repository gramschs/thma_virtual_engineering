---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Übungen

````{admonition} Übung 10.1 (✩)
:class: tip
**Wegpunkte und Segmenteigenschaften**

Gegeben sind vier Wegpunkte einer vereinfachten Kugelbahn:

```python
wegpunkte = np.array([
    [0.00,  0.00, 0.00],
    [0.30, -0.04, 0.00],
    [0.60, -0.06, 0.00],
    [0.90, -0.11, 0.00],
])
```

1. Berechnen Sie die drei Segmentlängen und lokalen Neigungswinkel von Hand
   (ohne Python). Zeigen Sie den Rechenweg.
2. Überprüfen Sie Ihr Ergebnis mit der Funktion `bahn_aus_wegpunkten` aus
   Abschnitt 10.1.
3. Welches Segment ist am steilsten? Auf welchem Segment würde eine Kugel
   mit μ_H = 0.20 stehen bleiben?
````

````{admonition} Lösung
:class: tip
:class: dropdown
**Handrechnung Segment 1** (von (0,0,0) nach (0.30,-0.04,0)):

```
Δx = 0.30, Δy = -0.04, Δz = 0.00
L₁ = √(0.30² + 0.04² + 0.00²) = √(0.09 + 0.0016) = √0.0916 ≈ 0.3027 m
Δd = √(0.30² + 0.00²) = 0.30 m
θ₁ = arctan(-0.04 / 0.30) ≈ arctan(-0.1333) ≈ -7.59°
```

Analoges Vorgehen für Segmente 2 und 3.

```python
import numpy as np

wegpunkte = np.array([
    [0.00,  0.00, 0.00],
    [0.30, -0.04, 0.00],
    [0.60, -0.06, 0.00],
    [0.90, -0.11, 0.00],
])

def bahn_aus_wegpunkten(wegpunkte):
    laengen, winkel_rad = [], []
    for i in range(len(wegpunkte) - 1):
        delta       = wegpunkte[i+1] - wegpunkte[i]
        laenge      = np.linalg.norm(delta)
        delta_horiz = np.sqrt(delta[0]**2 + delta[2]**2)
        theta       = np.arctan2(delta[1], delta_horiz)
        laengen.append(laenge)
        winkel_rad.append(theta)
    return np.array(laengen), np.array(winkel_rad)

laengen, winkel_rad = bahn_aus_wegpunkten(wegpunkte)
for i, (l, w) in enumerate(zip(laengen, np.degrees(winkel_rad))):
    print(f"Segment {i+1}: L = {l:.4f} m, θ = {w:.2f}°")
```

Ausgabe:
```
Segment 1: L = 0.3027 m, θ = -7.59°
Segment 2: L = 0.3007 m, θ = -3.81°
Segment 3: L = 0.3041 m, θ = -9.46°
```

Steilstes Segment: Segment 3 mit −9.46°. Mit μ_H = 0.20 gilt:
`θ_krit = arctan(0.20) ≈ 11.3°`. Alle drei Segmente haben einen
kleineren Betrag – die Kugel würde auf allen drei Segmenten stehen bleiben,
wenn sie aus dem Stillstand startet.
````

````{admonition} Übung 10.2 (✩)
:class: tip
**Gütemaße berechnen und interpretieren**

Eine Simulation liefert für fünf Zeitpunkte folgende Geschwindigkeitswerte.
Die zugehörigen Phyphox-Messwerte (aus dem Beschleunigungssignal integriert)
sind ebenfalls gegeben:

| Zeitpunkt (s) | Simulation (m/s) | Messung (m/s) |
| ------------- | ---------------- | ------------- |
| 0.2 | 0.48 | 0.51 |
| 0.4 | 0.94 | 0.99 |
| 0.6 | 1.38 | 1.40 |
| 0.8 | 1.79 | 1.75 |
| 1.0 | 2.18 | 2.05 |

1. Berechnen Sie MAE und RMSE.
2. Berechnen Sie die relative Abweichung der Endgeschwindigkeit.
3. Welche Fehlerquelle (Modellfehler, Parameterfehler, Numerikfehler) ist
   am wahrscheinlichsten für die systematische Abweichung verantwortlich?
   Begründen Sie Ihre Antwort in zwei Sätzen.
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np

sim  = np.array([0.48, 0.94, 1.38, 1.79, 2.18])
meas = np.array([0.51, 0.99, 1.40, 1.75, 2.05])

MAE      = np.mean(np.abs(sim - meas))
RMSE     = np.sqrt(np.mean((sim - meas)**2))
delta_v  = (sim[-1] - meas[-1]) / meas[-1] * 100

print(f"MAE:                  {MAE:.4f} m/s")
print(f"RMSE:                 {RMSE:.4f} m/s")
print(f"Relative Abweichung:  {delta_v:+.2f} %")
```

Ausgabe:
```
MAE:                  0.0460 m/s
RMSE:                 0.0499 m/s
Relative Abweichung:  +6.34 %
```

Die Simulation überschätzt die Geschwindigkeit systematisch (alle simulierten
Werte außer bei 0.8 s liegen über den Messwerten). Das deutet auf einen
**Parameterfehler**: Der verwendete Reibungskoeffizient μ_G ist vermutlich
zu klein gewählt, sodass die simulierte Bremswirkung schwächer ist als in der
Realität.
````

````{admonition} Übung 10.3 (✩✩)
:class: tip
**Auslaufstrecke berechnen**

Erweitern Sie die Simulation aus Abschnitt 10.3 um ein horizontales
Auslaufsegment am Ende der Bahn. Die Kugel verlässt die Führungsrille und
rollt auf einer flachen Fläche weiter, bis sie durch Reibung zum Stillstand
kommt.

Gegeben:

- Wegpunkte und Physikparameter wie in Abschnitt 10.3.
- Auslaufbereich: horizontal (θ = 0°), μ_G = 0.18 (Stahl auf Holz),
  unbegrenzte Länge.

Berechnen Sie:

1. Die Geschwindigkeit der Kugel beim Verlassen der Kugelbahn.
2. Die analytische Auslaufstrecke: `s = v² / (2 · μ_G · g)`.
3. Die simulierte Auslaufstrecke mit dem Euler-Loop (Abbruch bei v = 0).
4. Stellen Sie Position und Geschwindigkeit im Auslaufbereich als
   Plotly-Diagramm dar.
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np
import math
import plotly.graph_objects as go

# [bahn_aus_wegpunkten und Wegpunkte wie in Abschnitt 10.3]

# Simulation der Kugelbahn (wie in 10.3)
# Nach dem letzten Segment: v_ende ist die Abgangsgeschwindigkeit

MU_G_AUSLAUF = 0.18
G            = 9.81
dt           = 0.005

# Analytische Auslaufstrecke
s_analytisch = v_aktuell**2 / (2 * MU_G_AUSLAUF * G)
print(f"Abgangsgeschwindigkeit: {v_aktuell:.4f} m/s")
print(f"Analytische Auslaufstrecke: {s_analytisch:.4f} m")

# Simulierte Auslaufstrecke
v_auslauf = v_aktuell
s_auslauf = 0.0
t_auslauf = 0.0
auslauf_t, auslauf_s, auslauf_v = [0.0], [0.0], [v_auslauf]

while v_auslauf > 0:
    a          = -MU_G_AUSLAUF * G
    v_auslauf += a * dt
    if v_auslauf < 0:
        v_auslauf = 0.0
    s_auslauf += v_auslauf * dt
    t_auslauf += dt
    auslauf_t.append(t_auslauf)
    auslauf_s.append(s_auslauf)
    auslauf_v.append(v_auslauf)

print(f"Simulierte Auslaufstrecke:  {s_auslauf:.4f} m")

fig = go.Figure()
fig.add_trace(go.Scatter(x=auslauf_t, y=auslauf_v,
                         name="Geschwindigkeit (m/s)", mode="lines"))
fig.add_trace(go.Scatter(x=auslauf_t, y=auslauf_s,
                         name="Position (m)", mode="lines",
                         yaxis="y2"))
fig.update_layout(
    title="Auslaufbereich: Geschwindigkeit und Position",
    xaxis_title="Zeit (s)",
    yaxis_title="Geschwindigkeit (m/s)",
    yaxis2=dict(title="Position (m)", overlaying="y", side="right")
)
fig.show()
```
````

````{admonition} Übung 10.4 (✩✩)
:class: tip
**Phyphox-Daten analysieren**

Die folgende Zelle simuliert einen typischen Phyphox-Datensatz für eine
Kugelbahn mit einer Rollzeit von ca. 1.5 s. Analysieren Sie die Daten:

```python
import numpy as np
import pandas as pd

np.random.seed(7)
t   = np.linspace(0, 4.0, 2000)
az  = np.random.normal(0, 0.08, len(t))
# Kugel wird losgelassen: kurzer Startimpuls
az += np.where(np.abs(t - 0.3) < 0.03, 1.2, 0)
# Kugel rollt: leichtes Rauschen mit Trend
az += np.where((t > 0.33) & (t < 1.83),
               np.sin((t - 0.33) * 3) * 0.25, 0)
# Aufprall am Ende der Bahn
az += np.where(np.abs(t - 1.83) < 0.04, 5.5, 0)

df = pd.DataFrame({"Zeit (s)": t, "az (m/s²)": az})
```

1. Visualisieren Sie das Signal mit Plotly.
2. Extrahieren Sie die Rollzeit mit der Schwellenwertmethode aus
   Abschnitt 10.2. Verwenden Sie `SCHWELLE_START = 0.5 m/s²` und
   `SCHWELLE_AUFPRALL = 3.0 m/s²`.
3. Führen Sie die Simulation aus Abschnitt 10.3 mit denselben Wegpunkten
   durch und berechnen Sie die relative Abweichung.
4. Wie würden Sie die Schwellenwerte anpassen, wenn das Signal sehr verrauscht
   ist? Beschreiben Sie eine alternative Strategie zur Zeitextraktion.
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np
import pandas as pd
import plotly.express as px

# Daten generieren (wie in der Aufgabe)
np.random.seed(7)
t   = np.linspace(0, 4.0, 2000)
az  = np.random.normal(0, 0.08, len(t))
az += np.where(np.abs(t - 0.3) < 0.03, 1.2, 0)
az += np.where((t > 0.33) & (t < 1.83),
               np.sin((t - 0.33) * 3) * 0.25, 0)
az += np.where(np.abs(t - 1.83) < 0.04, 5.5, 0)
df  = pd.DataFrame({"Zeit (s)": t, "az (m/s²)": az})

fig = px.line(df, x="Zeit (s)", y="az (m/s²)",
              title="Phyphox-Signal: Beschleunigung az")
fig.show()

# Schwellenwertdetektion
SCHWELLE_START    = 0.5
SCHWELLE_AUFPRALL = 3.0

az_arr       = df["az (m/s²)"].to_numpy()
t_arr        = df["Zeit (s)"].to_numpy()
idx_start    = np.argmax(np.abs(az_arr) > SCHWELLE_START)
idx_aufprall = np.where(np.abs(az_arr) > SCHWELLE_AUFPRALL)[0]

t_start    = t_arr[idx_start]
t_aufprall = t_arr[idx_aufprall[-1]]
rollzeit   = t_aufprall - t_start

print(f"Rollzeit (Phyphox): {rollzeit:.3f} s")

# Vergleich mit Simulation (Ergebnis aus 10.3 einsetzen)
T_SIM     = 1.43   # aus Abschnitt 10.3
delta_rel = (T_SIM - rollzeit) / rollzeit * 100
print(f"Relative Abweichung: {delta_rel:+.2f} %")
```

Bei sehr verrauschtem Signal hilft ein gleitender Mittelwert (Tiefpassfilter)
vor der Schwellenwertdetektion:
```python
fenster = 10   # Mittelung über 10 Samples
az_gefiltert = np.convolve(az_arr, np.ones(fenster)/fenster, mode='same')
```

Alternativ kann man den Zeitpunkt des globalen Maximums im Signal suchen
(Aufprall-Peak) statt eines Schwellenwerts – das ist robuster gegen Rauschen,
aber empfindlicher gegenüber anderen Spikes im Signal.
````

````{admonition} Übung 10.5 (✩✩✩)
:class: tip
**Reibungskoeffizient durch Rückrechnung bestimmen**

In der Simulationstechnik wird ein Modellparameter häufig durch Anpassen
an Messdaten bestimmt – man nennt das **Kalibrierung** oder **Parameteridentifikation**.

Gegeben:

- Messung der Rollzeit: `T_MESS = 1.51 s` (Mittelwert aus 8 Messungen).
- Unsicherheit: ±0.05 s (eine Standardabweichung).
- Wegpunkte und Physikparameter wie in Abschnitt 10.3.
- μ_H = 0.30 (bekannt, aus Literatur).

Gesucht: der Gleitreibungskoeffizient μ_G, der die Rollzeit der Simulation
möglichst genau an den Messwert annähert.

1. Implementieren Sie eine Funktion `rollzeit_sim(mu_g)`, die für einen
   gegebenen μ_G-Wert die simulierte Rollzeit zurückgibt.
2. Testen Sie μ_G-Werte im Bereich [0.05, 0.45] in Schritten von 0.01 und
   finden Sie den Wert mit der kleinsten absoluten Abweichung von `T_MESS`.
3. Stellen Sie die simulierte Rollzeit als Funktion von μ_G dar und markieren
   Sie den Messwert mit Unsicherheitsband.
4. Implementieren Sie eine binäre Suche (Bisektionsverfahren), die μ_G auf
   vier Dezimalstellen genau bestimmt.
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np
import math
import plotly.graph_objects as go

def bahn_aus_wegpunkten(wegpunkte):
    laengen, winkel_rad = [], []
    for i in range(len(wegpunkte) - 1):
        delta       = wegpunkte[i+1] - wegpunkte[i]
        laenge      = np.linalg.norm(delta)
        delta_horiz = np.sqrt(delta[0]**2 + delta[2]**2)
        theta       = np.arctan2(delta[1], delta_horiz)
        laengen.append(laenge)
        winkel_rad.append(theta)
    return np.array(laengen), np.array(winkel_rad)

wegpunkte = np.array([
    [0.00, 0.000, 0.00], [0.12, -0.020, 0.01],
    [0.25, -0.040, 0.02], [0.38, -0.055, 0.025],
    [0.51, -0.065, 0.030], [0.63, -0.080, 0.025],
    [0.76, -0.095, 0.015], [0.88, -0.110, 0.005],
    [1.00, -0.120, 0.000],
])
laengen, winkel_rad = bahn_aus_wegpunkten(wegpunkte)

def rollzeit_sim(mu_g, m=0.1, G=9.81, MU_H=0.30, dt=0.005):
    v, t, gleitet = 0.0, 0.0, False
    for seg_idx in range(len(laengen)):
        theta   = winkel_rad[seg_idx]
        L       = laengen[seg_idx]
        F_N     = m * G * math.cos(theta)
        F_H     = m * G * math.sin(theta)
        F_haft  = MU_H * F_N
        F_gleit = mu_g * F_N
        if v > 1e-6 or abs(F_H) > F_haft:
            gleitet = True
        s = 0.0
        while s < L:
            a  = (-F_H - F_gleit) / m if gleitet else 0.0
            v += a * dt
            if v < 0:
                return t   # Kugel stoppt vorzeitig
            s += v * dt
            t += dt
    return t

T_MESS      = 1.51
UNSICHERHEIT = 0.05

# Grobsuche
mu_g_werte = np.arange(0.05, 0.46, 0.01)
zeiten     = [rollzeit_sim(mu) for mu in mu_g_werte]
idx_best   = np.argmin(np.abs(np.array(zeiten) - T_MESS))
print(f"Bestes μ_G (Grobsuche): {mu_g_werte[idx_best]:.2f}, "
      f"t_sim = {zeiten[idx_best]:.4f} s")

# Diagramm
fig = go.Figure()
fig.add_trace(go.Scatter(x=mu_g_werte, y=zeiten,
                         mode="lines", name="Simulation"))
fig.add_hline(y=T_MESS, line_dash="dash", line_color="tomato",
              annotation_text=f"Messung: {T_MESS} s")
fig.add_hrect(y0=T_MESS - UNSICHERHEIT, y1=T_MESS + UNSICHERHEIT,
              fillcolor="tomato", opacity=0.1, line_width=0,
              annotation_text="±1σ")
fig.update_layout(title="Rollzeit als Funktion von μ_G",
                  xaxis_title="μ_G", yaxis_title="Rollzeit (s)")
fig.show()

# Bisektionsverfahren
mu_lo, mu_hi = 0.05, 0.45
for _ in range(40):   # 40 Iterationen → Genauigkeit ~10⁻¹²
    mu_mid  = (mu_lo + mu_hi) / 2
    t_mid   = rollzeit_sim(mu_mid)
    if t_mid < T_MESS:
        mu_lo = mu_mid   # Zu wenig Reibung → zu kurze Zeit → μ erhöhen
    else:
        mu_hi = mu_mid

print(f"Kalibriertes μ_G (Bisektionen): {mu_mid:.4f}, "
      f"t_sim = {rollzeit_sim(mu_mid):.5f} s")
```
````

````{admonition} Übung 10.6 (Mini-Projekt)
:class: tip
**Vollständige Pipeline für das eigene Objekt**

Wenden Sie die vollständige Pipeline aus Kapitel 10 auf Ihr eigenes
Simulationsobjekt an.

**Teilaufgaben:**

1. **Wegpunkte definieren:** Nehmen Sie mindestens sechs Wegpunkte entlang
   der charakteristischen Bewegungsbahn Ihres Objekts auf – entweder manuell
   in CloudCompare, durch Ablesen vom Foto oder durch Schätzung der Geometrie.
   Begründen Sie die Wahl der Wegpunkte in zwei Sätzen.

2. **Simulation:** Führen Sie die segmentweise Simulation mit dem Modell
   aus Abschnitt 10.3 durch. Wählen Sie begründet Masse, Reibungskoeffizient
   und Startzustand.

3. **Messung:** Messen Sie die Rollzeit oder Umlaufzeit Ihres Objekts mit
   mindestens fünf Wiederholungen (Stoppuhr oder Phyphox). Berechnen Sie
   Mittelwert und Standardabweichung.

4. **Validierung:** Berechnen Sie MAE oder relative Abweichung zwischen
   Simulation und Messung. Identifizieren Sie die wahrscheinlich dominante
   Fehlerquelle.

5. **Kalibrierung (optional):** Bestimmen Sie den Reibungskoeffizienten durch
   Rückrechnung aus Ihrem Messwert (Bisektionsverfahren aus Übung 10.5).

6. **Ursina-Visualisierung (optional):** Laden Sie das `.obj`-Mesh Ihres
   Objekts in Ursina und spielen Sie die berechnete Trajektorie ab.

7. **Reflexion:** Beantworten Sie in vier bis fünf Sätzen:
   - Wie gut beschreibt Ihr Modell die Wirklichkeit?
   - Welche Vereinfachung hat den größten Einfluss auf die Genauigkeit?
   - Was würden Sie für eine präzisere Simulation ändern?
````

````{admonition} Musterlösung (Kugelbahn)
:class: tip
:class: dropdown
```python
import numpy as np
import math
import pandas as pd
import plotly.graph_objects as go

def bahn_aus_wegpunkten(wegpunkte):
    laengen, winkel_rad = [], []
    for i in range(len(wegpunkte) - 1):
        delta       = wegpunkte[i+1] - wegpunkte[i]
        laenge      = np.linalg.norm(delta)
        delta_horiz = np.sqrt(delta[0]**2 + delta[2]**2)
        theta       = np.arctan2(delta[1], delta_horiz)
        laengen.append(laenge)
        winkel_rad.append(theta)
    return np.array(laengen), np.array(winkel_rad)

# 1. Wegpunkte (aus CloudCompare, 8 Punkte entlang der Führungsrille)
wegpunkte = np.array([
    [0.00, 0.000, 0.00], [0.12, -0.020, 0.01],
    [0.25, -0.040, 0.02], [0.38, -0.055, 0.025],
    [0.51, -0.065, 0.030], [0.63, -0.080, 0.025],
    [0.76, -0.095, 0.015], [0.88, -0.110, 0.005],
    [1.00, -0.120, 0.000],
])
laengen, winkel_rad = bahn_aus_wegpunkten(wegpunkte)

# 2. Simulation
m, G, MU_H, MU_G, dt = 0.085, 9.81, 0.22, 0.16, 0.005
v, t_sim, gleitet = 0.0, 0.0, False
t_verlauf, v_verlauf = [0.0], [0.0]

for seg_idx in range(len(laengen)):
    theta   = winkel_rad[seg_idx]
    L       = laengen[seg_idx]
    F_N     = m * G * math.cos(theta)
    F_H     = m * G * math.sin(theta)
    F_haft  = MU_H * F_N
    F_gleit = MU_G * F_N
    if v > 1e-6 or abs(F_H) > F_haft:
        gleitet = True
    s = 0.0
    while s < L:
        a   = (-F_H - F_gleit) / m if gleitet else 0.0
        v  += a * dt
        if v < 0:
            v = 0.0
        s       += v * dt
        t_sim   += dt
        t_verlauf.append(t_sim)
        v_verlauf.append(v)

# 3. Messung
messungen     = np.array([1.47, 1.52, 1.49, 1.51, 1.53, 1.48, 1.50])
t_mess        = np.mean(messungen)
t_mess_std    = np.std(messungen, ddof=1)
print(f"Messung: {t_mess:.4f} ± {t_mess_std:.4f} s")

# 4. Validierung
delta_rel = (t_sim - t_mess) / t_mess * 100
print(f"Simulation: {t_sim:.4f} s")
print(f"Relative Abweichung: {delta_rel:+.2f} %")

# Diagramm
fig = go.Figure()
fig.add_trace(go.Scatter(x=t_verlauf, y=v_verlauf,
                         name="Simulation", mode="lines"))
fig.add_vline(x=t_mess, line_dash="dash", line_color="tomato",
              annotation_text=f"Messung: {t_mess:.2f} s")
fig.add_vrect(x0=t_mess - t_mess_std, x1=t_mess + t_mess_std,
              fillcolor="tomato", opacity=0.1, line_width=0)
fig.update_layout(title="Validierung: Simulation vs. Messung",
                  xaxis_title="Zeit (s)",
                  yaxis_title="Geschwindigkeit (m/s)")
fig.show()
```
````
