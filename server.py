#!/usr/bin/env python
from datetime import datetime
from flask import Flask, request
import json
import uuid


app = Flask(__name__)
app.config.from_object(__name__)


data = dict(
    power = "off"
    brightness = 1.0
    hue = 0.0
    saturation = 0.0
    kelvin = 3500
)


@app.route('/')
def main():
    return "It works!"


@app.route('/v1/lights/all')
def list_lights():
    return json.dumps({
        "id": "l1fxl4mp",
        "label": "lamp",
        "uuid": str(uuid.uuid4()),
        "connected": True,
        "power": data['power'],
        "color": {
            "hue": data['hue'],
            "saturation": data['saturation'],
            "kelvin": data['kelvin'],
        },
        "brightness": brightness,
        "last_seen": datetime.now().isoformat(),
    }, indent=4)


@app.route('/v1/lights/all/state', methods=['PUT'])
def set_state():
    for key, value in json.loads(request.data).items():
        data['key'] = value

    return json.dumps({
        "results": [
            {
                "id": "l1fxl4mp",
                "label": "lamp",
                "status": "ok",
            }
        ]
    }, indent=4)


if __name__ == "__main__":
    app.run(debug=True)
