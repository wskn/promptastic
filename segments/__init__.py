import importlib

from utils import colors, sys
import config
theme = importlib.import_module('themes.{}'.format(sys.get_current_theme_name()))


class Segment(object):
    bg = ''  # Default: no color.
    fg = ''  # Default: no color.
    spaces = False # Default: no spaces.

    def __init__(self, *args, **kwargs):
        class_name = type(self).__name__.lower()
        if class_name in ['newline', 'root', 'divider', 'padding']:
            # These segments are always active.
            self.active = True
        else:
            # Other segments are active if the config files states so.
            self.active = config.SEGMENTS.get(class_name, False)

        if(config.SPACES):
            if class_name not in ['newline', 'root', 'divider', 'padding', 'exitcode']:
                self.spaces = True

        if self.active:
            self.init(*args, **kwargs)

    def init(self):
        pass

    def render(self):
        output = list()
        output.append(self.bg)
        output.append(self.fg)
        output.append(' ' + self.text + ' ' if self.spaces else self.text)
        output.append(colors.reset() if self.bg or self.fg else '')
        return ''.join(output)

    def length(self):
        lenght = len(self.text)
        if(self.spaces): lenght+=2;
        return lenght