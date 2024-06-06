import PySimpleGUI as sg
from utils import database

usuarios_db = database.carregar_usuarios()

def mostrar_detalhes_projetos(email):
    # Encontrar o líder
    lider = next((user for user in usuarios_db["usuarios"] if user['email'] == email), None)
    if not lider:
        sg.popup(f"Líder com email {email} não encontrado.")
        return

    # Verificar se o líder tem projetos
    if 'projetos' not in lider or not lider['projetos']:
        sg.popup("Nenhum projeto encontrado para este líder.")
        return

    # Construir a lista de projetos, equipes e membros
    projetos_detalhes = []
    for projeto, info_projeto in lider['projetos'].items():
        detalhes_projeto = [f"Projeto: {projeto}"]
        for equipe, membros in info_projeto['equipes'].items():
            detalhes_equipe = [f"\tEquipe: {equipe}"]
            for membro, papel in membros.items():
                detalhes_equipe.append(f"\t\t{membro} - {papel}")
            detalhes_projeto.extend(detalhes_equipe)
        detalhes_projeto.append("")  # Adiciona uma linha vazia entre projetos
        projetos_detalhes.extend(detalhes_projeto)

    # Mostrar os detalhes dos projetos e equipes em uma janela
    layout = [
        [sg.Listbox(values=projetos_detalhes, size=(50, 20))],
        [sg.Button('Sair')]
    ]

    window = sg.Window('Detalhes dos Projetos e Equipes', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Sair':
            break

    window.close()

# Função principal para iniciar a interface de edição de equipes
def abre_tela(email):
    layout = [
        [sg.Button('Ver Projetos e Equipes', key='ver_projetos')],
        [sg.Button('Sair')]
    ]

    window = sg.Window('Editar Equipes', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Sair':
            break

        if event == 'ver_projetos':
            mostrar_detalhes_projetos(email)

    window.close()