import serial
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

SERIAL_PORT = 'COM9' #端口号
BAUD_RATE = 115200 #波特率

ROWS = 10 
COLS = 11 
CELL_WIDTH = 20  
CELL_HEIGHT = CELL_WIDTH * 2  
ROW_LENGTH = ROWS * 3  

class LightBoardSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LED")
        self.geometry(f"{COLS * CELL_WIDTH}x{ROWS * CELL_HEIGHT}")

        self.image = Image.new("RGB", (COLS * CELL_WIDTH, ROWS * CELL_HEIGHT), "black")
        self.photo = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(self, image=self.photo)
        self.label.pack()

        self.serial_port = serial.Serial(SERIAL_PORT, BAUD_RATE)
        self.buffer = b''
        self.after(20, self.read_serial) 

    def read_serial(self):
        if self.serial_port.in_waiting > 0:
            new_data = self.serial_port.read(self.serial_port.in_waiting)
            self.buffer += new_data
            self.process_buffer()
        self.after(20, self.read_serial) 

    def process_buffer(self):
        while len(self.buffer) >= 2:
            header = self.buffer[:2]
            if header[0] == 0xE0 and header[1] in [0x00, 0x01]:
                # 处理数据包
                if header[1] == 0x00:
                    data_length = ROW_LENGTH * 5 
                elif header[1] == 0x01:
                    data_length = ROW_LENGTH * 6 

                if len(self.buffer) >= 2 + data_length:
                    data = self.buffer[2:2 + data_length]
                    self.buffer = self.buffer[2 + data_length:]
                    self.update_image(data, header[1])
                else:
                    break
            else:
                self.buffer = self.buffer[1:]

    def update_image(self, data, header_type):
        brightness_factor = 10.0  #对亮度进行放大

        if header_type == 0x00:
            col_start = 0
            num_cols = 5
        elif header_type == 0x01:
            col_start = 5
            num_cols = 6

        try:
            array = np.frombuffer(data, dtype=np.uint8).reshape((num_cols, ROWS, 3))
            array = np.clip(array * brightness_factor, 0, 255).astype(np.uint8)
        except ValueError:
            return

        try:
            image_array = np.array(self.image)

            for j in range(num_cols):
                for i in range(ROWS):
                    if (col_start + j) % 2 == 0:
                        row_index = i  
                    else:
                        row_index = ROWS - 1 - i  

                    image_array[row_index * CELL_HEIGHT:(row_index + 1) * CELL_HEIGHT,
                                (col_start + j) * CELL_WIDTH:(col_start + j + 1) * CELL_WIDTH] = array[j, i]

            self.image = Image.fromarray(image_array.astype('uint8'), 'RGB')
            self.photo = ImageTk.PhotoImage(self.image)
            self.label.config(image=self.photo)
        except Exception as e:
            print(f"Error during image update: {e}")

if __name__ == "__main__":
    app = LightBoardSimulator()
    app.mainloop()
