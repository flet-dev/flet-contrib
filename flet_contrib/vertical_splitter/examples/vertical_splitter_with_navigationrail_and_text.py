import flet as ft

from flet_contrib.vertical_splitter import VerticalSplitter, FixedPane


def main(page: ft.Page):
    c_left = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.FAVORITE_BORDER,
                selected_icon=ft.icons.FAVORITE,
                label="First",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                label="Second",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Settings"),
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )

    c_right = ft.Column(
        controls=[
            ft.Text("Display Large", style=ft.TextThemeStyle.DISPLAY_LARGE),
            ft.Text("Display Medium", style=ft.TextThemeStyle.DISPLAY_MEDIUM),
            ft.Text("Display Small", style=ft.TextThemeStyle.DISPLAY_SMALL),
            ft.Text("Headline Large", style=ft.TextThemeStyle.HEADLINE_LARGE),
            ft.Text("Headline Medium", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.Text("Headline Small", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
            ft.Text("Title Large", style=ft.TextThemeStyle.TITLE_LARGE),
            ft.Text("Title Medium", style=ft.TextThemeStyle.TITLE_MEDIUM),
            ft.Text("Title Small", style=ft.TextThemeStyle.TITLE_SMALL),
            ft.Text("Label Large", style=ft.TextThemeStyle.LABEL_LARGE),
            ft.Text("Label Medium", style=ft.TextThemeStyle.LABEL_MEDIUM),
            ft.Text("Label Small", style=ft.TextThemeStyle.LABEL_SMALL),
            ft.Text("Body Large", style=ft.TextThemeStyle.BODY_LARGE),
            ft.Text("Body Medium", style=ft.TextThemeStyle.BODY_MEDIUM),
            ft.Text("Body Small", style=ft.TextThemeStyle.BODY_SMALL),
        ]
    )

    vertical_splitter = VerticalSplitter(
        # height=400,
        expand=True,
        right_pane=c_right,
        left_pane=c_left,
        fixed_pane_min_width=70
        # fixed_pane=FixedPane.RIGHT,
    )

    page.add(vertical_splitter)


ft.app(target=main)
