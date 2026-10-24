/* session-09_malloc.c - dynamic memory: malloc, check, use, free, NULL */
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int n = 5;
    int *ids = malloc(n * sizeof *ids);       /* request memory from the heap */
    if (ids == NULL) {                        /* always check */
        fprintf(stderr, "out of memory\n");
        return 1;
    }
    for (int i = 0; i < n; i++) ids[i] = 1000 + i;

    int *bigger = realloc(ids, 2 * n * sizeof *ids);   /* grow the block */
    if (bigger == NULL) { free(ids); return 1; }
    ids = bigger;
    for (int i = n; i < 2 * n; i++) ids[i] = 1000 + i;

    printf("IDs:");
    for (int i = 0; i < 2 * n; i++) printf(" %d", ids[i]);
    printf("\n");

    free(ids);          /* give the memory back */
    ids = NULL;         /* avoid a dangling pointer (use-after-free) */
    printf("memory released, ids is now %s\n", ids == NULL ? "NULL" : "dangling");
    return 0;
}
