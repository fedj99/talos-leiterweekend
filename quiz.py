#!/usr/bin/python3

from pyfiglet import Figlet

code = '123456'

def print_figlet(text, font='standard', alignment='left'):
    fig = Figlet(font=font, justify=alignment)
    print(fig.renderText(text))


def intro():
    figlet = Figlet()
    print_figlet('Willkommen, Andrin')
    print('\n' * 3)


def passcode_prompt():
    print('Um fortzufahren, tippe den Code ein.\n')
    while True:
        trial = input('Passwort: ')
        if trial.strip() == code:
            print('\n')
            print_figlet('!!! Passwort korrekt !!!', font='banner', alignment='center')
            break
        else:
            print('\nFalsches Passwort. Bitte erneut versuchen.\n')


def quiz():
    print('Um die restichen Ziffern zu erhalten, musst du das folgende Quiz bestehen. Du hast einen Versuch. Dazu musst du mindestens 85%% aller Fragen richtig beantworten.')


def main():
    intro()
    passcode_prompt()
    quiz()


if __name__ == '__main__':
    main()
