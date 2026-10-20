from werkzeug.security import generate_password_hash, check_password_hash


class Usuario:
    """Representa um usuário do sistema.

    Por que uma classe? Para guardar os dados e as regras que pertencem
    ao usuário (como conferir a senha) num lugar só, em vez de espalhar
    isso pelas rotas.
    """

    def __init__(self, nome, email, senha_hash, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        # Atributo "protegido" (underscore): por convenção, quem usa a
        # classe não mexe nele direto. Isso é encapsulamento em Python.
        self._senha_hash = senha_hash

    @classmethod
    def criar(cls, nome, email, senha_pura):
        """Fábrica: cria um usuário já com a senha transformada em hash.

        Por que um classmethod? Para que NINGUÉM consiga criar um Usuario
        guardando a senha pura por descuido. O hash acontece aqui dentro.
        """
        return cls(nome, email, generate_password_hash(senha_pura))

    @property
    def senha_hash(self):
        # Só leitura: o repositório precisa ler o hash para salvar,
        # mas ninguém altera por fora.
        return self._senha_hash

    def conferir_senha(self, senha_pura):
        """O usuário sabe verificar a própria senha (responsabilidade dele)."""
        return check_password_hash(self._senha_hash, senha_pura)