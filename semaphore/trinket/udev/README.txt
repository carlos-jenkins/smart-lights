In order to program the Trinket execute:

    sudo cp 99-adafruit-boards.rules /etc/udev/rules.d/
    sudo reload udev

At least this is required in Ubuntu 14.04.

In Ubuntu 16.04, instead of
    sudo reload udev

try running:
    sudo udevadm control --reload-rules
    sudo udevadm trigger

If it still fails try stopping ModemManager service:
    sudo systemctl stop ModemManager.service
