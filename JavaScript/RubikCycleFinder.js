function findCycleLength(sequence) {
    function applyMoves(state, moves) {
        for (let move of moves) {
            state = rotate(state, move);
        }
        return state;
    }
    
    function rotate(state, move) {
        return state.split('').map(c => (c === move.toUpperCase() ? c.toLowerCase() : (c === move.toLowerCase() ? c.toUpperCase() : c))).join('');
    }
    
    let initialState = 'UUUUUUUUUFFFFFFFFFDDDDDDDDDRRRRRRRRRLLLLLLLLLBBBBBBBBB';
    let currentState = initialState;
    let count = 0;
    
    do {
        currentState = applyMoves(currentState, sequence);
        count++;
    } while (currentState !== initialState);
    
    return count;
}

function processInput(input) {
    return input.trim().split('\n').map(findCycleLength).join('\n');
}

// Example usage
const input = `Rr\nLLL\ndl\nRUUdBd`;
console.log(processInput(input));
