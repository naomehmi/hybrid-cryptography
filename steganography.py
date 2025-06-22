import tkinter as tk
from tkinter import filedialog
from PIL import Image

def pick_image_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tk window
    root.update() 
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("PNG images", "*.png"), ("BMP images", "*.bmp")]
    )
    return file_path

def str_to_bin(data):
    return ''.join(format(ord(char), '08b') for char in data)

def hide_data_in_image(input_path, output_path, data):
    img = Image.open(input_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = img.load()

    binary_data = str_to_bin(data) + '1111111111111110'  # EOF marker
    data_len = len(binary_data)
    width, height = img.size

    idx = 0
    for y in range(height):
        for x in range(width):
            if idx >= data_len:
                break
            r, g, b = pixels[x, y]
            # Replace LSB of R, G, B
            r_bin = format(r, '08b')
            g_bin = format(g, '08b')
            b_bin = format(b, '08b')

            if idx < data_len:
                r_bin = r_bin[:-1] + binary_data[idx]
                idx += 1
            if idx < data_len:
                g_bin = g_bin[:-1] + binary_data[idx]
                idx += 1
            if idx < data_len:
                b_bin = b_bin[:-1] + binary_data[idx]
                idx += 1

            pixels[x, y] = (int(r_bin, 2), int(g_bin, 2), int(b_bin, 2))

        if idx >= data_len:
            break

    img.save(output_path)

def extract_data_from_image(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    binary_data = ""
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_data += format(r, '08b')[-1]
            binary_data += format(g, '08b')[-1]
            binary_data += format(b, '08b')[-1]

    # Split binary by 8 bits
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    for byte in all_bytes:
        if byte == '11111110':  # Our EOF marker
            break
        decoded_data += chr(int(byte, 2))
    return decoded_data
