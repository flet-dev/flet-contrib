import flet as ft


class VerticalSplitter(ft.Row):
    def __init__(self, right_content, left_content, width, height, spacing):
        super().__init__(width=width, height=height, spacing=spacing)
        self.right_content = right_content
        self.left_content = left_content
        self.splitter = ft.GestureDetector(
            content=ft.VerticalDivider(),
            drag_interval=10,
            on_pan_update=self.move_vertical_splitter,
            on_hover=self.show_draggable_cursor,
        )
        self.controls = [self.right_content, self.splitter, self.left_content]

    def move_vertical_splitter(self, e: ft.DragUpdateEvent):
        if (e.delta_x > 0 and self.right_content.width < 300) or (
            e.delta_x < 0 and self.right_content.width > 100
        ):
            self.right_content.width += e.delta_x
        self.right_content.update()

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
        width=400, height=400, spacing=0, right_content=c_right, left_content=c_left
    )

    # page.add(
    #     ft.Row(
    #         controls=[
    #             c,
    #             ft.GestureDetector(
    #                 content=ft.VerticalDivider(),
    #                 drag_interval=10,
    #                 on_pan_update=move_vertical_divider,
    #                 on_hover=show_draggable_cursor,
    #             ),
    #             ft.Container(
    #                 bgcolor=ft.colors.BROWN_400,
    #                 alignment=ft.alignment.center,
    #                 expand=1,
    #             ),
    #         ],
    #         spacing=0,
    #         width=400,
    #         height=400,
    #     )
    # )

    page.add(vertical_splitter)


ft.app(target=main)
