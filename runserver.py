"""..."""
import pprint

from sserver import *
import os
import json


ss = Ss()

# We can use random free socket :)
ss.init('localhost')  # , 8181)

# noinspection HttpUrlsUsage
print("Server started at http://"+ss.host+":"+ss.port+"/")

# noinspection HttpUrlsUsage
address = "http://"+ss.host+":"+ss.port+"/"

ss.set_root(removesuffix(os.path.abspath("."), "/")+"/idash/htdocs")

print(ss.root)
print(" "*3, ss.root+"/index.html")


errors = {
    404: f"Location: {address}error/404/index.html\r\n\r\nRedirecting..."
}

redirects = {
    "./index.html": f"Location: {address}home/unsigned/index.html\r\n\r\nRedirecting..."
}


@ss.handler("GET")
def func(request):
    """ standard GET handler"""

    try:
        # logs
        print("new GET request:\n", "   "+str(request.path)+"\n" +
              pprint.pformat(request.headers).replace("\n", "\n    "))

        if not os.path.exists(request.path.normalize()):
            responce = Responce("301 REDIRECT", errors[404])
        else:
            responce = Responce("200 OK", autoload(request.path.normalize()))

        for red in redirects:
            if str(request.path) == red:
                responce = Responce("301 REDIRECT", redirects[red])
                break

        if request.path.raw == "./favicon.ico":
            responce = Responce("404")
            return responce

        print("responce: "+repr(responce.to_bytes()[:128]))
        return responce
    except Exception as exc:
        return Responce("500 SERVER ERROR", "\n".join(tuple(tb.format_exception(exc))))


def parse_args(data: str):
    """..."""
    return dict(zip(zip(i.split("=") for i in data.split("&"))))


@ss.handler("POST")
def func(request: Request):
    """ API POST handler"""
    scope, function = str(request.path).split("/api/", 1)[1].split("/")
    function, args = function.split("?")
    args = parse_args(args)

    return Responce("200 OK", json.dumps({"scope": scope, "func": function, "args": args}))


ss.polling()
