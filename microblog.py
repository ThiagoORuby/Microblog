from app import init_app, db
from app.models import User, Post

app = init_app()

# cria um contexto de shell que adiciona a instância e os modelos do banco de dados à sessão de shell
@app.shell_context_processor
def make_shell_context():
    return {'db' : db, 'User' : User, 'Post' : Post}

if __name__ == '__main__':
    app.run(debug= True)