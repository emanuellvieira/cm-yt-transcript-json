import os
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Carregar a SECRET_KEY do arquivo .env ou variáveis de ambiente
app.secret_key = os.getenv('SECRET_KEY')

# Configurar OAuth para Google
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('CLIENT_ID'),  # Pega CLIENT_ID do .env ou variáveis de ambiente
    client_secret=os.getenv('CLIENT_SECRET'),  # Pega CLIENT_SECRET do .env ou variáveis de ambiente
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_params=None,
    refresh_token_url=None,
    client_kwargs={'scope': 'openid profile email'}
)

# Rota de login para redirecionar o usuário para o Google
@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

# Rota de autorização para lidar com o retorno do Google
@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    session['user'] = user_info
    return redirect('/')

# Rota principal que exibe as informações do usuário autenticado
@app.route('/')
def index():
    user = session.get('user')
    if user:
        return f'Logado como: {user["email"]}'
    return 'Você não está logado. <a href="/login">Faça login com o Google</a>'

# Rodar a aplicação Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
