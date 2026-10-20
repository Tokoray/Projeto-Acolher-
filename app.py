import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.usuario import Usuario
from repositories.usuario_repositorio import UsuarioRepositorio

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-so-para-desenvolvimento")

# Uma única instância do repositório, compartilhada por todas as rotas.
repo = UsuarioRepositorio()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        usuario = repo.buscar_por_email(email)
        if usuario and usuario.conferir_senha(senha):
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            return redirect(url_for("inicio"))

        flash("E-mail ou senha incorretos.")
    return render_template("login.html")


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        if not nome or not email or len(senha) < 6:
            flash("Preencha tudo; a senha precisa de 6+ caracteres.")
            return render_template("cadastro.html")

        try:
            repo.salvar(Usuario.criar(nome, email, senha))
        except ValueError as erro:
            flash(str(erro))
            return render_template("cadastro.html")
        return redirect(url_for("login"))
    return render_template("cadastro.html")


@app.route("/inicio")
def inicio():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    return f"Olá, {session['usuario_nome']}!"

@app.route("/login/google")
def login_google():
    return "Login com Google em desenvolvimento"


@app.route("/login/facebook")
def login_facebook():
    return "Login com Facebook em desenvolvimento"


if __name__ == "__main__":
    app.run(debug=True)