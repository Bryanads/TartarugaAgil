import PySimpleGUI as sg
from utils import database
from src.colaboradores import infos_pessoais
from src import habilidades

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
        [sg.Text('Informações do Colaborador', font=('Helvetica', 18), justification='center')],
        [sg.Text('_' * 40, pad=(None, (10, 20)))],
        [sg.Text(f'Nome: {colaborador["nome"]}', font=('Helvetica', 14), justification='center')],
        [sg.Text('Equipes:', font=('Helvetica', 16, 'bold'), justification='center')],
        [sg.Text(', '.join(colaborador['projetos']), font=('Helvetica', 14), justification='center')],
        [sg.Text(f'Número de Celular: {colaborador["celular"]}', font=('Helvetica', 14), justification='center')],
        [sg.Text(f'Idade: {colaborador["idade"]}', font=('Helvetica', 14), justification='center')],
        [sg.Text('Papéis SCRUM:', font=('Helvetica', 16, 'bold'), justification='center')],
        [sg.Text(', '.join([papel for papel in colaborador['papeis_scrum'] if colaborador['papeis_scrum'][papel]]), font=('Helvetica', 14), justification='center')],
        [sg.Text('Especialidades:', font=('Helvetica', 16, 'bold'), justification='center')],
        [sg.Text(', '.join([habilidade for habilidade in colaborador['especialidades'] if colaborador['especialidades'][habilidade]]), font=('Helvetica', 14), justification='center')],
        [sg.Text('Outra Especialização:', font=('Helvetica', 16, 'bold'), justification='center')],
        [sg.Text(colaborador['outra_especializacao'], font=('Helvetica', 14), justification='center')],
        [sg.Button('Sair', size=(10, 2)), sg.Button('Editar', size=(10, 2)), sg.Button('Novas Habilidades', size=(10, 2))]
    ]

    janela_info = sg.Window('Informações do Colaborador', layout_info, element_justification='center')
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

    janela_info.close()
