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

    # Função para atualizar o membro
    def atualizar_membro(projeto, equipe, membro, equipe_destino, nova_funcao):
        # Remover membro da equipe atual
        if equipe in lider['projetos'][projeto]['equipes']:
            if membro in lider['projetos'][projeto]['equipes'][equipe]:
                del lider['projetos'][projeto]['equipes'][equipe][membro]
        else:
            sg.popup(f"A equipe {equipe} não existe no projeto {projeto}.")
            return

        # Adicionar membro à nova equipe com a nova função
        if equipe_destino not in lider['projetos'][projeto]['equipes']:
            lider['projetos'][projeto]['equipes'][equipe_destino] = {}

        lider['projetos'][projeto]['equipes'][equipe_destino][membro] = nova_funcao

        for usuario in usuarios_db["usuarios"]:
            if usuario["email"] == membro:
                usuario_projetos = usuario['projetos']
                for projeto_nome, equipe_nome in usuario_projetos.items():
                    if projeto_nome == projeto and equipe_nome == equipe:
                        usuario['projetos'][projeto_nome] = equipe_destino
                        break

        sg.popup(f"Membro {membro} atualizado para a função {nova_funcao} na equipe {equipe_destino} do projeto {projeto}.")
        database.salvar_usuarios(usuarios_db)

    # Construir a lista de projetos, equipes e membros
    projetos_detalhes = []

    # Layout da janela de detalhes com edição
    layout = [
        [sg.Listbox(values=projetos_detalhes, size=(50, 20), key='-PROJETOS-', enable_events=True)],
        [sg.Text('Projeto:'), sg.Combo([], key='-PROJETO-', enable_events=True)],
        [sg.Text('Equipe:'), sg.Combo([], key='-EQUIPE-', enable_events=True)],
        [sg.Text('Membro:'), sg.Combo([], key='-MEMBRO-')],
        [sg.Text('Equipe de Destino:'), sg.Combo([], key='-EQUIPE_DESTINO-')],
        [sg.Text('Função:'), sg.Combo(['scrum_master', 'po', 'dev'], key='-FUNCAO-')],
        [sg.Button('Atualizar Membro')],
        [sg.Button('Sair')]
    ]

    window = sg.Window('Detalhes dos Projetos e Equipes', layout, finalize=True)

    # Preencher a lista de projetos ao abrir a janela
    projetos = list(lider['projetos'].keys())
    window['-PROJETO-'].update(values=projetos)

    # Mostrar detalhes dos projetos ao iniciar
    atualizar_detalhes_projetos(lider, window, projetos_detalhes)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Sair':
            break

        if event == '-PROJETO-':
            projeto_selecionado = values['-PROJETO-']
            equipes = list(lider['projetos'][projeto_selecionado]['equipes'].keys())
            window['-EQUIPE-'].update(values=equipes)
            window['-EQUIPE_DESTINO-'].update(values=equipes)
            window['-MEMBRO-'].update(values=[])

        if event == '-EQUIPE-':
            projeto_selecionado = values['-PROJETO-']
            equipe_selecionada = values['-EQUIPE-']
            membros = list(lider['projetos'][projeto_selecionado]['equipes'][equipe_selecionada].keys())
            window['-MEMBRO-'].update(values=membros)

        if event == 'Atualizar Membro':
            try:
                projeto = values['-PROJETO-']
                equipe = values['-EQUIPE-']
                membro = values['-MEMBRO-']
                equipe_destino = values['-EQUIPE_DESTINO-']
                nova_funcao = values['-FUNCAO-']

                if not projeto or not equipe or not membro or not equipe_destino or not nova_funcao:
                    sg.popup("Por favor, preencha todos os campos.")
                    continue

                atualizar_membro(projeto, equipe, membro, equipe_destino, nova_funcao)

                # Atualizar a lista de detalhes
                atualizar_detalhes_projetos(lider, window, projetos_detalhes)

            except Exception as e:
                sg.popup(f"Erro ao atualizar membro: {str(e)}")

    window.close()

# Função para atualizar detalhes dos projetos na lista
def atualizar_detalhes_projetos(lider, window, projetos_detalhes):
    projetos_detalhes.clear()
    for proj, info_projeto in lider['projetos'].items():
        detalhes_projeto = [f"---------------------------{proj}---------------------------"]
        for eqp, membros in info_projeto['equipes'].items():
            detalhes_equipe = [f"\t---------{eqp}---------"]
            for membro, papel in membros.items():
                detalhes_equipe.append(f"\t\t{membro} - {papel}")
            detalhes_projeto.extend(detalhes_equipe)
        detalhes_projeto.append("")
        projetos_detalhes.extend(detalhes_projeto)
    window['-PROJETOS-'].update(projetos_detalhes)

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