from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from server.game_logic import Game
from server.websocket_manager import WebSocketManager

app = FastAPI()

manager = WebSocketManager()
game = Game()

@app.websocket("/ws/game")
async def game_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    print("Client connected")
    try:
        while True:
            data = await websocket.receive_json()
            print("Received data:", data)
            action = data.get('action')

            if action == 'initialize':
                player_a = data['player_a']
                player_b = data['player_b']
                print(f"Initializing game with Player A: {player_a} and Player B: {player_b}")
                game.initialize_game(player_a, player_b)
                await manager.broadcast(game.get_game_state())

            elif action == 'move':
                player = data['player']
                character = data['character']
                direction = data['direction']
                if game.current_turn == player and game.make_move(player, character, direction):
                    await manager.broadcast(game.get_game_state())
                    if game.check_game_over():
                        await manager.broadcast({'message': f'Player {player} wins!'})
                        break
                else:
                    await websocket.send_json({'message': 'Invalid move'})

            elif action == 'reset_game':
                print("Resetting game...")
                game.reset_game()
                print("Game state after reset:", game.get_game_state())
                
                # Optionally reinitialize with default players
                # For example:
                default_player_a = ['P1', 'P2', 'H1', 'H2', 'P3']
                default_player_b = ['P1', 'P2', 'H1', 'H2', 'P3']
                game.initialize_game(default_player_a, default_player_b)
                
                await manager.broadcast(game.get_game_state())

    except WebSocketDisconnect:
        print("Client disconnected")
        manager.disconnect(websocket)


@app.get("/")
async def root():
    return {"message": "WebSocket server is running!"}
