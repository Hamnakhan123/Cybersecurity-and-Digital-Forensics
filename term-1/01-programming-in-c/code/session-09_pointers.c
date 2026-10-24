/* session-09_pointers.c - addresses, dereferencing, pointer arithmetic, arrays */
#include <stdio.h>

void swap(int *a, int *b) { int t = *a; *a = *b; *b = t; }

int main(void)
{
    int port = 22;
    int *p = &port;                         /* p holds the address of port */
    printf("port = %d, *p = %d\n", port, *p);
    *p = 2222;                              /* change port through the pointer */
    printf("after *p = 2222 -> port = %d\n", port);
    printf("p == &port ? %s\n", (p == &port) ? "yes" : "no");

    int arr[5] = {10, 20, 30, 40, 50};
    int *q = arr;                           /* array name decays to &arr[0] */
    printf("q[2] = %d, *(q + 2) = %d\n", q[2], *(q + 2));
    printf("bytes between &arr[3] and &arr[0] = %ld\n",
           (long)((char *)&arr[3] - (char *)&arr[0]));
    printf("elements between them = %ld\n", (long)(&arr[3] - &arr[0]));

    int a = 1, b = 2;
    swap(&a, &b);
    printf("after swap: a = %d, b = %d\n", a, b);

    int grid[2][3] = {{1, 2, 3}, {4, 5, 6}};
    printf("grid[1][2] = %d, *(*(grid + 1) + 2) = %d\n", grid[1][2], *(*(grid + 1) + 2));
    return 0;
}
