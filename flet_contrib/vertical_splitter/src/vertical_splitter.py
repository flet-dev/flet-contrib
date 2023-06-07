import flet as ft


class VerticalSplitter(ft.Row):
    def __init__(
        self,
        right_pane,
        left_pane,
        height,
        spacing,
        fixed_pane_min_width=50,
        fixed_pane_max_width=300,
        fixed_pane_width=100,
        fixed_pane="left",
        width=None,
    ):
        super().__init__(width=width, height=height, spacing=spacing)
        # self.right_pane = right_pane
        # self.left_pane = left_pane
        self.fixed_pane_min_width = fixed_pane_min_width
        self.fixed_pane_max_width = fixed_pane_max_width
        self.fixed_pane_width = fixed_pane_width
        self.fixed_pane = fixed_pane
        self.splitter = ft.GestureDetector(
            content=ft.VerticalDivider(),
            drag_interval=10,
            on_pan_update=self.move_vertical_splitter,
            on_hover=self.show_draggable_cursor,
        )
        self.generate_layout(left_pane, right_pane)

    def generate_layout(self, left_pane, right_pane):
        if self.fixed_pane == "left":
            self.left_container = ft.Container(
                width=self.fixed_pane_width, content=left_pane
            )
            self.right_container = ft.Container(expand=1, content=right_pane)
        elif self.fixed_pane == "right":
            self.left_container = ft.Container(expand=1, content=left_pane)
            self.right_container = ft.Container(
                width=self.fixed_pane_width, content=right_pane
            )

        self.controls = [
            self.left_container,
            self.splitter,
            self.right_container,
        ]

    def move_vertical_splitter(self, e: ft.DragUpdateEvent):
        if self.fixed_pane == "right":
            if (
                e.delta_x > 0 and self.right_pane.width > self.fixed_pane_min_width
            ) or (e.delta_x < 0 and self.right_pane.width < self.fixed_pane_max_width):
                self.right_pane.width += e.delta_x
            self.right_pane.update()
        elif self.fixed_pane == "left":
            if (
                e.delta_x > 0 and self.left_container.width < self.fixed_pane_max_width
            ) or (
                e.delta_x < 0 and self.left_container.width > self.fixed_pane_min_width
            ):
                self.left_container.width += e.delta_x
            self.left_container.update()

    def show_draggable_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()


def main(page: ft.Page):
    def show_draggable_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    c_left = ft.Container(
        bgcolor=ft.colors.ORANGE_300,
        alignment=ft.alignment.center,
        # width=100,
        # expand=1,
    )

    c_right = ft.Container(
        bgcolor=ft.colors.BROWN_400,
        alignment=ft.alignment.center,
        # width=100,
        # expand=1,
    )

    vertical_splitter = VerticalSplitter(
        height=400,
        spacing=0,
        right_pane=c_right,
        left_pane=c_left,
        fixed_pane="left",
        fixed_pane_min_width=50,
        fixed_pane_max_width=300,
        fixed_pane_width=100,
    )

    page.add(vertical_splitter)


ft.app(target=main)
