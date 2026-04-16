from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Game

client = Blueprint('client', __name__)

@client.route('/lobby')
@login_required
def lobby():
    return render_template('client/lobby.html')

@client.route('/game/<int:game_id>')
@login_required
def game_view(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template('client/game.html', game=game)