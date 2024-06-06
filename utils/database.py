import json


def carregar_usuarios():
    try:
        with open('usuarios.json', 'r') as arquivo:
            usuarios = json.load(arquivo)

    except FileNotFoundError:
        usuarios = {'usuarios': []}
    except json.JSONDecodeError:
        usuarios = {'usuarios': []}
    return usuarios

def salvar_usuarios(usuarios):
        with open('usuarios.json', 'w') as arquivo:
            json.dump(usuarios, arquivo, indent=4)
