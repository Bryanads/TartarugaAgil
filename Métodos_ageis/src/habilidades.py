import PySimpleGUI as sg
from utils import database
import json

def adicionar_habilidades(email):
    usuarios = database.carregar_usuarios()
    colaborador = next((usuario for usuario in usuarios['usuarios'] if usuario['email'] == email), None)

    layout_papeis_scrum = [
        [sg.Text('Quais papeis já desempenhou na metodologia SCRUM?')],
        [sg.Checkbox('Scrum Master', key='-SCRUM_MASTER-', default=colaborador['papeis_scrum'].get('scrum_master', False))],
        [sg.Checkbox('PO', key='-PO-', default=colaborador['papeis_scrum'].get('po', False))],
        [sg.Checkbox('Dev', key='-DEV-', default=colaborador['papeis_scrum'].get('dev', False))],
        [sg.Checkbox('Nunca participei de uma equipe SCRUM', key='-NUNCA_PARTICIPEI-', default=colaborador['papeis_scrum'].get('nunca_participei', False))]
    ]

    layout_especialidades = [
        [sg.Text('Qual a sua especialidade?')],
        [sg.Checkbox('Desenvolvedor BackEnd', key='-BACKEND-', default=colaborador['especialidades'].get('backend', False))],
        [sg.Checkbox('Desenvolvedor FrontEnd', key='-FRONTEND-', default=colaborador['especialidades'].get('frontend', False))],
        [sg.Checkbox('Desenvolvedor FullStack', key='-FULLSTACK-', default=colaborador['especialidades'].get('fullstack', False))],
        [sg.Checkbox('Designer UX/UI', key='-UX_UI-', default=colaborador['especialidades'].get('ux_ui', False))],
        [sg.Text('Outro:'), sg.Input(key='-OUTRO-', default_text=colaborador['especialidades'].get('outro', ''))]
    ]

    layout_outra_especializacao = [
        [sg.Text('Tem mais alguma especialização?')],
        [sg.Input(key='-OUTRA_ESPECIALIZACAO-', default_text=colaborador.get('outra_especializacao', ''))]
    ]

    layout = [
        [sg.TabGroup([
            [sg.Tab('Papéis SCRUM', layout_papeis_scrum),
             sg.Tab('Especialidades', layout_especialidades),
             sg.Tab('Outras Especializações', layout_outra_especializacao)]
        ])],
        [sg.Button('Salvar'), sg.Button('Cancelar')]
    ]

    janela = sg.Window('Adicionar Habilidades', layout)

    while True:
        evento, valores = janela.read()
        if evento == sg.WIN_CLOSED or evento == 'Cancelar':
            break
        if evento == 'Salvar':
            colaborador['papeis_scrum'] = {
                'scrum_master': valores['-SCRUM_MASTER-'],
                'po': valores['-PO-'],
                'dev': valores['-DEV-'],
                'nunca_participei': valores['-NUNCA_PARTICIPEI-']
            }
            colaborador['especialidades'] = {
                'backend': valores['-BACKEND-'],
                'frontend': valores['-FRONTEND-'],
                'fullstack': valores['-FULLSTACK-'],
                'ux_ui': valores['-UX_UI-'],
                'outro': valores['-OUTRO-']
            }
            colaborador['outra_especializacao'] = valores['-OUTRA_ESPECIALIZACAO-']
            with open('usuarios.json', 'w') as arquivo:
                json.dump(usuarios, arquivo, indent=4)

            sg.popup('Habilidades salvas com sucesso!')
            break

    janela.close()