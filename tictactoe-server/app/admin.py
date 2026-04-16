from flask import Blueprint, render_template, abort, jsonify
from flask_login import login_required, current_user
from .models import Game, User, db
from . import socketio

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
def dashboard():
    if not current_user.is_admin: abort(403)
    games = Game.query.all()
    users = User.query.all()
    return render_template('admin/dashboard.html', games=games, users=users)

@admin.route('/terminate/<int:game_id>', methods=['POST'])
@login_required
def terminate_game(game_id):
    if not current_user.is_admin: abort(403)
    game = Game.query.get_or_404(game_id)
    game.status = 'terminated'
    db.session.commit()
    
    # Notify the players immediately via WebSocket
    socketio.emit('game_terminated', {'msg': 'An admin ended this game.'}, room=f"game_{game_id}")
    socketio.emit('new_log', {'msg': f"Admin terminated Game #{game_id}"}, room='admin_room')
    
    return jsonify({'success': True})