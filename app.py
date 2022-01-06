from flask import Flask, render_template, request, jsonify
from cpu_stress import stress
import kijiji_scraper as ks
import psutil
import os
from pymongo import MongoClient, collection
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')

mongo_client = MongoClient(MONGO_URI)
db = mongo_client.kijiji
collection = db.kijiji

app = Flask(__name__)

@app.route('/collect', methods=['GET', 'POST'])
def collect_car_data():

    with open('kijiji-links.txt', 'r') as f:

        all_links = f.readlines()

    all_data = []

    for link in all_links:

        data = ks.get_data(link)
        
        all_data.append(data)

    for data in all_data:

        collection.insert_many(data)

    for i in all_data:

        for j in i:

            j.pop('_id')

    stress()

    return jsonify(all_data)

@app.route('/view', methods=['GET', 'POST'])
def view_car_data():

    all_data = []

    for data in collection.find():

        all_data.append(data)

    for i in all_data:
        
        i.pop('_id')

    return jsonify(all_data)

@app.route('/info', methods=['GET', 'POST'])
def info():

    cpu_util = psutil.cpu_percent()

    return jsonify({"cpu_util": cpu_util})

@app.route('/', methods=['GET', 'POST'])
def index():

    return jsonify({"ping": "pong"})

if __name__ == '__main__':

    app.run(debug=True, port=9000, host='0.0.0.0')