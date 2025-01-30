function fibonacciWithCalls(n, calls) {
    if (n === 0) return { result: 0, calls: calls };
    if (n === 1) return { result: 1, calls: calls };
    
    let left = fibonacciWithCalls(n - 1, calls + 1);
    let right = fibonacciWithCalls(n - 2, left.calls + 1);
    
    return { result: left.result + right.result, calls: right.calls };
}

function processTestCases(testCases) {
    for (let x of testCases) {
        let { result, calls } = fibonacciWithCalls(x, 0);
        console.log(`fib(${x}) = ${calls} calls = ${result}`);
    }
}

// Exemplo de entrada
const testCases = [5, 4];
processTestCases(testCases);
