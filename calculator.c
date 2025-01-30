#include <stdio.h>

float soma(float a, float b);
float subtracao(float a, float b);
float multiplicacao(float a, float b);
float divisao(float a, float b);
float potenciacao(float base, int expoente);
float raiz_quadrada(float numero);
long long fatorial(int numero);
int mdc(int a, int b);
int calcular_mdc(int numeros[], int quantidade);
int mmc(int a, int b);
int calcular_mmc(int numeros[], int quantidade);
void equacao_segundo_grau(float a, float b, float c);

int main() {
    int opcao;
    do {
        printf("Escolha a operacao:\n");
        printf("0. Sair\n");
        printf("1. Soma\n");
        printf("2. Subtracao\n");
        printf("3. Multiplicacao\n");
        printf("4. Divisao\n");
        printf("5. Potenciacao\n");
        printf("6. Raiz Quadrada\n");
        printf("7. Fatorial\n");
        printf("8. MDC\n");
        printf("9. MMC\n");
        printf("10. Equacao de Segundo Grau\n");
        printf("Digite a sua escolha: ");
        scanf("%d", &opcao);

        float num1, num2, resultado;
        int expoente, numero;
        int numeros[5];

        switch (opcao) {
            case 1:
                printf("Digite o primeiro numero: ");
                scanf("%f", &num1);
                printf("Digite o segundo numero: ");
                scanf("%f", &num2);
                resultado = soma(num1, num2);
                printf("Resultado: %.5f\n", resultado);
                break;
            case 2:
                printf("Digite o primeiro numero: ");
                scanf("%f", &num1);
                printf("Digite o segundo numero: ");
                scanf("%f", &num2);
                resultado = subtracao(num1, num2);
                printf("Resultado: %.5f\n", resultado);
                break;
            case 3:
                printf("Digite o primeiro numero: ");
                scanf("%f", &num1);
                printf("Digite o segundo numero: ");
                scanf("%f", &num2);
                resultado = multiplicacao(num1, num2);
                printf("Resultado: %.5f\n", resultado);
                break;
            case 4:
                printf("Digite o primeiro numero: ");
                scanf("%f", &num1);
                printf("Digite o segundo numero: ");
                scanf("%f", &num2);
                if (num2 != 0) {
                    resultado = divisao(num1, num2);
                    printf("Resultado: %.5f\n", resultado);
                } else {
                    printf("Erro: Divisao por zero nao permitida.\n");
                }
                break;
            case 5:
                printf("Digite a base: ");
                scanf("%f", &num1);
                printf("Digite o expoente: ");
                scanf("%d", &expoente);
                resultado = potenciacao(num1, expoente);
                printf("Resultado: %.5f\n", resultado);
                break;
            case 6:
                printf("Digite o numero: ");
                scanf("%f", &num1);
                if (num1 >= 0) {
                    resultado = raiz_quadrada(num1);
                    printf("Resultado: %.5f\n", resultado);
                } else {
                    printf("Erro: Raiz quadrada de numero negativo nao permitida.\n");
                }
                break;
            case 7:
                printf("Digite o numero: ");
                scanf("%d", &numero);
                if (numero >= 0) {
                    long long fat = fatorial(numero);
                    printf("Resultado: %lld\n", fat);
                } else {
                    printf("Erro: Fatorial de numero negativo nao permitido.\n");
                }
                break;
            case 8:
                for (int i = 0; i < 5; i++) {
                    printf("Digite o numero %d: ", i + 1);
                    scanf("%d", &numeros[i]);
                }
                int mdc_resultado = calcular_mdc(numeros, 5);
                printf("Resultado: %d\n", mdc_resultado);
                break;
            case 9:
                for (int i = 0; i < 5; i++) {
                    printf("Digite o numero %d: ", i + 1);
                    scanf("%d", &numeros[i]);
                }
                int mmc_resultado = calcular_mmc(numeros, 5);
                printf("Resultado: %d\n", mmc_resultado);
                break;
            case 10:
                printf("Digite o valor de a: ");
                scanf("%f", &num1);
                printf("Digite o valor de b: ");
                scanf("%f", &num2);
                printf("Digite o valor de c: ");
                float num3;
                scanf("%f", &num3);
                equacao_segundo_grau(num1, num2, num3);
                break;
            case 0:
                printf("Encerrando o programa.\n");
                break;
            default:
                printf("Opcao invalida!\n");
        }
    } while (opcao != 0);

    return 0;
}
