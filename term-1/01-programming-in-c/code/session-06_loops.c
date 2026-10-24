/* session-06_loops.c - for, while, do-while, comma operator and nested loops */
#include <stdio.h>

int main(void)
{
    /* for loop with the comma operator: two counters at once */
    printf("for + comma : ");
    for (int i = 1, j = 10; i <= 5; i++, j -= 2)
        printf("(%d,%d) ", i, j);
    printf("\n");

    /* while loop: halve a number until it reaches 1 (like binary search steps) */
    int n = 1000, steps = 0;
    while (n > 1) { n /= 2; steps++; }
    printf("while       : 1000 halves to 1 in %d steps\n", steps);

    /* do-while: body runs at least once (menus, retry prompts) */
    int k = 0;
    do { printf("do-while    : runs once even though k=%d\n", k); } while (k > 0);

    /* nested loops: a small multiplication grid */
    printf("nested grid :\n");
    for (int r = 1; r <= 3; r++) {
        for (int c = 1; c <= 4; c++) printf("%4d", r * c);
        printf("\n");
    }
    return 0;
}
