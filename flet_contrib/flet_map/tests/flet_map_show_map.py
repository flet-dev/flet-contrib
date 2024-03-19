import flet as ft

from flet_contrib.flet_map import FletMap

def main(page: ft.Page):
    
    page.add(
        ft.ListView(
            expand=True,
            controls=[
                FletMap(expand=True, latitude=40.766666,
                           longtitude=29.916668,zoom=15,screenView = [8,4],)
            ]
        ))

    # page.add(ft.FletMap(expand=True))


if __name__ == '__main__':
    # FletMap()
    ft.app(target=main)
