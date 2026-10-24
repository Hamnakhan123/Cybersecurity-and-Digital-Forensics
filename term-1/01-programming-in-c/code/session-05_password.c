/* session-05_password.c - if / else-if ladder: rate password strength */
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    const char *samples[] = {"abc", "summer2026", "Summer2026", "S#mmer_2026!"};
    for (int s = 0; s < 4; s++) {
        const char *p = samples[s];
        int len = (int)strlen(p), upper = 0, lower = 0, digit = 0, symbol = 0;
        for (int i = 0; i < len; i++) {
            if (isupper((unsigned char)p[i]))      upper = 1;
            else if (islower((unsigned char)p[i])) lower = 1;
            else if (isdigit((unsigned char)p[i])) digit = 1;
            else                                   symbol = 1;
        }
        int score = upper + lower + digit + symbol;
        printf("%-14s len=%2d classes=%d -> ", p, len, score);
        if (len < 8)
            printf("REJECT (too short)\n");
        else if (score <= 2)
            printf("WEAK\n");
        else if (score == 3)
            printf("MEDIUM\n");
        else
            printf("STRONG\n");
    }
    return 0;
}
