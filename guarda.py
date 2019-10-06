import sys
import json
import os
import hashlib
import shutil


class GuardaHash:
    def __init__(self, password: str = ""):
        self.password = password

    # Faz o hash do array de bytes
    def hash(self, b: bytes):
        m = hashlib.sha256()
        m.update(b)
        # Append da senha caso a opção escolhida seja hmac
        m.update(self.password.encode('utf-8'))
        # Calcula o hash e salva o resultado em uma string no formato hexadecimal
        return m.hexdigest()


class Guarda:
    def __init__(self, guarda_hash, dir_path):
        # Objeto de hash que será utilizado pelo Guarda
        self._guarda_hash = guarda_hash
        # Caminho do diretorio que deve ser verificado
        self._dir_path = dir_path
        # Caminho do arquivo onde a hash dos arquivos será armazenada
        self._hash_path = os.path.join(self.update_guardadir(), 'guarda.json')

    def inspect(self):
        """
        Inspeciona os arquivos presentes no diretorio e salva a hash de cada arquivo
        """
        hashs = {}
        # Iterando pelo diretorio
        for root, dirs, files in os.walk(self._dir_path):
            # Ignorar a pasta criada pelo guarda onde a hash fica salva
            if root.startswith(os.path.join(self._dir_path, "guarda")):
                continue
            # Iterando sobre os arquivo presentes
            for file in files:
                path_file = os.path.join(root, file)
                # Calcula a hash do arquivo
                h = self._guarda_hash.hash(open(path_file, mode='rb').read())
                # Salva a hash no dicionario utilizando como chave o caminho do arquivo
                hashs[path_file] = h
        # Salva o dicionario com todas as hashs em um arquivo no formato json
        json.dump(hashs, open(self._hash_path, mode='w'), indent=4)
        # Printando o resultado
        for key in hashs:
            print(key + ": " + hashs[key])

    def tracking(self):
        # Le o arquivo de hash presente no diretorio
        files_hash = self.read_hash()
        result = ""
        for root, dirs, files in os.walk(self._dir_path):
            if root.startswith(os.path.join(self._dir_path, "guarda")):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                h = self._guarda_hash.hash(open(file_path, mode='rb').read())
                # Verifica se o arquivo estáno dicionario.
                if file_path in files_hash.keys():
                    old_h = files_hash[file_path]
                    files_hash.pop(file_path)
                    if h != old_h:
                        # Caso a hash esteja diferente significa que o arquivo foi alterado
                        result += f"[ALTERADO] {file_path}\n"
                else:
                    # Caso o arquivo não esteja no dicionario significa que ele foi criado após a varredura
                    result += f"[NOVO] {file_path}\n"
        # os arquivos no dicionario que não foram encontrados
        for deleted_file_path in files_hash.keys():
            result += f"[REMOVIDO] {deleted_file_path}\n"
        if not result:
            print("Nenhuma alteração detectada.")
            return
        print("Arquivos modificados: ")
        print(result)

    def untracking(self):
        shutil.rmtree(os.path.join(self._dir_path, 'guarda'), ignore_errors=True)
        print("Guarda desativada.")

    def read_hash(self):
        if os.path.isfile(self._hash_path):
            try:
                files_hashs = json.load(open(self._hash_path, mode='rb'))
            except json.JSONDecodeError:
                print('Erro na leitura do arquivo de hash, criando novo arquivo.')
                json.dump({}, open(self._hash_path, mode='w'))
                files_hashs = {}
        else:
            json.dump({}, open(self._hash_path, mode='w'))
            files_hashs = {}
        return files_hashs

    def update_guardadir(self):
        if not os.path.isdir(self._dir_path):
            print(self._dir_path + " nao é um diretorio.")
            sys.exit(1)
        hash_dir = os.path.join(self._dir_path, 'guarda')
        try:
            os.mkdir(hash_dir)
        except FileExistsError:
            pass
        return hash_dir
