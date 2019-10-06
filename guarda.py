import sys
import json
import os
import hashlib
import shutil

class GuardaHash:
    def __init__(self, password: str = ""):
        self.password = password

    def hash(self, b: bytes):
        m = hashlib.sha256()
        m.update(b)
        m.update(self.password.encode('utf-8'))
        return m.digest().hex()


class Guarda:
    def __init__(self, guarda_hash: GuardaHash, dir_path):
        self._guarda_hash = guarda_hash
        self._dir_path = dir_path
        self._hash_path = os.path.join(self.update_guardadir(), 'guarda.json')

    def inspect(self):
        hashs = {}
        for root, dirs, files in os.walk(self._dir_path):
            if root.startswith(os.path.join(self._dir_path, "guarda")):
                continue
            for file in files:
                path_file = os.path.join(root, file)
                h = self._guarda_hash.hash(open(path_file, mode='rb').read())
                hashs[path_file] = h
        json.dump(hashs, open(self._hash_path, mode='w'), indent=4)
        for key in hashs:
            print(key + ": " + hashs[key])

    def tracking(self):
        files_hash = self.read_hash()
        result = ""
        for root, dirs, files in os.walk(self._dir_path):
            if root.startswith(os.path.join(self._dir_path, "guarda")):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                h = self._guarda_hash.hash(open(file_path, mode='rb').read())
                if file_path in files_hash.keys():
                    old_h = files_hash[file_path]
                    files_hash.pop(file_path)
                    if h != old_h:
                        result += f"[ALTERADO] {file_path}\n"
                else:
                    result += f"[NOVO] {file_path}\n"
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
