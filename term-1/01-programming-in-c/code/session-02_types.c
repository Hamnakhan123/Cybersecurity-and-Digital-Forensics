/* session-02_types.c - variables, constants and the size of each data type */
#include <stdio.h>
#define MAX_LOGIN_ATTEMPTS 3      /* symbolic constant (preprocessor) */

int main(void)
{
    const float PI = 3.14159f;    /* typed constant: cannot be changed */
    int    attempts = 0;
    char   grade    = 'A';
    float  cgpa     = 3.67f;
    double balance  = 125000.75;

    printf("Type      Size(bytes)  Example\n");
    printf("char      %zu            %c\n", sizeof(char), grade);
    printf("int       %zu            %d\n", sizeof(int), attempts);
    printf("float     %zu            %.2f\n", sizeof(float), cgpa);
    printf("double    %zu            %.2f\n", sizeof(double), balance);
    printf("PI = %.5f, max attempts = %d\n", PI, MAX_LOGIN_ATTEMPTS);
    return 0;
}
