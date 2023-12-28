import json

from .keys import BasicKeys, FuncKey, FuncKeys, KeyType, KeyTypes, MediaKeys, MouseKeys, ProgrammedKey, ProgrammedKeys
from .commands import BaseCommand, KeyChainCommand, MediaKeyCommand, MouseCommand

def from_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()

class ParseException(Exception):
    ...

def read_json_layout(json_data: str) -> list[BaseCommand]:
    data = json.loads(json_data)
    result = []
    for k in data:
        if not hasattr(ProgrammedKeys, k):
            raise ParseException(f'Unknown programmable key {k}')
        programmed_key: ProgrammedKey = getattr(ProgrammedKeys, k)
        specs = data[k]
        if not isinstance(specs, list):
            specs = [specs]
        command = parse_key_specs(programmed_key, specs)
        result.append(command)
    return result

def parse_key_specs(programmed_key: ProgrammedKey, specs: list[str]) -> BaseCommand:
    if len(specs) == 0:
        raise ParseException('Key chord list cannot be empty')
    chords = list(map(parse_key_spec, specs))
    if any([x[0] == KeyTypes.MEDIA for x in chords]):
        if len(chords) > 1:
            raise ParseException('When binding media keys, only one key chord is supported')
        chord = chords[0]
        if chord[1] != FuncKeys.NONE:
            raise ParseException('Media keys do not support combining with function keys')
        return MediaKeyCommand(programmed_key, chord[2])
    if any([x[0] == KeyTypes.MOUSE for x in chords]):
        if len(chords) > 1:
            raise ParseException('When binding mouse keys, only one key chord is supported')
        chord = chords[0]
        return MouseCommand(programmed_key, chord[1], chord[2])
    chord_specs = [x[1:] for x in chords]
    return KeyChainCommand(programmed_key, *chord_specs)

def parse_key_spec(spec: str) -> tuple[KeyType, FuncKey, int]:
    if spec.strip() == '':
        raise ParseException('Key chord spec cannot be empty')
    parts = [x.strip() for x in spec.split('+')]
    func_key: FuncKey = 0
    for p in parts[:-1]:
        if p in ['CTRL', 'ALT', 'SHIFT', 'SUPER']:
            p = 'LEFT_' + p
        if not hasattr(FuncKeys, p):
            raise ParseException(f'Unknow function key {p}')
        func_key |= getattr(FuncKeys, p)
    final = parts[-1]
    if final.startswith('MEDIA_'):
        k = final[6:]
        if not hasattr(MediaKeys, k):
            raise ParseException(f'Unknown media key {k}')
        return KeyTypes.MEDIA, func_key, getattr(MediaKeys, k)
    elif final.startswith('MOUSE_'):
        k = final[6:]
        if not hasattr(MouseKeys, k):
            raise ParseException(f'Unknown mouse key {k}')
        return KeyTypes.MOUSE, func_key, getattr(MouseKeys, k)
    else:
        if not hasattr(BasicKeys, final):
            raise ParseException(f'Unknown basic key {final}')
        return KeyTypes.BASIC_AND_FUNC, func_key, getattr(BasicKeys, final)
