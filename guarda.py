import argparse
import sys
import json
import os




def hash():
    print(None)

def hmac(password):
    def hmac_i():
        print(password)

    return hmac_i

def set_hash_action(hash_type: str):
    class SetHashAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if hash_type == "hash":
                hash_func = hash
            else:
                value = values[0]
                hash_func = hmac(value)
            setattr(namespace, "hash_func", hash_func)

    return SetHashAction


def set_directory(opcao: str):
    class SetDirectoryAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            value = {'opcao': opcao, 'directory': values[0]}
            setattr(namespace, "opcao", value)

    return SetDirectoryAction


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Guarda verificar arquivos")
    metodo = parser.add_mutually_exclusive_group(required=True)
    metodo.add_argument('-hash', nargs=0, action=set_hash_action("hash"),
                        help="Utilizar a função de hash SHA256")
    metodo.add_argument('-hmac', nargs=1, metavar='SENHA', action=set_hash_action("hmac"),
                        help="Utilizar a funcao de hash SHA256 com senha para autenticacao")
    opcao = parser.add_mutually_exclusive_group(required=True)
    opcao.add_argument('-i', nargs=1, metavar='PASTA', action=set_directory('-i'),
                       help=" inicia a guarda da pasta indicada em <pasta>, ou seja, faz a leitura de todos os "
                            "arquivos da pasta (recursivamente) registrando os dados e Hash/HMAC")
    opcao.add_argument('-t', nargs=1, metavar='PASTA', action=set_directory('-t'),
                       help=" faz o rastreio (tracking) da pasta indicada em <pasta>, inserindo informações sobre "
                            "novos arquivos e indicando alterações detectadas/exclusões")
    opcao.add_argument('-x', nargs=1, metavar='PASTA', action=set_directory('-x'),
                       help="Desativa a guarda e remove a estrutura alocada")
    parser.add_argument('-o', type=str, nargs=1, dest='saida', help="Arquivo de saida do relatorio, "
                                                                    "por padrao o relatorio será exibido no terminal")
    return parser.parse_args(argv[1:])

def guarda(dir_path, hash_path):
    hashs = []

def tracking(dir_path, files_hash):
    pass
def untracking(dir_path, hash_path):
    pass


def read_hash(hash_dir):
    hash_path = os.path.join(hash_dir, 'guarda.json')
    if os.path.isfile(hash_path):
        try:
            files_hashs = json.load(hash_path)
        except json.JSONDecodeError:
            print('Decoding hash error, creating new hash')
            files_hashs = json.dump([], hash_path)
    else:
        files_hashs = json.dump([], hash_path)
    return files_hashs

def update_guardadir(dir_path):
    if not os.path.isdir(dir_path):
        print(dir_path + "is not a directory.")
        sys.exit(1)
    hash_dir = os.path.join(dir_path, 'guarda')
    try:
        os.mkdir(hash_dir)
    except FileExistsError:
        pass
    return hash_dir
if __name__ == "__main__":
    args = parse_args(sys.argv)
    hashs, hash_path = update_guardadir(args.dir_path)
    print(args)
