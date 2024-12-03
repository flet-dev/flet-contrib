import flet as ft

from flet_contrib.vertical_splitter import FixedPane, VerticalSplitter


def main(page: ft.Page):
    c_left = ft.Container(bgcolor=ft.Colors.BLUE_400)

    c_right = ft.Container(bgcolor=ft.Colors.YELLOW_400)

    vertical_splitter = VerticalSplitter(
        # height=400,
        expand=True,
        right_pane=c_right,
        left_pane=c_left,
        fixed_pane_min_width=200,
        fixed_pane_width=300,
        fixed_pane_max_width=400,
        fixed_pane=FixedPane.RIGHT,
    )

    page.add(vertical_splitter)


ft.app(target=main)
