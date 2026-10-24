/* session-07_functions.c - prototypes, call by value vs call by reference, scope */
#include <stdio.h>

int  square(int x);                 /* prototype (declaration) */
void try_reset(int value);
void reset(int *value);
void counter(void);

int global_hits = 0;                /* global: visible to every function below */

int main(void)
{
    printf("square(7) = %d\n", square(7));

    int score = 50;
    try_reset(score);
    printf("after try_reset (by value)    : %d\n", score);
    reset(&score);
    printf("after reset (by reference)    : %d\n", score);

    for (int i = 0; i < 3; i++) counter();
    printf("global_hits = %d\n", global_hits);
    return 0;
}

int square(int x) { return x * x; }          /* definition */

void try_reset(int value) { value = 0; }     /* changes only its own copy */

void reset(int *value) { *value = 0; }       /* changes the caller's variable */

void counter(void)
{
    static int calls = 0;   /* static local: keeps its value between calls */
    int temp = 0;           /* auto local: recreated each call */
    calls++; temp++; global_hits++;
    printf("counter(): calls=%d temp=%d\n", calls, temp);
}
