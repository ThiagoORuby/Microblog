import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Configurações do Flask
class Config:
    """
    Chave criptografica para assinaturas e tokens
    O valor da chave secreta é definido como uma expressão com dois termos, unidos pelo or operador. 
    O primeiro termo procura o valor de uma variável de ambiente, também chamada SECRET_KEY. 
    O segundo termo é apenas uma string codificada
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL' ) or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['trs57595@gmail.com']
    