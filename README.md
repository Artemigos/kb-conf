# Utility for a programmable keyboard VID:PID == 1189:8890

**Should I use it?**

No, use <https://github.com/kriomant/ch57x-keyboard-tool> instead.

**Which models?**

Just one model tested: 6 keys (3x2), one encoder, no RGB, no layer switch (specificaly only features IN that model are supported).

**Which OS-es?**

Tested on Linux and Windows.

## Dependencies

On all supported platforms [hidapi](https://github.com/libusb/hidapi) is required.

On Linux `hidapi` is required in the `libusb` flavor.

On Windows the library files can be put next to the scripts and they will get loaded.

## Installation

Install dependencies and clone this repo.

## Usage

Run from directory above cloned repository.

```
usage: python3 -m kb-conf [-h] [--spec-file SPEC_FILE] [--test] [--persist]

Utility for a programmable keyboard VID:PID == 1189:8890

options:
  -h, --help            show this help message and exit
  --spec-file SPEC_FILE, -f SPEC_FILE
                        JSON file with key assignments
  --test, -t            Do not make any changes, just test the file and device connection
  --persist, -p         Use to persist the changes on the keyboard
```

## `<spec-file>.json`

See example JSON files in this repository.

### Function keys

```
CTRL
SHIFT
ALT
SUPER
LEFT_CTRL
LEFT_SHIFT
LEFT_ALT
LEFT_SUPER
RIGHT_CTRL
RIGHT_SHIFT
RIGHT_ALT
RIGHT_SUPER
```

### Media keys

Must appear **by themselves**.

Correct: `"TOP1": "MEDIA_MUTE"`

Incorrect: `"TOP1": "CTRL + MEDIA_MUTE"`

Incorrect: `"TOP1": [ "MEDIA_MUTE", "MEDIA_MUTE" ]`

```
MEDIA_PLAY_PAUSE
MEDIA_NEXT_SONG
MEDIA_PREV_SON
MEDIA_MUTE
MEDIA_VOL_INC
MEDIA_VOL_DEC
```

### Mouse keys

Can be combined with function keys, but only one key chord is allowed.

Correct: `"TOP1": "MOUSE_LEFT"`

Correct: `"TOP1": "CTRL + MOUSE_LEFT"`

Incorrect: `"TOP1": [ "MOUSE_LEFT", "MOUSE_LEFT" ]`

```
MOUSE_LEFT
MOUSE_RIGHT
MOUSE_MIDDLE
MOUSE_WHEEL_UP
MOUSE_WHEEL_DOWN
```

### All other keys

Can be combined with function keys and chained.

Correct: `"TOP1": "A"`

Correct: `"TOP1": "CTRL + A"`

Correct: `"TOP1": [ "A", "A" ]`

```
A
B
C
D
E
F
G
H
I
J
K
L
M
N
O
P
Q
R
S
T
U
V
W
X
Y
Z
N1
N2
N3
N4
N5
N6
N7
N8
N9
N0
ENTER
ESC
BACKSPACE
TAB
SPACE
MINUS_UNDERSCORE
EQUALS_ADD
LEFT_SQUARE_CURLY
RIGHT_SQUARE_CURLY
BACKSLASH_PIPE
SEMICOLON_COLON
APOSTROPHE_QUOTE
GRAVE_TILDE
COMMA_LEFT_ANGLE
PERIOD_RIGHT_ANGLE
SLASH_QUESTION_MARK
CAPS_LOCK
F1
F2
F3
F4
F5
F6
F7
F8
F9
F10
F11
F12
PRINT_SCREEN
SCROLL_LOCK
PAUSE_BREAK
INSERT
HOME
PAGE_UP
DELETE
END
PAGE_DOWN
RIGHT_ARROW
LEFT_ARROW
DOWN_ARROW
UP_ARROW
NUM_LOCK
NUM_DIV
NUM_MUL
NUM_SUB
NUM_ADD
NUM_1
NUM_2
NUM_3
NUM_4
NUM_5
NUM_6
NUM_7
NUM_8
NUM_9
NUM_0
NUM_DECIMAL_POINT
MENU
```
