from PyQt5.QtGui import QColor

def parse_rgba(rgba_str: str) -> list[int]:
    rgba_str = rgba_str.strip().replace(' ', '')
    try:
        rgba = rgba_str.split('(', 1)[-1].split(')', 1)[0].split(",")
    except IndexError:
        raise ValueError(f"Invalid RGBA format: '{rgba_str}'")

    parsed_rgba = []

    for i in range(len(rgba)):
        _ci = rgba[i]
        if _ci == '':
            if i < 3: # if alpha channel is missing skip
                parsed_rgba.append(0)
        elif _ci.isdigit():
            _ci = int(_ci)
            parsed_rgba.append(min(_ci, 255))
        else:
            return [0,0,0,255]

    # Default channel value 0
    while len(parsed_rgba) < 3:
        parsed_rgba.append(0)

    # Default alpha 255
    if len(parsed_rgba) == 3:
        parsed_rgba.append(255)

    return parsed_rgba

def str_to_rgba(color: str):
    if QColor.isValidColor(color):
        rgba = QColor(color)
        return (rgba.red(), rgba.green(), rgba.blue(), rgba.alpha())

    return parse_rgba(color)

def str_to_qcolor(color: str):
    color = color

    if QColor.isValidColor(color):
        return QColor(color)

    return QColor(*parse_rgba(color))

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def rgba_to_hex(r, g, b, a):
    """QSS uses the format #AARRGGBB"""
    return '#{:02x}{:02x}{:02x}{:02x}'.format(a, r, g, b)