from abc import ABC, abstractmethod

from .keys import BasicKey, FuncKey, KeyTypes, MediaKey, MouseKey, MouseKeys, ProgrammedKey

REPORT_ID = 3
PACKET_SIZE = 65

def pad_packet(packet: bytes, pad_to=PACKET_SIZE) -> bytes:
    plen = len(packet)
    assert plen <= pad_to
    if plen == pad_to:
        return packet
    return packet + bytes([0]*(pad_to-plen))

class BaseCommand(ABC):
    @abstractmethod
    def as_packets(self) -> list[bytes]:
        raise NotImplementedError()

class PersistCommand(BaseCommand):
    def __init__(self):
        self._cache = [pad_packet(bytes([REPORT_ID, 170, 170]))]
    def as_packets(self) -> list[bytes]:
        return self._cache

persistCommand = PersistCommand()

KeyChord = tuple[FuncKey, BasicKey]
class KeyChainCommand(BaseCommand):
    def __init__(self, key: ProgrammedKey, *chords: KeyChord):
        self.key = key
        self.chords = chords
        self._cache = [
            pad_packet(bytes([
                REPORT_ID,
                key,
                KeyTypes.BASIC_AND_FUNC,
                len(chords),
            ])),
        ]
        for i in range(len(chords)):
            f, k = chords[i]
            self._cache.append(pad_packet(bytes([
                REPORT_ID,
                key,
                KeyTypes.BASIC_AND_FUNC,
                len(chords),
                i+1,
                f,
                k,
            ])))
    def as_packets(self) -> list[bytes]:
        return self._cache

class MediaKeyCommand(BaseCommand):
    def __init__(self, key: ProgrammedKey, media_key: MediaKey):
        self.key = key
        self.media_key = media_key
        self._cache = [
            pad_packet(bytes([
                REPORT_ID,
                key,
                KeyTypes.MEDIA,
                media_key,
            ])),
        ]
    def as_packets(self) -> list[bytes]:
        return self._cache

class MouseCommand(BaseCommand):
    def __init__(self, key: ProgrammedKey, func_key: FuncKey, mouse_key: MouseKey):
        self.key = key
        self.func_key = func_key
        self.mouse_key = mouse_key
        wheel_byte = 0
        if mouse_key == MouseKeys.WHEEL_UP:
            wheel_byte = 1
        elif mouse_key == MouseKeys.WHEEL_DOWN:
            wheel_byte = 255
        self._cache = [
            pad_packet(bytes([
                REPORT_ID,
                key,
                KeyTypes.MOUSE,
                mouse_key if mouse_key < 254 else 0, # wheel is always 0
                0,
                0,
                wheel_byte,
                func_key,
            ])),
        ]
    def as_packets(self) -> list[bytes]:
        return self._cache
