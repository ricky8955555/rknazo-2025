# patch_your_neko

## 题解

### 预期题解

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

### 非预期题解

在编译的时候忘记给 `getflag` 函数去符号了（x

可以直接利用 Python 的 `ctypes` 库直接调用 `getflag(char*)` 函数获得 flag。

```log
/rknazo/chal/05-patch_your_neko # python3
Python 3.12.8 (main, Dec  9 2024, 20:38:54) [GCC 14.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from ctypes import CDLL, c_char
>>> lib = CDLL("./lib.so")
>>> flag = (c_char * 64)()
>>> lib.getflag(flag)
-102940927
>>> flag.value
b'flag{e0525645-2b36-00ef-fa05-6adedcdc9cd2}'
```
