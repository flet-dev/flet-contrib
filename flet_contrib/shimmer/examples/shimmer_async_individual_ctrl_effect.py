import asyncio
import flet as ft
from flet_contrib.shimmer import Shimmer


async def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    holder = ft.Container()
    page.add(holder)
    lt = ft.ListTile(
        leading=ft.Icon(ft.icons.ALBUM, data="shimmer_load"),
        title=ft.Text("The Enchanted Nightingale", data="shimmer_load"),
        subtitle=ft.Text(
            "Music by Julie Gable. Lyrics by Sidney Stein.", data="shimmer_load"
        ),
    )
    row = ft.Row(
        alignment=ft.MainAxisAlignment.END,
        controls=[
            ft.TextButton("Buy tickets", data="shimmer_load"),
            ft.TextButton("Listen", data="shimmer_load"),
        ],
    )
    column = ft.Column(controls=[lt, row])
    container = ft.Container(content=column, height=130, width=400, padding=10)
    ctrl = ft.Card(content=container)

    temp = []
    for i in range(5):  # individual mode shimmer effect
        temp.append(
            Shimmer(
                ref=ft.Ref[ft.ShaderMask](),
                control=ctrl,
                height=ctrl.height,
                width=ctrl.width,
                auto_generate=True,
            )
        )
    holder.content = ft.Column(temp)
    holder.update()

    await asyncio.sleep(6)  # assume this to be some data fetching task

    holder.content = ft.Column([ctrl for each in range(5)])
    holder.update()


ft.app(target=main)
