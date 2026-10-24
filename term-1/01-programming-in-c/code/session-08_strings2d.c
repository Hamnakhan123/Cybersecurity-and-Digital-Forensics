/* session-08_strings2d.c - character arrays, string functions and a 2-D array */
#include <stdio.h>
#include <string.h>

int main(void)
{
    char user[16] = "analyst";
    char banner[32];
    snprintf(banner, sizeof banner, "Welcome, %s!", user);   /* bounded copy */
    printf("%s (length %zu, capacity %zu)\n", banner, strlen(banner), sizeof banner);

    /* 2-D array: 3 servers x 4 days of alert counts */
    int alerts[3][4] = { {1, 0, 2, 5}, {0, 0, 1, 0}, {7, 9, 4, 12} };
    const char *servers[3] = {"web01", "db01", "mail01"};
    printf("\n%-7s D1 D2 D3 D4 | total\n", "server");
    for (int r = 0; r < 3; r++) {
        int sum = 0;
        printf("%-7s", servers[r]);
        for (int c = 0; c < 4; c++) { printf("%3d", alerts[r][c]); sum += alerts[r][c]; }
        printf(" | %d\n", sum);
    }
    return 0;
}
