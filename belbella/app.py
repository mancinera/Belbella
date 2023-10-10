# Framework usado = FLASK
# pip install flask
# pip install flask-sqlalchemy
from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash #Criptografa a senha
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loja.sqlite3'
db = SQLAlchemy(app)


#Classe de produto
class User(db.Model):
    user_id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(60), unique=True, nullable=False)#Login do usuario
    senha = db.Column(db.String(60), nullable=False)#Senha do usuario


class Produto(db.Model):
    id_poduto = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome_produto = db.Column(db.String(50))
    preco = db.Column(db.Float)
    tamanho = db.Column(db.String(1))
    numero = db.Column(db.Integer)
    descricao = db.Column(db.String(255))

    def __init__(self, id_produto, nome_produto, preco, tamanho, numero, descricao):
        self.id_produto = id_produto
        self.nome_produto = nome_produto
        self.preco = preco
        self.tamanho = tamanho
        self.numero = numero
        self.descricao = descricao

#ROTAS
@app.route('/')
def index():
    return render_template('_index/index.html')

@app.route('/register')
def register():
    return render_template('_index/register.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        hashed_password = generate_password_hash(senha, method='sha256')
        novo_usuario = User(usuario=usuario, senha=hashed_password)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Registro bem-sucedido! Agora você pode fazer login.', 'success')
        return redirect(url_for('login'))
    return render_template('_index/register.html')

@app.route('/login')
def login():
    return render_template('_index/login.html')


@app.route('/login/auth', methods=['GET', 'POST'])
def login_auth():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        usuario = User.query.filter_by(usuario=usuario).first()
        if usuario and check_password_hash(usuario.senha, senha):
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('_index/profile-page.html'))
        else:
            flash('Falha no login. Verifique suas credenciais.', 'danger')
    return render_template('_index/index.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você saiu com sucesso.', 'success')
    return redirect(url_for('_index/index.html'))


@app.route('/profile-page')
def profile():
    return render_template('_index/profile-page.html')
    
if __name__ == '__main__':
    with app.app_context():
      db.create_all()
    app.run(debug=True)