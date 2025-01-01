#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "data.h"

#define DIE(msg)            \
    {                       \
        perror(msg);        \
        exit(EXIT_FAILURE); \
    }

int main() {
    int ret;
    char out[64], err[64];
    char flag[FLAG_LENGTH];

    ret = readlink("/proc/self/fd/1", out, sizeof(out));
    if (ret == -1) DIE("readlink");
    out[ret] = '\0';

    ret = readlink("/proc/self/fd/2", err, sizeof(err));
    if (ret == -1) DIE("readlink");
    err[ret] = '\0';

    if (strstr(out, "/dev/pts/") != 0 || strcmp(err, "/dev/null") != 0) {
        puts(
            "Pipe stderr to the null device, and pipe stdout to a file. I will "
            "write the flag to the file via stdout.");
        puts("把标准错误扔掉, 然后把标准输出丢给文件. 我会走标准输出把 flag 给你的~");
    } else {
        getflag(flag);
        printf("%s\n", flag);
    }

    return 0;
}
