# Flet controls in Python by the community

`flet-contrib` package includes reusable Flet controls written in Python only and using existing Flet primitives.

## Controls

* [ColorPicker](flet_contrib/color_picker) ([Live demo](https://flet-controls-gallery.fly.dev/contrib/colorpicker))

## Usage

To install `flet-contrib` package:

```
pip install flet-contrib
```

To use in your app:

```python
from flet_contrib.color_picker import ColorPicker

picker = ColorPicker(...)
```

## How to contribute

Contributions are welcome!

Fork this repo.

Create a new directory inside `flet_contrib` for your control(s) - that will be control's module name, for example `flet_contrib.my_control`.

Control directory structure:

* `README.md` - control description, usage, examples, support information.
* `/src` - control implementation.
* `/media` - images, multimedia files, databases and other files required by control to function or used in `README.md`.
* `/examples` - one or more examples of usage of your control.
* `__init__.py` - classes and functions exported to users of your control.

See [ColorPicker](flet_contrib/color_picker) for folder structure example.

Submit Pull Request (PR) with your changes.

Once your PR is merged into `main` a new "dev" package will be released [here](https://pypi.org/project/flet-contrib/) which can be installed with `pip install flet-contrib --pre`.

When the contribution is tested by Flet team/community a new `flet-contrib` release will be published.