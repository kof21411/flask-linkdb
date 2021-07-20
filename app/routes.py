import datetime
import json

from flask import render_template, jsonify, request
from sqlalchemy import text, or_, and_

from app import app, db
from app.models import Category, Links, ProsAndCons
from common.utils import ConfigUtils, Utils


@app.route('/')
def index():
    categorys = Category.query.order_by(Category.order).all()
    category_objs = {}
    for category in categorys:
        category_objs[str(category.id)] = category.name

    data = {
        "categorys": categorys,
        "category_objs": category_objs
    }
    return render_template('index.html', data=data, web=ConfigUtils.get_web_config())


@app.route('/get_links')
def get_links():
    try:
        num, page, sort, order, keyword = \
            request.args.get('rows'), request.args.get("page"), request.args.get('sort', None), request.args.get(
                'order', None), request.args.get('keyword', None)
        if sort == "undefined": sort = None
        if order == "undefined": order = None
        if order and order == "desc": sort = text(sort + " desc")

        if keyword:
            filters = or_(
                Links.link.like("%" + keyword + "%"),
                Links.title.like("%" + keyword + "%"),
                Links.author.like("%" + keyword + "%"),
            )
            objs, total = Links.query.order_by(sort).filter(filters).offset(int(num) * (int(page) - 1)).limit(
                num), Links.query.filter(filters).count()
        else:
            objs, total = Links.query.order_by(sort).offset(int(num) * (int(page) - 1)).limit(
                num).all(), Links.query.count()

        list = []
        for obj in objs:
            obj.create_time = obj.create_time.strftime("%Y-%m-%d")
            list.append(obj.to_json())

        return jsonify({'total': total, 'rows': list})
    except Exception as e:
        print(e)
        return jsonify({'total': 0, 'rows': []})


@app.route('/go', methods=["POST"])
def go_to_link():
    datas = request.form

    try:
        form = json.loads(datas.get("data"))
        link_id = form.get("link_id", None)

        if not link_id:
            raise RuntimeError("输入表单填写有误")

        link = Links.query.filter_by(id=int(link_id)).first()
        if not link:
            raise RuntimeError("不存在该链接")
        return json.dumps({"status": True, "msg": link.link}, ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps({"status": False, "msg": "发生系统错误"}, ensure_ascii=False)


@app.route('/op', methods=["POST"])
def op_pros_and_cons():
    datas = request.form

    try:
        form = json.loads(datas.get("data"))
        link_id, type = form.get("link_id", None), form.get("type", None)

        if not link_id or not type:
            return json.dumps({"status": False, "msg": "输入表单填写有误"}, ensure_ascii=False)

        ipaddr = request.remote_addr
        pros_and_cons = ProsAndCons.query.filter(
            and_(ProsAndCons.ipaddr == ipaddr, ProsAndCons.link == int(link_id))).first()
        if pros_and_cons:
            return json.dumps({"status": False, "msg": "已经操作过了"}, ensure_ascii=False)

        link = Links.query.filter_by(id=int(link_id)).first()
        if not link:
            return json.dumps({"status": False, "msg": "不存在该链接"}, ensure_ascii=False)

        new_pros_and_cons = ProsAndCons(link=link_id, type=int(type), ipaddr=ipaddr)
        db.session.add(new_pros_and_cons)

        if int(type) == 1:
            link.pros += 1
        elif int(type) == 0:
            link.cons += 1

        db.session.commit()
        return json.dumps({"status": True, "msg": "提交成功"}, ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps({"status": False, "msg": "发生系统错误"}, ensure_ascii=False)


@app.route('/post', methods=["POST"])
def post_link():
    datas = request.form

    try:
        form = json.loads(datas.get("data"))
        link, title, author, category = form.get("link", ""), form.get("title", ""), form.get("author", ""), form.get(
            "category", None)

        if len(link) == 0 or not category:
            return json.dumps({"status": False, "msg": "输入表单填写有误"}, ensure_ascii=False)

        ipaddr = request.remote_addr

        author_link = Links.query.filter_by(ipaddr=ipaddr).order_by(text("create_time desc")).first()
        if author_link \
                and not ((datetime.datetime.now() - author_link.create_time).seconds > 30):
            return json.dumps({"status": False, "msg": "无法连续提交，稍等一段时间"}, ensure_ascii=False)

        if len(author) == 0:
            author = "匿名者"

        status, html = Utils.check_url(link)
        if status == None or len(html) < 100:
            return json.dumps({"status": False, "msg": "此链接无效"}, ensure_ascii=False)

        if len(title) == 0:
            title = Utils.get_web_title(html)

        if Links.query.filter_by(link=link).first():
            return json.dumps({"status": False, "msg": "该链接已存在"}, ensure_ascii=False)

        link = Links(title=title, author=author, link=link, category=category, ipaddr=ipaddr)
        db.session.add(link)
        db.session.commit()
        return json.dumps({"status": True, "msg": "提交成功"}, ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps({"status": False, "msg": "发生系统错误"}, ensure_ascii=False)
