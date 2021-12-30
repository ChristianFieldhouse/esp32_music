from scipy.io import wavfile
import serial
import numpy as np
from tqdm import tqdm

infile = "jingle16.wav"
infile = "cotton.wav"
freq, arr = wavfile.read(infile)

arr = arr.astype("float")
arr = arr / np.std(arr)

def s(sig = 2.5):
    # esp reads 255 by default or something, so can't use it
    return (254 * np.clip(arr + sig, 0, 2*sig) / (2*sig)).astype("int")

s8 = [t[0] for t in s(5)]

b = 9
N = min(1101710, len(s8) // b)
print(f"copying {N / (len(s8) // b)} of file")
with open("src/song.h", "w") as f:
    f.write("//#include <Arduino.h>\n\n")
    f.write(f"#define song_step {int(1_000_000 / (freq/b))}\n")
    f.write(f"#define song_len {N}\n")
    f.write("const uint8_t PROGMEM song[song_len] {\n")
    for i in range(N-1):
        f.write(str(s8[i*b])+", ")
        if i%1500 == 0:
            f.write("\n")
    f.write(str(s8[(N-1)*b])+"\n};")

#ser = serial.Serial("/dev/ttyUSB0", baudrate=115200)
#for i in tqdm(range(200000)):
#    byte = int(s8[2*i]).to_bytes(1, byteorder="big")
#    ser.write(b'*')
#    ser.write(byte)
#    print(ser.read_until(b'\n'))
