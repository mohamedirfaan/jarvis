import numpy as np
from faster_whisper import WhisperModel
class AudioTranscribePool:
    def __init__(self):
        self.whisper = WhisperModel("base", device="cpu", compute_type="int8")
        self.transcribed_audio = ""

    def transcribe(self, audio):
        audio = np.concatenate(audio)
        segments, info = self.whisper.transcribe(audio, language="en")
        text = ""
        for segment in segments:
            text += segment.text + " "
        return text.strip()

    def produce(self, speech_buffer):
        transcribed_text = self.transcribe(speech_buffer)
        self.transcribed_audio += transcribed_text + " "

    def consume(self):
        pass