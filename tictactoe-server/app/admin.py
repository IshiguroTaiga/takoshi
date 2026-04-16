from flask import Blueprint, render_template, abort, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Game, User, db, GameLog, QueueEntry
from . import socketio

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
def dashboard():
    if not current_user.is_admin: abort(403)
    games = Game.query.order_by(Game.id.desc()).all()
    users = User.query.all()
    return render_template('admin/dashboard.html', games=games, users=users)

# --- NEW: Watch a specific game UI ---
@admin.route('/monitor/<int:game_id>')
@login_required
def monitor_game(game_id):
    if not current_user.is_admin: abort(403)
    game = Game.query.get_or_404(game_id)
    return render_template('admin/monitor.html', game=game)

# --- NEW: Clear all history and reset IDs ---
@admin.route('/clear_history', methods=['POST'])
@login_required
def clear_history():
    if not current_user.is_admin: abort(403)
    try:
        # Delete all logs, queue entries, and games
        GameLog.query.delete()
        QueueEntry.query.delete()
        Game.query.delete()
        
        # Reset the ID counter (SQLite specific)
        db.session.execute(db.text("DELETE FROM sqlite_sequence WHERE name='game'"))
        db.session.execute(db.text("DELETE FROM sqlite_sequence WHERE name='game_log'"))
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@admin.route('/terminate/<int:game_id>', methods=['POST'])
@login_required
def terminate_game(game_id):
    if not current_user.is_admin: abort(403)
    game = Game.query.get_or_404(game_id)
    game.status = 'terminated'
    db.session.commit()
    socketio.emit('game_terminated', room=f"game_{game_id}")
    return jsonify({'success': True})