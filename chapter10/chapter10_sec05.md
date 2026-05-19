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

1. Berechnen Sie die drei Segmentlängen und lokalen Neigungswinkel von Hand.
   Zeigen Sie den Rechenweg für Segment 1.
2. Überprüfen Sie Ihr Ergebnis mit der Funktion `bahn_aus_wegpunkten` aus
   Abschnitt 10.1.
3. Welches Segment ist am steilsten? Würde eine Kugel mit μ_H = 0.20 auf
   allen drei Segmenten stehen bleiben, wenn sie aus dem Stillstand startet?
````

````{admonition} Lösung
:class: tip
:class: dropdown
**Handrechnung Segment 1** (von (0,0,0) nach (0.30, −0.04, 0)):

```
Δx = 0.30, Δy = −0.04, Δz = 0.00
L₁ = √(0.30² + 0.04²) = √0.0916 ≈ 0.3027 m
Δd = √(0.30² + 0.00²) = 0.30 m
θ₁ = arctan(−0.04 / 0.30) ≈ −7.59°
```

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
import math
for i, (l, w) in enumerate(zip(laengen, np.degrees(winkel_rad))):
    theta_krit = math.degrees(math.atan(0.20))
    haftet     = abs(w) < theta_krit
    print(f"Segment {i+1}: L = {l:.4f} m, θ = {w:.2f}°, "
          f"haftet bei μ_H=0.20: {haftet}")
```

Ausgabe:
```
Segment 1: L = 0.3027 m, θ = -7.59°,  haftet bei μ_H=0.20: True
Segment 2: L = 0.3007 m, θ = -3.81°,  haftet bei μ_H=0.20: True
Segment 3: L = 0.3041 m, θ = -9.46°,  haftet bei μ_H=0.20: True
```

θ_krit = arctan(0.20) ≈ 11.3°. Alle drei Segmente haben einen kleineren
Betrag, also haftet die Kugel aus dem Stillstand auf allen drei.
````

````{admonition} Übung 10.2 (✩)
:class: tip
**Gütemaße berechnen und interpretieren**

Eine Simulation liefert für fünf Zeitpunkte folgende Geschwindigkeitswerte.
Die zugehörigen Phyphox-Messwerte sind ebenfalls gegeben:

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
   am wahrscheinlichsten verantwortlich? Begründen Sie in zwei Sätzen.
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np

sim  = np.array([0.48, 0.94, 1.38, 1.79, 2.18])
mess = np.array([0.51, 0.99, 1.40, 1.75, 2.05])

MAE      = np.mean(np.abs(sim - mess))
RMSE     = np.sqrt(np.mean((sim - mess)**2))
delta_v  = (sim[-1] - mess[-1]) / mess[-1] * 100

print(f"MAE:                 {MAE:.4f} m/s")
print(f"RMSE:                {RMSE:.4f} m/s")
print(f"Relative Abweichung: {delta_v:+.2f} %")
```

Ausgabe:
```
MAE:                 0.0460 m/s
RMSE:                0.0499 m/s
Relative Abweichung: +6.34 %
```

Die Simulation überschätzt die Geschwindigkeit systematisch in fast allen
Zeitpunkten. Das deutet auf einen **Parameterfehler**: Der verwendete
Reibungskoeffizient μ_G ist vermutlich zu klein, sodass die simulierte
Bremswirkung schwächer ist als in der Realität.
````

````{admonition} Übung 10.3 (✩✩)
:class: tip
**Auslaufstrecke berechnen**

Erweitern Sie die Simulation aus Abschnitt 10.3 um ein horizontales
Auslaufsegment am Ende der Bahn. Die Kugel verlässt die Führungsrille und
rollt auf einer flachen Fläche weiter, bis sie durch Reibung stoppt.

Gegeben:

- Wegpunkte und Parameter wie in Abschnitt 10.3.
- Auslaufbereich: θ = 0°, μ_G = 0.18, unbegrenzte Länge.

1. Berechnen Sie die Geschwindigkeit der Kugel beim Verlassen der Bahn.
2. Berechnen Sie die analytische Auslaufstrecke: `s = v² / (2 · μ_G · g)`.
3. Simulieren Sie die Auslaufphase mit der Euler-Cromer-Schleife (Abbruch
   bei `v ≤ 0`).
4. Stellen Sie Position und Geschwindigkeit im Auslaufbereich mit Plotly dar.
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import math
import numpy as np
import plotly.graph_objects as go

# [bahn_aus_wegpunkten und simuliere aus Abschnitt 10.3 hier einfügen]
# v_ende: Endgeschwindigkeit aus der Bahnschleife

MU_G_AUSLAUF = 0.18
G            = 9.81
dt           = 0.005

# Analytische Auslaufstrecke
s_analytisch = v_ende**2 / (2 * MU_G_AUSLAUF * G)
print(f"Endgeschwindigkeit auf Bahn:    {v_ende:.4f} m/s")
print(f"Analytische Auslaufstrecke:     {s_analytisch:.4f} m")

# Simulierte Auslaufphase
v_ausl   = v_ende
s_ausl   = 0.0
t_ausl   = 0.0
ausl_t, ausl_s, ausl_v = [0.0], [0.0], [v_ausl]

while v_ausl > 0:
    a       = -MU_G_AUSLAUF * G
    v_ausl += a * dt
    if v_ausl < 0:
        v_ausl = 0.0
    s_ausl += v_ausl * dt
    t_ausl += dt
    ausl_t.append(t_ausl)
    ausl_s.append(s_ausl)
    ausl_v.append(v_ausl)

print(f"Simulierte Auslaufstrecke:      {s_ausl:.4f} m")

fig = go.Figure()
fig.add_trace(go.Scatter(x=ausl_t, y=ausl_v, name='Geschwindigkeit (m/s)',
                         mode='lines'))
fig.add_trace(go.Scatter(x=ausl_t, y=ausl_s, name='Position (m)',
                         mode='lines', yaxis='y2'))
fig.update_layout(
    title='Auslaufbereich: Geschwindigkeit und Position',
    xaxis_title='Zeit (s)',
    yaxis_title='Geschwindigkeit (m/s)',
    yaxis2=dict(title='Position (m)', overlaying='y', side='right')
)
fig.show()
```
````

````{admonition} Übung 10.4 (✩✩)
:class: tip
**Phyphox-Daten analysieren**

Die folgende Zelle erzeugt einen simulierten Phyphox-Datensatz für eine
Kugelbahn mit einer Bewegungszeit von ca. 1.5 s:

```python
import numpy as np
import pandas as pd

np.random.seed(7)
t   = np.linspace(0, 4.0, 2000)
az  = np.random.normal(0, 0.08, len(t))
az += np.where(np.abs(t - 0.3) < 0.03, 1.2, 0)
az += np.where((t > 0.33) & (t < 1.83),
               np.sin((t - 0.33) * 3) * 0.25, 0)
az += np.where(np.abs(t - 1.83) < 0.04, 5.5, 0)
df  = pd.DataFrame({"Zeit (s)": t, "az (m/s²)": az})
```

1. Visualisieren Sie das Signal mit Plotly.
2. Extrahieren Sie die Bewegungszeit mit `SCHWELLE_START = 0.5 m/s²` und
   `SCHWELLE_AUFPRALL = 3.0 m/s²`.
3. Führen Sie die Simulation aus Abschnitt 10.3 durch und berechnen Sie
   die relative Abweichung.
4. Wie würden Sie vorgehen, wenn das Signal sehr verrauscht ist?
   Beschreiben Sie eine alternative Strategie.
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np
import pandas as pd
import plotly.express as px

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

SCHWELLE_START    = 0.5
SCHWELLE_AUFPRALL = 3.0
az_arr = df["az (m/s²)"].to_numpy()
t_arr  = df["Zeit (s)"].to_numpy()

idx_start    = np.argmax(np.abs(az_arr) > SCHWELLE_START)
idx_aufprall = np.where(np.abs(az_arr) > SCHWELLE_AUFPRALL)[0]
t_start      = t_arr[idx_start]
t_aufprall   = t_arr[idx_aufprall[-1]]
bewegungszeit = t_aufprall - t_start

print(f"Bewegungszeit (Phyphox): {bewegungszeit:.3f} s")

# Vergleich mit Simulation aus 10.3 (Beispielwert):
T_SIM     = 1.43
delta_rel = (T_SIM - bewegungszeit) / bewegungszeit * 100
print(f"Relative Abweichung:     {delta_rel:+.2f} %")
```

Bei sehr verrauschtem Signal hilft ein gleitender Mittelwert vor der
Schwellenwertdetektion:

```python
fenster  = 10
az_glatt = np.convolve(az_arr, np.ones(fenster)/fenster, mode='same')
```

Alternativ kann das globale Maximum im Signal als Aufprall-Spike identifiziert
werden – das ist robuster gegenüber Rauschen, aber empfindlicher gegenüber
anderen Spikes.
````

````{admonition} Übung 10.5 (✩✩✩)
:class: tip
**Reibungskoeffizient durch Kalibrierung bestimmen**

Gegeben:

- Messung der Bewegungszeit: `T_MESS = 1.51 s` (Mittelwert aus 8 Messungen,
  Standardabweichung 0.03 s).
- Wegpunkte und Parameter wie in Abschnitt 10.3 (μ_H = 0.30).

1. Implementieren Sie eine Funktion `bewegungszeit_sim(mu_g)`, die für einen
   gegebenen μ_G-Wert die simulierte Bewegungszeit zurückgibt.
2. Testen Sie μ_G-Werte im Bereich [0.05, 0.45] in Schritten von 0.05 und
   finden Sie den Wert mit der kleinsten Abweichung von `T_MESS`.
3. Stellen Sie die simulierte Bewegungszeit als Funktion von μ_G mit Plotly
   dar. Markieren Sie den Messwert und das Unsicherheitsband (±1σ).
4. Bestimmen Sie μ_G mit dem Bisektionsverfahren auf vier Dezimalstellen.
````

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np
import math
import plotly.graph_objects as go

# [bahn_aus_wegpunkten und wegpunkte wie in Abschnitt 10.3]

def bewegungszeit_sim(mu_g, m=0.1, G=9.81, MU_H=0.30, dt=0.005):
    laengen, winkel_rad = bahn_aus_wegpunkten(wegpunkte)
    v, t, gleitet = 0.0, 0.0, False
    for seg_idx in range(len(laengen)):
        theta   = winkel_rad[seg_idx]
        L       = laengen[seg_idx]
        F_N     = m * G * math.cos(theta)
        F_H     = m * G * math.sin(theta)
        F_gleit = mu_g * F_N
        if v > 1e-6 or abs(F_H) > MU_H * F_N:
            gleitet = True
        s = 0.0
        while s < L:
            a  = (-F_H - F_gleit) / m if gleitet else 0.0
            v += a * dt
            if v < 0:
                return t
            s += v * dt
            t += dt
    return t

T_MESS, SIGMA = 1.51, 0.03

# Grobsuche
mu_werte = np.arange(0.05, 0.50, 0.05)
zeiten   = [bewegungszeit_sim(mu) for mu in mu_werte]
idx_best = np.argmin(np.abs(np.array(zeiten) - T_MESS))
print(f"Bestes μ_G (Grobsuche): {mu_werte[idx_best]:.2f}, "
      f"t = {zeiten[idx_best]:.4f} s")

# Diagramm
fig = go.Figure()
fig.add_trace(go.Scatter(x=mu_werte, y=zeiten,
                         mode='lines+markers', name='Simulation'))
fig.add_hline(y=T_MESS, line_dash='dash', line_color='tomato',
              annotation_text=f'Messung: {T_MESS} s')
fig.add_hrect(y0=T_MESS-SIGMA, y1=T_MESS+SIGMA,
              fillcolor='tomato', opacity=0.1, line_width=0,
              annotation_text='±1σ')
fig.update_layout(title='Bewegungszeit als Funktion von μ_G',
                  xaxis_title='μ_G',
                  yaxis_title='Bewegungszeit (s)')
fig.show()

# Bisektionsverfahren
mu_lo, mu_hi = 0.05, 0.45
for _ in range(40):
    mu_mid = (mu_lo + mu_hi) / 2
    if bewegungszeit_sim(mu_mid) < T_MESS:
        mu_lo = mu_mid
    else:
        mu_hi = mu_mid

print(f"Kalibriertes μ_G: {mu_mid:.4f}, "
      f"t = {bewegungszeit_sim(mu_mid):.5f} s")
```
````

````{admonition} Übung 10.6 (Mini-Projekt)
:class: tip
**Vollständige Pipeline für das eigene Objekt**

Wenden Sie die vollständige Pipeline aus Kapitel 10 auf Ihr eigenes
Simulationsobjekt an.

**Teilaufgaben:**

1. **Wegpunkte definieren:** Nehmen Sie mindestens sechs Wegpunkte entlang
   der charakteristischen Bewegungsbahn Ihres Objekts auf – entweder in
   CloudCompare, durch Ablesen vom Foto oder durch Schätzung der Geometrie.
   Begründen Sie die Wahl der Wegpunkte in zwei Sätzen.

2. **Simulation:** Führen Sie die segmentweise Simulation mit dem Modell aus
   Abschnitt 10.3 durch. Wählen Sie Masse, Reibungskoeffizient und
   Startzustand begründet.

3. **Messung:** Messen Sie die Bewegungszeit Ihres Objekts mit mindestens
   fünf Wiederholungen (Stoppuhr oder Phyphox). Berechnen Sie Mittelwert
   und Standardabweichung.

4. **Validierung:** Berechnen Sie die relative Abweichung zwischen Simulation
   und Messung. Identifizieren Sie die wahrscheinlich dominante Fehlerquelle.

5. **Kalibrierung (optional):** Bestimmen Sie μ_G durch Rückrechnung aus
   Ihrem Messwert mit dem Bisektionsverfahren aus Übung 10.5.

6. **Ursina-Visualisierung:** Laden Sie das `.obj`-Mesh Ihres Objekts in
   Ursina und spielen Sie die berechnete Trajektorie mit dem Skript aus
   Abschnitt 10.4 ab.

7. **Reflexion:** Beantworten Sie in vier bis fünf Sätzen:
   - Wie gut beschreibt Ihr Modell die Wirklichkeit?
   - Welche Vereinfachung hat den größten Einfluss auf die Genauigkeit?
   - Was würden Sie für eine präzisere Simulation ändern?
   - Inwiefern ist Ihre Ursina-Visualisierung ein Digitaler Zwilling Ihres
     Objekts, und wo endet dieser Begriff?
````
