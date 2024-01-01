import asyncio
import flet as ft
from flet_contrib.shimmer import Shimmer
async def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    holder = ft.Container()
    await page.add_async(holder)
    lt = ft.ListTile()
    lt.leading = ft.Icon(ft.icons.ALBUM, data = 'shimmer_load')
    lt.title = ft.Text("The Enchanted Nightingale", data = 'shimmer_load')
    lt.subtitle = ft.Text("Music by Julie Gable. Lyrics by Sidney Stein.", data = 'shimmer_load')
    
    row = ft.Row()
    row.alignment = ft.MainAxisAlignment.END
    row.controls.append(ft.TextButton("Buy tickets", data = 'shimmer_load'))
    row.controls.append(ft.TextButton("Listen", data = 'shimmer_load'))
    
    column = ft.Column()
    column.controls = [lt, row]
    
    container = ft.Container()
    container.content = column
    container.height = 130
    container.width = 400
    container.padding = 10
    
    ctrl = ft.Card()
    ctrl.content = container

    temp = []
    for i in range(5): # individual mode shimmer effect
        temp.append(Shimmer(ref = ft.Ref[ft.ShaderMask](),control=ctrl, height = ctrl.height, width=ctrl.width, auto_generate= True, full= False))
    holder.content = ft.Column(temp)
    await holder.update_async()
    for each in temp:
        each.start_async()
    await asyncio.sleep(9) # assume this to be some data fetching task
    for each in temp:
        each.stop_async()

ft.app(target=main)
