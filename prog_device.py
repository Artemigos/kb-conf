from . import hid

VID = 0x1189
PID = 0x8890
PROGRAM_REPORT_ID = 3

# TODO: add remaining basic keys
# TODO: add remaining media keys
# TODO: add mouse actions
# TODO: check if LED needs to be done or can be ignored
# TODO: check if the delay feature is actually useless or not
# TODO: declutter the API?
# TODO: load layout from json
# TODO: ask if windows support would be useful

ProgrammedKey = int
class ProgrammedKeys:
    BOTTOM_LEFT: ProgrammedKey = 1
    MIDDLE_LEFT: ProgrammedKey = 2
    TOP_LEFT: ProgrammedKey = 3
    BOTTOM_RIGHT: ProgrammedKey = 4
    MIDDLE_RIGHT: ProgrammedKey = 5
    TOP_RIGHT: ProgrammedKey = 6
    KNOB_LEFT: ProgrammedKey = 13
    KNOB_CLICK: ProgrammedKey = 14
    KNOB_RIGHT: ProgrammedKey = 15

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

MediaKey = int
class MediaKeys:
    PLAY_PAUSE: MediaKey = 205
    NEXT_SONG: MediaKey = 181
    PREV_SONG: MediaKey = 182
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
