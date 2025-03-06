from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'chave_secreta'

# Informações de login hardcoded
usuarios = {
    "admin@laminacao.com": "admin123",  # Chave: email, Valor: senha
    "usuario@laminacao.com": "senha123",
}

# Função para verificar o login
def verify_login(email, senha):
    # Verifica se o email e senha correspondem aos armazenados no dicionário 'usuarios'
    if email in usuarios and usuarios[email] == senha:
        return True
    return False

# Rota da página inicial
@app.route('/')
def home():
    return render_template('index.html')  # Página inicial simples com um login

# Rota para login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    if verify_login(email, senha):
        session['user'] = email  # Armazena o email do usuário na sessão
        flash('Seja bem-vindo à Laminação Galdino! O site estará disponível em breve!')
        return redirect(url_for('welcome'))  # Redireciona para a página de boas-vindas
    else:
        flash('Email ou senha inválidos. Tente novamente.')
        return redirect(url_for('home'))  # Redireciona para a página de login

# Página de boas-vindas
@app.route('/welcome')
def welcome():
    if 'user' not in session:
        return redirect(url_for('home'))  # Se não estiver logado, redireciona para o login

    return render_template('welcome.html', user=session['user'])  # Passa o nome de usuário para a tela de boas-vindas

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove o usuário da sessão
    flash('Você foi desconectado com sucesso!')
    return redirect(url_for('home'))  # Redireciona para a página de login

if __name__ == '__main__':
    app.run(debug=True)
