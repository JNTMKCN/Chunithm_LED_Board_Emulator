# Chunithm_LED_Board_Emulator
Chunithm灯板模拟器\
需配合支持输出灯板数据的IO使用，可用的IO有：https://github.com/JNTMKCN/Affine_IO \
还需配合com0com使用，设置COM8与COM9串口对\
键盘IO可以使用Dniel97的segatools\
配置文件如下：
```ini
[led15093] 
; Enable emulation of the 15093-06 controlled lights, which handle the air tower
; RGBs and the rear LED panel (billboard) on the cabinet.
enable=1

[led]
; Output billboard LED strip data to a named pipe called "\.\pipe\chuni_led"
cabLedOutputPipe=0
; Output billboard LED strip data to serial
cabLedOutputSerial=1

; Output slider LED data to the named pipe
controllerLedOutputPipe=0
; Output slider LED data to the serial port
controllerLedOutputSerial=0

; Serial port to send data to if using serial output. Default is COM5.
serialPort=COM8
; Baud rate for serial data
serialBaud=115200
```
