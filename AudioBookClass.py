import os
import PyPDF2
from elevenlabs import voices, generate, play, set_api_key
from API_KEYS import API_KEY
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
        voices = voices()
        self.voice = voices[-2]

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

        if pageNum:
            self.currentPage = pageNum
        else:
            self.currentPage = self.get_first_page()

        self.reading()

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
        
    def reading(self, ):
        voices = voices()
        while True:
            # get(text here)
            audio = generate(text=text, voice=self.voice)
