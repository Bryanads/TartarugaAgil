import PySimpleGUI as sg
from utils import database
from src.colaboradores import infos_pessoais
from src import habilidades
from src.lideres import criar_equipes
from src.lideres import editar_equipes

def carregar_colaborador(email):
    usuarios = database.carregar_usuarios()
    colaborador = next((usuario for usuario in usuarios['usuarios'] if usuario['email'] == email), None)
    return usuarios, colaborador

def mostrar_informacoes(email):
    _, colaborador = carregar_colaborador(email)

    if colaborador is None:
        return

    sg.theme('DarkGrey13')

    layout_info = [
        [sg.Text('Informações do Líder', font=('Helvetica', 18), justification='center')],
        [sg.Text('_' * 40, pad=(None, (10, 20)))],
        [sg.Text(f'Nome: {colaborador["nome"]}', font=('Helvetica', 14), justification='center')],
        [sg.Text('Equipes:', font=('Helvetica', 16, 'bold'), justification='center')],
        [sg.Text(', '.join(colaborador['equipes']), font=('Helvetica', 14), justification='center')],
        [sg.Text(f'Número de Celular: {colaborador["celular"]}', font=('Helvetica', 14), justification='center')],
        [sg.Text(f'Idade: {colaborador["idade"]}', font=('Helvetica', 14), justification='center')],
        [sg.Button('Criar novo projeto', size=(10, 2)), sg.Button('Editar Projeto', size=(10, 2))],
        [sg.Button('Sair', size=(10, 2)), sg.Button('Editar', size=(10, 2)), sg.Button('Novas Habilidades', size=(10, 2))]
    ]

    janela_info = sg.Window('Informações do Líder', layout_info, element_justification='center')
    while True:
        evento_info, _ = janela_info.read()
        if evento_info == sg.WIN_CLOSED or evento_info == 'Sair':
            break
        if evento_info == 'Editar':
            janela_info.close()
            infos_pessoais.tela_colaborador(email)
        if evento_info == 'Novas Habilidades':
            janela_info.close()
            habilidades.adicionar_habilidades(email)
        if evento_info == 'Criar novo projeto':
            janela_info.close()
            criar_equipes.abre_tela()
        if evento_info == 'Editar Projeto':
            janela_info.close()
            editar_equipes.abre_tela()


    janela_info.close()
