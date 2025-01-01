# my_users

## 题解

根据提示 “有个用户持有着 flag.”，可做出查看用户列表的决策。

可使用 `cat /etc/passwd` 或 `getent passwd` 指令获取用户列表。

在获取得 `passwd` 之后，可看到 `flag` 用户 `GECOS` 字段存有一段 Hex 字符串，对该字符串进行 Hex 解码即可获得 flag。

```log
/rknazo/chal/01-dont_get_lost # getent passwd
root:x:0:0:root:/root:/bin/sh
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/mail:/sbin/nologin
news:x:9:13:news:/usr/lib/news:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
ftp:x:21:21::/var/lib/ftp:/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
games:x:35:35:games:/usr/games:/sbin/nologin
ntp:x:123:123:NTP:/var/empty:/sbin/nologin
guest:x:405:100:guest:/dev/null:/sbin/nologin
nobody:x:65534:65534:nobody:/:/sbin/nologin
flag:x:1000:1000:666c61677b36626564353336662d626465322d303063322d666130302d3663313036306234343762367d:/dev/null:/sbin/nologin

/rknazo/chal/01-dont_get_lost # echo 666c61677b36626564353336662d626465322d303063322d666130302d3663313036306234343762367d | xxd -r -p
flag{6bed536f-bde2-00c2-fa00-6c1060b447b6}
```
