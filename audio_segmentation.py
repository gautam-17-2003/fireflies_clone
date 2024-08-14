from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyaudio
import wave
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import soundfile as sf
from pyannote.audio import Pipeline
from pydub import AudioSegment

######### Script to perform audio segmentaiton

# Perform diarization
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
diarization = pipeline("meeting_audio.wav")

# Extract segments
def extract_segments(diarization, audio_file):
    audio = AudioSegment.from_wav(audio_file)
    segments = {}
    for segment, _, speaker in diarization.itertracks(yield_label=True):
        if speaker not in segments:
            segments[speaker] = []
        start = segment.start * 1000  # pydub works in milliseconds
        end = segment.end * 1000
        segments[speaker].append(audio[start:end])
    return segments

def save_segment(segment, filename):
    segment.export(filename, format="wav")

# Extract and save each segment
segments = extract_segments(diarization, "meeting_audio.wav")
for speaker, segs in segments.items():
    for i, seg in enumerate(segs):
        filename = f"{speaker}_segment_{i}.wav"
        save_segment(seg, filename)

# Transcribe each segment
def transcribe_audio(audio_file):
    model_name = "facebook/wav2vec2-large-960h"
    processor = Wav2Vec2Processor.from_pretrained(model_name)
    model = Wav2Vec2ForCTC.from_pretrained(model_name)

    audio_input, sample_rate = sf.read(audio_file)
    input_values = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt").input_values

    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.decode(predicted_ids[0])

    print("Transcription: ", transcription)
    return transcription

# Transcribe each segment
for speaker, segs in segments.items():
    for i, seg in enumerate(segs):
        filename = f"{speaker}_segment_{i}.wav"
        transcription = transcribe_audio(filename)
        print(f"Speaker {speaker}, Segment {i}: {transcription}")
