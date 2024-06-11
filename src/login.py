import PySimpleGUI as sg
from src.utils import database
from src import cadastro
from src.colaboradores import colaboradores
from src.lideres import lideres





def verificar_usuario(email, senha):
    usuarios = database.carregar_usuarios()
    for usuario in usuarios['usuarios']:
        if usuario['email'] == email and usuario['senha'] == senha:
            return usuario
    return None

def verificar_email_existe(email):
    usuarios = database.carregar_usuarios()
    for usuario in usuarios['usuarios']:
        if usuario['email'] == email:
            return True
    return False

def tela_login():
    layout = [
        [sg.Text('Email'), sg.Input(key='-EMAIL-')],
        [sg.Text('Senha'), sg.Input(key='-SENHA-', password_char='*')],
        [sg.Button('Login'), sg.Button('Cancelar')]
    ]

    janela = sg.Window('Login', layout)

    while True:
        evento, valores = janela.read()
        if evento == sg.WIN_CLOSED or evento == 'Cancelar':
            break
        if evento == 'Login':
            email = valores['-EMAIL-']
            senha = valores['-SENHA-']

            if verificar_email_existe(email):
                usuario = verificar_usuario(email, senha)
                if usuario:
                    if usuario['lider']:
                        lideres.mostrar_informacoes(email)
                    else:
                        colaboradores.mostrar_informacoes(email)
                else:
                    sg.popup('Senha incorreta!')
            else:
                sg.popup('Email não encontrado, redirecionando para cadastro...')
                cadastro.tela_cadastro(email)
                break

    janela.close()
