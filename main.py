from AudioBookClass import AudioBook

def main():
    audiobook = AudioBook()
    while audiobook.isOn:
        ins = input('Enter a command: ')
        cmd = ins.split(' ')
        func = audiobook.funtions[cmd[0]]
        if len(cmd) > 1:
            func(cmd[1:])
        else:
            func()
        
if __name__=='__main__':
    main()