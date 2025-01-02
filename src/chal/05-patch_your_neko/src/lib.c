#define _GNU_SOURCE

#include <dlfcn.h>
#include <fcntl.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

#include "data.h"

#define DIE(msg)            \
    {                       \
        perror(msg);        \
        exit(EXIT_FAILURE); \
    }

int create_flag_memfd() {
    int fd, ret;
    void* shm;
    char flag[FLAG_LENGTH];

    fd = memfd_create("flag", 0);
    if (fd == -1) DIE("memfd_create");

    ret = ftruncate(fd, FLAG_LENGTH);
    if (ret == -1) DIE("ftruncate");

    shm = mmap(NULL, FLAG_LENGTH, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (shm == MAP_FAILED) DIE("mmap");

    getflag(flag);
    sprintf(shm, "%s", flag);

    return fd;
}

int open(const char* pathname, int flags, ...) {
    static int (*real_open)(const char*, int, ...) = NULL;
    if (real_open == NULL) {
        real_open = dlsym(RTLD_NEXT, "open");
    }

    if (strcmp(pathname, "flag") == 0) {
        return create_flag_memfd();
    } else {
        return real_open(pathname, flags);
    }
}
