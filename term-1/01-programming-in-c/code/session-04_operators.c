/* session-04_operators.c - relational, logical, assignment, cast and precedence */
#include <stdio.h>

int main(void)
{
    int x = 10;
    x += 5;  x *= 2;  x -= 4;  x /= 2;              /* compound assignment */
    printf("x after += *= -= /= : %d\n", x);

    int age = 20, has_id = 1;
    printf("age >= 18 && has_id : %d\n", age >= 18 && has_id);
    printf("!(age < 18)         : %d\n", !(age < 18));

    int total = 7, n = 2;
    printf("no cast  : %d\n", total / n);
    printf("with cast: %.2f\n", (float)total / n);

    printf("2 + 3 * 4   = %d\n", 2 + 3 * 4);       /* * before + */
    printf("(2 + 3) * 4 = %d\n", (2 + 3) * 4);
    int i = 5;
    printf("i++ gives %d, ", i++);
    printf("now i = %d, ", i);
    printf("++i gives %d\n", ++i);   /* one side effect per statement */
    return 0;
}
