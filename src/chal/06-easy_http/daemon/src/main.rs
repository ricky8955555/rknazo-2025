use anyhow::Result;
use daemon::{FLAG, KEY};
use http_body_util::combinators::BoxBody;
use http_body_util::{BodyExt, Empty, Full};
use hyper::body::{Bytes, Incoming};
use hyper::service::service_fn;
use hyper::{Method, Request, Response, StatusCode};
use hyper_util::rt::TokioIo;
use log::{debug, info, warn};
use rand::prelude::*;
use std::net::{Ipv4Addr, SocketAddr, SocketAddrV4};
use std::time::Duration;
use tokio::net::{TcpListener, TcpStream};
use tokio::task::JoinHandle;
use tokio::time::timeout;

const PROXY: &str = "127.79.0.1:80";
const NOTIFIER: &str = "127.79.0.68:80";

const PROXY_ID: &str = "proxy@rknazo";

fn empty() -> BoxBody<Bytes, hyper::Error> {
    Empty::<Bytes>::new()
        .map_err(|never| match never {})
        .boxed()
}

fn full<T: Into<Bytes>>(chunk: T) -> BoxBody<Bytes, hyper::Error> {
    Full::new(chunk.into())
        .map_err(|never| match never {})
        .boxed()
}

async fn real_service(req: Request<Incoming>) -> Result<Response<BoxBody<Bytes, hyper::Error>>> {
    let path = req
        .uri()
        .path_and_query()
        .map(|x| x.as_str())
        .unwrap_or("/");

    if path == "/" {
        info!(target: "real_server", "Root path accessed. 访问了根目录.");
        let resp = Response::new(full("You can access the flag via '/flag'.\n你可以通过访问 '/flag' 获得 flag."));
        return Ok(resp);
    }

    if path != "/flag" {
        info!(target: "real_server", "Non-existent resource accessed. 访问到了不存在的资源.");
        let mut resp = Response::new(empty());
        *resp.status_mut() = StatusCode::NOT_FOUND;
        return Ok(resp);
    }

    if let Some(id) = req.headers().get(hyper::header::FROM) {
        if id == PROXY_ID {
            info!(target: "real_server", "Proxy ID detected in headers. 在 Header 检测到了 Proxy ID.");
            let mut resp = Response::new(full("Proxy detected.\n检测到了代理."));
            *resp.status_mut() = StatusCode::FORBIDDEN;
            return Ok(resp);
        }
    }

    if req.method() != Method::GET {
        info!(target: "real_server", "Invalid HTTP method. 无效的 HTTP 方法.");
        let mut resp = Response::new(empty());
        *resp.status_mut() = StatusCode::METHOD_NOT_ALLOWED;
        return Ok(resp);
    }

    info!(target: "real_server", "Passed the challenge, sending flag to user... 通过了 challenge, 正在发送 flag 给用户.");
    let resp = Response::new(full(FLAG.to_string()));
    Ok(resp)
}

async fn run_real_server(addr: SocketAddrV4) -> Result<()> {
    info!(target: "real_server", "Real server will run on {addr} and expires after 10 secs or any data received. Real server 将会运行在 {addr} 并在 10 秒后或者收到数据后被销毁.");
    let listener = TcpListener::bind(addr).await?;

    debug!(target: "real_server", "Waiting for data. 正在等待数据.");
    // open for 10 secs only
    let (stream, client) = match timeout(Duration::from_secs(10), listener.accept()).await {
        Ok(data) => data?,
        Err(_) => {
            debug!(target: "real_server", "Socket on {addr} is dropping due to timeout reached. 在 {addr} 上的 Socket 由于超时被销毁.");
            return Ok(());
        }
    };

    debug!(target: "real_server", "Received data from {client} and going to handle it. 准备处理来自 {client} 的数据.");
    let io = TokioIo::new(stream);
    let service = service_fn(real_service);
    hyper::server::conn::http1::Builder::new()
        .serve_connection(io, service)
        .await?;

    info!(target: "real_server", "Socket on {addr} is dropping. 正在销毁在 {addr} 上的 Socket");
    Ok(())
}

fn create_real_server() -> SocketAddrV4 {
    // 127.79.1.0 - 127.79.255.255
    let mut rng = rand::thread_rng();
    let ip = Ipv4Addr::new(127, 79, rng.gen_range(1..=255), rng.gen());
    let port: u16 = rng.gen_range(1..=65535);
    let addr = SocketAddrV4::new(ip, port);

    tokio::spawn(async move {
        let result = run_real_server(addr).await;
        if let Err(e) = result {
            warn!(target: "real_server", "Error occured when running real server (在运行 Real server 时发生了错误): {e}");
        }
    });

    addr
}

async fn notifier_service(
    req: Request<Incoming>,
) -> Result<Response<BoxBody<Bytes, hyper::Error>>> {
    let path = req
        .uri()
        .path_and_query()
        .map(|x| x.as_str())
        .unwrap_or("/");

    debug!(target: "notifier", "Authenticating... 正在认证...");

    match req.headers().get(hyper::header::AUTHORIZATION) {
        Some(key) => {
            if key.to_str()? != *KEY {
                info!(target: "notifier", "Wrong key got. 获取到了错误的 Key.");
                let mut resp = Response::new(full("Wrong key. 密钥错误."));
                *resp.status_mut() = StatusCode::FORBIDDEN;
                return Ok(resp);
            }
        }
        None => {
            info!(target: "notifier", "Session was unauthorized. 会话未认证.");
            let mut resp = Response::new(full("Authorization needed. 需要认证."));
            *resp.status_mut() = StatusCode::UNAUTHORIZED;
            return Ok(resp);
        }
    };

    info!(target: "notifier", "Authentication passed. 通过认证.");

    if path != "/create" {
        info!(target: "notifier", "Non-existent resource accessed. 访问到了不存在的资源.");
        let mut resp = Response::new(empty());
        *resp.status_mut() = StatusCode::NOT_FOUND;
        return Ok(resp);
    }

    if req.method() != Method::GET {
        info!(target: "notifier", "Invalid HTTP method. 无效的 HTTP 方法.");
        let mut resp = Response::new(empty());
        *resp.status_mut() = StatusCode::METHOD_NOT_ALLOWED;
        return Ok(resp);
    }

    let addr = create_real_server();
    let resp = Response::new(full(addr.to_string()));

    info!(target: "notifier", "Created address {addr} and sending to user. 创建了地址 {addr} 并正在发送给用户.");
    Ok(resp)
}

async fn run_notifier() -> Result<()> {
    info!(target: "notifier", "Bind TCP socket on {NOTIFIER}. TCP Socket 监听在 {NOTIFIER} 上.");
    let listener = TcpListener::bind(NOTIFIER).await?;

    loop {
        debug!(target: "notifier", "Waiting for data. 正在等待数据.");
        let (stream, addr) = listener.accept().await?;

        info!(target: "notifier", "Received data from {addr} and going to handle it. 准备处理来自 {addr} 的数据.");
        let io = TokioIo::new(stream);
        let service = service_fn(notifier_service);

        let result = hyper::server::conn::http1::Builder::new()
            .serve_connection(io, service)
            .await;

        if let Err(e) = result {
            warn!(target: "notifier", "Error occured when handling notifier incoming (在处理 notifier 的请求时发生了错误): {e}");
        }
    }
}

async fn proxy_service(req: Request<Incoming>) -> Result<Response<Incoming>> {
    let stream = TcpStream::connect(NOTIFIER).await?;
    let io = TokioIo::new(stream);

    debug!(target: "proxy", "Trying to create real server via notifier... 尝试通过 notifier 创建 Real server 实例...");

    let (mut sender, conn) = hyper::client::conn::http1::handshake(io).await?;

    tokio::spawn(async move {
        if let Err(err) = conn.await {
            warn!(target: "proxy", "Connection to notifier failed (连接至 notifier 失败): {err}");
        }
    });

    let notifier_req = Request::builder()
        .uri("/create")
        .header(hyper::header::HOST, NOTIFIER.to_string())
        .header(hyper::header::AUTHORIZATION, KEY.to_string())
        .body(empty())?;

    let res = sender.send_request(notifier_req).await?;
    let addr: SocketAddr = String::from_utf8_lossy(&res.collect().await?.to_bytes()).parse()?;

    debug!(target: "proxy", "Got real server address {addr}. 获得 Real server 地址 {addr}.");

    debug!(target: "proxy", "Transferring request to real server... 正在传输请求至 Real server.");

    let stream = TcpStream::connect(addr).await?;
    let io = TokioIo::new(stream);

    let (mut sender, conn) = hyper::client::conn::http1::handshake(io).await?;

    tokio::spawn(async move {
        if let Err(err) = conn.await {
            warn!(target: "proxy", "Connection to real server failed (连接至 real server 失败): {err}");
        }
    });

    let mut req = req;
    let headers = req.headers_mut();

    headers.insert(hyper::header::HOST, addr.to_string().parse()?);
    headers.insert(hyper::header::FROM, PROXY_ID.parse()?);

    let res = sender.send_request(req).await?;
    info!(target: "proxy", "Got data from real server and redirecting to user (从 Real server 中获得数据并重定向给用户):\n{res:?}");

    Ok(res)
}

async fn run_proxy() -> Result<()> {
    info!(target: "proxy", "Bind TCP socket on {PROXY}. TCP Socket 监听在 {PROXY} 上.");

    let listener = TcpListener::bind(PROXY).await?;

    loop {
        debug!(target: "proxy", "Waiting for data. 正在等待数据.");
        let (stream, addr) = listener.accept().await?;

        info!(target: "proxy", "Received data from {addr} and going to handle it. 准备处理来自 {addr} 的数据.");
        let io = TokioIo::new(stream);
        let service = service_fn(proxy_service);

        let result = hyper::server::conn::http1::Builder::new()
            .serve_connection(io, service)
            .await;

        if let Err(e) = result {
            warn!(target: "proxy", "Error occured when handling proxy incoming (在处理 proxy 的请求时发生了错误): {e}");
        }
    }
}

async fn flatten<T>(handle: JoinHandle<Result<T>>) -> Result<T> {
    match handle.await {
        Ok(Ok(result)) => Ok(result),
        Ok(Err(err)) => Err(err),
        Err(err) => Err(err.into()),
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    simple_logger::init_with_level(log::Level::Debug)?;

    _ = tokio::try_join!(
        flatten(tokio::spawn(run_proxy())),
        flatten(tokio::spawn(run_notifier())),
    )?;

    Ok(())
}
