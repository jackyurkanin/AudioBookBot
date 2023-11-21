import PyPDF2

def interpret_pdf(title):
    pdfFileObj = open(f'Books/{title}.pdf', 'rb')
    
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    
    # printing number of pages in pdf file
    print(len(pdfReader.pages))
    
    # creating a page object
    # pageObj = pdfReader.pages[0]
    # print(len(pageObj.extract_text()))
    # pageObj = pdfReader.pages[1]
    # print(len(pageObj.extract_text()))
    # pageObj = pdfReader.pages[2]
    # print(len(pageObj.extract_text()))
    # pageObj = pdfReader.pages[535]
    # print(len(pageObj.extract_text()))

    
    
    ###### Testing my first relevant page finder #####
    diff = 0
    ind = 0
    while diff < 200:
        pageObj = pdfReader.pages[ind]  
        first  = len(pageObj.extract_text())
        print(first)
        pageObj = pdfReader.pages[ind+1]
        second = len(pageObj.extract_text())
        print(second)
        diff = second - first
        ind += 1
    print(ind)


if __name__=='__main__':
    interpret_pdf('SnowCrash')