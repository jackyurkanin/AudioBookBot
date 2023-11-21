import os
import PyPDF2


class AudioBook:
    def __init__(self) -> None:
        self.funtions = {
           'quit': self.quit,
            'library': self.library,
            'read': self.read
        }
        self.isOn = True

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
        if isinstance(bookName, int):
            catalog = os.listdir('Books')
            bookName = catalog[bookName]
        pdfFileObj = open(f'Books/{bookName}.pdf', 'rb')
        self.book = PyPDF2.PdfReader(pdfFileObj)

        if pageNum:
            self.current = pageNum
        else:
            self.currentPage = self.get_first_page()


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
        