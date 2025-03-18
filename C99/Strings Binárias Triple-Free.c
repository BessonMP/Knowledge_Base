#include <stdio.h>
#include <string.h>

int isTripleFree(char *s, int len) {
    for (int size = 1; size * 3 <= len; size++) {
        for (int i = 0; i <= len - 3 * size; i++) {
            int triple = 1;
            for (int j = 0; j < size; j++) {
                if (s[i + j] != s[i + j + size] || s[i + j] != s[i + j + 2 * size]) {
                    triple = 0;
                    break;
                }
            }
            if (triple) return 0;
        }
    }
    return 1;
}

void generate(int pos, char *pattern, char *current, int len, int *count) {
    if (pos == len) {
        current[pos] = '\0';
        if (isTripleFree(current, len)) {
            (*count)++;
        }
        return;
    }

    if (pattern[pos] == '*') {
        current[pos] = '0';
        generate(pos + 1, pattern, current, len, count);
        current[pos] = '1';
        generate(pos + 1, pattern, current, len, count);
    } else {
        current[pos] = pattern[pos];
        generate(pos + 1, pattern, current, len, count);
    }
}

int main() {
    int caseNumber = 1;

    while (1) {
        int n;
        char pattern[31];
        scanf("%d", &n);

        if (n == 0) break;

        scanf("%s", pattern);
        int count = 0;

        char current[31];
        generate(0, pattern, current, n, &count);

        printf("Case %d: %d\n", caseNumber++, count);
    }

    return 0;
}


//Explicação do código:
//Função isTripleFree:
//Verifica se a string contém uma subsequência formada por uma repetição de uma string (SSS).
//Retorna 1 se for "triple-free", caso contrário, retorna 0.

//Função generate:
//Gera todas as combinações binárias possíveis substituindo os asteriscos *.
//Checa cada combinação para ver se é "triple-free" e incrementa o contador.

//Entrada e saída:
//O programa lê o tamanho N e o padrão P.
//Para cada padrão, calcula o número de strings binárias que são "triple-free" e exibe o resultado.
