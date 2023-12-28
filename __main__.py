import argparse

from .prog_device import ProgDevice
from .serde import from_file, read_json_layout

def program_from_json(path: str, persist=True):
    commands = read_json_layout(from_file(path))
    with ProgDevice.find() as dev:
        for command in commands:
            dev.write_command(command)
        if persist:
            dev.persist_keys()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Utility for programming that one keyboard we bought.')
    parser.add_argument('--spec-file', '-f', type=str, help='JSON file with key assignments')
    parser.add_argument(
        '--test',
        '-t',
        action='store_true',
        help='Do not make any changes, just test the file and device connection')
    parser.add_argument(
        '--persist',
        '-p',
        action='store_true',
        help='Use to persist the changes on the keyboard')
    args = parser.parse_args()

    if not args.test and args.spec_file is None:
        print('At least one of --test or --spec-file is required')
        parser.exit(1)

    if args.test is True:
        with ProgDevice.find():
            print('Successfully connected to the keyboard')
        if args.spec_file is not None:
            _ = read_json_layout(from_file(args.spec_file))
            print('Successfully parsed spec file')
    else:
        program_from_json(args.spec_file, args.persist)
