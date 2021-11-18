#!/usr/bin/python3

import sys
import psutil
from functools import reduce
from pyfiglet import Figlet
from time import sleep, time
from random import random
from PIL import Image

# Auxiliary methods

base_path = '.'
disable_animations = True


def path(relative_path):
    return base_path + '/' + relative_path


def concat(lists):
    return reduce(lambda acc, x: acc + x, lists, [])


def concat_map(func, list):
    return concat(map(func, list))


def typewrite(*values: object, speed=300, unit='char', newline=True):
    if (disable_animations):
        print(*values)
    else:
        def write(str):
            sleep(1 / speed)
            sys.stdout.write(str)
            sys.stdout.flush()
        mappers = {
            'char': lambda values: '\n'.join(map(str, values)),
            'line': lambda values: concat_map(lambda val: str(val).splitlines(True), values)
        }
        for item in mappers[unit](values):
            write(item)
        if newline:
            write('\n')


def tw_input(prompt):
    typewrite(prompt + ' ', newline=False)
    return input()


def print_figlet(text, font='standard', alignment='left'):
    fig = Figlet(font=font, justify=alignment)
    typewrite(fig.renderText(text), speed=15, unit='line')


def show_image_timed(path, timeout=5):
    img = Image.open(path)
    img.show()
    sleep(timeout)
    for proc in psutil.process_iter():
        if proc.name() in ['display', 'Preview', 'Microsoft.Photos.exe', 'Photos']:
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
        tw_input('Drücke <ENTER> um fortzufahren...')
    return fn


def mc_question(question, options, answer):
    def fn():
        typewrite(question + '\n')
        op_no = 1
        for option in options:
            typewrite(str(op_no) + ': ' + option)
            op_no += 1
        typewrite()
        guess = 0
        while True:
            guess_string = tw_input(
                'Gib die Zahl deiner Antwort ein und drücke <ENTER>:')
            try:
                guess = int(guess_string)
                if (guess > 0 and guess <= len(options)):
                    break
            except:
                typewrite('Keine gültige eingabe.')
        correct = options[guess - 1] == answer
        typewrite('Deine Antwort ist ' +
                  ('KORREKT!' if correct else ' FALSCH...'))
        typewrite()
    return fn


def image_question(image, question, options, answer):
    def fn():
        show_image_timed(path(image), timeout=2.3)
        mc_question(question, options, answer)()
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
                (
                    'text',
                    info(
                        'Im folgenden wird dir je ein Bild für 2 Sekunden angezeigt. Du musst dann die Fragen beantworten.')
                ),
                (
                    'text',
                    confirm('Bereit?')
                ),
                (
                    'question',
                    image_question('images/knoten_1.png',
                                   'Welcher Knoten ist das?', knots, 'Samariter')
                ),
                (
                    'question',
                    image_question('images/knoten_2.jpg',
                                   'Welcher Knoten ist das?', knots, 'Achter (doppelt)')
                )
                (
                    'question',
                    image_question('images/knoten_5.JPG',
                                   'Welcher Knoten ist das?', knots, 'Mastwurf')
                ),
                (
                    'question',
                    image_question('images/knoten_6.png',
                                   'Welcher Knoten ist das?', knots, 'Spanner')
                )
            ]
        },
        {
            'title': '1. Hilfe',
            'script': [
                (
                    'question',
                    mc_question(
                        'Was ist das erste, was du bei einem Unfall tust?',
                        [
                            'Alarmieren',
                            'Weglaufen',
                            'Person(en) ansprechen',
                            'Unfallort sichern',
                            'Ein Foto machen'
                        ],
                        'Unfallort sichern'
                    )
                ),
                (
                    'question',
                    mc_question(
                        'Wofür steht "BLS-AED"?',
                        [
                            'Beatmen, Lagern, Sichern - Automatische elektrische Defibrillation',
                            'Basic Life Support - Automatic Electric Defibrillation',
                            'Be Like Sherlock - Analyze Every Detail',
                            'Begin Life Saving - Alert Every Domain'
                        ],
                        'Basic Life Support - Automatic Electric Defibrillation'
                    )
                ),
                (
                    'question',
                    mc_question(
                        'Bei einem Sonnenstich, wie soll die Person gelagert werden?',
                        [
                            'Füsse erhöht',
                            'Oberkörper erhöht',
                            'Aufrecht',
                            'Flach auf Boden'
                        ],
                        'Oberkörper erhöht'
                    )
                )
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
