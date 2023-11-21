import os


class AudioBook:
    def __init__(self) -> None:
        self.funtions = {
           'quit': self.quit,
            'library': self.library
        }
        self.isOn = True

    def quit(self):
        self.isOn = False

    def library(self):
        catalog = os.listdir('Books')
        print('---------------------------------')
        print('Below are all of the available books:\n')

        for title in catalog:
            print(title)

        print('---------------------------------')