import flet as ft
import colorsys

COLOR_MATRIX_WIDTH = 280
COLOR_MATRIX_HEIGHT = 160
SLIDER_WIDTH = 180
CIRCLE_SIZE = 16


def rgb2hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb[0] * 255.0), int(rgb[1] * 255.0), int(rgb[2] * 255.0)
    )


def hex2rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def hex2hsv(value):
    rgb_color = hex2rgb(value)
    return colorsys.rgb_to_hsv(
        rgb_color[0] / 255, rgb_color[1] / 255, rgb_color[2] / 255
    )


class HueSlider(ft.GestureDetector):
    def __init__(self, on_change_hue, hue=1, number_of_hues=10):
        super().__init__()
        self.hue = hue
        self.number_of_hues = number_of_hues
        self.content = ft.Stack(height=CIRCLE_SIZE, width=SLIDER_WIDTH)
        self.generate_hues()
        self.on_change_hue = on_change_hue
        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag

    def update_hue_slider(self, hue):
        self.hue = hue
        x = self.hue * self.number_of_hues * self.hue_width + CIRCLE_SIZE
        self.update_selected_hue(x)

    def find_hue(self, x):
        for hue_block in self.content.controls[
            :-1
        ]:  # excluding the last element of the stack controls list which is the circle
            if x >= hue_block.left and x <= hue_block.left + self.hue_width:
                color = hue_block.bgcolor
                rgb_color = hex2rgb(color)
                hsv_color = colorsys.rgb_to_hsv(
                    round(rgb_color[0] / 255, 1),
                    round(rgb_color[1] / 255, 1),
                    round(rgb_color[2] / 255, 1),
                )
                self.hue = hsv_color[0]

    def update_selected_hue(self, x):
        self.find_hue(x)
        color = rgb2hex(colorsys.hsv_to_rgb(self.hue, 1, 1))
        self.circle.left = max(
            0,
            min(
                x - CIRCLE_SIZE / 2,
                self.hue_width * ((self.number_of_hues + 1)),
            ),
        )

        self.circle.bgcolor = color
        self.circle.update()
        self.on_change_hue(self.hue)

    def start_drag(self, e: ft.DragStartEvent):
        self.update_selected_hue(x=e.local_x)

    def drag(self, e: ft.DragUpdateEvent):
        self.update_selected_hue(x=e.local_x)

    def generate_hues(self):
        self.hue_width = (self.content.width - CIRCLE_SIZE) / (self.number_of_hues + 1)
        for i in range(0, self.number_of_hues + 1):
            color = rgb2hex(colorsys.hsv_to_rgb(i / self.number_of_hues, 1, 1))
            if i == 0:
                border_radius = ft.border_radius.only(top_left=5, bottom_left=5)
            elif i == self.number_of_hues:
                border_radius = ft.border_radius.only(top_right=5, bottom_right=5)
            else:
                border_radius = None
            self.content.controls.append(
                ft.Container(
                    height=CIRCLE_SIZE / 2,
                    width=self.hue_width,
                    bgcolor=color,
                    border_radius=border_radius,
                    top=CIRCLE_SIZE / 4,
                    left=i * self.hue_width + CIRCLE_SIZE / 2,
                )
            )

        self.circle = ft.Container(
            width=CIRCLE_SIZE,
            height=CIRCLE_SIZE,
            border_radius=CIRCLE_SIZE,
            border=ft.border.all(width=2, color="white"),
        )

        self.content.controls.append(self.circle)


class CustomColorPicker(ft.Column):
    def __init__(self, color="#000000", color_block_size=20):
        super().__init__()
        self.tight = True
        self.color = color
        self.color_block_size = color_block_size
        self.hue_slider = HueSlider(
            on_change_hue=self.update_color_matrix, hue=hex2hsv(self.color)[0]
        )
        self.generate_color_matrix()
        self.generate_selected_color_view()

    def did_mount(self):
        self.update_color_picker()

    def update_color_picker(self):
        hue = hex2hsv(self.color)[0]
        self.update_circle_position()
        self.update_color_matrix(hue)
        self.hue_slider.update_hue_slider(hue)

    def update_circle_position(self):
        hsv_color = hex2hsv(self.color)
        self.circle.left = (
            hsv_color[1] * self.colors_x
        ) * self.color_block_size + self.color_block_size / 2
        self.circle.top = (
            self.colors_y * (1 - hsv_color[2]) * self.color_block_size
            + self.color_block_size / 2
        )
        self.circle.update()

    def find_color(self, x, y):
        for color_square in self.color_matrix.content.controls[
            :-1
        ]:  # excluding the last element of the controls list which is the circle
            if (
                y >= color_square.top
                and y <= color_square.top + self.color_block_size
                and x >= color_square.left
                and x <= color_square.left + self.color_block_size
            ):
                self.color = color_square.bgcolor

    def generate_selected_color_view(self):
        rgb = hex2rgb(self.color)

        def on_hex_submit(e):
            self.color = e.control.value
            self.update_color_picker()

        def on_rgb_submit(e):
            rgb = (
                int(self.r.value) / 255,
                int(self.g.value) / 255,
                int(self.b.value) / 255,
            )
            print(rgb)
            self.color = rgb2hex(rgb)
            print(self.color)
            self.update_color_picker()

        self.hex = ft.TextField(
            label="Hex",
            text_size=12,
            value=self.color,
            height=40,
            width=90,
            on_submit=on_hex_submit,
            on_blur=on_hex_submit,
        )
        self.r = ft.TextField(
            label="R",
            height=40,
            width=55,
            value=rgb[0],
            text_size=12,
            on_submit=on_rgb_submit,
            on_blur=on_rgb_submit,
        )
        self.g = ft.TextField(
            label="G",
            height=40,
            width=55,
            value=rgb[1],
            text_size=12,
            on_submit=on_rgb_submit,
            on_blur=on_rgb_submit,
        )
        self.b = ft.TextField(
            label="B",
            height=40,
            width=55,
            value=rgb[2],
            text_size=12,
            on_submit=on_rgb_submit,
            on_blur=on_rgb_submit,
        )
        self.selected_color_view = ft.Column(
            spacing=20,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        ft.Container(
                            width=30, height=30, border_radius=30, bgcolor=self.color
                        ),
                        # ft.Text(color),
                        self.hue_slider,
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        self.hex,
                        self.r,
                        self.g,
                        self.b,
                    ],
                ),
            ],
        )

        self.controls.append(self.selected_color_view)

    def update_selected_color_view(self):
        rgb = hex2rgb(self.color)
        self.selected_color_view.controls[0].controls[
            0
        ].bgcolor = self.color  # Colored circle
        self.hex.value = self.color  # Hex
        self.r.value = rgb[0]  # R
        self.g.value = rgb[1]  # G
        self.b.value = rgb[2]  # B
        self.circle.bgcolor = self.color  # Color matrix circle
        self.update()

    def generate_color_matrix(self, hue=0):
        # self.color_block_size = COLOR_BLOCK_SIDE
        self.colors_x = int(COLOR_MATRIX_WIDTH / self.color_block_size)
        self.colors_y = int(COLOR_MATRIX_HEIGHT / self.color_block_size)

        def move_circle(x, y):
            self.circle.top = max(
                0,
                min(
                    y - CIRCLE_SIZE / 2,
                    self.color_matrix.content.height - CIRCLE_SIZE,
                ),
            )
            self.circle.left = max(
                0,
                min(
                    x - CIRCLE_SIZE / 2,
                    self.color_matrix.content.width - CIRCLE_SIZE,
                ),
            )
            self.find_color(
                x=self.circle.left + CIRCLE_SIZE / 2,
                y=self.circle.top + CIRCLE_SIZE / 2,
            )

        def on_pan_start(e: ft.DragStartEvent):
            move_circle(x=e.local_x, y=e.local_y)
            self.update_selected_color_view()

        def on_pan_update(e: ft.DragUpdateEvent):
            move_circle(x=e.local_x, y=e.local_y)
            self.update_selected_color_view()

        self.color_matrix = ft.GestureDetector(
            content=ft.Stack(
                height=(self.colors_y + 1) * self.color_block_size + CIRCLE_SIZE,
                width=(self.colors_x + 1) * self.color_block_size + CIRCLE_SIZE,
            ),
            on_pan_start=on_pan_start,
            on_pan_update=on_pan_update,
        )

        for j in range(0, self.colors_y + 1):
            for i in range(0, self.colors_x + 1):
                color = rgb2hex(
                    colorsys.hsv_to_rgb(
                        hue,
                        (i) / self.colors_x,
                        1 * (self.colors_y - j) / self.colors_y,
                    )
                )
                if i == 0 and j == 0:
                    border_radius = ft.border_radius.only(top_left=5)
                elif i == 0 and j == self.colors_y:
                    border_radius = ft.border_radius.only(bottom_left=5)
                elif i == self.colors_x and j == 0:
                    border_radius = ft.border_radius.only(top_right=5)
                elif i == self.colors_x and j == self.colors_y:
                    border_radius = ft.border_radius.only(bottom_right=5)
                else:
                    border_radius = None
                self.color_matrix.content.controls.append(
                    ft.Container(
                        height=self.color_block_size,
                        width=self.color_block_size,
                        border_radius=border_radius,
                        # bgcolor=color,
                        top=j * self.color_block_size + CIRCLE_SIZE / 2,
                        left=i * self.color_block_size + CIRCLE_SIZE / 2,
                    )
                )

        self.circle = ft.Container(
            width=CIRCLE_SIZE,
            height=CIRCLE_SIZE,
            border_radius=CIRCLE_SIZE,
            border=ft.border.all(width=2, color="white"),
        )

        self.color_matrix.content.controls.append(self.circle)
        self.controls.append(self.color_matrix)

    def update_color_matrix(self, hue):
        n = 0
        for j in range(0, self.colors_y + 1):
            for i in range(0, self.colors_x + 1):
                color = rgb2hex(
                    colorsys.hsv_to_rgb(
                        hue,
                        (i) / self.colors_x,
                        1 * (self.colors_y - j) / self.colors_y,
                    )
                )
                self.color_matrix.content.controls[n].bgcolor = color
                n += 1
        self.find_color(
            y=self.circle.top + CIRCLE_SIZE / 2, x=self.circle.left + CIRCLE_SIZE / 2
        )
        self.update_selected_color_view()
        self.update()
