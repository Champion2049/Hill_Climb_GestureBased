import ctypes
import time

# Bind the Windows SendInput API so Python can synthesize keyboard events.
SendInput = ctypes.windll.user32.SendInput

# DirectInput scan code for the right arrow key.
right_pressed = 0x4D

# DirectInput scan code for the left arrow key.
left_pressed = 0x4B

# C struct redefinitions
# Pointer type used by INPUT structures for extra metadata.
PUL = ctypes.POINTER(ctypes.c_ulong)


# Equivalent to Win32 KEYBDINPUT.
class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),      # Virtual key code (unused here; we use scan code).
        ("wScan", ctypes.c_ushort),    # Hardware scan code for the key.
        ("dwFlags", ctypes.c_ulong),   # Event flags (scan code mode, key up/down, etc.).
        ("time", ctypes.c_ulong),      # Timestamp for event (0 lets OS assign current time).
        ("dwExtraInfo", PUL),          # Optional extra message info pointer.
    ]


# Equivalent to Win32 HARDWAREINPUT (unused by this project, kept for INPUT union completeness).
class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort),
    ]


# Equivalent to Win32 MOUSEINPUT (unused here, but part of INPUT union).
class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


# Equivalent to Win32 INPUT union.
class Input_I(ctypes.Union):
    _fields_ = [
        ("ki", KeyBdInput),
        ("mi", MouseInput),
        ("hi", HardwareInput),
    ]


# Equivalent to Win32 INPUT struct.
class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),  # 1 means keyboard input.
        ("ii", Input_I),           # Union containing the keyboard payload.
    ]


def PressKey(hexKeyCode):
    """Send a key-down event using a DirectInput scan code.

    Args:
        hexKeyCode: Keyboard scan code (for example 0x4B for left arrow).
    """
    # Extra info pointer required by the Win32 structure.
    extra = ctypes.c_ulong(0)

    # Create the INPUT union payload.
    ii_ = Input_I()

    # 0x0008 = KEYEVENTF_SCANCODE (interpret wScan as scan code).
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))

    # type=1 means INPUT_KEYBOARD.
    x = Input(ctypes.c_ulong(1), ii_)

    # Send exactly one keyboard event to Windows.
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    """Send a key-up event using a DirectInput scan code.

    Args:
        hexKeyCode: Keyboard scan code (for example 0x4B for left arrow).
    """
    # Extra info pointer required by the Win32 structure.
    extra = ctypes.c_ulong(0)

    # Create the INPUT union payload.
    ii_ = Input_I()

    # 0x0008 = KEYEVENTF_SCANCODE, 0x0002 = KEYEVENTF_KEYUP.
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))

    # type=1 means INPUT_KEYBOARD.
    x = Input(ctypes.c_ulong(1), ii_)

    # Send exactly one keyboard event to Windows.
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


if __name__ == '__main__':
    # Tiny local test: press and release scan code 0x11 repeatedly once per second.
    # Note: 0x11 is a scan code example; for game controls the main program uses arrow codes.
    while True:
        PressKey(0x11)
        time.sleep(1)
        ReleaseKey(0x11)
        time.sleep(1)