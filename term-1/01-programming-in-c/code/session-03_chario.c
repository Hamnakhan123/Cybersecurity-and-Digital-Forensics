/* session-03_chario.c - getchar()/putchar(): count and mask characters of a password */
#include <stdio.h>

int main(void)
{
    int ch, count = 0, digits = 0;
    printf("Type a password and press Enter: ");
    while ((ch = getchar()) != '\n' && ch != EOF) {
        count++;
        if (ch >= '0' && ch <= '9') digits++;
    }
    printf("\nMasked : ");
    for (int i = 0; i < count; i++) putchar('*');   /* never echo secrets */
    putchar('\n');
    printf("Length : %d, digits: %d\n", count, digits);
    return 0;
}
