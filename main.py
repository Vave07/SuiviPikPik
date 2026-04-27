import flet as ft
import flet.canvas as cv
import math

ZONES = ["Bras Droit", "Ventre Droit", "Cuisse Droite",
         "Cuisse Gauche", "Ventre Gauche", "Bras Gauche"]

def main(page: ft.Page):
    page.title = "The PikPik Wheel"
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # --- STOCKAGE WEB ---
    # On récupère l'index stocké dans le navigateur (ou 0 par défaut)
    idx_saved = page.client_storage.get("index")
    state = {"index": idx_saved if idx_saved is not None else 0}

    cp = cv.Canvas(
        expand=True,
        shapes=[],
    )

    def dessiner_roue():
        cp.shapes.clear()
        rayon_max = 150
        rayon_normal = 135
        centre = 200
        angle_segment = (2 * math.pi / 6)
        padding_angle = 0.08 
        offset_rotation = -math.pi / 2 

        for i in range(len(ZONES)):
            start_angle = offset_rotation + i * angle_segment + (padding_angle / 2)
            sweep_angle = angle_segment - padding_angle
            middle_angle = start_angle + (sweep_angle / 2)

            color = ft.Colors.GREY_300
            rayon_style = rayon_normal
            text_color = ft.Colors.BLACK
            
            if i == state["index"]:
                color = ft.Colors.RED_ACCENT_700
                rayon_style = rayon_max
                text_color = ft.Colors.WHITE
            elif i == (state["index"] + 1) % 6:
                color = ft.Colors.GREEN_400
                rayon_style = rayon_normal
                text_color = ft.Colors.WHITE

            # Arc
            cp.shapes.append(
                cv.Arc(
                    centre - rayon_style, centre - rayon_style,
                    rayon_style * 2, rayon_style * 2,
                    start_angle, sweep_angle,
                    use_center=True,
                    paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL),
                )
            )
            
            # Texte
            distance_texte = rayon_style * 0.65
            tx = centre + distance_texte * math.cos(middle_angle)
            ty = centre + distance_texte * math.sin(middle_angle)

            cp.shapes.append(
                cv.Text(
                    x=tx, y=ty,
                    value=ZONES[i],
                    style=ft.TextStyle(size=14, weight="bold", color=text_color),
                    alignment=ft.Alignment.CENTER,
                )
            )
        page.update()

    def valider(e):
        # Mise à jour de l'index
        state["index"] = (state["index"] + 1) % 6
        # Sauvegarde dans le stockage du navigateur
        page.client_storage.set("index", state["index"])
        dessiner_roue()

    # Layout
    page.add(
        ft.Text("Ma Rotation", size=25, weight="bold"),
        ft.Container(cp, width=400, height=400, alignment=ft.alignment.CENTER),
        ft.ElevatedButton("Zone suivante", icon=ft.Icons.CHECK, on_click=valider)
    )

    dessiner_roue()

ft.run(main)
