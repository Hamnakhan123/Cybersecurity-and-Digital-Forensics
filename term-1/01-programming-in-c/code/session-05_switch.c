/* session-05_switch.c - switch: map a port number to a service, nested if for risk */
#include <stdio.h>

void describe(int port)
{
    printf("Port %-5d : ", port);
    switch (port) {
        case 21:  printf("FTP");    break;
        case 22:  printf("SSH");    break;
        case 23:  printf("Telnet"); break;
        case 80:  printf("HTTP");   break;
        case 443: printf("HTTPS");  break;
        case 3389:printf("RDP");    break;
        default:  printf("unknown");
    }
    /* nested if: classify risk only for well-known ports */
    if (port < 1024) {
        if (port == 21 || port == 23)
            printf("  [plaintext - avoid]\n");
        else
            printf("  [well-known]\n");
    } else {
        printf("  [registered/dynamic]\n");
    }
}

int main(void)
{
    int ports[] = {22, 23, 443, 3389, 8080};
    for (int i = 0; i < 5; i++) describe(ports[i]);
    return 0;
}
