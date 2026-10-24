/* session-03_io.c - formatted input with scanf() and output with printf() */
#include <stdio.h>

int main(void)
{
    char name[30];
    int  age;
    float marks;

    printf("Enter name, age and marks: ");
    if (scanf("%29s %d %f", name, &age, &marks) != 3) {   /* always check! */
        printf("Invalid input\n");
        return 1;
    }
    printf("\n|%-10s|%5d|%8.2f|\n", name, age, marks);
    printf("|%10s|%-5d|%-8.1f|\n", name, age, marks);
    return 0;
}
