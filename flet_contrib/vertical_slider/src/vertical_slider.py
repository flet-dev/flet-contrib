from enum import Enum
from typing import Optional
import flet as ft
import flet.canvas as cv


class VerticalSlider(ft.GestureDetector):
    def __init__(
        self,
        vertical=False,
        length=200,
        thickness=5,
        value=200,
        min=100,
        max=900,
        thumb=cv.Circle(
            radius=10,
            paint=ft.Paint(color=ft.colors.PRIMARY),
        ),
        divisions=None,
        track_color=ft.colors.OUTLINE_VARIANT,
        selected_track_color=ft.colors.PRIMARY,
        division_color_on_track=ft.colors.PRIMARY_CONTAINER,
        division_color_on_selected=ft.colors.OUTLINE,
    ):
        super().__init__()
        self.value = value
        self.vertical = vertical
        self.min = min
        self.max = max
        self.thickness = thickness
        self.length = length
        self.divisions = divisions
        self.track_color = track_color
        self.selected_track_color = selected_track_color
        self.division_color_on_track = division_color_on_track
        self.division_color_on_selected = division_color_on_selected
        self.thumb = thumb
        self.content = self.generate_slider()
        self.on_hover = self.change_cursor
        self.on_pan_start = self.change_value_on_click
        self.on_pan_update = self.change_value_on_drag

    def generate_slider(self):
        c = ft.Container(content=cv.Canvas(shapes=self.generate_shapes()))
        if self.vertical:
            c.height = self.length + self.thumb.radius * 2
            c.width = self.thumb.radius * 2
        else:
            c.width = (self.length + self.thumb.radius * 2,)
            c.height = (self.thumb.radius * 2,)
        return c

    def generate_shapes(self):
        if self.vertical:
            self.thumb.x = self.thumb.radius
            self.thumb.y = self.get_position(self.value)
            self.track = cv.Rect(
                x=self.thumb.radius - self.thickness / 2,
                y=self.thumb.radius,
                width=self.thickness,
                border_radius=self.thickness / 2,
                paint=ft.Paint(color=self.track_color),
                height=self.length,
            )
            self.selected_track = cv.Rect(
                x=self.thumb.radius - self.thickness / 2,
                y=self.thumb.y,
                width=self.thickness,
                border_radius=self.thickness / 2,
                paint=ft.Paint(color=self.selected_track_color),
                height=self.track.height + self.thumb.radius - self.thumb.y,
            )
        else:
            self.thumb.x = (
                self.value * self.length / (self.max - self.min) + self.thumb.radius
            )
            self.thumb.y = self.thumb.radius
            self.track = cv.Rect(
                x=self.thumb.radius,
                y=self.thumb.radius - self.thickness / 2,
                height=self.thickness,
                border_radius=self.thickness / 2,
                paint=ft.Paint(color=ft.colors.GREY_500),
                width=self.length,
            )
            self.selected_track = cv.Rect(
                x=self.thumb.radius,
                y=self.thumb.radius - self.thickness / 2,
                height=self.thickness,
                border_radius=self.thickness / 2,
                paint=ft.Paint(color=ft.colors.RED),
                width=self.value * self.length / (self.max - self.min)
                + self.thumb.radius,
            )
        self.generate_divisions()
        shapes = [self.track, self.selected_track] + self.division_shapes + [self.thumb]
        return shapes

    def generate_divisions(self):
        self.division_shapes = []
        if self.divisions == None:
            return
        else:
            if self.divisions > 1:
                for i in range(1, self.divisions):
                    if self.vertical:
                        y = (
                            self.track.height
                            + self.thumb.radius
                            - (self.track.height / self.divisions) * i
                        )
                        if y > self.get_position(self.value):
                            color = self.division_color_on_selected
                        else:
                            color = self.division_color_on_track
                        self.division_shapes.append(
                            cv.Circle(
                                y=y,
                                x=self.thumb.radius,
                                radius=self.thickness / 4,
                                paint=ft.Paint(color=color),
                            )
                        )

    def update_divisions(self):
        for division_shape in self.division_shapes:
            if self.vertical:
                if (
                    division_shape.y
                    < self.track.height - self.selected_track.height + self.thumb.radius
                ):
                    color = self.division_color_on_track
                else:
                    color = self.division_color_on_selected
            division_shape.paint.color = color

    def find_closest_division_shape_position(self, position):
        if self.vertical:
            previous_y = self.thumb.radius + self.track.height
            for division_shape in self.division_shapes:
                if position < division_shape.y:
                    previous_y = division_shape.y
                else:
                    if abs(previous_y - position) < abs(division_shape.y - position):
                        return previous_y
                    else:
                        return division_shape.y

        if abs(self.thumb.radius - position) < abs(previous_y - position):
            return self.thumb.radius
        else:
            return previous_y

    def get_value(self, position):
        if self.vertical:
            return self.max - (
                (position - self.thumb.radius)
                * (self.max - self.min)
                / self.track.height
            )

    def get_position(self, value):
        return self.thumb.radius + ((self.max - value) * self.length) / (
            self.max - self.min
        )

    def change_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.CLICK
        e.control.update()

    def update_thumb_position(self, position):
        self.value = self.get_value(position)
        print(f"Value: {self.value}")
        if self.vertical:
            self.selected_track.y = position
            self.selected_track.height = (
                self.track.height - position + self.thumb.radius
            )
            self.thumb.y = position

    def change_value_on_click(self, e: ft.DragStartEvent):
        if self.vertical:
            y = max(
                self.thumb.radius, min(e.local_y, self.track.height + self.thumb.radius)
            )
            if self.divisions == None:
                self.update_thumb_position(y)
            else:
                discrete_y = self.find_closest_division_shape_position(y)
                self.update_thumb_position(discrete_y)

        self.update_divisions()
        self.page.update()

    def change_value_on_drag(self, e: ft.DragUpdateEvent):
        if self.vertical:
            y = max(
                self.thumb.radius,
                min(e.local_y + e.delta_y, self.track.height + self.thumb.radius),
            )
            if self.divisions == None:
                self.update_thumb_position(y)
            else:
                discrete_y = self.find_closest_division_shape_position(y)
                self.update_thumb_position(discrete_y)
        self.update_divisions()
        self.page.update()


class HorizontalSlider(ft.GestureDetector):
    def __init__(
        self,
        length=200,
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
        self.length = length
        self.divisions = divisions
        self.division_color_on_track = division_color_on_track
        self.division_color_on_selected = division_color_on_selected
        self.thumb = thumb

        # shapes = self.generate_shapes()

        self.content = ft.Container(
            width=length + self.thumb.radius * 2,
            height=self.thumb.radius * 2,
            bgcolor=ft.colors.GREEN_100,
            content=cv.Canvas(shapes=self.generate_shapes()),
        )
        self.on_hover = self.change_cursor
        self.on_pan_start = self.change_value_on_click
        self.on_pan_update = self.change_value_on_drag

    def generate_shapes(self):
        self.thumb.x = (
            self.value * self.length / (self.max - self.min) + self.thumb.radius
        )
        self.thumb.y = self.thumb.radius
        self.track = cv.Rect(
            x=self.thumb.radius,
            y=self.thumb.radius - self.thickness / 2,
            height=self.thickness,
            border_radius=self.thickness / 2,
            paint=ft.Paint(color=ft.colors.GREY_500),
            width=self.length,
        )
        self.selected_track = cv.Rect(
            x=self.thumb.radius,
            y=self.thumb.radius - self.thickness / 2,
            height=self.thickness,
            border_radius=self.thickness / 2,
            paint=ft.Paint(color=ft.colors.RED),
            width=self.value * self.length / (self.max - self.min) + self.thumb.radius,
        )
        self.generate_divisions()
        shapes = [self.track, self.selected_track] + self.division_shapes + [self.thumb]
        return shapes

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
