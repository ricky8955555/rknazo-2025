# dont_get_lost

## 题解

根据提示 “'flag' 符号链接最终指向的文件名是正确的且可用于解密出最终结果” 中的 “最终” 一词可推断出 `flag` 文件的链接为多层链接。

可以使用 `realpath <symlink>` 或 `readlink -f <symlink>` 追踪到最终指向的文件。

```log
/rknazo/chal/01-dont_get_lost # readlink -f flag
/rknazo/chal/01-dont_get_lost/chaos/666c61677b33316265656562642d353636662d303061632d666130312d3233633434646438323564657d

/rknazo/chal/01-dont_get_lost # realpath flag
/rknazo/chal/01-dont_get_lost/chaos/666c61677b33316265656562642d353636662d303061632d666130312d3233633434646438323564657d

/rknazo/chal/01-dont_get_lost # echo 666c61677b33316265656562642d353636662d303061632d666130312d3233633434646438323564657d | xxd -r -p
flag{31beeebd-566f-00ac-fa01-23c44dd825de}
```
