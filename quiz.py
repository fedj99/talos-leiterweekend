#!/usr/bin/python3

import sys
import psutil
from functools import reduce
from pyfiglet import Figlet
from time import sleep, time
from random import random
from PIL import Image

# Auxiliary methods


def concat(lists):
    return reduce(lambda acc, x: acc + x, lists, [])


def concat_map(func, list):
    return concat(map(func, list))


def typewrite(*values: object, speed=60, unit='char'):
    def write(str):
        sleep(1 / speed + (random() - 0.5) * 2 / speed)
        sys.stdout.write(str)
        sys.stdout.flush()
    mappers = {
        'char': lambda values: '\n'.join(map(str, values)),
        'line': lambda values: concat_map(lambda val: str(val).splitlines(True), values)
    }
    for item in mappers[unit](values):
        write(item)
    write('\n')


def print_figlet(text, font='standard', alignment='left'):
    fig = Figlet(font=font, justify=alignment)
    typewrite(fig.renderText(text), speed=15, unit='line')


def show_image_timed(path, timeout=5):
    img = Image.open(path)
    img.show()
    sleep(timeout)
    for proc in psutil.process_iter():
        if proc.name() in ['display', 'Preview', 'dllhost.exe']:
            proc.kill()
    img.close()

# Program variables


code = '123456'


# Quiz framework

def info(info):
    def fn():
        typewrite('INFO: ' + info)
    return fn


def confirm(prompt):
    def fn():
        typewrite(prompt)
        typewrite('Drücke <ENTER> um fortzufahren...')
        input()
    return fn


def mc_question(question, options, answer):
    def fn():
        pass
    return fn


def image_question(image, question, options, answer):
    def fn():
        show_image_timed(image, timeout=3)
        mc_question(question, options, answer)
    return fn


def run_quiz(quiz):
    part_no = 1
    typewrite('==== ' + quiz['title'] + ' ====')
    for part in quiz['parts']:
        typewrite('TEIL ' + str(part_no) + ': ' + part['title'] + '\n')
        question_no = 1
        for step in part['script']:
            t = step[0]
            code = step[1]
            if t == 'text' or t == 't':
                code()
            elif t == 'question' or t == 'q':
                typewrite('FRAGE ' + str(question_no) + ':\n')
                question_no += 1
                code()
        part_no += 1
    typewrite('Du hast das Quiz erfolgreich abgeschlossen.')


# Quiz construction

knots = ['Einfacher Knoten', 'Samariter', 'Brezel',
         'Achter (einfach)', 'Achter (doppelt)', 'Spanner', 'Mastwurf', 'Fesselknoten', 'Wickelknoten', 'Maurerknoten']

main_quiz = {
    'title': 'DAS CEVI-QUIZ',
    'parts': [
        {
            'title': 'Knoten',
            'script': [
                ('text', info(
                    'Im folgenden wird dir je ein Bild für 2 Sekunden angezeigt. Du musst dann die Fragen beantworten.')),
                ('text', confirm('Bereit?')),
                ('question', image_question('images/knoten_1.png',
                                            'Welcher Knoten ist das?', knots, 'Samariter')),
                ('question', image_question('images/knoten_2.jpg',
                                            'Welcher Knoten ist das?', knots, 'Achter (doppelt)'))
            ]
        }
    ]
}

# Program


def intro():
    figlet = Figlet()
    print_figlet('Willkommen, Andrin')
    typewrite('\n' * 3)


def passcode_prompt():
    typewrite('Um fortzufahren, tippe den Code ein.\n')
    while True:
        trial = input('Passwort: ')
        if trial.strip() == code:
            typewrite('\n')
            print_figlet('!!! Passwort korrekt !!!',
                         font='banner', alignment='center')
            break
        else:
            typewrite('\nFalsches Passwort. Bitte erneut versuchen.\n')


def quiz():
    typewrite('Um die restichen Ziffern zu erhalten, musst du das folgende Quiz bestehen. Du hast einen Versuch. Dazu musst du mindestens 85%% aller Fragen richtig beantworten.\n\n')
    run_quiz(main_quiz)


def main():
    intro()
    passcode_prompt()
    quiz()


# Main entry point

if __name__ == '__main__':
    main()
