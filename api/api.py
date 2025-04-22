import os
from flask import Flask,jsonify,request
from flask_cors import CORS
from layout import Layout

app=Flask(__name__)
CORS(app)

@app.route("/compute_layout",methods=["POST"])
def compute_layout():
    request_json=request.json
    L=Layout(config=request_json)
    response_dict=L.compute_layout_to_response_dict(layout_type=request_json["layout_type"])
    return jsonify(response_dict)

if __name__=="__main__":
    app.run(debug=True)