function solveLightUpPuzzle(input) {
    const lines = input.trim().split('\n');
    let index = 0;
    let result = [];
    
    while (index < lines.length) {
        let [N, M] = lines[index].split(' ').map(Number);
        if (N === 0 && M === 0) break;
        index++;

        let B = parseInt(lines[index]);
        index++;
        
        let board = Array.from({ length: N }, () => Array(M).fill('.'));
        let barriers = [];

        for (let i = 0; i < B; i++, index++) {
            let [R, C, K] = lines[index].split(' ').map(Number);
            board[R - 1][C - 1] = K;
            barriers.push([R - 1, C - 1, K]);
        }

        let minLamps = findMinimumLamps(board, barriers, N, M);
        result.push(minLamps !== Infinity ? minLamps : 'No solution');
    }
    
    return result.join('\n');
}

function findMinimumLamps(board, barriers, N, M) {
    let minLamps = Infinity;
    
    function isValid(x, y) {
        return x >= 0 && x < N && y >= 0 && y < M;
    }
    
    function checkSolution(lamps) {
        let lit = board.map(row => row.slice());
        let lampCount = lamps.length;
        
        for (let [x, y] of lamps) {
            if (lit[x][y] !== '.') return false;
            lit[x][y] = 'L';
            
            let directions = [[-1, 0], [1, 0], [0, -1], [0, 1]];
            for (let [dx, dy] of directions) {
                let nx = x + dx, ny = y + dy;
                while (isValid(nx, ny) && typeof lit[nx][ny] !== 'number') {
                    if (lit[nx][ny] === 'L') return false;
                    lit[nx][ny] = '*';
                    nx += dx;
                    ny += dy;
                }
            }
        }

        for (let [x, y, k] of barriers) {
            if (k === -1) continue;
            let count = 0;
            for (let [dx, dy] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) {
                let nx = x + dx, ny = y + dy;
                if (isValid(nx, ny) && lit[nx][ny] === 'L') count++;
            }
            if (count !== k) return false;
        }
        
        for (let row of lit) {
            if (row.includes('.')) return false;
        }
        
        minLamps = Math.min(minLamps, lampCount);
        return true;
    }
    
    function backtrack(lamps, x, y) {
        if (x === N) {
            checkSolution(lamps);
            return;
        }
        let nextX = y + 1 === M ? x + 1 : x;
        let nextY = (y + 1) % M;
        
        if (board[x][y] === '.') {
            lamps.push([x, y]);
            backtrack(lamps, nextX, nextY);
            lamps.pop();
        }
        backtrack(lamps, nextX, nextY);
    }
    
    backtrack([], 0, 0);
    return minLamps;
}

// Example usage
const input = `2 2\n0\n2 2\n1\n2 2 1\n6 7\n7\n2 3 -1\n3 3 0\n4 2 1\n5 4 3\n5 6 2\n1 7 -1\n6 5 -1\n0 0`;
console.log(solveLightUpPuzzle(input));
