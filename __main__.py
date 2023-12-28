from .prog_device import ProgDevice, ProgrammedKeys, BasicKeys, FuncKeys, MediaKeys

if __name__ == '__main__':
    dev = ProgDevice.find()
    with dev:
        dev.program_media_key(ProgrammedKeys.TOP_LEFT, MediaKeys.NEXT_SONG)
        dev.program_key(ProgrammedKeys.TOP_RIGHT, (FuncKeys.LEFT_SUPER, BasicKeys.N1))
        dev.program_key(ProgrammedKeys.MIDDLE_LEFT, (FuncKeys.LEFT_SUPER, BasicKeys.N2))
        dev.program_key(ProgrammedKeys.MIDDLE_RIGHT, (FuncKeys.LEFT_SUPER, BasicKeys.N3))
        dev.program_key(ProgrammedKeys.BOTTOM_LEFT, (FuncKeys.LEFT_SUPER, BasicKeys.N4))
        dev.program_key(ProgrammedKeys.BOTTOM_RIGHT, (FuncKeys.LEFT_SUPER, BasicKeys.N5))
        dev.program_media_key(ProgrammedKeys.KNOB_LEFT, MediaKeys.VOL_DEC)
        dev.program_media_key(ProgrammedKeys.KNOB_RIGHT, MediaKeys.VOL_INC)
        dev.program_media_key(ProgrammedKeys.KNOB_CLICK, MediaKeys.PLAY_PAUSE)
