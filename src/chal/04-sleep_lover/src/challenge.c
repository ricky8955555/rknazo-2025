#define _GNU_SOURCE

#include <pthread.h>
#include <signal.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "data.h"

#define DIE(msg)            \
    {                       \
        perror(msg);        \
        exit(EXIT_FAILURE); \
    }

#ifdef __GLIBC__
typedef __sighandler_t sighandler_t;
#endif

void* child(void* arg) {
    char flag[FLAG_LENGTH];

    // wait for signal
    pause();

    getflag(flag);
    printf("%s\n", flag);

    return NULL;
}

void ignore_signal_handler(int signum) {}

int main() {
    int ret;
    sighandler_t sighandler;
    pthread_t th;

    ret = pthread_create(&th, NULL, child, NULL);
    if (ret != 0) DIE("pthread_create");

    sighandler = signal(SIGINT, ignore_signal_handler);
    if (sighandler == SIG_ERR) DIE("signal");

    puts(
        "I don't know the flag, but my child, a sleep lover, do. Let it "
        "wake up and it will tell you the flag.");
    puts("flag? 那是什么? 我有个懒鬼孩子, 你可以去叫醒他问问他~");

    ret = pthread_join(th, NULL);
    if (ret != 0) DIE("pthread_join");

    return 0;
}
