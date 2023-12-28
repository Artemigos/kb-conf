from .prog_device import ProgDevice
from .serde import from_file, read_json_layout

# TODO: check if LED needs to be done or can be ignored
# TODO: windows support
# TODO: CLI API

def program_from_json(path: str, persist=True):
    commands = read_json_layout(from_file(path))
    with ProgDevice.find() as dev:
        for command in commands:
            dev.write_command(command)
        if persist:
            dev.persist_keys()

if __name__ == '__main__':
    # program_from_json('kb-conf/reset.json')
    # program_from_json('kb-conf/mouse_test.json')
    program_from_json('kb-conf/my_layout.json')
