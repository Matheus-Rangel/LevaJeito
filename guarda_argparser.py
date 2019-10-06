import argparse
from guarda import GuardaHash

def set_hash_action(hash_type: str):
    class SetHashAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if hash_type == "hash":
                guarda_hash = GuardaHash()
            else:
                guarda_hash = GuardaHash(values[0])
            setattr(namespace, "guarda_hash", guarda_hash)
    return SetHashAction


def set_directory(opcao: str):
    class SetDirectoryAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            value = {'modo': opcao, 'dir_path': values[0]}
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
