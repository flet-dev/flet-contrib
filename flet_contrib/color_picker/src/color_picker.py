import flet as ft
import colorsys
from .hue_slider import HueSlider
from .utils import *

COLOR_MATRIX_WIDTH = 340
COLOR_MATRIX_HEIGHT = 200
CIRCLE_SIZE = 20


class ColorPicker(ft.Column):
    def __init__(self, color="#000000", color_block_size=30):
        super().__init__()
        self.tight = True
        self.__color = color
        self.color_block_size = color_block_size
        self.hue_slider = HueSlider(
            on_change_hue=self.update_color_matrix, hue=hex2hsv(self.color)[0]
        )
        self.generate_color_matrix()
        self.generate_selected_color_view()

    # color
    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value

    def _before_build_command(self):
        super()._before_build_command()
        # called every time on self.update()
        self.hue_slider.hue = hex2hsv(self.color)[0]
        self.update_circle_position()
        self.circle.bgcolor = self.color
        self.update_color_field()
        self.update_selected_color_view_values()
        print("ON UPDATE")

    def update_color_picker(self):
        self.hue_slider.hue = hex2hsv(self.__color)[0]
        self.update_circle_position()
        self.update_color_matrix(self.hue_slider.hue)
        self.hue_slider.update()

    def update_circle_position(self):
        hsv_color = hex2hsv(self.color)

        # s * width
        self.circle.left = hsv_color[1] * self.color_field.width

        # (1-v)*height
        self.circle.top = (1 - hsv_color[2]) * self.color_field.height
        # self.circle.update()

    def find_color(self, x, y):
        # x / color matrix container width
        s = x / self.color_field.width

        # (height - y)/height
        v = (self.color_field.height - y) / self.color_field.height
        h = self.hue_slider.hue
        self.color = rgb2hex(colorsys.hsv_to_rgb(h, s, v))

    def generate_selected_color_view(self):
        rgb = hex2rgb(self.color)

        def on_hex_submit(e):
            self.color = e.control.value
            self.update()

        def on_rgb_submit(e):
            rgb = (
                int(self.r.value) / 255,
                int(self.g.value) / 255,
                int(self.b.value) / 255,
            )
            self.color = rgb2hex(rgb)
            # self.update_color_picker()
            self.update()

        self.hex = ft.TextField(
            label="Hex",
            text_size=12,
            value=self.__color,
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
                            width=30, height=30, border_radius=30, bgcolor=self.__color
                        ),
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
        self.update_selected_color_view_values()
        self.selected_color_view.update()

    def update_selected_color_view_values(self):
        rgb = hex2rgb(self.color)
        self.selected_color_view.controls[0].controls[
            0
        ].bgcolor = self.color  # Colored circle
        self.hex.value = self.__color  # Hex
        self.r.value = rgb[0]  # R
        self.g.value = rgb[1]  # G
        self.b.value = rgb[2]  # B
        self.circle.bgcolor = self.color  # Color matrix circle

    def generate_color_matrix(self):
        def move_circle(x, y):
            self.circle.top = max(
                0,
                min(
                    y - CIRCLE_SIZE / 2,
                    self.color_field.height,
                ),
            )
            self.circle.left = max(
                0,
                min(
                    x - CIRCLE_SIZE / 2,
                    self.color_field.width,
                ),
            )
            self.find_color(x=self.circle.left, y=self.circle.top)

        def on_pan_start(e: ft.DragStartEvent):
            move_circle(x=e.local_x, y=e.local_y)
            self.circle.update()
            self.update_selected_color_view()

        def on_pan_update(e: ft.DragUpdateEvent):
            move_circle(x=e.local_x, y=e.local_y)
            self.circle.update()
            self.update_selected_color_view()

        self.color_matrix = ft.GestureDetector(
            content=ft.Stack(
                height=COLOR_MATRIX_HEIGHT,
                width=COLOR_MATRIX_WIDTH,
            ),
            on_pan_start=on_pan_start,
            on_pan_update=on_pan_update,
        )

        saturation_container = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=[ft.colors.WHITE, ft.colors.RED],
            ),
            width=COLOR_MATRIX_WIDTH - CIRCLE_SIZE,
            height=COLOR_MATRIX_HEIGHT - CIRCLE_SIZE,
            border_radius=5,
        )

        self.color_field = ft.ShaderMask(
            top=CIRCLE_SIZE / 2,
            left=CIRCLE_SIZE / 2,
            content=saturation_container,
            blend_mode=ft.BlendMode.MULTIPLY,
            shader=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.WHITE, ft.colors.BLACK],
                # stops=[0.5, 1.0],
            ),
            border_radius=5,
            width=saturation_container.width,
            height=saturation_container.height,
        )

        self.circle = ft.Container(
            width=CIRCLE_SIZE,
            height=CIRCLE_SIZE,
            border_radius=CIRCLE_SIZE,
            border=ft.border.all(width=2, color="white"),
        )

        self.color_matrix.content.controls.append(self.color_field)
        self.color_matrix.content.controls.append(self.circle)
        self.controls.append(self.color_matrix)

    def update_color_field(self):
        h = self.hue_slider.hue
        s = hex2hsv(self.color)[1]
        v = hex2hsv(self.color)[2]
        container_gradient_colors = [
            rgb2hex(colorsys.hsv_to_rgb(h, 0, 1)),
            rgb2hex(colorsys.hsv_to_rgb(h, 1, 1)),
        ]

        self.color_field.content.gradient.colors = container_gradient_colors
        new_color = rgb2hex(colorsys.hsv_to_rgb(h, s, v))
        self.color = new_color

    def update_color_matrix(self):
        self.update_color_field()
        self.update_selected_color_view()
        self.color_matrix.update()
