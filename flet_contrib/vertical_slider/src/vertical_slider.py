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
        min=100,
        max=500,
        thumb=cv.Circle(
            radius=20,
            paint=ft.Paint(color=ft.colors.GREY_900),
        ),
        divisions=10,
        division_color_on_track=ft.colors.WHITE,
        division_color_on_selected=ft.colors.BLUE,
    ):
        super().__init__()
        self.value = value
        self.min = min
        self.max = max
        self.thickness = thickness
        self.divisions = divisions
        self.division_color_on_track = division_color_on_track
        self.division_color_on_selected = division_color_on_selected
        self.thumb = thumb
        self.thumb.x = self.value * width / (self.max - self.min) + self.thumb.radius
        self.thumb.y = self.thumb.radius
        self.track = cv.Rect(
            x=self.thumb.radius,
            y=self.thumb.radius - thickness / 2,
            height=thickness,
            border_radius=thickness / 2,
            paint=ft.Paint(color=ft.colors.GREY_500),
            width=width,
        )
        self.selected_track = cv.Rect(
            x=self.thumb.radius,
            y=self.thumb.radius - thickness / 2,
            height=thickness,
            border_radius=thickness / 2,
            paint=ft.Paint(color=ft.colors.RED),
            width=self.value * width / (self.max - self.min) + self.thumb.radius,
        )
        self.generate_divisions()
        shapes = [self.track, self.selected_track] + self.division_shapes + [self.thumb]

        self.content = ft.Container(
            width=width + self.thumb.radius * 2,
            height=self.thumb.radius * 2,
            bgcolor=ft.colors.GREEN_100,
            content=cv.Canvas(shapes=shapes),
        )
        self.on_hover = self.change_cursor
        self.on_pan_start = self.change_value_on_click
        self.on_pan_update = self.change_value_on_drag

    def generate_divisions(self):
        self.division_shapes = []
        if self.divisions == None:
            return
        else:
            if self.divisions > 1:
                for i in range(1, self.divisions):
                    print(i)
                    x = (self.track.width / self.divisions) * i + self.thumb.radius
                    if x < self.selected_track.width + self.thumb.radius:
                        color = self.division_color_on_selected
                    else:
                        color = self.division_color_on_track
                    print(x)
                    self.division_shapes.append(
                        cv.Circle(
                            x=x,
                            y=self.thumb.radius,
                            radius=self.thickness / 4,
                            paint=ft.Paint(color=color),
                        )
                    )

    def update_divisions(self):
        for division_shape in self.division_shapes:
            if division_shape.x < self.selected_track.width + self.thumb.radius:
                color = self.division_color_on_selected
            else:
                color = self.division_color_on_track
            division_shape.paint.color = color

    def find_closest_division_shape_x(self, x):
        previous_x = self.thumb.radius
        for division_shape in self.division_shapes:
            if x > division_shape.x:
                previous_x = division_shape.x
            else:
                if x - previous_x < division_shape.x - x:
                    return previous_x
                else:
                    return division_shape.x

        return self.track.width + self.thumb.radius

    def get_value(self, x):
        return (x - self.thumb.radius) * (
            self.max - self.min
        ) / self.track.width + self.min

    def change_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.CLICK
        e.control.update()

    def change_value_on_click(self, e: ft.DragStartEvent):
        x = max(self.thumb.radius, min(e.local_x, self.track.width + self.thumb.radius))
        print(x)
        if self.divisions == None:
            self.value = self.get_value(x)
            print(self.value)
            self.selected_track.width = x - self.thumb.radius
            self.thumb.x = x
        else:
            discreet_x = self.find_closest_division_shape_x(x)
            self.value = self.get_value(discreet_x)
            self.selected_track.width = discreet_x - self.thumb.radius
            self.thumb.x = discreet_x

        self.update_divisions()
        self.page.update()

    def change_value_on_drag(self, e: ft.DragUpdateEvent):
        x = max(
            self.thumb.radius,
            min(e.local_x + e.delta_x, self.track.width + self.thumb.radius),
        )
        if self.divisions == None:
            self.value = self.get_value(x)
            self.selected_track.width = x - self.thumb.radius
            self.thumb.x = x
        else:
            discreet_x = self.find_closest_division_shape_x(x)
            self.value = self.get_value(discreet_x)
            self.selected_track.width = discreet_x - self.thumb.radius
            self.thumb.x = discreet_x
        self.update_divisions()
        self.page.update()
