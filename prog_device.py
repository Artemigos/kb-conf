from . import hid

VID = 0x1189
PID = 0x8890
PROGRAM_REPORT_ID = 3

# TODO: add mouse actions
# TODO: check if LED needs to be done or can be ignored
# TODO: check if the delay feature is actually useless or not
# TODO: declutter the API?
# TODO: load layout from json
# TODO: windows support

ProgrammedKey = int
class ProgrammedKeys:
    TOP1: ProgrammedKey = 1
    TOP2: ProgrammedKey = 2
    TOP3: ProgrammedKey = 3
    BOTTOM1: ProgrammedKey = 4
    BOTTOM2: ProgrammedKey = 5
    BOTTOM3: ProgrammedKey = 6
    ENC_CCW: ProgrammedKey = 13
    ENC_CLICK: ProgrammedKey = 14
    ENC_CW: ProgrammedKey = 15

KeyType = int
class KeyTypes:
    BASIC_AND_FUNC: KeyType = 1
    MEDIA: KeyType = 2
    MOUSE: KeyType = 3
    LED: KeyType = 8

FuncKey = int
class FuncKeys:
    NONE: FuncKey = 0
    LEFT_CTRL: FuncKey = 1
    LEFT_SHIFT: FuncKey = 2
    LEFT_ALT: FuncKey = 4
    LEFT_SUPER: FuncKey = 8
    RIGHT_CTRL: FuncKey = 16
    RIGHT_SHIFT: FuncKey = 32
    RIGHT_ALT: FuncKey = 64
    RIGHT_SUPER: FuncKey = 128

BasicKey = int
class BasicKeys:
    A: BasicKey = 4
    B: BasicKey = 5
    C: BasicKey = 6
    D: BasicKey = 7
    E: BasicKey = 8
    F: BasicKey = 9
    G: BasicKey = 10
    H: BasicKey = 11
    I: BasicKey = 12
    J: BasicKey = 13
    K: BasicKey = 14
    L: BasicKey = 15
    M: BasicKey = 16
    N: BasicKey = 17
    O: BasicKey = 18
    P: BasicKey = 19
    Q: BasicKey = 20
    R: BasicKey = 21
    S: BasicKey = 22
    T: BasicKey = 23
    U: BasicKey = 24
    V: BasicKey = 25
    W: BasicKey = 26
    X: BasicKey = 27
    Y: BasicKey = 28
    Z: BasicKey = 29
    N1: BasicKey = 30
    N2: BasicKey = 31
    N3: BasicKey = 32
    N4: BasicKey = 33
    N5: BasicKey = 34
    N6: BasicKey = 35
    N7: BasicKey = 36
    N8: BasicKey = 37
    N9: BasicKey = 38
    N0: BasicKey = 39
    ENTER: BasicKey = 40
    ESC: BasicKey = 41
    BACKSPACE: BasicKey = 42
    TAB: BasicKey = 43
    SPACE: BasicKey = 44
    MINUS_UNDERSCORE: BasicKey = 45
    EQUALS_ADD: BasicKey = 46
    LEFT_SQUARE_CURLY: BasicKey = 47
    RIGHT_SQUARE_CURLY: BasicKey = 48
    BACKSLASH_PIPE: BasicKey = 49
    SEMICOLON_COLON: BasicKey = 51
    APOSTROPHE_QUOTE: BasicKey = 52
    GRAVE_TILDE: BasicKey = 53
    COMMA_LEFT_ANGLE: BasicKey = 54
    PERIOD_RIGHT_ANGLE: BasicKey = 55
    SLASH_QUESTION_MARK: BasicKey = 56
    CAPS_LOCK: BasicKey = 57
    F1: BasicKey = 58
    F2: BasicKey = 59
    F3: BasicKey = 60
    F4: BasicKey = 61
    F5: BasicKey = 62
    F6: BasicKey = 63
    F7: BasicKey = 64
    F8: BasicKey = 65
    F9: BasicKey = 66
    F10: BasicKey = 67
    F11: BasicKey = 68
    F12: BasicKey = 69
    PRINT_SCREEN: BasicKey = 70
    SCROLL_LOCK: BasicKey = 71
    PAUSE_BREAK: BasicKey = 72
    INSERT: BasicKey = 73
    HOME: BasicKey = 74
    PAGE_UP: BasicKey = 75
    DELETE: BasicKey = 76
    END: BasicKey = 77
    PAGE_DOWN: BasicKey = 78
    RIGHT_ARROW: BasicKey = 79
    LEFT_ARROW: BasicKey = 80
    DOWN_ARROW: BasicKey = 81
    UP_ARROW: BasicKey = 82
    NUM_LOCK: BasicKey = 83
    NUM_DIV: BasicKey = 84
    NUM_MUL: BasicKey = 85
    NUM_SUB: BasicKey = 86
    NUM_ADD: BasicKey = 87
    NUM_1: BasicKey = 89
    NUM_2: BasicKey = 90
    NUM_3: BasicKey = 91
    NUM_4: BasicKey = 92
    NUM_5: BasicKey = 93
    NUM_6: BasicKey = 94
    NUM_7: BasicKey = 95
    NUM_8: BasicKey = 96
    NUM_9: BasicKey = 97
    NUM_0: BasicKey = 98
    NUM_DECIMAL_POINT: BasicKey = 99
    MENU: BasicKey = 101

MediaKey = int
class MediaKeys:
    PLAY_PAUSE: MediaKey = 205
    NEXT_SONG: MediaKey = 181
    PREV_SONG: MediaKey = 182
    MUTE: MediaKey = 226
    VOL_INC: MediaKey = 233
    VOL_DEC: MediaKey = 234

Key = BasicKey | MediaKey

def pad_packet(packet, pad_to=65):
    print(packet)
    plen = len(packet)
    assert plen <= pad_to
    if plen == pad_to:
        return packet
    return packet + bytes([0]*(pad_to-plen))

def make_empty_key_packet(
        programmed_key: ProgrammedKey,
        typ: KeyType,
        num_of_keys: int,
        ):
    return pad_packet(bytes([
        PROGRAM_REPORT_ID,
        programmed_key,
        typ,
        num_of_keys,
    ]))

def make_key_packet(
        programmed_key: ProgrammedKey,
        typ: KeyType,
        num_of_keys: int,
        key_ordinal: int,
        func_key: FuncKey,
        key: BasicKey,
        ):
    return pad_packet(bytes([
        PROGRAM_REPORT_ID,
        programmed_key,
        typ,
        num_of_keys,
        key_ordinal,
        func_key,
        key,
    ]))

def make_media_key_packet(
        programmed_key: ProgrammedKey,
        typ: KeyType,
        key: MediaKey,
        ):
    return pad_packet(bytes([
        PROGRAM_REPORT_ID,
        programmed_key,
        typ,
        key,
    ]))

def make_flush_packet():
    return pad_packet(bytes([PROGRAM_REPORT_ID, 170, 170]))

class ProgDevice(hid.Device):
    @staticmethod
    def find():
        devices = hid.enumerate(VID, PID)
        if len(devices) == 0:
            raise Exception(f'device {VID}:{PID} not found')
        for device in devices:
            if device['interface_number'] == 1:
                break
        else:
            raise Exception(f'interface number 1 not found on device {VID}:{PID}')
        path = device['path']
        return ProgDevice(path=path)

    def program_key(self, programmed_key: ProgrammedKey, *keys: tuple[FuncKey, Key]):
        self.write(make_empty_key_packet(programmed_key, KeyTypes.BASIC_AND_FUNC, len(keys)))
        for i in range(len(keys)):
            f, k = keys[i]
            self.write(make_key_packet(
                programmed_key,
                KeyTypes.BASIC_AND_FUNC,
                len(keys),
                i+1,
                f,
                k,
            ))
        self.write(make_flush_packet())

    def program_media_key(self, programmed_key: ProgrammedKey, key: MediaKey):
        self.write(make_media_key_packet(
            programmed_key,
            KeyTypes.MEDIA,
            key
        ))
        self.write(make_flush_packet())
