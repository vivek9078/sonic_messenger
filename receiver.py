# receiver.py
import numpy as np
import sounddevice as sd
from scipy.fft import fft

SAMPLE_RATE = 44100
DURATION_PER_BIT = 0.5  # seconds
FREQ_ZERO = 3000  # Hz for 0
FREQ_ONE = 5000   # Hz for 1
THRESHOLD = 0.02  # Adjust threshold for noise filtering

def record_audio(duration):
    print(f"Recording for {duration:.2f} seconds...")
    audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float64')
    sd.wait()
    return audio.flatten()

def detect_bit(chunk):
    fft_result = np.abs(fft(chunk))
    freqs = np.fft.fftfreq(len(chunk), 1/SAMPLE_RATE)

    # Only keep positive frequencies
    fft_result = fft_result[:len(fft_result)//2]
    freqs = freqs[:len(freqs)//2]

    # Find closest indexes for 3000 Hz and 5000 Hz
    idx_zero = np.argmin(np.abs(freqs - FREQ_ZERO))
    idx_one = np.argmin(np.abs(freqs - FREQ_ONE))

    amp_zero = fft_result[idx_zero]
    amp_one = fft_result[idx_one]

    if amp_one > amp_zero and amp_one > THRESHOLD:
        return '1'
    elif amp_zero > amp_one and amp_zero > THRESHOLD:
        return '0'
    else:
        return ''  # Silence or noise

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def receive_message(expected_chars):
    total_bits = expected_chars * 8
    record_time = 1.0 + total_bits * DURATION_PER_BIT + 0.5  # Sync + message + margin
    audio = record_audio(record_time)

    samples_per_bit = int(SAMPLE_RATE * DURATION_PER_BIT)
    sync_samples = int(1.0 * SAMPLE_RATE)
    audio = audio[sync_samples:]

    bits = ''
    for i in range(0, total_bits * samples_per_bit, samples_per_bit):
        chunk = audio[i:i+samples_per_bit]
        if len(chunk) == samples_per_bit:
            bit = detect_bit(chunk)
            bits += bit

    print(f"Received raw bits: {bits}")
    text = bits_to_text(bits)
    return text

if __name__ == "__main__":
    expected_chars = int(input("Enter expected number of characters: "))
    message = receive_message(expected_chars)
    print("Received message:", message)