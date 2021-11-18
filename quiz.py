#!/usr/bin/python3

import sys
import psutil
from functools import reduce
from pyfiglet import Figlet
from time import sleep
from random import random
from PIL import Image

# Auxiliary methods

base_path = '.'
disable_animations = False


def path(relative_path):
    return base_path + '/' + relative_path


def concat(lists):
    return reduce(lambda acc, x: acc + x, lists, [])


def concat_map(func, list):
    return concat(map(func, list))


def typewrite(*values: object, speed=150, unit='char', newline=True):
    if (disable_animations):
        print(*values, end='\n' if newline else '')
    else:
        def write(str):
            sleep(1 / speed + random() * 1 / speed)
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


def pause(seconds):
    if not disable_animations:
        sleep(seconds)


def print_figlet(text, font='standard', alignment='left'):
    fig = Figlet(font=font, justify=alignment)
    typewrite(fig.renderText(text), speed=15, unit='line')


def show_image_timed(path, timeout=5):
    img = Image.open(path)
    img.show()
    sleep(timeout)
    for proc in psutil.process_iter():
        if proc.name() in ['display', 'Preview', 'Microsoft.Photos.exe', 'Photos']:
            # proc.kill()
            proc.terminate()
    img.close()

# Program variables


code = '123456'

final_code_part = '78'


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


def sc_question(question, options, answer):
    def fn():
        if question != None:
            typewrite(question + '\n')
        op_no = 1
        for option in options:
            typewrite(str(op_no) + ': ' + option, speed=300)
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
                else:
                    typewrite('Keine gültige eingabe.')
            except:
                typewrite('Keine gültige eingabe.')
        correct = guess == answer
        return correct
    return fn


def image_question(image, question, options, answer):
    def fn():
        typewrite(question + '\n')
        pause(1)
        show_image_timed(path(image), timeout=2.3)
        return sc_question(None, options, answer)()
    return fn


def run_quiz(quiz):
    part_no = 1
    num_correct = 0
    pts_total = 0
    typewrite('==== ' + quiz['title'] + ' ====')
    for part in quiz['parts']:
        typewrite('TEIL ' + str(part_no) + ': ' + part['title'] + '\n')
        question_no = 1
        num_correct_part = 0
        pts_part = 0
        for step in part['script']:
            t = step[0]
            code = step[1]
            if t == 'text' or t == 't':
                code()
            elif t == 'question' or t == 'q':
                typewrite('FRAGE ' + str(question_no) + ':\n')
                question_no += 1
                correct = code()
                typewrite('\nDeine Antwort ist ' +
                          ('KORREKT!' if correct else ' FALSCH...'))
                pts_total += 1
                pts_part += 1
                if (correct):
                    num_correct += 1
                    num_correct_part += 1
                typewrite()
                pause(1)
        typewrite('-------------')
        typewrite('Teil abgeschlossen. Erreichte Punktzahl: ' +
                  str(num_correct_part) + '/' + str(pts_part))
        pause(1)
        typewrite('\n-------------')
        part_no += 1
    percentage = num_correct / pts_total * 100
    typewrite('Du hast das Quiz abgeschlossen. Erreichte Punktzahl: ' +
              str(num_correct) + '/' + str(pts_total) +
              ' (' + str(percentage) + '%%)')
    return percentage


# Quiz construction

knots = [
    'Einfacher Knoten',  # 1
    'Samariter',  # 2
    'Brezel',  # 3
    'Achter (einfach)',  # 4
    'Achter (doppelt)',  # 5
    'Spanner',  # 6
    'Mastwurf',  # 7
    'Fesselknoten',  # 8
    'Wickelknoten',  # 9
    'Maurerknoten'  # 10
]

main_quiz = {
    'title': 'DAS CEVI-QUIZ',
    'parts': [
        {
            'title': 'Knotenkunde',
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
                                   'Welcher Knoten ist das?', knots, 2)
                ),
                (
                    'question',
                    image_question('images/knoten_2.jpg',
                                   'Welcher Knoten ist das?', knots, 5)
                ),
                (
                    'question',
                    image_question('images/knoten_5.JPG',
                                   'Welcher Knoten ist das?', knots, 7)
                ),
                (
                    'question',
                    image_question('images/knoten_6.png',
                                   'Welcher Knoten ist das?', knots, 6)
                )
            ]
        },
        {
            'title': '1. Hilfe',
            'script': [
                (
                    'question',
                    sc_question(
                        'Was ist das erste, was du bei einem Unfall tust?',
                        [
                            'Alarmieren',
                            'Weglaufen',
                            'Person(en) ansprechen',
                            'Unfallort sichern',
                            'Ein Foto machen'
                        ],
                        4
                    )
                ),
                (
                    'question',
                    sc_question(
                        'Wofür steht "BLS-AED"?',
                        [
                            'Beatmen, Lagern, Sichern - Automatische elektrische Defibrillation',
                            'Basic Life Support - Automatic Electric Defibrillation',
                            'Be Like Sherlock - Analyze Every Detail',
                            'Begin Life Saving - Alert Every Doctor'
                        ],
                        2
                    )
                ),
                (
                    'question',
                    sc_question(
                        'Bei einem Sonnenstich, wie soll die Person gelagert werden?',
                        [
                            'Füsse erhöht',
                            'Stehend',
                            'Flach auf Boden',
                            'Oberkörper erhöht',
                            'Kopfstand'
                        ],
                        4
                    )
                ),
                (
                    'question',
                    sc_question(
                        'Notrufnummern - Wähle die Richtige antwort',
                        [
                            'Ambulanz -> 144 --- Feuerwehr -> 117 --- Polizei -> 112 --- Rega -> 1144 --- Internationaler Notruf -> 145',
                            'Ambulanz -> 144 --- Feuerwehr -> 117 --- Polizei -> 118 --- Rega -> 4141 --- Internationaler Notruf -> 112',
                            'Ambulanz -> 114 --- Feuerwehr -> 118 --- Polizei -> 117 --- Rega -> 1414 --- Internationaler Notruf -> 112',
                            'Ambulanz -> 114 --- Feuerwehr -> 118 --- Polizei -> 112 --- Rega -> 1414 --- Internationaler Notruf -> 117',
                            'Ambulanz -> 144 --- Feuerwehr -> 118 --- Polizei -> 117 --- Rega -> 1414 --- Internationaler Notruf -> 112'
                        ],
                        5
                    )
                ),
                (
                    'question',
                    sc_question(
                        'Welche der folgenden Fragen musst du *NICHT* bei einem Notruf beantworten?',
                        [
                            'Wo hat sich der Unfall ereignet?',
                            'Wer telefoniert?',
                            'Warum ist der Unfall geschehen?',
                            'Was ist vorgefallen?',
                            'Wann ist der Unfall geschehen?',
                            'Wie viele Personen sind verletzt?'
                        ],
                        3
                    )
                ),
                (
                    'question',
                    sc_question(
                        'Die stabile Seitenlage wird angewandt bei...',
                        [
                            'einem Bewusstlosen mit normaler Atmung',
                            'einen Betroffenen im Schockzustand',
                            'eine Person ohne normale Atmung',
                            'einem Freunden, der die Fresse nicht halten will'
                        ],
                        1
                    )
                )
            ]
        },
        {
            'title': 'Cevi-Geschichte',
            'script': [
                (
                    'question',
                    sc_question(
                        'Wer hat die erste Cevi-Gruppe der Schweiz gegründet?',
                        [
                            'Christoph Blocher',
                            'Henry Dunant',
                            'Friedrich Maria Remarque',
                            'George Williams',
                            'Angela Merkel'
                        ],
                        2
                    )
                ),
                (
                    'question',
                    sc_question(
                        'Wofür steht YMCA?',
                        [
                            'Young Mormons Club Association',
                            'Youth Male Christian Association',
                            'Yemen Modern Combat Association',
                            'Young Men\'s Christian Association'
                        ],
                        4
                    )

                ),
                (
                    'question',
                    sc_question(
                        'Welche Abteilung hat die Foulard-Farben Orange und Blau?',
                        [
                            'Töss',
                            'Wülflingen',
                            'Veltheim',
                            'Seuzach',
                            'Wiesendangen-Elsau-Hegi',
                        ],
                        1
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
    typewrite('Um die restichen Ziffern zu erhalten, musst du das folgende Quiz bestehen. '
              + 'Du hast einen Versuch, wenn du es nicht schaffst löscht sich diese Datei von selbst. '
              + 'Du musst dazu mindestens 84.61538461538461%% aller Fragen richtig beantworten.\n\n')
    return run_quiz(main_quiz)


def outro(percentage):
    typewrite()
    if (percentage >= 84):
        print_figlet('Quiz bestanden', font='digital', alignment='center')
        typewrite(
            'Der Code war noch nicht vollständig... Du hast dir nun auch den letzten Teil wohl verdient.')
    else:
        print_figlet('Nicht bestanden', font='digital')
        typewrite(
            '\nAch was solls, ich wollte dir eh nur Zeit verlieren lassen...')
        typewrite(
            'Der code war noch nicht vollständig... Ich gebe dir jetzt trotzdem noch den letzten Teil.')
    typewrite('Der letzte Teil des Codes lautet...')
    pause(1)
    print_figlet(str(final_code_part), font='big', alignment='center')
    typewrite('\nMerke ihn dir gut!\n')
    pause(1)
    typewrite('Folge nun dem Ladekabel so weit wie möglich...\n')
    pause(2)
    print_figlet('Viel Spass', font='lean')


def main():
    intro()
    passcode_prompt()
    percentage = quiz()
    outro(percentage)


# Main entry point

if __name__ == '__main__':
    main()
