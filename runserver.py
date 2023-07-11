"""..."""

from sserver import *
import os, json


ss = Ss()

# We can use random free socket :)
ss.init('localhost', 8181)

# noinspection HttpUrlsUsage
print("Server started at http://"+ss.host+":"+ss.port+"/")

# noinspection HttpUrlsUsage
address = "http://"+ss.host+":"+ss.port+"/"

ss.set_root(removesuffix(os.path.abspath("."), "/")+"/idash/htdocs")

print(ss.root)
print(" "*3, ss.root+"/index.html")


errors = {
    404: f"<script>location.href = '\r\nLocation: https://localhost:8181/error/404/index.html'\r\n"
}

redirects = {
    ss.root+"/index.html": "\r\nLocation: https://localhost:8181/home/unsigned/index.html\r\n"
}


@ss.handler("GET")
def func(request):
    """ standard GET handler"""
    path = request.path.normalize()
    print("GET", path)
    for red in redirects:
        if str(path) == red:
            print("   ", "301", "REDIRECT", path, redirects[red])
            print(">>>"+Responce("HTTP/1.0", "301 REDIRECT", redirects[red]).to_bytes().__repr__()+"<<<")
            return Responce("HTTP/1.0", "301 REDIRECT", redirects[red])
    if not os.path.exists(str(path)):
        return Responce("HTTP/1.0", "301 REDIRECT", errors[404])
    else:
        ret = Responce("HTTP/1.0", "200 OK", autoload(path))
        return ret


def parse_args(data: str):
    """..."""
    return dict(i.split("=") for i in data.split("&"))


@ss.handler("POST")
def func(request: Request):
    """ API POST handler"""
    scope, function = str(request.path).split("/api/", 1)[1].split("/")
    function, args = function.split("?")
    args = parse_args(args)

    return Responce("HTTP/1.0", "200 OK", json.dumps({"scope": scope, "func": function, "args": args}))


ss.polling()
