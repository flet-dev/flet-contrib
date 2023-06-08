import flet as ft

from flet_contrib.vertical_splitter import VerticalSplitter, FixedPane


def main(page: ft.Page):
    c_left = ft.Container(
        bgcolor=ft.colors.ORANGE_300,
        alignment=ft.alignment.center,
    )

    c_right = ft.Container(
        bgcolor=ft.colors.BROWN_400,
        alignment=ft.alignment.center,
    )

    vertical_splitter = VerticalSplitter(
        # height=400,
        expand=True,
        right_pane=c_right,
        left_pane=c_left,
        fixed_pane=FixedPane.RIGHT,
    )

    page.add(vertical_splitter)


ft.app(target=main)
