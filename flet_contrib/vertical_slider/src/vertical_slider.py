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
    def __init__(
        self,
        width=200,
        thickness=10,
        value=200,
        divisions=2,
        min=100,
        max=500,
        thumb=cv.Circle(
            radius=20,
            paint=ft.Paint(color=ft.colors.GREY_900),
        ),
    ):
        super().__init__()
        self.value = value
        self.min = min
        self.max = max
        self.divisions = divisions
        self.thumb = thumb
        self.thumb.x = self.value * width / (self.max - self.min) + self.thumb.radius
        self.thumb.y = self.thumb.radius
        self.track = cv.Rect(
            x=self.thumb.radius,
            y=self.thumb.radius - thickness / 2,
            height=thickness,
            border_radius=3,
            paint=ft.Paint(color=ft.colors.GREY_500),
            width=width,
        )
        self.selected_track = cv.Rect(
            x=self.thumb.radius,
            y=self.thumb.radius - thickness / 2,
            height=thickness,
            border_radius=3,
            paint=ft.Paint(color=ft.colors.RED),
            width=self.value * width / (self.max - self.min) + self.thumb.radius,
        )

        self.division_shapes = []
        self.division_shapes.append(
            cv.Oval(
                x=self.track.width / 2 + self.thumb.radius,
                y=self.thumb.radius - thickness / 2,
                width=2,
                height=thickness,
                paint=ft.Paint(color=ft.colors.GREEN),
            )
        )

        self.content = ft.Container(
            width=width + self.thumb.radius * 2,
            height=self.thumb.radius * 2,
            bgcolor=ft.colors.GREEN_100,
            content=cv.Canvas(
                shapes=[
                    self.track,
                    self.selected_track,
                ]
                + self.division_shapes
                + [self.thumb]
            ),
        )
        self.on_hover = self.change_cursor
        self.on_pan_start = self.change_value_on_click
        self.on_pan_update = self.change_value_on_drag

    def change_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.CLICK
        e.control.update()

    def change_value_on_click(self, e: ft.DragStartEvent):
        x = max(self.thumb.radius, min(e.local_x, self.track.width + self.thumb.radius))
        print(x)
        self.value = (x - self.thumb.radius) * (
            self.max - self.min
        ) / self.track.width + self.min
        print(self.value)
        self.selected_track.width = x - self.thumb.radius
        self.thumb.x = x  ## Thumb
        self.page.update()

    def change_value_on_drag(self, e: ft.DragUpdateEvent):
        x = max(
            self.thumb.radius,
            min(e.local_x + e.delta_x, self.track.width + self.thumb.radius),
        )

        self.value = (x - self.thumb.radius) * (
            self.max - self.min
        ) / self.track.width + self.min

        print(self.value)
        self.selected_track.width = x - self.thumb.radius
        self.thumb.x = x
        self.page.update()
