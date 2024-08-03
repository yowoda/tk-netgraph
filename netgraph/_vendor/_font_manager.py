# MIT License from https://github.com/TomSchimansky/CustomTkinter
# Copyright (c) 2023 Tom Schimansky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import pathlib
import shutil
import typing as t

LINUX_FONT_PATH: t.Final[str] = pathlib.Path("~/.fonts/").expanduser()

def _linux_create_font_dir() -> None:
    if sys.platform.startswith("linux"):
        LINUX_FONT_PATH.mkdir(exist_ok=True)

def _windows_load_font(font_path: t.Union[str, bytes], private: bool = True, enumerable: bool = False) -> bool:
    """ Function taken from: https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter/30631309#30631309 """

    from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

    FR_PRIVATE = 0x10
    FR_NOT_ENUM = 0x20

    if isinstance(font_path, bytes):
        path_buffer = create_string_buffer(font_path)
        add_font_resource_ex = windll.gdi32.AddFontResourceExA
    elif isinstance(font_path, str):
        path_buffer = create_unicode_buffer(font_path)
        add_font_resource_ex = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('font_path must be of type bytes or str')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    num_fonts_added = add_font_resource_ex(byref(path_buffer), flags, 0)
    return bool(min(num_fonts_added, 1))

def load_font(font_path: str) -> bool:
    # Windows
    if sys.platform.startswith("win"):
        return _windows_load_font(font_path, private=True, enumerable=False)

    # Linux
    elif sys.platform.startswith("linux"):
        try:
            shutil.copy(font_path, LINUX_FONT_PATH)
            return True
        except Exception as err:
            sys.stderr.write("FontManager error: " + str(err) + "\n")
            return False

    # macOS and others
    else:
        return False