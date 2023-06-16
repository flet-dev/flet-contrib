from enum import Enum
from typing import Optional
import flet as ft
import flet.canvas as cv


class VerticalSlider(ft.GestureDetector):
    def __init__(self):
        super().__init__()
        self.previous_volume = 1
        self.content = ft.Container(
            width=100,
            height=5,
            content=cv.Canvas(
                shapes=[
                    cv.Rect(
                        x=0,
                        y=0,
                        height=4,
                        border_radius=3,
                        paint=ft.Paint(color=ft.colors.GREY_500),
                        width=100,
                    ),
                    cv.Rect(
                        x=0,
                        y=0,
                        height=4,
                        border_radius=3,
                        paint=ft.Paint(color=ft.colors.GREY_900),
                        width=100,
                    ),
                    cv.Circle(
                        x=100,
                        y=2,
                        radius=6,
                        paint=ft.Paint(color=ft.colors.GREY_900),
                    ),
                ]
            ),
        )
        self.on_hover = self.change_cursor
        self.on_pan_start = self.change_volume
        self.on_pan_update = self.change_volume

    def change_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.CLICK
        e.control.update()

    def change_volume(self, e):
        if e.local_x >= 0 and e.local_x <= self.content.width:
            self.content.content.shapes[1].width = e.local_x  ## New volume
            self.content.content.shapes[2].x = e.local_x  ## Thumb
            self.page.update()


class HorizontalSlider(ft.GestureDetector):
    def __init__(self):
        super().__init__()
        self.previous_volume = 1
        self.content = ft.Container(
            width=100,
            height=5,
            content=cv.Canvas(
                shapes=[
                    cv.Rect(
                        x=0,
                        y=0,
                        height=4,
                        border_radius=3,
                        paint=ft.Paint(color=ft.colors.GREY_500),
                        width=100,
                    ),
                    cv.Rect(
                        x=0,
                        y=0,
                        height=4,
                        border_radius=3,
                        paint=ft.Paint(color=ft.colors.GREY_900),
                        width=100,
                    ),
                    cv.Circle(
                        x=100,
                        y=2,
                        radius=6,
                        paint=ft.Paint(color=ft.colors.GREY_900),
                    ),
                ]
            ),
        )
        self.on_hover = self.change_cursor
        self.on_pan_start = self.change_volume
        self.on_pan_update = self.change_volume

    def change_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.CLICK
        e.control.update()

    def change_volume(self, e):
        if e.local_x >= 0 and e.local_x <= self.content.width:
            self.content.content.shapes[1].width = e.local_x  ## New volume
            self.content.content.shapes[2].x = e.local_x  ## Thumb
            self.page.update()
