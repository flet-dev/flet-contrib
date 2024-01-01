import time
import flet as ft
from flet_contrib.shimmer import Shimmer
def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    holder = ft.Container()
    page.add(holder)
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

    dummy = Shimmer(control= ctrl, auto_generate= True)

    holder.content = dummy
    holder.update()

    dummy.start() # Sync Mode
    time.sleep(3)
    dummy.stop()

    holder.content = ctrl
    holder.update()

ft.app(target=main)