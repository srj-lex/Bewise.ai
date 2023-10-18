from typing import Final

from flask import Flask, request, Response
import requests

from db import write_object_in_db, get_object_from_db


URL: Final[str] = "https://jservice.io/api/random?count="
MESSAGE_ERROR: Final[str] = "Значение должно быть целочисленным!"

app = Flask(__name__)


@app.route(
    "/quiz/",
    methods=[
        "POST",
    ],
)
def quiz_view() -> Response:
    count_value = request.get_json()["questions_num"]
    if not count_value.isdigit():
        return (MESSAGE_ERROR, 404)

    while True:
        response = requests.get(URL + f"{count_value}")
        if write_object_in_db(response.json()):
            break
        print("duplicate")

    resp = get_object_from_db()
    return (resp, 200)


if __name__ == "__main__":
    app.debug = False
    app.run(host="0.0.0.0")
