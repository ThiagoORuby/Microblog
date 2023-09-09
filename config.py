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
    