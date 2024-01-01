# import os, sys
# sys.path.append(os.getcwd())
import flet as ft
import time, asyncio, threading
class Shimmer(ft.UserControl):
    """
    Shimmer (Class) - To auto generate dummy controls and create shimmer loading effect.
    """
    def __init__(self, ref: ft.Ref = None, control: ft.Control = None, color: ft.colors = None, color1: ft.colors = None, color2 = None, height = None, width = None, full: bool = True, auto_generate: bool = False) -> None:
        super().__init__()
        if auto_generate:
            self.control = self.create_dummy(control)#control
        else: self.control = control
        self.color = color
        self.color1 = color1
        self.color2 = color2
        if height is None: self.height = self.control.height
        else: self.height = height
        if self.width is None: self.width = self.control.width
        else: self.width = width
        self.full = full
        if ref is None: self.ref = ft.Ref[ft.ShaderMask]()
        else: self.ref = ref
        # self.__async = True
        self.__stop_shine = False

    def build(self):
        self.i = -0.1
        self.gap = 0.075

        if self.color1 is None and self.color2 is None and self.color is None:
            self.__color1 = ft.colors.TRANSPARENT
            self.__color2 = ft.colors.BACKGROUND#ft.colors.with_opacity(0.75,ft.colors.BACKGROUND)
        elif self.color is not None:
            self.__color1 = self.color
            self.__color2 = ft.colors.with_opacity(0.5,self.color)
        elif self.color1 is not None and self.color2 is not None:
            self.__color1 = self.color1
            self.__color2 = ft.colors.with_opacity(0.5,self.color2)

        self.__shadermask = ft.ShaderMask(ref= self.ref)
        self.__shadermask.content = self.control
        self.__shadermask.blend_mode = ft.BlendMode.DST_IN
        self.__shadermask.height = self.height
        self.__shadermask.width = self.width

        gradient = ft.LinearGradient(colors = [self.__color2, self.__color1, self.__color2])
        gradient.stops = [0 + self.i - self.gap, self.i, self.gap + self.i, ]
        gradient.begin = ft.alignment.top_left
        gradient.end = ft.alignment.bottom_right
        self.__shadermask.shader = gradient
        return self.__shadermask
        
    async def shine_async(self):
        i = -0.1
        gap = 0.075
        gradient = ft.LinearGradient(colors = [self.__color2, self.__color1, self.__color2])
        gradient.stops = [0+i-gap,i,gap+i,]
        gradient.begin = ft.alignment.top_left
        gradient.end = ft.alignment.bottom_right

        while i <= 5:
            gradient.stops = [0+i-gap,i,gap+i,]
            self.ref.current.shader = gradient
            await self.ref.current.update_async()
            i += 0.02
            if i >= 1.1:
                i = -0.1
                time.sleep(0.2)
            if self.full:
                time.sleep(0.01)
            else:
                time.sleep(0.003)
    def shine(self):
        i = -0.1
        gap = 0.075
        gradient = ft.LinearGradient(colors = [self.__color2, self.__color1, self.__color2])
        gradient.stops = [0+i-gap,i,gap+i,]
        gradient.begin = ft.alignment.top_left
        gradient.end = ft.alignment.bottom_right
        # invert = True
        while i <= 5 and not self.__stop_shine:
            gradient.stops = [0+i-gap,i,gap+i,]
            self.ref.current.shader = gradient
            self.ref.current.update()
            i += 0.02
            if i >= 1.1:
                i = -0.1
                time.sleep(0.2)
            time.sleep(0.01)
            
    def create_dummy(self,target = None):
        opacity = 0.1
        color = ft.colors.ON_PRIMARY_CONTAINER
        circle = lambda size = 60: ft.Container(height=size, width=size, bgcolor= ft.colors.with_opacity(opacity, color), border_radius= size)
        rectangle = lambda height, content = None: ft.Container(content= content, height= height, width= height * 2.5, bgcolor= ft.colors.with_opacity(opacity, color), border_radius= 20, alignment= ft.alignment.bottom_center, padding= 20)
        tube = lambda width: ft.Container(height= 10, width= width, bgcolor= ft.colors.with_opacity(opacity,color), border_radius= 20, expand= 0)

        if target is None:
            target = self.control
        controls, content, title, subtitle, leading, trailing = False, False, False, False, False, False
        ctrl_name = target._get_control_name()
        # print('..................................', ctrl_name)
        for key in list(ft.__dict__.keys())[::-1]:
            if key.lower() == ctrl_name and key != ctrl_name:
                dummy = ft.__dict__[key]()
    
        if ctrl_name in ['text'] and target.data == 'shimmer_load':
            # print(target.__dict__['_Control__attrs']['value'][0])
            dummy = tube(len(target.__dict__['_Control__attrs']['value'][0])*7.5)
        elif ctrl_name in ['textbutton'] and target.data == 'shimmer_load':
            dummy = rectangle(30)
        elif ctrl_name in ['icon'] and target.data == 'shimmer_load':
            dummy = circle(30)
        elif ctrl_name in ['image'] and target.data == 'shimmer_load':
            dummy = rectangle(100)

        for key in list(target.__dict__.keys())[::-1]:
            if key.lower().split('__')[-1] == 'controls' and target.__dict__[key] is not None:
                controls = True
            elif key.lower().split('__')[-1] == 'content' and target.__dict__[key] is not None:
                content = True
            elif key.lower().split('__')[-1] == 'title' and target.__dict__[key] is not None:
                title = True
            elif key.lower().split('__')[-1] == 'subtitle' and target.__dict__[key] is not None:
                subtitle = True
            elif key.lower().split('__')[-1] == 'leading' and target.__dict__[key] is not None:
                leading = True
            elif key.lower().split('__')[-1] == 'trailing' and target.__dict__[key] is not None:
                trailing = True
            
        ctrl_attrs = target.__dict__['_Control__attrs']
        if ctrl_attrs is not None:
            for each_pos in ctrl_attrs.keys():
                if each_pos not in ['text','value','label',
                                    'foregroundimageurl','bgcolor',
                                    'name','color','icon','src']:
                    # print(each_pos,ctrl_attrs[each_pos], 'ATTRS')
                    try:
                        dummy._set_attr(each_pos,ctrl_attrs[each_pos][0])
                    except Exception as e: print('EXCEPTION', e, ctrl_name, each_pos)

        for each_pos in target.__dict__:
            if target.__dict__[each_pos] is not None:
                pos = each_pos.split('__')[-1]
                # if pos in ['rotate','scale','border_radius','alignment','horizontal_alignment',
                #            'vertical_alignment','top','bottom','left','right','rows','columns','label', 'cells']:
                #     print(pos, each_pos,target.__dict__[each_pos])
                if pos == 'rotate':
                    dummy.rotate = target.__dict__[each_pos]
                elif pos == 'scale':
                    dummy.scale = target.__dict__[each_pos]
                elif pos == 'border_radius':
                    dummy.border_radius = target.__dict__[each_pos]
                elif pos == 'alignment':
                    dummy.alignment = target.__dict__[each_pos]
                elif pos == 'padding':
                    dummy.padding = target.__dict__[each_pos]
                elif pos == 'horizontal_alignment':
                    dummy.horizontal_alignment = target.__dict__[each_pos]
                elif pos == 'vertical_alignment':
                    dummy.vertical_alignment = target.__dict__[each_pos]
                elif pos == 'top':
                    dummy.top = target.__dict__[each_pos]
                elif pos == 'bottom':
                    dummy.bottom = target.__dict__[each_pos]
                elif pos == 'left':
                    dummy.left = target.__dict__[each_pos]
                elif pos == 'right':
                    dummy.right = target.__dict__[each_pos]
                elif pos == 'rows':
                    dummy.rows = [ft.DataRow([ft.DataCell(tube(100)) if each_col.content.data == 'shimmer_load' else ft.DataCell(ft.Text()) for each_col in each_control.cells]) for each_control in target.__dict__[each_pos]]
                elif pos == 'columns':
                    # dt_col = target.__dict__[each_pos]
                    dummy.columns = [ft.DataColumn(tube(100)) if each_control.label.data == 'shimmer_load' else ft.DataColumn(ft.Text()) for each_control in target.__dict__[each_pos]]
                # else:
                #     print(pos, None)
                
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
            dummy.controls = [self.create_dummy(each_control) for each_control in target.controls]
        
        if target.data == 'shimmer_load':
            dummy.bgcolor = ft.colors.with_opacity(opacity,color)
    
        return dummy
    def start_async(self):
        self.task = asyncio.ensure_future(self.shine_async())
    
    def start(self):
        self.__stop_shine = False
        self.__thread = threading.Thread(target= self.shine)    
        self.__thread.start()
            
    def stop_async(self):
        self.task.cancel()
    
    def stop(self):
        self.__stop_shine = True
        
    