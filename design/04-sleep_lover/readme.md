# sleep_lover

## 赛时补充说明

1. 为了叫醒他，你需要 **中断** 他的睡眠。

## 结束后补充说明

这道题目设计上存在问题。

见 Manpage 中 `signal (2)`:

> The effects of signal() in a multithreaded process are unspecified.
> 在多线程进程中使用 signal() 的效果是未定义的。

另外 Manpage 中 `kill (1)`:

> it is not possible to send a signal to an explicitly selected thread in a multithreaded process.
> 无法向多线程进程中明确的一个线程发送信号。

## 题解

执行 `challenge` 之后可获得提示 “我有个懒鬼孩子, 你可以去叫醒他问问他~”，并且在执行过后程序并没有退出。

可推测提示所提到的 *孩子* 指子线程，*叫醒他* 指中断 sleep。

此时可按下 `^Z` (`Ctrl + Z`) 让主线程停止，重新获得 Shell 的使用能力。

通过 `ps -T | grep challenge` 指令可获得子线程的 PID，随后可使用 `kill -INT <pid>` 对子线程发送 *SIGINT* 信号以唤醒子线程。

发送完信号后使用 `fg` 将程序切换回前台即可获得 flag。

```log
/rknazo/chal/04-sleep_lover # ./challenge 
I don't know the flag, but my child, a sleep lover, do. Let it wake up and it will tell you the flag.
flag? 那是什么? 我有个懒鬼孩子, 你去问问他~
^Z[1]+  Stopped                    ./challenge

/rknazo/chal/04-sleep_lover # ps -T | grep challenge
   50 root      0:00 ./challenge
   51 root      0:00 ./challenge
   53 root      0:00 grep challenge

/rknazo/chal/04-sleep_lover # kill -INT 51
/rknazo/chal/04-sleep_lover # kill -INT 50

/rknazo/chal/04-sleep_lover # fg
./challenge
flag{d044058c-217e-00ef-fa04-829b4d6c5055}
```
