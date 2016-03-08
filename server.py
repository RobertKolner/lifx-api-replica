#!/usr/bin/env python
from datetime import datetime
from flask import Flask, request, render_template
import colorsys
import json
import uuid


app = Flask(__name__)
app.config.from_object(__name__)


data = dict(
    power = "off",
    brightness = 1.0,
    hue = 0.0,
    saturation = 0.0,
    kelvin = 3500
)


@app.route('/')
def main():
    return render_template('index.html')


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
        "brightness": data['brightness'],
        "last_seen": datetime.now().isoformat(),
    }, indent=4)


@app.route('/v1/lights/all/state', methods=['PUT'])
def set_state():
    print request.data
    request_data = json.loads(request.data).copy()
    color = request_data.pop('color', None)
    if color is not None:
        rgb = webcolors.hex_to_rgb(color)
        hls = colorsys.rgb_to_hls(*rgb)
        data['hue'] = hls[0]
        data['saturation'] = hls[2]
        data['brightness'] = hls[1]

    power = request_data.pop('power', None)
    if power is not None:
        if power in ['on', 'off']:
            request_data['power'] = power
        else:
            return json.dumps({
                'error': "Invalid value for 'power'!"
            }, indent=4), 400

    for key, value in json.loads(request_data).items():
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


@app.route('/v1/lights/all/toggle', methods=['POST'])
def toggle():
    data['power'] = 'on' if data['power'] == 'off' else 'off'
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
