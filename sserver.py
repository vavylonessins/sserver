"""..."""
import os.path
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import random
from multiprocessing import Process
from typing import Any
import traceback as tb


def removesuffix(st, sst):
    if st.endswith(sst):
        return st[:-len(sst)]
    else:
        return st


def removeprefix(st, sst):
    if st.startswith(sst):
        return st[len(sst):]
    else:
        return st


class Responce:
    """..."""
    protocol: str
    status: str
    content: str

    def __init__(self, p: str, s: str, c: str):
        self.protocol = p
        self.status = s
        self.content = c

    def to_bytes(self):
        """..."""
        if type(self.content) == bytes:
            cnt = self.content
        else:
            cnt = self.content.encode()
        return self.protocol.encode() + b" " + self.status.encode() + b"\n\n" + cnt


class Ss:
    """..."""
    sock: socket.socket
    host: str
    port: str
    root: str
    run: bool
    handlers: dict

    def __init__(self):
        self.handlers = {}
        pass

    def set_root(self, path: str):
        """..."""
        self.root = path

    def init(self, host: str, port: int = 65536):
        """..."""
        self.sock, self.host, self.port = init(host, port)

    def handler(self, method: str = "POST"):
        """..."""

        def wrapper(fn, _m: str = method):
            """..."""
            self.handlers[_m] = fn

        return wrapper

    def polling(self):
        """..."""
        self.run = True
        while self.run:
            # noinspection PyBroadException
            try:
                self.sock.listen(65535)
                conn, addr = self.sock.accept()
                data = conn.recv(1024).decode()
                if not data:
                    continue
                method, file, protocol, headers = parse_request(data)
                ret: Responce = self.handlers[method](Request(self, method, file, protocol, headers, addr))
                conn.sendall(ret.to_bytes())
                conn.close()
            except KeyboardInterrupt:
                self.run = False
            # noinspection PyBroadException
            except Exception as exc:
                tb.print_exception(exc)
                try:
                    # noinspection PyUnboundLocalVariable
                    conn.sendall(Responce("HTTP/1.1", "500 UNKNOWN", "Unknown error from server").to_bytes())
                except OSError:
                    pass
                except UnboundLocalError:
                    pass
                try:
                    # noinspection PyUnboundLocalVariable
                    conn.close()
                except OSError:
                    pass
                except UnboundLocalError:
                    pass
        try:
            conn.close()
            self.sock.detach()
        except:
            pass


class Path:
    """..."""
    def __init__(self, base, raw):
        self.base = base
        self.raw = raw

    def __getattribute__(self, item):
        if item in ("normalize", "base", "raw", "__new__", "__super__", "__str__", "__repr__", "__init__"):
            return object.__getattribute__(self, item)
        else:
            return self.raw.__getattribute__(item)

    def normalize(self):
        """..."""
        return parse_path(Path("/", removesuffix(self.base, "/")+"/"+removeprefix(parse_path(self.raw), "/")))

    def __str__(self):
        return self.raw

    def __repr__(self):
        return self.raw.__repr__()

    def __add__(self, other):
        if type(other) == str:
            return Path(self.base, self.raw+other).normalize()
        else:
            return Path(self.base, self.raw+other.raw).normalize()


class Request:
    """..."""
    server: Ss
    method: str
    path: Path
    protocol: str
    headers: dict
    client: tuple

    def __init__(self, server, m, pt, pr, h, c):
        self.server = server
        self.method = m
        self.protocol = pr
        self.headers = h
        self.path = pt if pt is Path else Path(self.server.root, pt)
        self.client = c


def threaded(fn):
    """..."""
    def thread(*a, **k):
        """..."""
        p = Process(target=fn, args=a, kwargs=k)
        p.daemon = True
        p.start()
        return p
    return thread


def init(host, port=65536):
    """..."""
    if port > 65535:
        port = random.randint(8000, 65535)
    try:
        _sock = socket.socket()
        _sock.bind((host, port))
        return _sock, host, str(port)
    except OSError:
        return init(host, port)


def parse_path(file):
    """..."""
    if file == "/":
        return "/index.html"
    elif file.endswith("/"):
        return file + "index.html"
    else:
        if os.path.isdir(file if type(file) == str else str(file)):
            return file + "/index.html"
        else:
            return file


# noinspection PyShadowingNames
def parse_request(data):
    """..."""
    method, file, protocol = data.splitlines()[0].strip().split()
    headers_raw = data.splitlines()[1:]
    while "" in headers_raw:
        headers_raw.remove("")
    headers = dict(i.split(": ") for i in headers_raw)
    return method, file, protocol, headers


def autoload(path, mode="rb"):
    """..."""
    with open(str(path) if path is not str else path, mode) as f:
        data = f.read()
    return data

# noinspection HttpUrlsUsage
# print("Server started at http://"+host+":"+str(port)+"/")

# conn: socket.socket = socket.socket()

# run = True

# noinspection PyBroadException
# while run:
# try:
# sock.listen(1)
# conn, addr = sock.accept()

# print('request from:', addr)

# data = conn.recv(1024).decode()
# if not data:
# break
# method, file, protocol, headers = parse_request(data)
# print(method, file)
# path = root+parse_path(file)
# if not os.path.exists(path):
# conn.send(b"HTTP/1.0 404 NOT FOUND\n\nnot found :(")
# with open(path, "rb") as f:
# rsp = b"HTTP/1.0 200 SUCCESS\n\n"+f.read()
# conn.send(rsp)

# conn.close()
# except KeyboardInterrupt:
# run = False
# except Exception as exc:
# tb.print_exception(exc)
# # noinspection PyBroadException
# try:
# conn.close()
# except Exception:
# pass
