from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

def conectar_banco():
    conexao = sqlite3.connect('database.db')
    conexao.row_factory = sqlite3.Row
    return conexao

def inicializar_banco():
    conexao = conectar_banco()
    conexao.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

inicializar_banco()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        conexao = conectar_banco()
        usuario = conexao.execute(
            'SELECT * FROM usuarios WHERE email = ? AND senha = ?', 
            (email, senha)
        ).fetchone()
        conexao.close()
        
        if usuario:
            session['usuario_nome'] = usuario['nome']
            return f"Login efetuado com sucesso! Bem-vindo(a) {usuario['nome']}"
        else:
            return "E-mail ou senha incorretos. Tente novamente."
            
    return render_template('login.html')

# Rota de Cadastro (responsável por salvar novos usuários no banco)
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        try:
            conexao = conectar_banco()
            conexao.execute(
                'INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)',
                (nome, email, senha)
            )
            conexao.commit()
            conexao.close()
            return redirect(url_for('login')) # Redireciona para o login após cadastrar com sucesso
        except sqlite3.IntegrityError:
            return "Este e-mail já está cadastrado! Tente outro."
            
    return render_template('cadastro.html')

@app.route('/login/google')
def login_google():
    return "Login com Google em desenvolvimento"

@app.route('/login/facebook')
def login_facebook():
    return "Login com Facebook em desenvolvimento"

if __name__ == '__main__':
    app.run(debug=True)