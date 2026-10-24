/* session-02_arith.c - arithmetic operators and the integer-division trap */
#include <stdio.h>

int main(void)
{
    int total_seconds = 3725;
    int hours   = total_seconds / 3600;          /* integer division */
    int minutes = (total_seconds % 3600) / 60;   /* % gives the remainder */
    int seconds = total_seconds % 60;

    printf("%d seconds = %dh %dm %ds\n", total_seconds, hours, minutes, seconds);
    printf("7 / 2   = %d   (int / int drops the fraction)\n", 7 / 2);
    printf("7.0 / 2 = %.1f (one double operand keeps it)\n", 7.0 / 2);
    printf("-7 %% 3  = %d\n", -7 % 3);
    return 0;
}
