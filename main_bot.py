# import required modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

import pyaudio
import wave
import wavio
import soundfile as sf
import sounddevice as sd
from pydub import AudioSegment


def turnOffMicCam():
	# turn off Microphone
	time.sleep(2)
	driver.find_element(By.CSS_SELECTOR,'div.U26fgb.JRY2Pb.mUbCce.kpROve.yBiuPb.y1zVCf.M9Bg4d.HNeRed').click()
	print('mic off')
	time.sleep(5)

	# turn off camera
	driver.find_element(By.CSS_SELECTOR,'div.U26fgb.JRY2Pb.mUbCce.kpROve.yBiuPb.y1zVCf.M9Bg4d.HNeRed').click()
	print('camera off')
	time.sleep(5)


def joinNow():
    # Join meet
    print("opened meet link")
    time.sleep(2)
    
    driver.find_element(By.CLASS_NAME, "qdOxv-fmcmS-wGMbrd").send_keys(name)
    time.sleep(2)
    

    try:
        # Try to find and click the "Join now" button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Join now']"))).click()
        print("Entered meet successfully\n")
    except Exception as e:
        print("Meeting is not open, asking host to let in...")
        try:
            # Find and click the "Ask to join" button
            ask_to_join_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Ask to join']")))
            ask_to_join_button.click()
            print("Request to join sent, waiting for the host to let in...")
            time.sleep(2)
            # Wait until the "Asking to be let in..." element disappears, indicating that the bot has been admitted
            WebDriverWait(driver, 300).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div#c35.dHFSie")))
            print("Entered meet successfully after host approval\n")
        except Exception as e:
            print("Some error occurred, exiting the operation:", e)
            raise e

    
    time.sleep(2)



def record_audio(duration, output_filename):

    ###### audio recording using pyAudio 

    # FORMAT = pyaudio.paInt16
    # CHANNELS = 1
    # RATE = 16000
    # CHUNK = 1024

    # audio = pyaudio.PyAudio()

    # for i in range(audio.get_device_count()):
    #     print(f"Device {i}: {audio.get_device_info_by_index(i)['name']}")


    # stream = audio.open(format=FORMAT, channels=CHANNELS,
    #                     rate=RATE, input=True,
    #                     frames_per_buffer=CHUNK)

    # print("Recording...")

    # frames = []
    # for _ in range(0, int(RATE / CHUNK * duration)):
    #     data = stream.read(CHUNK)
    #     frames.append(data)

    # print("Finished recording.")

    # stream.stop_stream()
    # stream.close()
    # audio.terminate()

    # with wave.open(output_filename, 'wb') as wf:
    #     wf.setnchannels(CHANNELS)
    #     wf.setsampwidth(audio.get_sample_size(FORMAT))
    #     wf.setframerate(RATE)
    #     wf.writeframes(b''.join(frames))

    ############################################################
    
    ### sound recording using sounddevice ------- gfg

    samplerate = 44100  # Hertz
    channels = 2  # Stereo

    # Record from VB-Audio Virtual Cable
    print("Recording...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
    sd.wait()

    wavio.write(output_filename, audio_data, samplerate, sampwidth=2)
    print(f"Recording saved as {output_filename}")


name = "bot"

opt = Options()
opt.add_argument('--disable-blink-features=AutomationControlled')
opt.add_argument('--start-maximized')
opt.add_experimental_option("prefs", {
	"profile.default_content_setting_values.media_stream_mic": 1,
	"profile.default_content_setting_values.media_stream_camera": 1,
	"profile.default_content_setting_values.geolocation": 0,
	"profile.default_content_setting_values.notifications": 1,
	"excludeSwitches": ["disable-popup-blocking"]
})
opt.add_argument("--disable-popup-blocking")
    
driver = webdriver.Chrome(options=opt)

driver.get('https://meet.google.com/bid-jsvh-tap')
time.sleep(3)

turnOffMicCam()
joinNow()

## wait untill the bot entered the meet

DURATION = 60 #second
record_audio(DURATION, 'meeting_audio.wav')
