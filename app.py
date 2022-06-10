from flask import Flask, jsonify
from tasks import get_celery_stats

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/celery/stats')
def get_celery_stats_route():
    response = get_celery_stats.delay().get()
    print("Get AsyncResult response ", response, flush=True)
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
