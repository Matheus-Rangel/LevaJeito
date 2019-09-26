import argparse

def hmac(senha):
    def hmac_i():
        pass
    return hmac_i

def hash():
    pass

def set_hash_action(hash_type : str):
    class setHashAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            value = values[0]
            if hash_type == "hash":
                hash_func = hash
            else:
                hash_func = hmac(value)
            setattr(namespace, "hash_func", hash_func)
    return setHashAction

def parse_args(){
    parser = argparse.ArgumentParser(description="Guarda verificar arquivos")
    metodo = parser.add_mutually_exclusive_group(True)
    metodo.add_argument('-hash', nargs=0, action=set_hash_action("hash"), description="Utilizar a função de hash SHA256")
    metodo.add_argument('-hmac', nargs=1, metavar='SENHA', action=set_hash_action("hmac"), description="Utilizar a funcao de hash SHA256 com senha para autenticacao")
    opcao = parser.add_mutually_exclusive_group(True)

}

if __name__ == "__main__":
    
    meetodo = sys.argv[1]
    senha = None
    if metodo == "-hmac":
        senha = sys.argv[2]
    opc 