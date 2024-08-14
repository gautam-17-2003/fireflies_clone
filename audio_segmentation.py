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


