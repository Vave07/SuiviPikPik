import flet as ft
import flet.canvas as cv
import math
import flet.fastapi as requests

DB_URL = "https://kvdb.io/A2QB57woxyPTdmuS4SCHr1/index_rotation"
ZONES = ["Bras Droit", "Ventre Droit", "Cuisse Droite", "Cuisse Gauche", "Ventre Gauche", "Bras Gauche"]

def main(page: ft.Page):
    page.title = "Suivi PikPik Sync"
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    
    # État interne
    state = {"index": 0}

    # --- FONCTIONS DE SYNCHRO CLOUD ---
    def load_from_cloud():
        try:
            # page.fetch est l'équivalent de requests.get mais autorisé par le navigateur
            response = page.fetch(DB_URL)
            if response:
                return int(response)
        except Exception as e:
            print(f"Erreur de chargement: {e}")
        return 0

    def save_to_cloud(val):
        try:
            # On utilise page.fetch avec la méthode PUT pour sauvegarder
            page.fetch(DB_URL, method="PUT", body=str(val))
        except Exception as e:
            print(f"Erreur de sauvegarde: {e}")
            
    # Chargement initial
    state["index"] = load_from_cloud()

    cp = cv.Canvas(expand=True, shapes=[])

    def dessiner_roue():
        cp.shapes.clear()
        rayon_max, rayon_normal, centre = 150, 135, 200
        angle_segment = (2 * math.pi / 6)
        padding_angle, offset_rotation = 0.08, -math.pi / 2 

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
                cv.Arc(centre - rayon_style, centre - rayon_style,
                       rayon_style * 2, rayon_style * 2,
                       start_angle, sweep_angle, use_center=True,
                       paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL))
            )
            
            tx = centre + (rayon_style * 0.65) * math.cos(middle_angle)
            ty = centre + (rayon_style * 0.65) * math.sin(middle_angle)

            cp.shapes.append(
                cv.Text(x=tx, y=ty, value=ZONES[i],
                        style=ft.TextStyle(size=12, weight="bold", color=text_color),
                        alignment=ft.Alignment(0, 0))
            )
        page.update()

    def valider(e):
        # 1. Mise à jour locale
        state["index"] = (state["index"] + 1) % 6
        # 2. Dessin immédiat pour la réactivité
        dessiner_roue()
        # 3. Sauvegarde silencieuse sur le cloud
        save_to_cloud(state["index"])

    # Construction de l'interface
    page.add(
        ft.Text("The PikPik Wheel", size=30, weight="bold"),
        ft.Container(
            content=cp, 
            width=400, 
            height=400, 
            alignment=ft.Alignment(0, 0)
        ),
        ft.ElevatedButton(
            "Zone suivante terminée", 
            icon=ft.Icons.SYNC, 
            on_click=valider,
            style=ft.ButtonStyle(padding=20)
        ),
        ft.Text("Données synchronisées en temps réel", size=10, color=ft.Colors.GREY_500)
    )

    dessiner_roue()

ft.run(main)
