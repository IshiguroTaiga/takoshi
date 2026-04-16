from . import db  # This imports the db we created in __init__.py
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    player2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    vs_ai = db.Column(db.Boolean, default=False)
    board_state = db.Column(db.String(9), default="         ") 
    current_turn = db.Column(db.Integer, default=1) # 1 for P1, 2 for P2/AI
    status = db.Column(db.String(20), default="active") # active, finished, terminated
    winner_id = db.Column(db.Integer, nullable=True) # 0 for draw, -1 for AI
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class QueueEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vs_ai = db.Column(db.Boolean, default=False)

class GameLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    action = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)