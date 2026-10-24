/* session-01_largest.c - algorithm "find the largest of three numbers" turned into C */
#include <stdio.h>

int main(void)
{
    int a = 17, b = 42, c = 29;
    int largest = a;              /* step 1: assume the first is largest */

    if (b > largest) largest = b; /* step 2: compare with b */
    if (c > largest) largest = c; /* step 3: compare with c */

    printf("Numbers: %d, %d, %d\n", a, b, c);
    printf("Largest: %d\n", largest);
    return 0;
}
