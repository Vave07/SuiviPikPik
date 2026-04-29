import flet as ft
import flet.canvas as cv
import math
import asyncio # Ajouté pour la petite pause de sécurité

ZONES = ["Bras Droit", "Ventre Droit", "Cuisse Droite", "Cuisse Gauche", "Ventre Gauche", "Bras Gauche"]

async def main(page: ft.Page):
    page.title = "PikPik Wheel"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    state = {"index": 0}

    # --- SYSTÈME DE SAUVEGARDE AMÉLIORÉ ---
    # On force l'utilisation de client_storage car storage n'existe pas chez toi
    async def get_storage():
        # Petite pause pour laisser Android réveiller le stockage
        await asyncio.sleep(0.2)
        return page.client_storage

    # --- CHARGEMENT INITIAL ---
    store = await get_storage()
    try:
        stored_index = await store.get_async("last_index")
        if stored_index is not None:
            state["index"] = int(stored_index)
    except Exception as e:
        print(f"Erreur de lecture : {e}")

    cp = cv.Canvas(expand=True, shapes=[])

    async def dessiner_roue():
        cp.shapes.clear()
        rayon_max, rayon_normal, centre = 150, 135, 180
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
                text_color = ft.Colors.WHITE

            cp.shapes.append(
                cv.Arc(
                    centre - rayon_style, centre - rayon_style,
                    rayon_style * 2, rayon_style * 2,
                    start_angle, sweep_angle, use_center=True,
                    paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL)
                )
            )
            
            tx = centre + (rayon_style * 0.6) * math.cos(middle_angle)
            ty = centre + (rayon_style * 0.6) * math.sin(middle_angle)
            
            cp.shapes.append(
                cv.Text(
                    x=tx, y=ty, value=ZONES[i],
                    style=ft.TextStyle(size=10, weight=ft.FontWeight.BOLD, color=text_color),
                    alignment=ft.Alignment(0, 0) 
                )
            )
        page.update()

    async def valider(e):
        state["index"] = (state["index"] + 1) % 6
        # On sauvegarde immédiatement
        try:
            await page.client_storage.set_async("last_index", state["index"])
        except Exception as ex:
            print(f"Erreur de sauvegarde : {ex}")
        await dessiner_roue()

    page.add(
        ft.Text("PikPik Wheel", size=32, weight=ft.FontWeight.BOLD),
        ft.Container(
            content=cp, width=360, height=360, 
            alignment=ft.Alignment.CENTER # Correction bien maintenue
        ),
        ft.FilledButton(
            content=ft.Row(
                [ft.Icon(ft.Icons.SYNC), ft.Text("FAIT", size=20, weight=ft.FontWeight.BOLD)],
                alignment=ft.MainAxisAlignment.CENTER, tight=True
            ),
            on_click=valider,
            style=ft.ButtonStyle(padding=25, shape=ft.RoundedRectangleBorder(radius=15))
        )
    )
    
    await dessiner_roue()

if __name__ == "__main__":
    ft.run(main)
