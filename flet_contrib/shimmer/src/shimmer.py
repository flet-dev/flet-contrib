import asyncio
import threading
import time

import flet_core as ft


class Shimmer(ft.Container):
    def __init__(
        self,
        ref=None,
        control=None,
        color=None,
        color1=None,
        color2=None,
        height=None,
        width=None,
        auto_generate: bool = False,
    ) -> None:
        super().__init__()

        self.color = color
        self.color1 = color1
        self.color2 = color2
        self.height = height
        self.width = width

        if ref is None:
            self.ref = ft.Ref[ft.ShaderMask]()
        else:
            self.ref = ref

        if self.color1 is None and self.color2 is None and self.color is None:
            self.__color1 = ft.colors.BACKGROUND
            self.__color2 = ft.colors.with_opacity(0.5, ft.colors.BACKGROUND)
        elif self.color is not None:
            self.__color1 = self.color
            self.__color2 = ft.colors.with_opacity(0.5, self.color)
        elif self.color1 is not None and self.color2 is not None:
            self.__color1 = self.color1
            self.__color2 = ft.colors.with_opacity(0.5, self.color2)
        if auto_generate:
            self.control = self.create_dummy(control)
        else:
            self.control = control

        self.__stop_shine = False

        self.i = -0.1
        self.gap = 0.075

    def build(self):
        gradient = ft.LinearGradient(
            colors=[self.__color2, self.__color1, self.__color2],
            stops=[
                0 + self.i - self.gap,
                self.i,
                self.gap + self.i,
            ],
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
        )

        self.__shadermask = ft.ShaderMask(
            ref=self.ref,
            content=self.control,
            blend_mode=ft.BlendMode.DST_IN,
            height=self.height,
            width=self.width,
            shader=gradient,
        )

        self.content = self.__shadermask
        self.bgcolor = self.__color1

    async def shine_async(self):
        try:
            while self.i <= 5:
                gradient = ft.LinearGradient(
                    colors=[self.__color2, self.__color1, self.__color2],
                    stops=[
                        0 + self.i - self.gap,
                        self.i,
                        self.gap + self.i,
                    ],
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                )
                self.ref.current.shader = gradient
                self.ref.current.update()
                self.i += 0.02
                if self.i >= 1.1:
                    self.i = -0.1
                    await asyncio.sleep(0.4)
                await asyncio.sleep(0.01)
        except:
            pass

    def create_dummy(self, target=None):
        opacity = 0.1
        color = ft.colors.ON_PRIMARY_CONTAINER
        circle = lambda size=60: ft.Container(
            height=size,
            width=size,
            bgcolor=ft.colors.with_opacity(opacity, color),
            border_radius=size,
        )
        rectangle = lambda height, content=None: ft.Container(
            content=content,
            height=height,
            width=height * 2.5,
            bgcolor=ft.colors.with_opacity(opacity, color),
            border_radius=20,
            alignment=ft.alignment.bottom_center,
            padding=20,
        )
        tube = lambda width: ft.Container(
            height=10,
            width=width,
            bgcolor=ft.colors.with_opacity(opacity, color),
            border_radius=20,
            expand=0,
        )

        if target is None:
            target = self.control
        controls, content, title, subtitle, leading, trailing = (
            False,
            False,
            False,
            False,
            False,
            False,
        )
        ctrl_name = target._get_control_name()
        for key in list(ft.__dict__.keys())[::-1]:
            if key.lower() == ctrl_name and key != ctrl_name:
                dummy = ft.__dict__[key]()

        if ctrl_name in ["text"] and target.data == "shimmer_load":
            dummy = tube(len(target.__dict__["_Control__attrs"]["value"][0]) * 7.5)
        elif ctrl_name in ["textbutton"] and target.data == "shimmer_load":
            dummy = rectangle(40)
        elif ctrl_name in ["icon"] and target.data == "shimmer_load":
            dummy = circle(30)
        elif ctrl_name in ["image"] and target.data == "shimmer_load":
            dummy = ft.Container(
                bgcolor=ft.colors.with_opacity(opacity, color), expand=True
            )
        elif ctrl_name in ["image"]:
            dummy = ft.Container(expand=True)

        for key in list(target.__dict__.keys())[::-1]:
            if (
                key.lower().split("__")[-1] == "controls"
                and target.__dict__[key] is not None
            ):
                controls = True
            elif (
                key.lower().split("__")[-1] == "content"
                and target.__dict__[key] is not None
            ):
                content = True
            elif (
                key.lower().split("__")[-1] == "title"
                and target.__dict__[key] is not None
            ):
                title = True
            elif (
                key.lower().split("__")[-1] == "subtitle"
                and target.__dict__[key] is not None
            ):
                subtitle = True
            elif (
                key.lower().split("__")[-1] == "leading"
                and target.__dict__[key] is not None
            ):
                leading = True
            elif (
                key.lower().split("__")[-1] == "trailing"
                and target.__dict__[key] is not None
            ):
                trailing = True

        ctrl_attrs = target.__dict__["_Control__attrs"]
        if ctrl_attrs is not None:
            for each_pos in ctrl_attrs.keys():
                if each_pos not in [
                    "text",
                    "value",
                    "label",
                    "foregroundimageurl",
                    "bgcolor",
                    "name",
                    "color",
                    "icon",
                    "src",
                    "src_base64",
                ]:
                    try:
                        dummy._set_attr(each_pos, ctrl_attrs[each_pos][0])
                    except Exception as e:
                        print("EXCEPTION", e, ctrl_name, each_pos)

        for each_pos in target.__dict__:
            if target.__dict__[each_pos] is not None:
                pos = each_pos.split("__")[-1]
                if pos == "rotate":
                    dummy.rotate = target.__dict__[each_pos]
                elif pos == "scale":
                    dummy.scale = target.__dict__[each_pos]
                elif pos == "border_radius":
                    dummy.border_radius = target.__dict__[each_pos]
                elif pos == "alignment":
                    dummy.alignment = target.__dict__[each_pos]
                elif pos == "padding":
                    dummy.padding = target.__dict__[each_pos]
                elif pos == "horizontal_alignment":
                    dummy.horizontal_alignment = target.__dict__[each_pos]
                elif pos == "vertical_alignment":
                    dummy.vertical_alignment = target.__dict__[each_pos]
                elif pos == "top":
                    dummy.top = target.__dict__[each_pos]
                elif pos == "bottom":
                    dummy.bottom = target.__dict__[each_pos]
                elif pos == "left":
                    dummy.left = target.__dict__[each_pos]
                elif pos == "right":
                    dummy.right = target.__dict__[each_pos]
                elif pos == "rows":
                    dummy.rows = [
                        ft.DataRow(
                            [
                                ft.DataCell(tube(100))
                                if each_col.content.data == "shimmer_load"
                                else ft.DataCell(ft.Text())
                                for each_col in each_control.cells
                            ]
                        )
                        for each_control in target.__dict__[each_pos]
                    ]
                elif pos == "columns":
                    dummy.columns = [
                        ft.DataColumn(tube(100))
                        if each_control.label.data == "shimmer_load"
                        else ft.DataColumn(ft.Text())
                        for each_control in target.__dict__[each_pos]
                    ]

        if content:
            dummy.content = self.create_dummy(target.content)
        if title:
            dummy.title = self.create_dummy(target.title)
        if subtitle:
            dummy.subtitle = self.create_dummy(target.subtitle)
        if leading:
            dummy.leading = self.create_dummy(target.leading)
        if trailing:
            dummy.trailing = self.create_dummy(target.trailing)
        if controls:
            try:
                dummy.controls = [
                    self.create_dummy(each_control) for each_control in target.controls
                ]
            except Exception as e:
                print(e)
                temp = []
                for each_control in target.controls:
                    try:
                        temp.append(self.create_dummy(each_control))
                    except Exception as e:
                        pass
                dummy.controls = temp

        if target.data == "shimmer_load":
            dummy.bgcolor = ft.colors.with_opacity(opacity, color)
        return ft.Container(ft.Stack([dummy]), bgcolor=self.__color1)

    def did_mount(self):
        self.task = self.page.run_task(self.shine_async)

    def will_unmount(self):
        self.task.cancel()
        
