from flask import Flask, request, jsonify
import csv
import pandas as pd

from main import application

# ----- root -------------------------------------------------------------------------------- 
@application.route("/")
def hello():
    return "Hello goorm!"
# -------------------------------------------------------------------------------------------    
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, threaded=True)