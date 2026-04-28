import flet as ft
import flet.canvas as cv
import math

# Les 6 zones de rotation
ZONES = ["Bras Droit", "Ventre Droit", "Cuisse Droite",
         "Cuisse Gauche", "Ventre Gauche", "Bras Gauche"]

def main(page: ft.Page):
    page.title = "Suivi PikPik"
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # --- LOGIQUE DE STOCKAGE ROBUSTE ---
    def obtenir_index_sauvegarde():
        try:
            # On cherche d'abord dans client_storage (le plus persistant sur mobile)
            if page.client_storage is not None:
                val = page.client_storage.get("index")
                if val is not None:
                    return int(val)
            # Secours si client_storage n'est pas dispo
            elif hasattr(page, "storage") and page.storage is not None:
                val = page.storage.get("index")
                if val is not None:
                    return int(val)
        except Exception as e:
            print(f"Erreur de lecture : {e}")
        return 0

    # État local de l'application
    state = {"index": obtenir_index_sauvegarde()}

    # Zone de dessin (Canvas)
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

            # Arc de cercle
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
                    alignment=ft.Alignment(0, 0),
                )
            )
        page.update()

    def valider(e):
        # Mise à jour de l'index
        state["index"] = (state["index"] + 1) % 6
        
        # Sauvegarde forcée
        try:
            if page.client_storage is not None:
                page.client_storage.set("index", state["index"])
            elif hasattr(page, "storage") and page.storage is not None:
                page.storage.set("index", state["index"])
        except Exception as ex:
            print(f"Erreur de sauvegarde : {ex}")
            
        dessiner_roue()

    # Interface
    page.add(
        ft.Text("Rotation", size=28, weight="bold"),
        ft.Container(
            content=cp, 
            width=400, 
            height=400, 
            alignment=ft.Alignment(0, 0)
        ),
        ft.ElevatedButton(
            "Zone suivante terminée", 
            icon=ft.Icons.CHECK_CIRCLE_OUTLINE, 
            on_click=valider,
            style=ft.ButtonStyle(padding=20)
        )
    )

    dessiner_roue()

# Lancement
ft.run(main)
