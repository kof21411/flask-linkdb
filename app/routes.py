from flask import render_template, jsonify

from app import app
from common.utils import ConfigUtils


@app.route('/')
def index():
    return render_template('index.html', web=ConfigUtils.get_web_config())


@app.route('/get_links')
def get_links():
    try:
        total = 1
        list = [{
            'id': 1,
            'title': 'test',
            'link': '点击访问',
            'author': 'test',
            'good': 213,
            'views': 21312,
            'create_time': '2021年11月12日'
        }]
        return jsonify({'total': total, 'rows': list})
    except:
        pass
