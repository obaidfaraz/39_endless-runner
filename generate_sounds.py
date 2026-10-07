import wave
import math
import struct
import os


os.makedirs("sounds", exist_ok=True)

SAMPLE_RATE = 44100


def create_sound(filename, frequencies, duration, volume=0.4):
    frames = []

    total_samples = int(SAMPLE_RATE * duration)

    for i in range(total_samples):
        t = i / SAMPLE_RATE

        frequency = frequencies[0]

        if len(frequencies) > 1:
            progress = i / total_samples
            frequency = (
                frequencies[0]
                + (frequencies[1] - frequencies[0]) * progress
            )

        sample = math.sin(2 * math.pi * frequency * t)

        fade = 1.0 - (i / total_samples)

        value = int(sample * volume * fade * 32767)

        frames.append(struct.pack("<h", value))

    with wave.open(filename, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(b"".join(frames))


create_sound(
    "sounds/jump.wav",
    (500, 900),
    0.15
)

create_sound(
    "sounds/score.wav",
    (700, 1100),
    0.12
)

create_sound(
    "sounds/game_over.wav",
    (500, 150),
    0.5
)

print("Sound files created successfully!")