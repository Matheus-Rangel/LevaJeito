from guarda import Guarda
from guarda_argparser import parse_args
import sys

def main():
    args = parse_args(sys.argv)
    if args.saida:
        sys.stdout = open(args.saida[0], 'w')
    modo = args.opcao['modo']
    dir_path = args.opcao['dir_path']
    guarda = Guarda(args.guarda_hash, dir_path)
    if modo == '-i':
        print("Arquivos identificados: ")
        guarda.inspect()
    elif modo == '-t':
        guarda.tracking()
    elif modo == '-x':
        guarda.untracking()


if __name__ == '__main__':
    main()
