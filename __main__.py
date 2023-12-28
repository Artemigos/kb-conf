from .prog_device import ProgDevice, ProgrammedKeys, BasicKeys, FuncKeys, MediaKeys

if __name__ == '__main__':
    dev = ProgDevice.find()
    with dev:
        dev.program_key(ProgrammedKeys.TOP1, (FuncKeys.LEFT_SUPER, BasicKeys.N1))
        dev.program_key(ProgrammedKeys.TOP2, (FuncKeys.LEFT_SUPER, BasicKeys.N2))
        dev.program_key(ProgrammedKeys.TOP3, (FuncKeys.LEFT_SUPER, BasicKeys.N3))
        dev.program_key(ProgrammedKeys.BOTTOM1, (FuncKeys.LEFT_SUPER, BasicKeys.N4))
        dev.program_key(ProgrammedKeys.BOTTOM2, (FuncKeys.LEFT_SUPER, BasicKeys.N5))
        dev.program_media_key(ProgrammedKeys.BOTTOM3, MediaKeys.NEXT_SONG)
        dev.program_media_key(ProgrammedKeys.ENC_CCW, MediaKeys.VOL_DEC)
        dev.program_media_key(ProgrammedKeys.ENC_CW, MediaKeys.VOL_INC)
        dev.program_media_key(ProgrammedKeys.ENC_CLICK, MediaKeys.PLAY_PAUSE)
