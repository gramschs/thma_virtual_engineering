import math
import numpy as np
import pyvista as pv


# =============================================================================
# Physik
# =============================================================================

def bahn_aus_wegpunkten(wegpunkte):
    """
    Berechnet Segmentlängen und lokale Neigungswinkel.

    Annahme: Wegpunkte als (x, y, z) in m, y ist die Höhenkoordinate.
    """
    laengen, winkel_rad = [], []
    for i in range(len(wegpunkte) - 1):
        delta       = wegpunkte[i + 1] - wegpunkte[i]
        laenge      = np.linalg.norm(delta)
        delta_horiz = np.sqrt(delta[0] ** 2 + delta[2] ** 2)
        theta       = np.arctan2(delta[1], delta_horiz)
        laengen.append(laenge)
        winkel_rad.append(theta)
    return np.array(laengen), np.array(winkel_rad)


def simuliere_trajektorie(wegpunkte, m=0.1, G=9.81,
                          MU_H=0.20, MU_G=0.15, dt=0.005):
    """
    Berechnet die vollständige Trajektorie als Liste von (Zeit, 3D-Position).

    Annahmen:
        - Wegpunkte als (x, y, z) in m, y ist die Höhenkoordinate.
        - Reibungsmodell: Haftreibung und Gleitreibung entlang der Bahn.
    Rückgabe:
        trajektorie : list of (t, np.array([x, y, z]))
    """
    laengen, winkel_rad = bahn_aus_wegpunkten(wegpunkte)
    trajektorie = [(0.0, wegpunkte[0].copy())]

    v = 0.0
    t = 0.0

    for L, theta, start, ziel in zip(laengen, winkel_rad,
                                     wegpunkte[:-1], wegpunkte[1:]):
        richtung  = (ziel - start) / L
        F_N       = m * G * math.cos(theta)
        F_H       = m * G * math.sin(theta)
        F_H_along = -F_H
        F_haft    = MU_H * F_N
        F_gleit   = MU_G * F_N

        if F_H_along <= F_haft and v <= 1e-6:
            break

        s_seg = 0.0

        while s_seg < L:
            if v <= 1e-6 and F_H_along <= F_haft:
                v = 0.0
                return trajektorie

            a  = (F_H_along - F_gleit) / m
            v += a * dt
            if v < 0:
                v = 0.0
                return trajektorie

            s_step = v * dt
            s_seg += s_step
            t     += dt

            pos_3d = start + richtung * min(s_seg, L)
            trajektorie.append((t, pos_3d.copy()))

    return trajektorie


# =============================================================================
# Wegpunkte und Simulation
# =============================================================================

wegpunkte = np.array([
    [ 0.08075079,  0.03540741, -0.04429221],
    [ 0.11615875,  0.02852899, -0.04392783],
    [ 0.16716073,  0.02120220, -0.04209511],
    [ 0.20815045,  0.01721681, -0.04486231],
    [ 0.23987089,  0.01578052, -0.04225944],
    [ 0.25288326,  0.01645789, -0.02781715],
    [ 0.25796390,  0.01647832, -0.01031585],
    [ 0.25636873,  0.00546466,  0.00567502],
])

# Spiegelung in x: nur aktivieren, wenn die Trajektorie spiegelverkehrt
# zur Führungsrille liegt. Das kann passieren, wenn CloudCompare oder
# Meshroom das Koordinatensystem gespiegelt exportiert haben.
# wegpunkte[:, 0] *= -1

m    = 0.1
G    = 9.81
MU_H = 0.05
MU_G = 0.03
dt   = 0.005

trajektorie = simuliere_trajektorie(
    wegpunkte, m=m, G=G, MU_H=MU_H, MU_G=MU_G, dt=dt
)

traj_t   = np.array([p[0] for p in trajektorie])
traj_pos = np.array([p[1] for p in trajektorie])

traj_v = np.zeros(len(traj_t))
for i in range(1, len(traj_t)):
    dp        = np.linalg.norm(traj_pos[i] - traj_pos[i - 1])
    dt_i      = traj_t[i] - traj_t[i - 1]
    traj_v[i] = dp / dt_i if dt_i > 0 else 0.0

print(f"Trajektorie berechnet: {len(trajektorie)} Punkte")
print(f"Bewegungszeit:         {traj_t[-1]:.4f} s")
print(f"Startposition:         {traj_pos[0]}")
print(f"Endposition:           {traj_pos[-1]}")
print(f"Maximale Geschwindigkeit: {traj_v.max():.3f} m/s")


# =============================================================================
# PyVista-Visualisierung
# =============================================================================

# --- Szene aufbauen ---
plotter = pv.Plotter(window_size=[1200, 700], title='Kugelbahn Simulation')
plotter.set_background('white')

# Kugelbahn-Mesh laden (.obj-Datei im selben Ordner)
# Falls das Mesh in Millimetern exportiert wurde: mesh.scale([0.001, 0.001, 0.001], inplace=True)
# Falls die Bahn auf der Seite liegt: mesh.rotate_x(-90, inplace=True)
mesh = pv.read('final_marble_track.obj')
plotter.add_mesh(
    mesh,
    color='lightgray',
    smooth_shading=True,
    specular=0.3,
    specular_power=20,
)

# Trajektorie als Linie einzeichnen
traj_linie = pv.Spline(traj_pos, n_points=500)
plotter.add_mesh(traj_linie, color='steelblue', line_width=2, label='Trajektorie')

# Wegpunkte als Referenzmarker
wegpunkt_cloud = pv.PolyData(wegpunkte)
plotter.add_mesh(
    wegpunkt_cloud,
    color='green',
    point_size=12,
    render_points_as_spheres=True,
    label='Wegpunkte',
)

# Kugel am Startpunkt
# Sphere wird einmalig bei (0,0,0) erzeugt; Position wird per SetPosition()
# verschoben, kein Neuerzeugen in jedem Frame nötig.
KUGELRADIUS = 0.015  # ca. 3 cm Durchmesser, in Metern anpassen
kugel_mesh  = pv.Sphere(radius=KUGELRADIUS, center=(0.0, 0.0, 0.0))
kugel_actor = plotter.add_mesh(kugel_mesh, color='crimson', smooth_shading=True)
kugel_actor.SetPosition(*traj_pos[0])

# Statustext
status_actor = plotter.add_text(
    't = 0.000 s | v = 0.000 m/s',
    position='upper_left',
    font_size=12,
    color='black',
)

# Legende
plotter.add_legend(size=(0.2, 0.1), loc='lower right')

# Kamera so ausrichten, dass die Kugel von oben nach unten rollt:
# y ist die Höhenachse, wir schauen von schräg vorne oben auf die Bahn.
# Mittelpunkt und Ausdehnung der Bahn automatisch berechnen.
mitte      = traj_pos.mean(axis=0)
ausdehnung = np.linalg.norm(traj_pos.max(axis=0) - traj_pos.min(axis=0))
plotter.camera.focal_point = mitte
plotter.camera.position    = mitte + np.array([0.0, ausdehnung * 0.8, ausdehnung * 1.2])
plotter.camera.up          = (0.0, 1.0, 0.0)  # y zeigt nach oben


# --- Animationszustand ---
import time as _time

zustand = {'idx': 0, 'laeuft': True, 'sim_zeit': 0.0}
FPS        = 60
DT_FRAME   = 1.0 / FPS   # Wanduhrzeit pro Frame in Sekunden
ZEITFAKTOR = 0.1          # 0.1 = 10x Zeitlupe, 1.0 = Echtzeit


def neustart():
    """Simulation von vorne starten (Taste R)."""
    zustand['idx']     = 0
    zustand['laeuft']  = True
    zustand['sim_zeit'] = 0.0
    kugel_actor.SetPosition(*traj_pos[0])


plotter.add_key_event('r', neustart)

print("\nSteuerung:")
print("  Maus         – Szene drehen, zoomen, verschieben")
print("  R            – Simulation neu starten")
print("  Q / Fenster  – Beenden")

# Render-Fenster öffnen ohne zu blockieren
plotter.show(interactive_update=True)

# Animations-Loop: läuft so lange das Fenster offen ist
wand_vorher = _time.perf_counter()

while plotter.ren_win is not None:
    jetzt       = _time.perf_counter()
    delta_wand  = jetzt - wand_vorher
    wand_vorher = jetzt

    if zustand['laeuft']:
        zustand['sim_zeit'] = min(
            zustand['sim_zeit'] + delta_wand * ZEITFAKTOR, traj_t[-1]
        )
        sim_zeit = zustand['sim_zeit']

        # Trajektoriepunkt zur aktuellen Simulationszeit suchen
        idx = int(np.searchsorted(traj_t, sim_zeit))
        idx = min(idx, len(traj_pos) - 1)

        kugel_actor.SetPosition(*traj_pos[idx])

        # CornerAnnotation: Text über SetText(position, text) setzen
        # position: 0=unten-links, 1=unten-rechts, 2=oben-links, 3=oben-rechts
        status_actor.SetText(
            2, f't = {sim_zeit:.3f} s | v = {traj_v[idx]:.3f} m/s'
        )

        if sim_zeit >= traj_t[-1]:
            zustand['laeuft'] = False

    # Fenster neu zeichnen und Ereignisse verarbeiten
    # Bei geschlossenem Fenster wirft plotter.update() eine Exception → Loop beenden
    try:
        plotter.update(stime=int(DT_FRAME * 1000))
        if not plotter.ren_win:
            break
    except Exception:
        break
