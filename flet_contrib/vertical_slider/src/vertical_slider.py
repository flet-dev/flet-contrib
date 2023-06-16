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
    def __init__(self, width=100, thickness=5, value=50, min=0, max=100):
        super().__init__(width=width, height=thickness)
        self.value = value
        self.track = cv.Rect(
            x=0,
            y=0,
            height=self.height,
            border_radius=3,
            paint=ft.Paint(color=ft.colors.GREY_500),
            width=self.width,
        )
        self.selected_track = cv.Rect(
            x=0,
            y=0,
            height=self.height,
            border_radius=3,
            paint=ft.Paint(color=ft.colors.YELLOW),
            width=self.value,
        )
        self.thumb = cv.Circle(
            x=self.value,
            y=3,
            radius=6,
            paint=ft.Paint(color=ft.colors.GREY_900),
        )
        self.content = ft.Container(
            width=100,
            height=5,
            # bgcolor=ft.colors.BLUE,
            content=cv.Canvas(
                shapes=[
                    self.track,
                    # self.thumb,
                    self.selected_track,
                    self.thumb,
                ]
            ),
        )
        self.on_hover = self.change_cursor
        self.on_pan_start = self.change_value_on_click
        self.on_pan_update = self.change_value_on_drag

    def change_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.CLICK
        e.control.update()

    def change_value_on_click(self, e: ft.DragStartEvent):
        # print(e.local_x)
        if e.local_x >= 0 and e.local_x <= self.content.width:
            self.content.content.shapes[1].width = e.local_x  ## New volume
            self.thumb.x = e.local_x  ## Thumb
            self.page.update()

    def change_value_on_drag(self, e: ft.DragUpdateEvent):
        # print(e.local_x)
        self.value = max(0, min(e.local_x + e.delta_x, self.width))
        if e.local_x >= 0 and e.local_x <= self.content.width:
            print(self.value)
            self.selected_track.width = self.value
            self.thumb.x = self.value
            self.page.update()
