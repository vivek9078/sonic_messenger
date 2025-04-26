# sender.py
import numpy as np
import sounddevice as sd

SAMPLE_RATE = 44100
DURATION_PER_BIT = 0.3  # seconds
FREQ_ZERO = 3000  # Hz
FREQ_ONE = 5000   # Hz

def text_to_bits(text):
    return ''.join(f'{ord(c):08b}' for c in text)

def play_tone(frequency, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(tone, samplerate=SAMPLE_RATE)
    sd.wait()

def send_message(message):
    bits = text_to_bits(message)
    print(f"Sending bits: {bits}")

    # Send 1s sync tone at FREQ_ONE
    print("Sending sync...")
    play_tone(FREQ_ONE, 1.0)

    for bit in bits:
        if bit == '1':
            play_tone(FREQ_ONE, DURATION_PER_BIT)
        else:
            play_tone(FREQ_ZERO, DURATION_PER_BIT)

if __name__ == "__main__":
    message = input("Enter message to send: ")
    send_message(message)