import importlib

from utils import colors, sys
import config
theme = importlib.import_module('themes.{}'.format(sys.get_current_theme_name()))


class Segment(object):
    bg = ''  # Default: no color.
    fg = ''  # Default: no color.
    ls = False
    rs = False

    def __init__(self, *args, **kwargs):
        class_name = type(self).__name__.lower()
        if class_name in ['newline', 'root', 'divider', 'padding']:
            # These segments are always active.
            self.active = True
        else:
            # Other segments are active if the config files states so.
            self.active = config.SEGMENTS.get(class_name, False)

        if( config.SPACES ):
            if class_name not in ['newline', 'root', 'divider', 'padding', 'exitcode']:
                self.ls = True
                self.rs = True

            if(class_name == 'git'):
                self.ls = True
                self.rs = False

        if self.active:
            self.init(*args, **kwargs)

    def init(self):
        pass

    def render(self):
        output = list()
        output.append(self.bg)
        output.append(self.fg)
        if(self.ls): output.append(' ')
        output.append(self.text)
        if(self.rs): output.append(' ')
        output.append(colors.reset() if self.bg or self.fg else '')
        return ''.join(output)

    def length(self):
        lenght = len(self.text)
        if(self.ls): lenght+=1;
        if(self.rs): lenght+=1;
        return lenght