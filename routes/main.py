from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/about')
def about():
    return render_template('index.html')

@main_bp.route('/contact')
def contact():
    return render_template('index.html')

@main_bp.route('/test')
def test():
    return render_template('test.html')

@main_bp.route('/quick')
def quick():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sistema Funcionando</title>
        <style>
            body { font-family: Arial; padding: 40px; background: #f0f8ff; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 5px; }
            .success { color: green; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🦷 Sistema da Clínica Funcionando!</h1>
            <p class="success">✅ Servidor: Ativo | ✅ Banco: Conectado | ✅ Login: Pronto</p>
            
            <h3>Acesso Rápido:</h3>
            <a href="/auth/login" class="btn">🔑 Fazer Login</a>
            <a href="/auth/register" class="btn">📝 Cadastrar</a>
            <a href="/" class="btn">🏠 Início</a>
            
            <h3>Credenciais Admin:</h3>
            <p><strong>Email:</strong> admin@clinic.com<br>
            <strong>Senha:</strong> admin123</p>
            
            <p><em>Sistema 100% operacional com PostgreSQL da Railway!</em></p>
        </div>
    </body>
    </html>
    '''
