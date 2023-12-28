from .prog_device import ProgDevice
from .keys import ProgrammedKeys, BasicKeys, FuncKeys, MediaKeys, MouseKeys

# TODO: check if LED needs to be done or can be ignored
# TODO: load layout from json
# TODO: windows support
# TODO: CLI API

def reset(dev: ProgDevice):
    dev.program_key(ProgrammedKeys.TOP1, (FuncKeys.NONE, BasicKeys.C))
    dev.program_key(ProgrammedKeys.TOP2, (FuncKeys.NONE, BasicKeys.C))
    dev.program_key(ProgrammedKeys.TOP3, (FuncKeys.NONE, BasicKeys.C))
    dev.program_key(ProgrammedKeys.BOTTOM1, (FuncKeys.NONE, BasicKeys.C))
    dev.program_key(ProgrammedKeys.BOTTOM2, (FuncKeys.NONE, BasicKeys.C))
    dev.program_key(ProgrammedKeys.BOTTOM3, (FuncKeys.NONE, BasicKeys.C))
    dev.program_key(ProgrammedKeys.ENC_CCW, (FuncKeys.NONE, BasicKeys.C))
    dev.program_key(ProgrammedKeys.ENC_CW, (FuncKeys.NONE, BasicKeys.C))
    dev.program_key(ProgrammedKeys.ENC_CLICK, (FuncKeys.NONE, BasicKeys.C))

def test(dev: ProgDevice):
    dev.program_mouse_key(ProgrammedKeys.TOP1, FuncKeys.NONE, MouseKeys.LEFT)
    dev.program_mouse_key(ProgrammedKeys.TOP2, FuncKeys.NONE, MouseKeys.MIDDLE)
    dev.program_mouse_key(ProgrammedKeys.TOP3, FuncKeys.NONE, MouseKeys.RIGHT)
    dev.program_mouse_key(ProgrammedKeys.BOTTOM1, FuncKeys.LEFT_CTRL, MouseKeys.WHEEL_UP)
    dev.program_mouse_key(ProgrammedKeys.BOTTOM2, FuncKeys.LEFT_SHIFT, MouseKeys.LEFT)
    dev.program_mouse_key(ProgrammedKeys.BOTTOM3, FuncKeys.LEFT_CTRL, MouseKeys.WHEEL_DOWN)
    dev.program_mouse_key(ProgrammedKeys.ENC_CCW, FuncKeys.NONE, MouseKeys.WHEEL_UP)
    dev.program_mouse_key(ProgrammedKeys.ENC_CW, FuncKeys.NONE, MouseKeys.WHEEL_DOWN)
    dev.program_mouse_key(ProgrammedKeys.ENC_CLICK, FuncKeys.NONE, MouseKeys.MIDDLE)

def my_layout(dev: ProgDevice):
    dev.program_key(ProgrammedKeys.TOP1, (FuncKeys.LEFT_SUPER, BasicKeys.N1))
    dev.program_key(ProgrammedKeys.TOP2, (FuncKeys.LEFT_SUPER, BasicKeys.N2))
    dev.program_key(ProgrammedKeys.TOP3, (FuncKeys.LEFT_SUPER, BasicKeys.N3))
    dev.program_key(ProgrammedKeys.BOTTOM1, (FuncKeys.LEFT_SUPER, BasicKeys.N4))
    dev.program_key(ProgrammedKeys.BOTTOM2, (FuncKeys.LEFT_SUPER, BasicKeys.N5))
    dev.program_media_key(ProgrammedKeys.BOTTOM3, MediaKeys.NEXT_SONG)
    dev.program_media_key(ProgrammedKeys.ENC_CCW, MediaKeys.VOL_DEC)
    dev.program_media_key(ProgrammedKeys.ENC_CW, MediaKeys.VOL_INC)
    dev.program_media_key(ProgrammedKeys.ENC_CLICK, MediaKeys.PLAY_PAUSE)

def program(keymap):
    dev = ProgDevice.find()
    with dev:
        keymap(dev)
        dev.persist_keys()

if __name__ == '__main__':
    program(my_layout)
