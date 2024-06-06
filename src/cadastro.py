import PySimpleGUI as sg
from utils import database
from src import login

def tela_cadastro(email):
    layout = [
        [sg.Text('Email'), sg.Input(default_text=email, key='-EMAIL-', readonly=True)],
        [sg.Text('Senha'), sg.Input(key='-SENHA-', password_char='*')],
        [sg.Button('Cadastrar'), sg.Button('Cancelar')]
    ]

    janela = sg.Window('Cadastro', layout)

    while True:
        evento, valores = janela.read()
        if evento == sg.WIN_CLOSED or evento == 'Cancelar':
            break
        if evento == 'Cadastrar':
            senha = valores['-SENHA-']

            usuarios = database.carregar_usuarios()
            novo_usuario = {
                "email": email,
                "senha": senha,
                "lider": False,
                "projetos": {},
                "nome": "",
                "celular": "",
                "idade": "",
                "papeis_scrum": {
                    "scrum_master": False,
                    "po": False,
                    "dev": False,
                    "nunca_participei": False
                },
                "especialidades": {
                    "backend": False,
                    "frontend": False,
                    "fullstack": False,
                    "ux_ui": False,
                    "outro": ""
                },
                "outra_especializacao": ""
            }
            usuarios['usuarios'].append(novo_usuario)
            database.salvar_usuarios(usuarios)
            sg.popup('Usuário cadastrado com sucesso!')
            break

    janela.close()
    login.tela_login()
