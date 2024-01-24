import flet_core as ft
import flet_core.canvas as cv


class FlexibleSlider(ft.GestureDetector):
    def __init__(
        self,
        on_change=None,
        vertical=False,
        length=200,
        thickness=5,
        value=0.0,
        min=0.0,
        max=1.0,
        thumb_radius=10,
        thumb_color=ft.colors.PRIMARY,
        divisions=None,
        inactive_color=ft.colors.OUTLINE_VARIANT,
        active_color=ft.colors.PRIMARY,
        division_inactive_color=ft.colors.PRIMARY_CONTAINER,
        division_active_color=ft.colors.OUTLINE,
    ):
        super().__init__()
        self.value = value
        self.on_change = on_change
        self.vertical = vertical
        self.min = min
        self.max = max
        self.thickness = thickness
        self.length = length
        self.thumb_radius = thumb_radius
        self.thumb_color = thumb_color
        self.divisions = divisions
        self.track_color = inactive_color
        self.selected_track_color = active_color
        self.division_color_on_track = division_inactive_color
        self.division_color_on_selected = division_active_color
        self.content = self.generate_slider()
        self.on_hover = self.change_cursor
        self.on_pan_start = self.change_value_on_click
        self.on_pan_update = self.change_value_on_drag

    def generate_slider(self):
        c = ft.Container(content=cv.Canvas(shapes=self.generate_shapes()))
        if self.vertical:
            c.height = self.length + self.thumb_radius * 2
            c.width = max(self.thickness, self.thumb.radius * 2)
        else:
            c.width = self.length + self.thumb_radius * 2
            c.height = max(self.thickness, self.thumb_radius * 2)
        return c

    def generate_shapes(self):
        # thumb
        self.thumb = cv.Circle(
            radius=self.thumb_radius,
            paint=ft.Paint(color=self.thumb_color),
        )

        self.track = cv.Rect(
            border_radius=self.thickness / 2,
            paint=ft.Paint(color=self.track_color),
        )
        self.selected_track = cv.Rect(
            border_radius=self.thickness / 2,
            paint=ft.Paint(color=self.selected_track_color),
        )

        if self.vertical:
            self.thumb.x = self.thumb_radius
            self.thumb.y = self.get_position(self.value)
            self.track.x = self.thumb_radius - self.thickness / 2
            self.track.y = self.thumb_radius
            self.track.width = self.thickness
            self.track.height = self.length
            self.selected_track.x = self.thumb_radius - self.thickness / 2
            self.selected_track.y = self.thumb.y
            self.selected_track.width = self.thickness
            self.selected_track.height = self.length + self.thumb_radius - self.thumb.y

        else:
            self.thumb.x = self.get_position(self.value)
            self.thumb.y = self.thumb_radius
            self.track.x = self.thumb_radius
            self.track.y = self.thumb_radius - self.thickness / 2
            self.track.width = self.length
            self.track.height = self.thickness
            self.selected_track.x = self.thumb_radius
            self.selected_track.y = self.thumb_radius - self.thickness / 2
            self.selected_track.width = (
                self.value * self.length / (self.max - self.min) + self.thumb_radius
            )
            self.selected_track.height = self.thickness

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
                            self.length
                            + self.thumb_radius
                            - (self.length / self.divisions) * i
                        )
                        if y > self.get_position(self.value):
                            color = self.division_color_on_selected
                        else:
                            color = self.division_color_on_track
                        self.division_shapes.append(
                            cv.Circle(
                                y=y,
                                x=self.thumb_radius,
                                radius=self.thickness / 4,
                                paint=ft.Paint(color=color),
                            )
                        )
                    else:
                        x = (self.length / self.divisions) * i + self.thumb_radius
                        if x < self.selected_track.width + self.thumb_radius:
                            color = self.division_color_on_selected
                        else:
                            color = self.division_color_on_track
                        self.division_shapes.append(
                            cv.Circle(
                                x=x,
                                y=self.thumb_radius,
                                radius=self.thickness / 4,
                                paint=ft.Paint(color=color),
                            )
                        )

    def update_divisions(self):
        for division_shape in self.division_shapes:
            if self.vertical:
                if (
                    division_shape.y
                    < self.length - self.selected_track.height + self.thumb_radius
                ):
                    color = self.division_color_on_track
                else:
                    color = self.division_color_on_selected
            else:
                if division_shape.x < self.selected_track.width + self.thumb_radius:
                    color = self.division_color_on_selected
                else:
                    color = self.division_color_on_track
            division_shape.paint.color = color

    def find_closest_division_shape_position(self, position):
        if self.vertical:
            previous_y = self.thumb_radius + self.length
            for division_shape in self.division_shapes:
                if position < division_shape.y:
                    previous_y = division_shape.y
                else:
                    if abs(previous_y - position) < abs(division_shape.y - position):
                        return previous_y
                    else:
                        return division_shape.y

            if abs(self.thumb_radius - position) < abs(previous_y - position):
                return self.thumb_radius
            else:
                return previous_y
        else:
            previous_x = self.thumb_radius
            for division_shape in self.division_shapes:
                if position > division_shape.x:
                    previous_x = division_shape.x
                else:
                    if abs(position - previous_x) < abs(division_shape.x - position):
                        return previous_x
                    else:
                        return division_shape.x
            if abs(previous_x - position) < abs(
                self.length + self.thumb_radius - position
            ):
                return previous_x
            else:
                return self.length + self.thumb_radius

    def get_value(self, position):
        if self.vertical:
            return self.max - (
                (position - self.thumb_radius) * (self.max - self.min) / self.length
            )
        else:
            return (position - self.thumb_radius) * (
                self.max - self.min
            ) / self.length + self.min

    def get_position(self, value):
        if self.vertical:
            return self.thumb_radius + ((self.max - value) * self.length) / (
                self.max - self.min
            )
        else:
            return value * self.length / (self.max - self.min) + self.thumb_radius

    def change_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.CLICK
        e.control.update()

    def move_thumb(self, position):
        self.value = self.get_value(position)
        # print(f"Value: {self.value}")
        if self.vertical:
            self.selected_track.y = position
            self.selected_track.height = (
                self.track.height - position + self.thumb_radius
            )
            self.thumb.y = position
        else:
            self.selected_track.width = position - self.thumb_radius
            self.thumb.x = position

    def update_slider(self, position):
        if self.divisions == None:
            self.move_thumb(position)
        else:
            discrete_position = self.find_closest_division_shape_position(position)
            self.move_thumb(discrete_position)
        self.update_divisions()
        if self.on_change is not None:
            self.on_change()
        self.update()

    def change_value_on_click(self, e: ft.DragStartEvent):
        if self.vertical:
            position = max(
                self.thumb_radius, min(e.local_y, self.length + self.thumb_radius)
            )
        else:
            position = max(
                self.thumb_radius, min(e.local_x, self.length + self.thumb_radius)
            )
        self.update_slider(position)
        self.update()

    def change_value_on_drag(self, e: ft.DragUpdateEvent):
        if self.vertical:
            position = max(
                self.thumb_radius,
                min(e.local_y + e.delta_y, self.length + self.thumb_radius),
            )
        else:
            position = max(
                self.thumb_radius,
                min(e.local_x + e.delta_x, self.length + self.thumb_radius),
            )
        self.update_slider(position)
        self.update()
