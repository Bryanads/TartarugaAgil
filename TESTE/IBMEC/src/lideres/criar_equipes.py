import PySimpleGUI as sg

def abre_tela():
    layout = [
        [sg.Text('CRIAR EQUIPES')],
        [sg.Button('SAIR')]
    ]
    window = sg.Window('CRIAR EQUIPES', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'SAIR':
            window.close()