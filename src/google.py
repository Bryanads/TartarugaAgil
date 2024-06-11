import PySimpleGUI as sg

def abrir_tela():
    # Layout da janela
    layout = [
        [sg.Text("LOGIN COM O GOOGLE INDISPONÍVEL NO MOMENTO")],
        [sg.Button("OK"), sg.Button("Sair")],

    ]

    # Criação da janela
    window = sg.Window("GOOGLE", layout)

    # Loop de eventos
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Sair':
            break
        if event == 'OK':
            break

    window.close()