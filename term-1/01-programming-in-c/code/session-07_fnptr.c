/* session-07_fnptr.c - recursion and function pointers (a tiny dispatch table) */
#include <stdio.h>

long factorial(int n) { return (n <= 1) ? 1 : n * factorial(n - 1); }

int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }
int mul(int a, int b) { return a * b; }

int main(void)
{
    printf("5! = %ld\n", factorial(5));

    int (*ops[3])(int, int) = {add, sub, mul};   /* array of function pointers */
    const char *names[3] = {"add", "sub", "mul"};
    for (int i = 0; i < 3; i++)
        printf("%s(12, 4) = %d\n", names[i], ops[i](12, 4));
    return 0;
}
