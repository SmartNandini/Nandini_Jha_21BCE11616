const gameBoard = document.getElementById('gameBoard');
const statusDiv = document.getElementById('status');
const selectedCharacterDiv = document.getElementById('selectedCharacter');
const moveButtonsDiv = document.getElementById('moveButtons');
const statusMessageDiv = document.getElementById('statusMessage');
const newGameButton = document.getElementById('newGameButton'); // New Game Button

const websocket = new WebSocket('ws://127.0.0.1:8000/ws/game');

let selectedCharacter = null;
let currentGrid = []; // To store the current grid state

websocket.onopen = function () {
    console.log('WebSocket connection established.');
    websocket.send(JSON.stringify({
        action: 'initialize',
        player_a: ['P1', 'P2', 'H1', 'H2', 'P3'],
        player_b: ['P1', 'P2', 'H1', 'H2', 'P3']
    }));
};

websocket.onmessage = function (event) {
    try {
        const message = JSON.parse(event.data);
        console.log('Message received:', message);

        if (message.grid) {
            currentGrid = message.grid; // Update the stored grid
            updateGameBoard(currentGrid);
            updateCurrentTurn(message.turn);
        } else if (message.message) {
            statusMessageDiv.textContent = message.message;
        }
    } catch (e) {
        console.error('Failed to parse message as JSON:', event.data);
    }
};

websocket.onerror = function (error) {
    console.error('WebSocket error:', error);
};

websocket.onclose = function () {
    console.log('WebSocket connection closed.');
};

function updateGameBoard(grid) {
    gameBoard.innerHTML = '';
    for (let row of grid) {
        let rowDiv = document.createElement('div');
        rowDiv.className = 'row';
        for (let cell of row) {
            let cellDiv = document.createElement('div');
            cellDiv.className = 'cell';
            cellDiv.textContent = cell;
            cellDiv.dataset.cell = cell; // Store cell content for reference
            cellDiv.onclick = () => selectCharacter(cell);
            if (selectedCharacter && cell === selectedCharacter) {
                cellDiv.classList.add('selected'); // Add the selected class
            } else {
                cellDiv.classList.remove('selected'); // Remove the selected class
            }
            rowDiv.appendChild(cellDiv);
        }
        gameBoard.appendChild(rowDiv);
    }
}

function selectCharacter(cell) {
    if (cell && cell.startsWith(websocket.current_turn)) {
        selectedCharacter = cell;
        selectedCharacterDiv.textContent = `Selected Character: ${cell}`;
        showMoveOptions(cell);
        updateGameBoard(currentGrid); // Refresh the board to highlight the selected character
    }
}

function showMoveOptions(character) {
    moveButtonsDiv.innerHTML = ''; // Clear previous buttons
    const moves = character.includes('H2') ? ['FL', 'FR', 'BL', 'BR'] : ['L', 'R', 'F', 'B'];

    moves.forEach(move => {
        const button = document.createElement('button');
        button.textContent = move;
        button.onclick = () => makeMove(character, move);
        moveButtonsDiv.appendChild(button);
    });
}

function makeMove(character, move) {
    if (character && move) {
        websocket.send(JSON.stringify({
            action: 'move',
            player: websocket.current_turn,
            character: character.split('-')[1],
            direction: move
        }));
    }
}

function updateCurrentTurn(turn) {
    websocket.current_turn = turn;
    statusDiv.textContent = `Current Turn: Player ${turn}`;
}

// New Game Button Click Handler
newGameButton.onclick = function () {
    websocket.send(JSON.stringify({ action: 'reset_game' }));
}
