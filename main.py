from flask import Flask, request, send_from_directory, Response, redirect
from flask_cors import CORS
import requests

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def catch_all(path):

    proxied_response = requests.request(
        request.method,
        f"https://accounts.google.com/{path}",
        headers={
            **{
                key: value
                for key, value in request.headers.items()
                if key.lower()
                not in [
                    "content-length",
                    "connection",
                    "origin",
                    "referer",
                    "x-forwarded-for",
                    "x-forwarded-host",
                    "x-forwarded-proto",
                ]
            },
            "host": "accounts.google.com",
            "origin": "https://accounts.google.com",
            "referer": "https://accounts.google.com",
        },
        data=request.get_data(as_text=True),
        params=request.args,
        allow_redirects=True,
    )

    headers = {
        key: value
        for key, value in proxied_response.headers.items()
        if key.lower()
        not in ["transfer-encoding", "content-encoding", "content-length"]
    }

    return Response(proxied_response.content, proxied_response.status_code, headers)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
