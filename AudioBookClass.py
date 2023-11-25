import os
import PyPDF2
from elevenlabs import voices, generate, play, set_api_key, stream
from API_KEYS import API_KEY
import threading
import keyboard
### need to make a separate thread that loads the next set of speech from text so that there is smooth audio

class AudioBook:
    def __init__(self) -> None:
        self.funtions = {
           'quit': self.quit,
            'library': self.library,
            'read': self.read
        }
        self.isOn = True
        self.currentPage = None

        set_api_key(API_KEY)
        vcs = voices()
        self.voice = vcs[-2]
        self.reading = True

    def quit(self):
        self.isOn = False

    def library(self):
        catalog = os.listdir('Books')
        print('---------------------------------')
        print('Below are all of the available books:\n')

        for titleInd in range(len(catalog)):
            print(f'{titleInd}: {catalog[titleInd]}')

        print('---------------------------------')

    def read(self, bookName, pageNum:False): 
        bookName = bookName[0]
        check = self.num_check(bookName)
        if check:
            catalog = os.listdir('Books')
            bookName = catalog[bookName]
        pdfFileObj = open(f'Books/{bookName}.pdf', 'rb')
        self.book = PyPDF2.PdfReader(pdfFileObj)

        # add a way to store the pagenum in a textfile when quitting
        if pageNum:
            self.currentPage = pageNum
        else:
            self.currentPage = self.get_first_page()

        self.tts()

    def num_check(self, var):
        try:
            return int(var)
        except:
            return False

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
            audio = generate(text=pageText, voice=self.voice)
            play(audio)
            # stream(audio)
            self.currentPage += 1
            print(f'Curent Page: {self.currentPage}')

    def input_listener(self):
        inp = input()
        if inp == 'pause':
            self.reading = False
            while True:
                if keyboard.is_pressed('q'):
                    break
            self.reading = True
            self.tts()
        elif inp == 'quit':
            self.reading = False
                 
        
