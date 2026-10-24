/* session-04_bitwise.c - bitwise operators used as permission flags (like file modes) */
#include <stdio.h>

#define READ  4   /* 100 */
#define WRITE 2   /* 010 */
#define EXEC  1   /* 001 */

void show_bits(const char *label, unsigned v)
{
    printf("%-14s %u = ", label, v);
    for (int b = 2; b >= 0; b--) putchar((v >> b) & 1 ? '1' : '0');
    putchar('\n');
}

int main(void)
{
    unsigned perm = READ | WRITE;              /* set two flags        */
    show_bits("READ|WRITE", perm);
    printf("can write? %s\n", (perm & WRITE) ? "yes" : "no");
    perm &= ~WRITE;                            /* clear WRITE          */
    show_bits("clear WRITE", perm);
    perm ^= EXEC;                              /* toggle EXEC          */
    show_bits("toggle EXEC", perm);
    printf("5 << 1 = %d, 20 >> 2 = %d\n", 5 << 1, 20 >> 2);
    printf("XOR mask demo: 'A'(%d) ^ 32 = '%c'\n", 'A', 'A' ^ 32);
    return 0;
}
