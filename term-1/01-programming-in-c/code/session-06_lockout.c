/* session-06_lockout.c - login attempts with break/continue and exit() */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(void)
{
    const char *correct = "Lab#2026";
    const char *typed[] = {"", "lab#2026", "Lab#2026"};  /* simulated user input */
    const int MAX = 3;

    for (int attempt = 1; attempt <= MAX; attempt++) {
        const char *pw = typed[attempt - 1];
        if (strlen(pw) == 0) {
            printf("Attempt %d: empty input ignored\n", attempt);
            continue;                       /* skip the rest of this iteration */
        }
        if (strcmp(pw, correct) == 0) {
            printf("Attempt %d: access granted\n", attempt);
            break;                          /* leave the loop immediately */
        }
        printf("Attempt %d: wrong password\n", attempt);
        if (attempt == MAX) {
            printf("Account locked\n");
            exit(1);                        /* end the whole program */
        }
    }
    printf("Welcome to the lab portal.\n");
    return 0;
}
