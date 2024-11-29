#include <stdio.h>
#include <unistd.h>

int main() {
    while(1)
    {
        // "Hello Process Manager!"
        printf("Hello Process Manager!\n");

        // sleep 200ms
        usleep(200000);
    }
}
