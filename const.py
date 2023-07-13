"""..."""
from sserver import *


debug = True

"""errors = {
    404: "Location: {address}error/404/index.html\r\n\r\nRedirecting..."
}"""

errors = {
    404: Response("404 NOT FOUND", "Redirecting...", {"Location": "error/404/index.html"})
}

redirects = {
    "./index.html": Response("301 REDIRECT", "Redirecting...", {"Location": "home/unsigned/index.html"})
}
