from .commands import BaseCommand, KeyChainCommand, KeyChord, MediaKeyCommand, persistCommand
from .hid import Device, enumerate
from .keys import ProgrammedKey, MediaKey

VID = 0x1189
PID = 0x8890
PROGRAM_REPORT_ID = 3

# TODO: add mouse actions
# TODO: check if LED needs to be done or can be ignored
# TODO: check if the delay feature is actually useless or not
# TODO: load layout from json
# TODO: windows support

class ProgDevice(Device):
    @staticmethod
    def find():
        devices = enumerate(VID, PID)
        if len(devices) == 0:
            raise Exception(f'device {VID}:{PID} not found')
        for device in devices:
            if device['interface_number'] == 1:
                break
        else:
            raise Exception(f'interface number 1 not found on device {VID}:{PID}')
        path = device['path']
        return ProgDevice(path=path)

    def write_command(self, command: BaseCommand):
        for packet in command.as_packets():
            self.write(packet)

    def program_key(self, programmed_key: ProgrammedKey, *keys: KeyChord):
        self.write_command(KeyChainCommand(programmed_key, *keys))

    def program_media_key(self, programmed_key: ProgrammedKey, key: MediaKey):
        self.write_command(MediaKeyCommand(programmed_key, key))

    def persist_keys(self):
        self.write_command(persistCommand)
