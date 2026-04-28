import flet as ft
import flet.canvas as cv
import math
import urllib.request

DB_URL = "https://kvdb.io/A2QB57woxyPTdmuS4SCHr1/index_rotation"
ZONES = ["Bras Droit", "Ventre Droit", "Cuisse Droite", "Cuisse Gauche", "Ventre Gauche", "Bras Gauche"]


def main(page: ft.Page):
    page.title = "Suivi PikPik Sync"
    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    state = {"index": 0}

    # --- SYNCHRO AVEC HEADERS ---
    def load_from_cloud():
        try:
            # On ajoute un User-Agent pour éviter la 403
            req = urllib.request.Request(
                DB_URL,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                val_txt = response.read().decode('utf-8')
                if val_txt and "not found" not in val_txt.lower():
                    return int(val_txt.strip())
        except Exception as e:
            # Le 404 est normal si le fichier n'existe pas encore
            print(f"Info Load: {e}")
        return 0

    def save_to_cloud(val):
        try:
            req = urllib.request.Request(
                DB_URL,
                data=str(val).encode('utf-8'),
                method='PUT',
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                print(f"Sauvegarde OK : {val}")
        except Exception as e:
            print(f"Erreur Save: {e}")

    # Initialisation
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
        state["index"] = (state["index"] + 1) % 6
        dessiner_roue()
        save_to_cloud(state["index"])

    # On utilise ton bouton qui fonctionne (FilledButton avec content)
    page.add(
        ft.Text("PikPik Wheel", size=28, weight="bold"),
        ft.Container(content=cp, width=400, height=400, alignment=ft.Alignment(0, 0)),
        ft.FilledButton(
            content=ft.Row(
                [ft.Icon(ft.Icons.SYNC), ft.Text("Fait !", size=16, weight="bold")],
                alignment=ft.MainAxisAlignment.CENTER, tight=True
            ),
            on_click=valider,
            style=ft.ButtonStyle(padding=20, shape=ft.RoundedRectangleBorder(radius=10))
        )
    )

    dessiner_roue()


ft.run(main)
