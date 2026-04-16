from flask_socketio import emit, join_room
from flask_login import current_user
from . import socketio, db
from .models import Game, QueueEntry, GameLog, User
from .logic import TicTacToe

# Helper function to send logs to Admin and Database
def log_event(game_id, message):
    log = GameLog(game_id=game_id, action=message)
    db.session.add(log)
    db.session.commit()
    # This sends the message to your Admin Dashboard live!
    socketio.emit('new_log', {'msg': message}, room='admin_room')

@socketio.on('connect')
def connect():
    if current_user.is_authenticated:
        # If the user is an admin, put them in a special room to receive all logs
        if current_user.is_admin:
            join_room('admin_room')
            print(f"Admin {current_user.username} connected to monitor.")

@socketio.on('join_game')
def on_join_game(data):
    game_id = data['game_id']
    join_room(f"game_{game_id}")
    print(f"User joined room: game_{game_id}")

@socketio.on('join_queue')
def join_queue(data):
    vs_ai = data.get('vs_ai', False)
    if vs_ai:
        game = Game(player1_id=current_user.id, vs_ai=True)
        db.session.add(game)
        db.session.commit()
        log_event(game.id, f"Player {current_user.username} started an AI Game.")
        emit('match_found', {'game_id': game.id})
    else:
        waiter = QueueEntry.query.filter_by(vs_ai=False).filter(QueueEntry.user_id != current_user.id).first()
        if waiter:
            game = Game(player1_id=waiter.user_id, player2_id=current_user.id)
            db.session.add(game)
            db.session.delete(waiter)
            db.session.commit()
            log_event(game.id, f"Match Found: {game.p1.username} vs {game.p2.username}")
            # Notify everyone so the specific users catch it
            emit('match_found', {'game_id': game.id}, broadcast=True)
        else:
            if not QueueEntry.query.filter_by(user_id=current_user.id).first():
                db.session.add(QueueEntry(user_id=current_user.id))
                db.session.commit()
            emit('waiting', {'msg': 'Searching for an opponent...'})

@socketio.on('make_move')
def make_move(data):
    game_id = data['game_id']
    game = Game.query.get(game_id)
    if not game or game.status != 'active':
        return

    idx = data['index']
    ttt = TicTacToe(game.board_state)
    
    # Determine which character this player uses
    char = "X" if current_user.id == game.player1_id else "O"
    
    # Check if it is actually their turn
    if (char == "X" and game.current_turn != 1) or (char == "O" and game.current_turn != 2):
        return

    if ttt.make_move(idx, char):
        game.board_state = "".join(ttt.board)
        game.current_turn = 2 if game.current_turn == 1 else 1
        
        res = ttt.check_winner()
        if res:
            game.status = 'finished'
            game.winner_id = current_user.id if res != "Draw" else 0
            log_event(game.id, f"Game #{game.id} ended. Result: {res}")
        else:
            log_event(game.id, f"{current_user.username} moved at index {idx}")

        db.session.commit()
        
        # Update everyone in the specific game room AND the admin
        update_payload = {
            'game_id': game.id,
            'board': game.board_state, 
            'turn': game.current_turn, 
            'status': game.status
        }
        emit('update', update_payload, room=f"game_{game.id}", broadcast=True)
        socketio.emit('update', update_payload, room='admin_room') # Send specifically to Admin Dashboard

        # Handle AI Turn
        if game.vs_ai and game.status == 'active' and game.current_turn == 2:
            socketio.sleep(0.5) # Simulate AI thinking
            ai_idx = ttt.get_ai_move()
            ttt.make_move(ai_idx, "O")
            game.board_state = "".join(ttt.board)
            game.current_turn = 1
            
            res_ai = ttt.check_winner()
            if res_ai:
                game.status = 'finished'
                game.winner_id = -1 # AI Winner
            
            db.session.commit()
            emit('update', {
                'game_id': game.id,
                'board': game.board_state, 
                'turn': game.current_turn, 
                'status': game.status
            }, broadcast=True)

@socketio.on('instant_restart')
def instant_restart(data):
    game = Game.query.get(data['game_id'])
    if game and game.vs_ai:
        game.board_state = "         "
        game.status = 'active'
        game.current_turn = 1
        db.session.commit()
        
        log_event(game.id, "AI Game Restarted.")
        
        # Notify the player
        emit('update', {
            'game_id': game.id,
            'board': game.board_state,
            'turn': game.current_turn,
            'status': game.status
        }, room=f"game_{game.id}")

@socketio.on('request_rematch')
def request_rematch(data):
    game_id = data['game_id']
    # Tell the OTHER player in the room that a rematch was offered
    # We broadcast to the room, but the person who clicked won't show the modal
    emit('rematch_offered', room=f"game_{game_id}", include_self=False)
    log_event(game_id, f"{current_user.username} requested a rematch.")

@socketio.on('accept_rematch')
def accept_rematch(data):
    game = Game.query.get(data['game_id'])
    if game:
        game.board_state = "         "
        game.status = 'active'
        game.current_turn = 1 # X always starts again
        db.session.commit()
        
        log_event(game.id, "Rematch Accepted. Board Reset.")
        
        # Update both players
        update_payload = {
            'game_id': game.id,
            'board': game.board_state,
            'turn': game.current_turn,
            'status': game.status
        }
        emit('update', update_payload, room=f"game_{game.id}")
        socketio.emit('update', update_payload, room='admin_room')