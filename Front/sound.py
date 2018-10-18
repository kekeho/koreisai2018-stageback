import sys
import numpy as np
import sounddevice as sd


def _audio_callback(indata, outdata, frames, time, status):
    """サンプリングごとに呼ばれるコールバック関数"""
    global latest_sound
    latest_sound = np.average(indata)


if __name__ == '__main__':
    samplerate = 400   # サンプリング周波数
    channels = 1        # チャンネル数（1固定）

    latest_sound = None

    stream = sd.Stream(channels=channels, callback=_audio_callback)
    
    with stream:
        while True:
            print(latest_sound)