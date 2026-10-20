import sqlite3
from models.usuario import Usuario


class UsuarioRepositorio:

    def __init__(self, caminho_banco="database.db"):
        self.caminho = caminho_banco
        self._criar_tabela()

    def _conectar(self):
        conexao = sqlite3.connect(self.caminho)  # era "caminhho"
        conexao.row_factory = sqlite3.Row
        return conexao

    def _criar_tabela(self):
        with self._conectar() as conexao:
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    senha_hash TEXT NOT NULL
                )
            """)

    def salvar(self, usuario):  # agora com 4 espaços, alinhado aos outros
        try:
            with self._conectar() as conexao:
                conexao.execute(
                    "INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
                    (usuario.nome, usuario.email, usuario.senha_hash),
                )
        except sqlite3.IntegrityError:
            raise ValueError("Este e-mail já está cadastrado.")

    def buscar_por_email(self, email):
        with self._conectar() as conexao:  # era "self.conectar()"
            linha = conexao.execute(
                "SELECT * FROM usuarios WHERE email = ?", (email,)
            ).fetchone()
        if linha is None:
            return None
        return Usuario(linha["nome"], linha["email"], linha["senha_hash"], linha["id"])