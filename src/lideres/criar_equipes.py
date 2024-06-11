import PySimpleGUI as sg
import random
from src.utils import database

usuarios_db = database.carregar_usuarios()


def criar_equipes(nome, numero_equipes, pessoas_por_equipe, lider_email):
    # Criar uma lista de equipes com nomes
    equipes = [f"Equipe {i+1}" for i in range(numero_equipes)]

    # Filtrar os usuários que são Scrum Masters, POs e Devs
    scrum_masters = [user for user in usuarios_db["usuarios"] if user['papeis_scrum']['scrum_master'] and not user['lider']]
    product_owners = [user for user in usuarios_db["usuarios"] if user['papeis_scrum']['po'] and not user['lider']]
    devs = [user for user in usuarios_db["usuarios"] if (user['papeis_scrum']['dev'] or user['papeis_scrum']['nunca_participei']) and not user['lider']]

    # Encontrar o líder
    lider = next((user for user in usuarios_db["usuarios"] if user['email'] == lider_email), None)
    if not lider:
        print(f"Líder com email {lider_email} não encontrado.")
        return

    # Inicializar o projeto do líder se não existir
    if nome not in lider['projetos']:
        lider['projetos'][nome] = {'equipes': {}}

    # Distribuir os Scrum Masters e Product Owners entre as equipes
    for idx, equipe_nome in enumerate(equipes):
        scrum_master = scrum_masters[idx]
        product_owner = product_owners[idx]

        if nome not in scrum_master["projetos"]:
            scrum_master["projetos"][nome] = equipe_nome
            print(f"{scrum_master['email']} será adicionado à {equipe_nome}")
        else:
            print(f"{scrum_master['email']} já está nesse projeto")

        if nome not in product_owner["projetos"]:
            product_owner["projetos"][nome] = equipe_nome
            print(f"{product_owner['email']} será adicionado à {equipe_nome}")
        else:
            print(f"{product_owner['email']} já está nesse projeto")

        # Adicionar informações ao projeto do líder
        lider['projetos'][nome]['equipes'][equipe_nome] = {
            scrum_master['email']: 'scrum_master',
            product_owner['email']: 'po'
        }

    # Adicionar Devs para preencher as equipes
    dev_idx = 0
    for equipe_nome in equipes:
        equipe_count = sum(1 for user in usuarios_db["usuarios"] if user.get("projetos", {}).get(nome) == equipe_nome)

        while equipe_count < pessoas_por_equipe and dev_idx < len(devs):
            dev = devs[dev_idx]
            if nome not in dev["projetos"]:
                dev["projetos"][nome] = equipe_nome
                print(f"{dev['email']} será adicionado à {equipe_nome}")
                equipe_count += 1

                # Adicionar informações ao projeto do líder
                lider['projetos'][nome]['equipes'][equipe_nome][dev['email']] = 'dev'
            else:
                print(f"{dev['email']} já está nesse projeto")
            dev_idx += 1

    # Salvar o conteúdo atualizado de volta no arquivo
    database.salvar_usuarios(usuarios_db)

def abre_tela(email):
    layout = [
        [sg.Text('Nome do Projeto'), sg.InputText(key='nome_projeto')],
        [sg.Text('Quantidade de Equipes'), sg.InputText(key='quantidade_equipes')],
        [sg.Text('Pessoas por Equipe'), sg.InputText(key='pessoas_por_equipe')],
        [sg.Button('Criar'), sg.Button('Sair')]
    ]

    window = sg.Window('Criar Equipes', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Sair':
            break

        if event == 'Criar':
            nome_projeto = values['nome_projeto']
            quantidade_equipes = int(values['quantidade_equipes'])
            pessoas_por_equipe = int(values['pessoas_por_equipe'])
            criar_equipes(nome_projeto, quantidade_equipes, pessoas_por_equipe, email)
            sg.popup('Equipes criadas com sucesso!')

    window.close()