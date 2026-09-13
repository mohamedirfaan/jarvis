import queue
import time

import torch
import sounddevice as sd
from threading import Thread
from silero_vad import load_silero_vad
from AudioTranscribePool import AudioTranscribePool

SAMPLE_RATE = 16000
VAD_THRESHOLD = 0.5
SILENCE_THRESHOLD = 0.8
CHUNK_SIZE = 512
class SpeechInput:
    def __init__(self):
        print("initializing")
        self.vad = load_silero_vad()
        self.queue = queue.Queue()
        self.speech_buffer = []
        self.speaking = False
        self.last_speech_time = None
        self.transcription_thread = AudioTranscribePool()
        print("initialized")

    def audio_callback(self, in_data, frame_count, time_info, status_flags):
        self.queue.put(in_data[:, 0].copy())

    def start(self):
        stream = sd.InputStream(samplerate=SAMPLE_RATE, blocksize=CHUNK_SIZE, callback=self.audio_callback, dtype="float32", channels=1)
        stream.start()
        while True:
            now = time.time()
            audio = self.queue.get()
            torch_audio = torch.from_numpy(audio)
            speech_probability = self.vad(torch_audio, SAMPLE_RATE).item()
            if speech_probability > VAD_THRESHOLD:
                if not self.speaking:
                    print("speech started")
                    self.speaking = True
                    self.speech_buffer = []
                self.speech_buffer.append(audio)
                self.last_speech_time = now
            elif self.speaking:
                self.speech_buffer.append(audio)
                silence_time = now - self.last_speech_time
                if silence_time > SILENCE_THRESHOLD:
                    print("speech ended")
                    transcription_thread = Thread(target=self.transcription_thread.produce, args=(self.speech_buffer.copy(),))
                    transcription_thread.start()
                    self.speech_buffer = []
                    self.speaking = False

if __name__ == "__main__":
    speech_input = SpeechInput()
    speech_input.start()
