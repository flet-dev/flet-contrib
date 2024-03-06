import asyncio
import flet as ft
from flet_contrib.shimmer import Shimmer


async def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    holder = ft.Container()
    page.add(holder)
    lt = ft.ListTile(
        leading=ft.Icon(
            ft.icons.ALBUM, data="shimmer_load"
        ),  # data = 'shimmer_load' inform the Shimmer class to create dummy for this control
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
    card = ft.Card(content=container)
    ctrl = ft.Column([card for i in range(5)])

    dummy = Shimmer(control=ctrl, auto_generate=True)  # passing ctrl to Shimmer
    holder.content = dummy  # can also use page.splash in place of holder
    holder.update()
    await asyncio.sleep(3)  # assume this to be any data fetching task
    holder.content = ctrl
    holder.update()


ft.app(target=main)
