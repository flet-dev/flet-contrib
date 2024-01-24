from enum import Enum
from typing import Optional

import flet_core as ft


class FixedPane(Enum):
    RIGHT = "right"
    LEFT = "left"


class VerticalSplitter(ft.Row):
    def __init__(
        self,
        right_pane: Optional[ft.Control],
        left_pane: Optional[ft.Control],
        spacing=0,
        fixed_pane_min_width=50,
        fixed_pane_max_width=200,
        fixed_pane_width=100,
        fixed_pane: FixedPane = FixedPane.LEFT,
        width=None,
        height=400,
        expand=False,
    ):
        super().__init__(width=width, height=height, spacing=spacing, expand=expand)
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
        self.left_container = ft.Container(content=left_pane)
        self.right_container = ft.Container(content=right_pane)
        if self.fixed_pane == FixedPane.LEFT:
            self.left_container.width = self.fixed_pane_width
            self.right_container.expand = 1

        elif self.fixed_pane == FixedPane.RIGHT:
            self.right_container.width = self.fixed_pane_width
            self.left_container.expand = 1

        self.controls = [
            self.left_container,
            self.splitter,
            self.right_container,
        ]

    def move_vertical_splitter(self, e: ft.DragUpdateEvent):
        if self.fixed_pane == FixedPane.LEFT:
            if e.control.mouse_cursor == ft.MouseCursor.RESIZE_LEFT_RIGHT and (
                (
                    e.delta_x > 0
                    and self.left_container.width + e.delta_x
                    < self.fixed_pane_max_width
                )
                or (
                    e.delta_x < 0
                    and self.left_container.width + e.delta_x
                    > self.fixed_pane_min_width
                )
            ):
                self.left_container.width += e.delta_x
            self.left_container.update()

        if self.fixed_pane == FixedPane.RIGHT:
            if (
                e.delta_x > 0
                and self.right_container.width - e.delta_x > self.fixed_pane_min_width
            ) or (
                e.delta_x < 0
                and self.right_container.width - e.delta_x < self.fixed_pane_max_width
            ):
                self.right_container.width -= e.delta_x
            self.right_container.update()

    def show_draggable_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()
