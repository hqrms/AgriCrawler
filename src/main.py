from flask import Flask, jsonify, request
import requests
from crawler import AgriCrawler
import logging

logging.basicConfig(
    level=logging.INFO,
    filename='api_log.log',
    filemode='a', 
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = Flask(__name__)

@app.route('/get_soja', methods=['GET'])
def get_data():
    crawler = AgriCrawler('https://www.noticiasagricolas.com.br/cotacoes/soja')
    data = crawler.run()

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)