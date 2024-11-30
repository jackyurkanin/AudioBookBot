import os
import PyPDF2
import threading
import torch
from TTS.api import TTS
import pyaudio
import wave
import time

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
file_path = "output.wav"

class AudioBook:
    def __init__(self) -> None:
        self.funtions = {
           'quit': self.quit,
            'library': self.library,
            'read': self.read
        }
        self.isOn = True
        self.currentPage = None
        self.voice = ""
        self.reading = True
        self.lastBook = False

        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        self.stream = None
        self.speaker = pyaudio.PyAudio()
        self.wf = None
        self.is_paused = False

    def quit(self):
        if self.stream:
            self.stream.close()
        if self.speaker:
            self.speaker.terminate()
        if self.wf:
            self.wf.close()
        self.isOn = False

    def library(self):
        catalog = os.listdir('Books')
        print('---------------------------------')
        print('Below are all of the available books:\n')

        for titleInd in range(len(catalog)):
            print(f'{titleInd}: {catalog[titleInd]}')

        print('---------------------------------')

    def read(self, package): 
        def num_check(var):
            try:
                return int(var)
            except:
                return False
        
        bookName = package[0]
        check = num_check(bookName)
        if check != None or check == 0:
            catalog = os.listdir('Books')
            bookName = catalog[check]
            bookName = bookName[:len(bookName)-4]

        pdfFileObj = open(f'Books/{bookName}.pdf', 'rb')
        self.book = PyPDF2.PdfReader(pdfFileObj)

        # add a way to store the pagenum in a textfile when quitting
        if len(package) == 2 and self.lastBook != bookName:
            self.currentPage = package[1]
        elif self.lastBook != bookName:
            self.currentPage = self.get_first_page()

        self.lastBook = bookName
        self.tts()

    def get_first_page(self): 
        diff = 0
        ind = 0
        while diff < 200:
            pageObj = self.book.pages[ind]  
            first  = len(pageObj.extract_text())
            pageObj = self.book.pages[ind+1]
            second = len(pageObj.extract_text())
            diff = second - first
            ind += 1
        return ind
        
    def tts(self):
        """
        self.book = PyPDF2.PdfReader(pdfFileObj) # the chosen pdf
        pageObj = self.book.pages[self.currentPage]  # ust to get current page
        pageText = pageObj.extract_text() # text from pdf of page

        """
        #input listening thread
        thread = threading.Thread(target=self.input_listener)
        thread.start()

        while self.reading:
            pageObj = self.book.pages[self.currentPage]  # ust to get current page
            pageText = pageObj.extract_text() # text from pdf of page
            self.tts.tts_to_file(text=pageText, speaker_wav="morganFreemanAudio/mf_audio.wav", language="en", output_path=file_path)
            
            # open wav
            self.wf = wave.open(file_path, "rb")

            self.stream = self.speaker.open(format=self.speaker.get_format_from_width(self.wf.getsampwidth()),
                    channels=self.wf.getnchannels(),
                    rate=self.wf.getframerate(),
                    output=True)

            # Read and play audio frames
            chunk_size = 1024
            data = self.wf.readframes(chunk_size)
            while data and self.stream:
                if not self.is_paused:
                    self.stream.write(data)
                    data = self.wf.readframes(chunk_size)
                else:
                    time.sleep(0.1)  # Wait while paused

            # Stop and close the stream
            self.stream.stop_stream()
            self.stream.close()
            self.wf.close()
            self.currentPage += 1
            print(f'Curent Page: {self.currentPage}')
        
        thread.join()
        print(thread.is_alive())

    def input_listener(self):
        while self.stream:
            inp = input()
            if inp == 'pause':
                print("Paused")
                self.is_paused = False
                inp = input('continue? Y/N: ')
                if inp == 'Y' or inp == 'y':
                    print("Resumed")
                    self.is_paused = True
                else:
                    print("Stopped")
                    self.stream.stop_stream()
                    self.stream.close()
                    self.reading = False
            elif inp == 'quit':
                print("Stopped")
                self.stream.stop_stream()
                self.stream.close()
                self.reading = False
            else:
                print('please use: pause or quit')
                continue
                 
        
