import flet as ft
import json
import flet.canvas as cv
import math
import os
import ssl

from flet import ThemeMode

# --- FIX SSL POUR LE TÉLÉCHARGEMENT INITIAL ---
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

# --- LOGIQUE DE SAUVEGARDE ---
FICHIER_SAVE = "data_rotation.json"
ZONES = ["B Droit", "V Droit", "C Droite",
         "C Gauche", "V Gauche", "B Gauche"]


def charger_index():
    if os.path.exists(FICHIER_SAVE):
        with open(FICHIER_SAVE, "r") as f:
            return json.load(f).get("index", 0)
    return 0


def sauvegarder_index(idx):
    with open(FICHIER_SAVE, "w") as f:
        json.dump({"index": idx}, f)


# --- INTERFACE FLET ---
def main(page: ft.Page):
    page.title = "The PikPik Wheel"
    page.theme_mode = ThemeMode.LIGHT
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"

    state = {"index": charger_index()}
    cartes_zones = []

    # On crée un Canvas pour dessiner
    cp = cv.Canvas(
        expand=True,
        shapes=[],  # On va remplir ça dynamiquement
    )

    def dessiner_roue():
        cp.shapes.clear()
        rayon_max = 150  # Rayon de la zone ROUGE (celle qui ressort)
        rayon_normal = 135  # Rayon des autres zones (crée le décalage)
        centre = 170  # Centre du Canvas (ajusté pour ne pas couper le cercle)
        offset = -math.pi / 2

        # Angle total d'un segment (60°)
        angle_segment = (2 * math.pi / 6)
        # Angle de séparation vide (on enlève environ 5° entre chaque part)
        padding_angle = 0.08
        # Rotation initiale pour aligner 3 gauche / 3 droite
        offset_rotation = -math.pi / 2

        for i in range(len(ZONES)):
            # Calcul de l'angle (60° par segment en radians)
            start_angle = offset_rotation + i * angle_segment + (padding_angle / 2)
            sweep_angle = angle_segment - padding_angle
            middle_angle = start_angle + (sweep_angle / 2)  # Pour centrer le texte


            # Choix de la couleur
            color = ft.Colors.GREY_300
            rayon_style = rayon_normal
            text_color = ft.Colors.BLACK
            if i == state["index"]:
                color = ft.Colors.RED_ACCENT_700
                rayon_style = rayon_max
                text_color = ft.Colors.WHITE
            elif i == (state["index"] + 1) % 6:
                color = ft.Colors.GREEN_400

            # On dessine le segment
            cp.shapes.append(
                cv.Arc(
                    centre - rayon_style, centre - rayon_style,  # Position haut-gauche
                    rayon_style * 2, rayon_style * 2,  # Taille (diamètre)
                    start_angle,
                    sweep_angle,
                    use_center=True,  # Pour faire une part de tarte
                    paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL),

                )
            )

            cp.shapes.append(
                cv.Arc(
                    centre - rayon_style, centre - rayon_style,
                    rayon_style * 2, rayon_style * 2,
                    start_angle,
                    sweep_angle,
                    use_center=True,
                    paint=ft.Paint(color=ft.Colors.WHITE, style=ft.PaintingStyle.STROKE, stroke_width=2),
                )
            )

            # 5. AJOUT DU TEXTE
            # On place le texte à 60% de la distance du rayon
            distance_texte = rayon_style * 0.65
            tx = centre + distance_texte * math.cos(middle_angle)
            ty = centre + distance_texte * math.sin(middle_angle)

            cp.shapes.append(
                cv.Text(
                    x=tx,
                    y=ty,
                    value=ZONES[i],
                    style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD, color=text_color),
                    alignment=ft.Alignment.CENTER,
                )
            )


        page.update()

    def valider(e):
        state["index"] = (state["index"] + 1) % 6
        sauvegarder_index(state["index"])
        dessiner_roue()

    # Layout
    page.add(
        ft.Text("Ma Rotation", size=25, weight=ft.FontWeight.BOLD),
        ft.Container(cp, width=400, height=400, alignment=ft.Alignment.CENTER),
        ft.ElevatedButton("Zone suivante", icon=ft.Icons.CHECK, on_click=valider)
    )

    dessiner_roue()

ft.run(main)