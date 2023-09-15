from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

# useri (seguidor) segue userj (seguido)
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),)

# UserMixin inclui implementações genéricas que são apropriadas para a maioria das classes de modelo de usuário.
class User(UserMixin, db.Model):

    # __tablename__ = "nome-da-tabela"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy = 'dynamic'
    )

    # followed = quem o usuario segue
    # followers = quem segue o usuario

    def __repr__(self):
        return f'<User {{{self.username}}}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()

        return f'https://www.gravatar.com/avatar/{digest}?d=monsterid&s={size}'
    
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # Pega os posts dos seguidos
    def followed_posts(self):
        '''
        Faz um join de Posts e followers pelo indice do usuario seguidoe e filtra para a condição onde o seguidor é o usuario atual, ordenando com base no tempo
        '''
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id = self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

class Post(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post {{{self.body}}}>'


# Carrega um usuario dado id para o flask-login identificar o usuario logado
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
