"""..."""
import pprint

from sserver import *
import os
import json
import const


ss = Ss(const.debug)

# We can use random free socket :)
ss.init('localhost')  # , 8181)

# noinspection HttpUrlsUsage
print("Server started at http://"+ss.host+":"+ss.port+"/")

# noinspection HttpUrlsUsage
address = "http://"+ss.host+":"+ss.port+"/"

ss.set_root(removesuffix(os.path.abspath("."), "/")+"/idash/htdocs")

print(ss.root)
print(" "*3, ss.root+"/index.html")


def to_html(data):
    return "<!DOCTYPE HTML><head><link rel=\"stylesheet\" hre"\
           "f=\"https://fonts.googleapis.com/css?family=Fira+Code\"></head><body style=\"back"\
           "ground-color: black; color: white; font-family: Fira Code;"\
           "font-famiily: monospace;\">" + data.replace("\t", "    ").replace(" ", "&nbsp;").replace("\n", "<br/>") +\
           "<body/>"


@ss.handler("GET")
def func(request):
    """ standard GET handler"""
    from sserver import Response

    try:
        if const.debug:
            print("new GET request:\n", "   "+str(request.path)+"\n" +
                  pprint.pformat(request.headers).replace("\n", "\n    "))

        if not os.path.exists(request.path.normalize()):
            response = Response("301 REDIRECT", const.errors[404].format())
        else:
            response = Response("200 OK", autoload(request.path.normalize()))

        for red in const.redirects:
            if str(request.path) == red:
                response = const.redirects[red]
                response.headers["Location"] = response.headers["Location"].format(address=address)
                break

        if request.path.raw == "./favicon.ico":
            response = Response("404")
            return response

        if const.debug:
            print("Response: "+repr(response.to_bytes()[:128]))

        return response
    except Exception as exc:
        response = Response("500 SERVER ERROR", to_html("\n".join(tuple(tb.format_exception(exc)))))
        print(response)
        return response


def parse_args(data: str):
    """..."""
    return dict(zip(zip(i.split("=") for i in data.split("&"))))


@ss.handler("POST")
def func(request: Request):
    """ API POST handler"""
    scope, function = str(request.path).split("/api/", 1)[1].split("/")
    function, args = function.split("?")
    args = parse_args(args)

    return Response("200 OK", json.dumps({"scope": scope, "func": function, "args": args}))


ss.polling()
