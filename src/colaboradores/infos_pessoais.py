from src.colaboradores import colaboradores
import PySimpleGUI as sg
from utils import database

def tela_colaborador(email):
    usuarios, colaborador = colaboradores.carregar_colaborador(email)

    if not colaborador:
        sg.popup('Colaborador não encontrado.')
        return


    layout = [
        [sg.Text('Nome'), sg.Input(default_text=colaborador.get('nome', ''), key='-NOME-')],
        [sg.Text('Número de Celular'), sg.Input(default_text=colaborador.get('celular', ''), key='-CELULAR-')],
        [sg.Text('Idade'), sg.Input(default_text=colaborador.get('idade', ''), key='-IDADE-')],
        [sg.Button('Salvar'), sg.Button('Sair')]
    ]

    janela = sg.Window('Colaborador', layout)

    while True:
        evento, valores = janela.read()
        if evento == sg.WIN_CLOSED or evento == 'Sair':
            break
        if evento == 'Salvar':
            colaborador['nome'] = valores['-NOME-']
            colaborador['celular'] = valores['-CELULAR-']
            colaborador['idade'] = valores['-IDADE-']
            database.salvar_usuarios(usuarios)
            if colaborador['nome'] and colaborador['celular'] and colaborador['idade']:
                janela.close()
                colaboradores.mostrar_informacoes(colaborador)


        colaboradores.mostrar_informacoes(colaborador)