# patch_your_neko

## 题解

根据提示:

> 试试加载 'lib.so' 并运行你的猫 (cat), 然后你告诉它你想要什么, 它会给你说出来的~

此处 *加载 'lib.so'* 指通过 `LD_PRELOAD` 环境变量使 `cat` 在执行时预加载 `lib.so`。

而 *告诉它你想要什么* 即所需要查看内容的 “文件名”。

可推断出 `lib.so` 对文件操作行为进行了篡改，并可使原本不存在的 `flag` 文件的打开行为合法化。

设置环境变量后 `cat flag` 即可获得 flag。

```log
/rknazo/chal/05-patch_your_neko # LD_PRELOAD=./lib.so cat flag
flag{e0525645-2b36-00ef-fa05-6adedcdc9cd2}
```
