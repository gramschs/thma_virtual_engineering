import math
import numpy as np
from ursina import *


def bahn_aus_wegpunkten(wegpunkte):
    """
    Berechnet Segmentlängen und lokale Neigungswinkel.

    Annahme: Wegpunkte als (x, y, z) in m, y ist die Höhenkoordinate.
    """
    laengen, winkel_rad = [], []
    for i in range(len(wegpunkte) - 1):
        delta  = wegpunkte[i+1] - wegpunkte[i]
        laenge = np.linalg.norm(delta)

        # horizontale Distanz in der x-z-Ebene
        delta_horiz = np.sqrt(delta[0]**2 + delta[2]**2)
        # Neigung: y als Höhe
        theta = np.arctan2(delta[1], delta_horiz)

        laengen.append(laenge)
        winkel_rad.append(theta)

    return np.array(laengen), np.array(winkel_rad)


# Wegpunkte (x, y, z), y = Höhe
wegpunkte = np.array([
    [0.08075079, 0.03540741, -0.04429221],
    [0.11615875, 0.02852899, -0.04392783],
    [0.16716073, 0.02120220, -0.04209511],
    [0.20815045, 0.01721681, -0.04486231],
    [0.23987089, 0.01578052, -0.04225944],
    [0.25288326, 0.01645789, -0.02781715],
    [0.25796390, 0.01647832, -0.01031585],
    [0.25636873, 0.00546466,  0.00567502],
])

# Spiegelung in x, damit Bahn und Trajektorie gleiche Richtung haben
wegpunkte[:, 0] *= -1


# Physikparameter
m    = 0.1      # Masse in kg
G    = 9.81     # Erdbeschleunigung in m/s²
MU_H = 0.05     # Haftreibungskoeffizient
MU_G = 0.03     # Gleitreibungskoeffizient
dt   = 0.005    # Zeitschritt in s


def simuliere_trajektorie(wegpunkte, m=0.1, G=9.81,
                          MU_H=0.20, MU_G=0.15, dt=0.005):
    """
    Berechnet die vollständige Trajektorie als Liste von (Zeit, 3D-Position).

    Annahmen:
        - Wegpunkte als (x, y, z) in m, y ist die Höhenkoordinate.
        - Reibungsmodell wie in Abschnitt 10.3.
    Rückgabe:
        trajektorie : list of (t, np.array([x, y, z]))
    """
    laengen, winkel_rad = bahn_aus_wegpunkten(wegpunkte)
    trajektorie = [(0.0, wegpunkte[0].copy())]

    v = 0.0   # Anfangsgeschwindigkeit
    t = 0.0   # Gesamtzeit

    # Über alle Segmente iterieren
    for L, theta, start, ziel in zip(laengen, winkel_rad,
                                     wegpunkte[:-1], wegpunkte[1:]):
        # Richtungsvektor des Segments (Länge 1)
        richtung = (ziel - start) / L

        # Kräfte im aktuellen Segment
        F_N       = m * G * math.cos(theta)
        F_H       = m * G * math.sin(theta)   # kann negativ sein (Gefälle)
        F_H_along = -F_H                      # bergab (≥ 0 bei durchgehend Gefälle)
        F_haft    = MU_H * F_N
        F_gleit   = MU_G * F_N

        # Kugel rollt in diesem Segment nicht mehr los
        if F_H_along <= F_haft and v <= 1e-6:
            break

        s_seg = 0.0

        # Innere Schleife: Euler-Cromer-Schritte im Segment
        while s_seg < L:
            # Wenn die Kugel (fast) steht und Haftung ausreicht, endet die Bewegung
            if v <= 1e-6 and F_H_along <= F_haft:
                v = 0.0
                return trajektorie

            # Gleitbewegung entlang der Bahn
            a = (F_H_along - F_gleit) / m

            # Euler-Cromer: erst Geschwindigkeit, dann Weg und Zeit
            v += a * dt
            if v < 0:
                v = 0.0
                return trajektorie

            s_step = v * dt
            s_seg += s_step
            t     += dt

            # Position im 3D-Raum (am Segmentende auf L klemmen)
            pos_3d = start + richtung * min(s_seg, L)
            trajektorie.append((t, pos_3d.copy()))

    return trajektorie


# --- Trajektorie vorberechnen ---

trajektorie = simuliere_trajektorie(
    wegpunkte, m=m, G=G, MU_H=MU_H, MU_G=MU_G, dt=dt
)

print(f"Trajektorie berechnet: {len(trajektorie)} Punkte")
print(f"Bewegungszeit:         {trajektorie[-1][0]:.4f} s")
print(f"Startposition:         {trajektorie[0][1]}")
print(f"Endposition:           {trajektorie[-1][1]}")

# Zeitstempel und Positionen als NumPy-Arrays
traj_t   = np.array([p[0] for p in trajektorie])
traj_pos = np.array([p[1] for p in trajektorie])

# Geschwindigkeit aus Differenzquotient vorberechnen
traj_v = np.zeros(len(traj_t))
for i in range(1, len(traj_t)):
    dp        = np.linalg.norm(traj_pos[i] - traj_pos[i-1])
    dt_i      = traj_t[i] - traj_t[i-1]
    traj_v[i] = dp / dt_i if dt_i > 0 else 0.0

print(f"Maximale Geschwindigkeit: {traj_v.max():.3f} m/s")
print(f"Zeitauflösung:            {np.mean(np.diff(traj_t)):.5f} s")


# --- Ursina-Teil ---

app = Ursina(title='Kugelbahn Simulation', width=1200, height=700)
window.color = color.white

# Kugelbahn-Mesh laden (.obj-Datei "final_marble_track.obj" im selben Ordner!)
kugelbahn = Entity(
    model='final_marble_track',   # Dateiname ohne .obj
    color=color.gray,
    scale=1.0,
    position=(0, 0, 0),
)

# Falls das Mesh in Millimetern exportiert wurde:
# kugelbahn.scale = 0.001

# Falls die Bahn in Ursina auf der Seite liegt:
# kugelbahn.rotation_x = -90

# Kugel am Startpunkt der Trajektorie
kugel = Entity(
    model='sphere',
    color=color.red,
    scale=0.02,                   # Durchmesser ca. 3 cm
    position=Vec3(*traj_pos[0])   # (x, y, z), y ist Höhe
)

# Optionaler Würfel zum visuellen Check des Startpunkts
marker = Entity(
    model='cube',
    color=color.green,
    scale=0.01,
    position=Vec3(*traj_pos[0])
)

# Kamera für freie Navigation
EditorCamera()

# Statusanzeige
anzeige = Text(
    text='t = 0.000 s | v = 0.000 m/s',
    position=(-0.85, 0.45),
    scale=1.2,
    color=color.black
)

# Simulationszeitsteuerung
sim_zeit = 0.0
laeuft   = True
ROLLZEIT = traj_t[-1]


def update():
    global sim_zeit, laeuft

    if not laeuft:
        return

    sim_zeit += time.dt
    if sim_zeit >= ROLLZEIT:
        sim_zeit = ROLLZEIT
        laeuft   = False

    # Nächstgelegenen Trajektoriepunkt nach aktueller Zeit suchen
    idx = min(np.searchsorted(traj_t, sim_zeit), len(traj_pos) - 1)
    kugel.position = Vec3(*traj_pos[idx])

    anzeige.text = f't = {sim_zeit:.3f} s | v = {traj_v[idx]:.3f} m/s'


def input(key):
    global sim_zeit, laeuft
    if key == 'r':                   # R zum Neustarten
        sim_zeit       = 0.0
        laeuft         = True
        kugel.position = Vec3(*traj_pos[0])


app.run()