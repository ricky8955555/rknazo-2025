#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "data.h"

#define RANDSEED 0x1919810
#define THRESHOLD 114514
#define SENTENCE_COUNT 8

static const char* sentences[SENTENCE_COUNT] = {
    "Are you really want to get the flag? 你真的这么想要吗?",
    "Are you ready? 你准备好了吗?",
    "I can't hear your voice~ Please repeat it! 听!不!见!再说一遍!!!",
    "Just keep say yes to me! 就这样!继续保持!",
    "Keep doing it and there will be a miracle! 加油!相信会有奇迹发生的!",
    "Come on! Keep saying yes! 加油!!!",
    "I want to see your determination! 我要看到你的决心!",
    "I believe you can do it! 我相信你可以的!"};

bool iseol(int c) { return c == '\n' || c == '\0' || c == EOF; }

int main() {
    size_t idx;
    char flag[FLAG_LENGTH];
    int* arr;
    int randval;
    int buf;

    srand(RANDSEED);
    randval = rand();

    do {  // count: 1524980
        idx = (size_t)randval % SENTENCE_COUNT;
        printf("%s (y/N)\n", sentences[idx]);
        buf = fgetc(stdin);
        if ((buf == 'Y' || buf == 'y') && iseol(buf = fgetc(stdin))) {
            randval = rand();
        } else {
            puts(
                "Don't say no or any other words to me~ If you keep doing "
                "this, it will be an infinite loop~");
            puts("认真点哦, 如果给我输入其他东西是没用的哦~");
        }

        while (!iseol(buf)) buf = fgetc(stdin);
        if (buf == EOF) clearerr(stdin);  // clear EOF
    } while (randval < (RAND_MAX - THRESHOLD));

    getflag(flag);
    printf("%s\n", flag);

    return 0;
}
