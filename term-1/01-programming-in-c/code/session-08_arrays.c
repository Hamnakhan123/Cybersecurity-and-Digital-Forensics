/* session-08_arrays.c - 1-D array statistics: failed logins per hour */
#include <stdio.h>

#define HOURS 8

int main(void)
{
    int failed[HOURS] = {2, 0, 1, 14, 3, 0, 27, 1};   /* initialiser list */
    int total = 0, max_i = 0;

    for (int i = 0; i < HOURS; i++) {
        total += failed[i];
        if (failed[i] > failed[max_i]) max_i = i;
    }
    double avg = (double)total / HOURS;
    printf("Total failures : %d\n", total);
    printf("Average/hour   : %.2f\n", avg);
    printf("Peak           : hour %d with %d failures\n", max_i, failed[max_i]);
    printf("Alerts (> 3x average):");
    for (int i = 0; i < HOURS; i++)
        if (failed[i] > 3 * avg) printf(" hour%d", i);
    printf("\nsizeof(failed) = %zu bytes, elements = %zu\n",
           sizeof failed, sizeof failed / sizeof failed[0]);
    return 0;
}
