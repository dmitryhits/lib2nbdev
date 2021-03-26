# lib2nbdev
> An all-inclusive package for converting your existing libraries and projects into `nbdev` ones. Developed by Novetta.


[nbdev](nbdev.fast.ai) is a fantastic workflow aimed at centralizing documentation, testing, and source code generation all out of one place: Jupyter Notebooks. However, what if you already have an existing project? As it stands the only way to convert your library over is through manual tasks (which can take > 30 hrs!). 

`lib2nbdev` is the solution!

Instead, we can perform a one-time conversion on any existing library. During the conversion process the library will help you generate a proper `settings.ini` configuration file for your project. However you can also generate your own `settings.ini` and put it in your project's core directory, such as:

- `lib2nbdev`
  - **`settings.ini`**
  - `lib2nbdev`
    - `convert.py`
    
For generating a valid `settings.ini`, see an example [here](https://github.com/fastai/nbdev_template/blob/master/settings.ini) and the related nbdev [documentation](https://nbdev.fast.ai/tutorial.html#Edit-settings.ini)

## Install

`pip install lib2nbdev`

## How to use

From your project directory (in bash), simply run:

```bash
convert_lib
```

And it will automatically generate the notebooks needed, as well as privatizing any functions that may need it (anything preceding with a `_` in the name) where they shouldn't show in the generated documentation. 

Afterwards you have a fully-functional `nbdev` library, and can make use of all its goodies!

### Note for Windows Users:

If you wish to use this library you should either:

1. Use [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) (WSL2)
2. Use the Python3 interpreter in Windows:
    - `python3`
    - `from lib2nbdev.convert import convert_lib; convert_lib()`

## Important Notice:

**This is a one-time conversion, this does not allow for repeated python -> notebook conversions.**
