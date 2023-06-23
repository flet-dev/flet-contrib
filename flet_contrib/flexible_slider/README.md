# VerticalSlider

`FlexibleSlider` can be configured to be horizontal or vertical.

`FlexibleSlider` inherits from [`GestureDetector`](https://flet.dev/docs/controls/gesturedetector).

## Examples

[Live example](https://flet-controls-gallery.fly.dev/contrib/flexibleslider)

### Vertical slider example

```python
import flet as ft

from flet_contrib.flexible_slider import FlexibleSlider


def main(page: ft.Page):
    def vertical_slider_changed():
        print(vertical_slider.value)

    vertical_slider = FlexibleSlider(
        vertical=True,
        divisions=10,
        min=100,
        max=600,
        value=500,
        on_change=vertical_slider_changed,
    )

    page.add(
        vertical_slider,
    )


ft.app(target=main)
```

## Properties

### `vertical`

If `vertical` property is `False`, the slider will be displayed horuzontally and if it set to `True`, the slider will be displated vertically. 

The detault value is `False`.

### `length`

Length of the slider track in virtual pixels.

The default value is `200`.

### `thickness`

Thickness of the slider track in virtual pixels.

The default value is `5`.

### `active_color`

The [color](https://flet.dev/docs/guides/python/colors/) to use for the portion of the slider track that is active.

The "active" side of the slider is the side between the thumb and the minimum value.

The default value is `ft.colors.PRIMARY`.

### `inactive_color`

The [color](https://flet.dev/docs/guides/python/colors/) for the inactive portion of the slider track.

The "inactive" side of the slider is the side between the thumb and the maximum value.

The default value is `ft.colors.OUTLINE_VARIANT`.

### `divisions`

The number of discrete divisions.

If not set, the slider is continuous.

### `division_active_color`

The [color](https://flet.dev/docs/guides/python/colors/) to use for the division shapes displayed on the slider track that is active.

The default value is `ft.colors.OUTLINE`.

### `division_inactive_color`

The [color](https://flet.dev/docs/guides/python/colors/) to use for the division shapes displayed on the slider track that is inactive.

The default value is `ft.colors.PRIMARY_CONTAINER`.

### `thumb_radius`

Thumb radius in virtual pixels. 

The default value is `10`.


### `thumb_color`

The color of the thumb.

The default value is `ft.colors.PRIMARY`.

### `value`

The currently selected value for this slider.

The slider's thumb is drawn at a position that corresponds to this value.

### `min`

The minimum value the user can select.

Defaults to `0.0`. Must be less than or equal to max.

### `max`

The maximum value the user can select.

Defaults to `1.0`. Must be greater than or equal to min.

## Events

### `on_change`

Fires when the value of the Slider is changed.