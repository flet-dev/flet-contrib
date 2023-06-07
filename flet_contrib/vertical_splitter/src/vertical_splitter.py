import flet as ft


class VerticalSplitter(ft.Row):
    def __init__(
        self,
        right_pane,
        left_pane,
        height,
        spacing,
        min_width,
        max_width,
        width=None,
    ):
        super().__init__(width=width, height=height, spacing=spacing)
        self.right_pane = right_pane
        self.left_pane = left_pane
        self.min_width = min_width
        self.max_width = max_width
        self.splitter = ft.GestureDetector(
            content=ft.VerticalDivider(),
            drag_interval=10,
            on_pan_update=self.move_vertical_splitter,
            on_hover=self.show_draggable_cursor,
        )
        self.controls = [
            ft.Container(self.right_pane),
            self.splitter,
            self.left_pane,
        ]

    def move_vertical_splitter(self, e: ft.DragUpdateEvent):
        if (e.delta_x > 0 and self.right_pane.width < self.max_width) or (
            e.delta_x < 0 and self.right_pane.width > self.min_width
        ):
            self.right_pane.width += e.delta_x
        self.right_pane.update()

    def show_draggable_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()


def main(page: ft.Page):
    def show_draggable_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    c_right = ft.Container(
        bgcolor=ft.colors.ORANGE_300,
        alignment=ft.alignment.center,
        width=100,
        # expand=1,
    )

    c_left = ft.Container(
        bgcolor=ft.colors.BROWN_400,
        alignment=ft.alignment.center,
        # width=100,
        expand=1,
    )

    vertical_splitter = VerticalSplitter(
        height=400,
        spacing=0,
        right_pane=c_right,
        left_pane=c_left,
        min_width=50,
        max_width=300,
    )

    page.add(vertical_splitter)


ft.app(target=main)
