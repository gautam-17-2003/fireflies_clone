# import required modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

import pyaudio
import wave
import soundfile as sf
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
        driver.find_element(By.XPATH, "//span[text()='Join now']").click()
        print("entered meet successfully\n")
    except Exception as e:
        print("Meeting is not open, asking host to let in...")
        try:
            # If the "Join now" button is not found, try the alternative button
            driver.find_element(By.XPATH, "//span[text()='Ask to join']").click()
            print("Entered meet successfully\n")
        except Exception as e:
            print("some error occured, exiting the operation:", e)
            raise e
    
    time.sleep(2)



def record_audio(duration, output_filename):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))


# assign email id and password
mail_address = 'gautampubreja@gmail.com'
password = 'gautam'
name = "bot"

# create chrome instance
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

# login to Google account
# Glogin(mail_address, password)

# go to google meet
driver.get('https://meet.google.com/ujr-vits-tqh')
time.sleep(3)

turnOffMicCam()
joinNow()



DURATION = 200
record_audio(DURATION, 'meeting_audio.wav')
