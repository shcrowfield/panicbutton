import sys
import platform

# Detect the operating system and import appropriate libraries
if platform.system() == "Linux":
    from evdev import InputDevice, list_devices, ecodes
elif platform.system() == "Windows":
    import keyboard

import webbrowser

# Configuration
DEVICE_NAME = "Panic Button"
WEBPAGE_URL = "192.168.0.172:64538"


def open_default_browser_webpage():
    try:
        webbrowser.open(WEBPAGE_URL)
    except Exception as e:
        print(f"Error opening webpage: {e}")


def linux_key_listener():
    def find_device_by_name(name):
        for path in list_devices():
            device = InputDevice(path)
            if name in device.name:
                return device
        return None

    device = find_device_by_name(DEVICE_NAME)

    if device:
        print(f"Listening to device: {device.name} at {device.path}")

        pressed_keys = set()

        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                if event.value == 1:  # Key press
                    pressed_keys.add(event.code)
                elif event.value == 0:  # Key release
                    pressed_keys.discard(event.code)

                if (ecodes.KEY_P in pressed_keys and
                        ecodes.KEY_LEFTALT in pressed_keys and
                        ecodes.KEY_LEFTSHIFT in pressed_keys):
                    print(f"Opening webpage in default browser: {WEBPAGE_URL}")
                    open_default_browser_webpage()
                    pressed_keys.clear()
    else:
        print(f"Device '{DEVICE_NAME}' not found. Check the connection and try again.")


def windows_key_listener():
    print("Listening for key combination (P + Left Alt + Left Shift)")
    keyboard.add_hotkey('p+left alt+left shift', open_default_browser_webpage)
    keyboard.wait()

def main():
    os_name = platform.system()

    try:
        if os_name == "Linux":
            linux_key_listener()
        elif os_name == "Windows":
            windows_key_listener()
        else:
            print(f"Unsupported operating system: {os_name}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nScript terminated by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()