import os
from flask import Flask,jsonify,request
from flask_cors import CORS
from layout import Layout

app=Flask(__name__)
CORS(app)

@app.route("/simple_test",methods=["POST"])
def simple_test():
    request_json=request.json
    simple_dict={}
    simple_dict["number"]=request_json["end_time"]-request_json["start_time"]
    return jsonify(simple_dict)

@app.route("/compute_layout",methods=["POST"])
def compute_layout():
    request_json=request.json
    print(type(request_json))
    L=Layout(config=request_json)
    response_dict=L.compute_layout_to_response_dict(layout_type=request_json["layout_type"])
    return jsonify(response_dict)

if __name__=="__main__":
    app.run(debug=True)