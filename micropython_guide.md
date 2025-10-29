# Micropython Setup Guide
### _With aliases for easier reusability_
### venv and dir creation
```
mkdir esp01
cd esp01
alias VENV_ACTIVATE="source .venvlin/bin/activate"
alias VENV_CREATE="python -m venv .venvlin"
pip install esptool
```
### First comm
```sudo usermod -aG dialout $USER```
### LOGOUT/RESTART
```dmesg | grep tty```
### Should be similar to: `ch341-uart converter now attached to ttyUSB0`
```esptool.py --port /dev/ttyUSB0 erase_flash```

### Select board and flash
```
https://micropython.org/download/?port=esp32
esptool.py --baud 460800 write_flash 0x1000 <ESP32_BOARD_NAME-DATE-VERSION>.bin
```

### Open REPL terminal (live python)
```
pip install mpremote
alias ESP_REPL="mpremote connect /dev/ttyUSB0 repl"
```

### Copy main.py file and run on the board
```alias ESP_CP="mpremote connect /dev/ttyUSB0 fs cp main.py :"```
