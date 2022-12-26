# Pengunci Pintu Otomatis Menggunakan Deteksi Wajah
Projek ini merupakan prototipe penguncian pintu otomatis menggunakan deteksi wajah sebagai kunci untuk membuka pintu.

## Stacks
- Python 3.10.x
- Arduino NodeMCU ESP8266 LoLin

## Dependency (Arduino)
- [ESP8266 Board Library](https://github.com/esp8266/Arduino)
- [Arduino Servo Library](https://github.com/arduino-libraries/Servo)

## Dependency (Python)
- [OpenCV2 Contributor Edition](https://github.com/opencv/opencv_contrib)
- [Adam Geitgey's DLIB Face Recognition](https://github.com/ageitgey/face_recognition)
- [pyserial](https://github.com/pyserial/pyserial)
- [NumPy](https://github.com/numpy/numpy)
- [Python Decouple](https://github.com/HBNetwork/python-decouple)

## Pin Location (Arduino)
| Pin | GPI | Target |
|-----|-----|--------|
| D0 | GPIO 16 | Buzzer |
| D1 | GPIO 5 | Push Button (Input Pullup) |
| D2 | GPIO 4 | Servo |
| G | GND (Right) | Grounding Buzzer & Push Button |
| VIN | 5V | Powering Servo |
| G | GND (Left) | Grounding Servo |

### Arduino VSCode Fix
Kadang kala, error yang terjadi saat menggunakan Arduino IDE di VSCode itu adalah mereka tidak bisa membaca file `.ino` apabila filenya dipisah. Untuk memperbaikinya, cari file `.vscode/c_cpp_properties.json` kemudian tambahkan semua yang ada di bawah ini:
```json
// Cari objek di bawah ini
"forcedInclude": [
    .....,
    // Copy dan Paste semua line di bawah ini
    "${workspaceFolder}\\Engine\\animate.ino"
]
```

*(C) 2022 - Ikramullah. Protected with Open Source License. All rights reserved.*
