# from color_picker import CustomColorPicker
import flet as ft


class ColorSwatch:
    def __init__(self, name, display_name, accent=True):
        self.name = name
        self.display_name = display_name
        self.accent = accent


class Color:
    def __init__(self, swatch, shade="", accent=False):
        if shade == "":
            self.name = swatch.name
            self.display_name = swatch.display_name
        else:
            if not accent:
                self.name = f"{swatch.name}{shade}"
                self.display_name = f"{swatch.display_name}_{shade}"
            else:
                self.name = f"{swatch.name}accent{shade}"
                self.display_name = f"{swatch.display_name}_ACCENT_{shade}"


SHADES = ["50", "100", "200", "300", "400", "500", "600", "700", "800", "900"]
ACCENT_SHADES = ["100", "200", "400", "700"]
WHITE_SHADES = ["10", "12", "24", "30", "38", "54", "70"]
BLACK_SHADES = ["12", "26", "38", "45", "54", "87"]


class PaletteColorPicker(ft.Row):
    def __init__(self, color="black"):
        super().__init__()
        self.tight = True
        self.color = color
        self.spacing = 1
        self.generate_color_matrix()

    def generate_color_matrix(self):
        swatches = [
            ColorSwatch(name="red", display_name="RED"),
            ColorSwatch(name="pink", display_name="PINK"),
            ColorSwatch(name="purple", display_name="PURPLE"),
            ColorSwatch(name="deeppurple", display_name="DEEP_PURPLE"),
            ColorSwatch(name="indigo", display_name="INDIGO"),
            ColorSwatch(name="blue", display_name="BLUE"),
            ColorSwatch(name="lightblue", display_name="LIGHT_BLUE"),
            ColorSwatch(name="cyan", display_name="CYAN"),
            ColorSwatch(name="teal", display_name="TEAL"),
            ColorSwatch(name="green", display_name="GREEN"),
            ColorSwatch(name="lightgreen", display_name="LIGHT_GREEN"),
            ColorSwatch(name="lime", display_name="LIME"),
            ColorSwatch(name="yellow", display_name="YELLOW"),
            ColorSwatch(name="amber", display_name="AMBER"),
            ColorSwatch(name="orange", display_name="ORANGE"),
            ColorSwatch(name="deeporange", display_name="DEEP_ORANGE"),
            ColorSwatch(name="brown", display_name="BROWN", accent=False),
            ColorSwatch(name="grey", display_name="GREY", accent=False),
            ColorSwatch(name="bluegrey", display_name="BLUE_GREY", accent=False),
            ColorSwatch(name="white", display_name="WHITE"),
            ColorSwatch(name="black", display_name="BLACK"),
        ]

        def generate_color_names(swatch):
            colors = []
            base_color = Color(swatch=swatch)
            colors.append(base_color)
            if swatch.name == "white":
                for shade in WHITE_SHADES:
                    color = Color(swatch=swatch, shade=shade)
                    colors.append(color)
                return colors
            if swatch.name == "black":
                for shade in BLACK_SHADES:
                    color = Color(swatch=swatch, shade=shade)
                    colors.append(color)
                return colors
            for shade in SHADES:
                color = Color(swatch=swatch, shade=shade)
                colors.append(color)
            if swatch.accent:
                for shade in ACCENT_SHADES:
                    color = Color(swatch=swatch, shade=shade, accent=True)
                    colors.append(color)
            return colors

        def color_clicked(e):
            self.color = e.control.bgcolor
            print(self.color)

        for swatch in swatches:
            swatch_colors = ft.Column(spacing=1, controls=[])
            for color in generate_color_names(swatch):
                swatch_colors.controls.append(
                    ft.Container(
                        height=20,
                        width=20,
                        border_radius=20,
                        bgcolor=color.name,
                        on_click=color_clicked,
                    )
                )
            self.controls.append(swatch_colors)


def main(page: ft.Page):
    color_picker = PaletteColorPicker()

    def dialog_closed(e):
        text_icon.icon_color = e.control.content.color
        text_icon.update()

    # color_picker = PaletteColorPicker()
    d = ft.AlertDialog(content=color_picker, on_dismiss=dialog_closed)

    page.dialog = d

    def open_color_picker(e):
        d.open = True
        page.update()

    text_icon = ft.IconButton(
        icon=ft.icons.FORMAT_COLOR_TEXT, on_click=open_color_picker
    )

    page.add(text_icon)


ft.app(target=main)
