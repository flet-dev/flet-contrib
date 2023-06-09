# VerticalSplitter

`VerticalSplitter` control is used for building layout with left and right panes divided by a vertical line that can be dragged in the left and/or right direction.

`VerticalSplitter` inherits from [`Row`](https://flet.dev/docs/controls/row).

## Examples

[Live example](https://flet-controls-gallery.fly.dev/contrib/verticalsplitter)

### VerticalSplitter example

```python
import flet as ft

from flet_contrib.vertical_splitter import VerticalSplitter, FixedPane


def main(page: ft.Page):
    c_left = ft.Container(bgcolor=ft.colors.BLUE_400)

    c_right = ft.Container(bgcolor=ft.colors.YELLOW_400)

    vertical_splitter = VerticalSplitter(
        # height=400,
        expand=True,
        right_pane=c_right,
        left_pane=c_left,
        fixed_pane_min_width=200,
        fixed_pane_width=300,
        fixed_pane_max_width=400,
        fixed_pane=FixedPane.RIGHT,
    )

    page.add(vertical_splitter)


ft.app(target=main)
```

## Properties

### `left_pane`

A child Control contained by the left pane of the vertical splitter.

### `right_pane`

A child Control contained by the right pane of the vertical splitter.

### `fixed_pane`

Configures which pane will have a `fixed_pane_width`, `fixed_pane_minumum_width` and `fixed_pane_maximum_width` properties, while the other pane will have `expand` property set to `True` and will take up the remainer of the VerticalSpliitter width. The value must be an instance of the `FixedPane` class:

```
vertical_splitter.fixed_pane = FixedPane.RIGHT
```
The default value is `FixedPane.LEFT`.

### `fixed_pane_width`

Width in virtual pixels of `left_pane` or `right_pane` container, depending on the `fixed_pane` property. 

The default value is `100`.

### `fixed_pane_min_width`

Minimum width in virtual pixels of `left_pane` or `right_pane` container when dragging the splitter, depending on the `fixed_pane` property. 

The default value is `50`.


### `fixed_pane_max_width`

Maximum width in virtual pixels of `left_pane` or `right_pane` container when dragging the splitter, depending on the `fixed_pane` property. 

The default value is `200`.