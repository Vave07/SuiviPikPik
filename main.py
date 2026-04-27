import flet as ft
import flet.canvas as cv
import math

# Les 6 zones de rotation
ZONES = ["B Droit", "V Droit", "C Droite",
         "C Gauche", "V Gauche", "B Gauche"]

def main(page: ft.Page):
    page.title = "Suivi PikPik"
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # --- LOGIQUE DE STOCKAGE ULTRA-COMPATIBLE ---
    idx_saved = None
    
    # On cherche où Flet a caché sa fonction de stockage
    if hasattr(page, "client_storage") and page.client_storage is not None:
        idx_saved = page.client_storage.get("index")
    elif hasattr(page, "storage") and page.storage is not None:
        idx_saved = page.storage.get("index")
    elif hasattr(page, "session_storage") and page.session_storage is not None:
        idx_saved = page.session_storage.get("index")

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

            cp.shapes.append(
                cv.Arc(
                    centre - rayon_style, centre - rayon_style,
                    rayon_style * 2, rayon_style * 2,
                    start_angle, sweep_angle,
                    use_center=True,
                    paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL),
                )
            )
            
            distance_texte = rayon_style * 0.65
            tx = centre + distance_texte * math.cos(middle_angle)
            ty = centre + distance_texte * math.sin(middle_angle)

            cp.shapes.append(
                cv.Text(
                    x=tx, y=ty,
                    value=ZONES[i],
                    style=ft.TextStyle(size=14, weight="bold", color=text_color),
                    alignment=ft.Alignment(0, 0), # Changement ici
                )
            )
        page.update()

    def valider(e):
        state["index"] = (state["index"] + 1) % 6
        
        if hasattr(page, "client_storage") and page.client_storage is not None:
            page.client_storage.set("index", state["index"])
        elif hasattr(page, "storage") and page.storage is not None:
            page.storage.set("index", state["index"])
            
        dessiner_roue()

    # Layout
    page.add(
        ft.Text("Ma Rotation", size=28, weight="bold"),
        ft.Container(
            content=cp, 
            width=400, 
            height=400, 
            alignment=ft.Alignment(0, 0) # Correction de l'erreur CENTER
        ),
        ft.ElevatedButton(
            "Zone suivante terminée", 
            icon=ft.Icons.CHECK_CIRCLE_OUTLINE, 
            on_click=valider
        )
    )

    dessiner_roue()

ft.run(main)
