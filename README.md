# rknazo-2025

2025 年的一场跨年 CTF 夺旗赛活动！有 Docker 即可参与！

题目难度不高，会用 Linux 就基本能做。

- 奖励：支付宝拼手气口令红包 `50 CNY/50 pcs`
- 开始时间：`2024.12.31 23:00 CST`
- 结束时间：口令红包领取完毕/截止时（`2025.1.1 22:30 CST`）

## 参与方法

1. 在设备上安装 Docker
3. `docker run -it ricky8955555/rknazo-2025:latest` 运行容器
4. 进入容器后 `cat readme.txt` 阅读须知

## 目录结构

```
src
├── chal        -   题目源代码
├── environ     -   环境共享库
├── out         -   产物文件
├── scripts     -   辅助构建脚本
└── build.py    -   构建脚本
```

## 题目

### 源码

0. [my_users](src/chal/00-my_users/)
1. [dont_get_lost](src/chal/01-dont_get_lost/)
2. [pipe_worker](src/chal/02-pipe_worker/)
3. [say_millions_of_yes_to_me!](src/chal/03-say_millions_of_yes_to_me!/)
4. [sleep_lover](src/chal/04-sleep_lover/)
5. [patch_your_neko](src/chal/05-patch_your_neko/)
6. [easy_http](src/chal/06-easy_http/)

### 题目设计及题解

0. [my_users](design/00-my_users/)
1. [dont_get_lost](design/01-dont_get_lost/)
2. [pipe_worker](design/02-pipe_worker/)
3. [say_millions_of_yes_to_me!](design/03-say_millions_of_yes_to_me!/)
4. [sleep_lover](design/04-sleep_lover/)
5. [patch_your_neko](design/05-patch_your_neko/)
6. [easy_http](design/06-easy_http/)
