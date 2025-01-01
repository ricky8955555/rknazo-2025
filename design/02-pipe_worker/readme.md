# pipe_worker

## 题解

执行 `challenge` 之后可看到提示: “把标准错误扔掉, 然后把标准输出丢给文件”。

按照提示做可直接获得 flag。

```log
/rknazo/chal/02-pipe_worker # ./challenge 1> flag 2> /dev/null

/rknazo/chal/02-pipe_worker # cat flag
flag{f83f58d9-f45f-00b6-fa02-8e5722dbdca9}
```
