# Shimmer Loading Effect
`Shimmer` control is used to create shimmer loading effect.

Also this control has the ability to auto generate dummy boxes that appears in the shimmer effect. To achieve it we have pass `auto_generate = True` to Shimmer and set `data = 'shimmer_load` to all those controls for which we want to create dummy boxes. 

This control can create shimmer effect either individually for one control or commonly for whole page.
Default `full = True` - common shimmer effect, Make it `False` for individual effect

This control also accept custom dummy boxes. We just need to pass a custom created dummy box to `control` parameter and set `auto_generate = False`

When height and width for shimmer effect is not given, Shimmer takes the size of given control.

Use params `color1` and `color2` to create dual color shimmer effect.
Use param `color` to create effect with variants of same root color.

## Example - Async, Common effect

```python
import asyncio
import flet as ft
from flet_contrib.shimmer import Shimmer
async def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    holder = ft.Container()
    await page.add_async(holder)
    lt = ft.ListTile()
    lt.leading = ft.Icon(ft.icons.ALBUM, data = 'shimmer_load') # data = 'shimmer_load' inform the Shimmer class to create dummy for this control
    lt.title = ft.Text("The Enchanted Nightingale", data = 'shimmer_load')
    lt.subtitle = ft.Text("Music by Julie Gable. Lyrics by Sidney Stein.", data = 'shimmer_load')
    
    row = ft.Row()
    row.alignment = ft.MainAxisAlignment.END
    row.controls.append(ft.TextButton("Buy tickets", data = 'shimmer_load'))
    row.controls.append(ft.TextButton("Listen", data = 'shimmer_load'))
    
    column = ft.Column()
    column.controls = [lt, row]
    
    container = ft.Container()
    container.content = column
    container.height = 130
    container.width = 400
    container.padding = 10
    
    card = ft.Card()
    card.content = container

    ctrl = ft.Column([card for i in range(5)])

    dummy = Shimmer(control=ctrl, auto_generate= True) # passing ctrl to Shimmer
    holder.content = dummy
    await holder.update_async()

    dummy.start_async() # start effect

    await asyncio.sleep(3) # assume this to be any data fetching task 
    
    dummy.stop_async() # stop effect

    holder.content = ctrl
    await holder.update_async()

ft.app(target=main)
```

## Output of above code
<video src="media/shimmer_common_async.mp4" width="320" height="640" autoplay></video>



