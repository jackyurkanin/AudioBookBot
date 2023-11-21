import PyPDF2

def interpret_pdf(title):
    pdfFileObj = open(f'Books/{title}.pdf', 'rb')
    
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    
    # printing number of pages in pdf file
    print(len(pdfReader.pages))
    
    # creating a page object
    pageObj = pdfReader.pages[0]
    print(len(pageObj.extract_text()))
    pageObj = pdfReader.pages[1]
    print(len(pageObj.extract_text()))
    pageObj = pdfReader.pages[2]
    print(len(pageObj.extract_text()))
    pageObj = pdfReader.pages[535]
    print(len(pageObj.extract_text()))
    return pdfReader

if __name__=='__main__':
    interpret_pdf('SnowCrash')