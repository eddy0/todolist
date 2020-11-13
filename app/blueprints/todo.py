from flask import render_template, Blueprint, jsonify, request
from flask_login import current_user

from app.extensions import db
from app.models import Item

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/')
def index():
    return render_template('index.html')


@todo_bp.route('/intro')
def intro():
    return render_template('_intro.html')


@todo_bp.route('/app')
def app():
    return render_template('_app.html')


@todo_bp.route('/items/new', methods=['POST'])
def new_item():
    data = request.get_json()
    if data is None or data['body'].strip() == '':
        return jsonify(message='Invalid item body.'), 400
    item = Item(body=data['body'], author=current_user._get_current_object())
    item.save()
    return jsonify(html=render_template('_item.html', item=item), message='+1')


@todo_bp.route('/item/<int:item_id>/edit', methods=['PUT'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user != item.author:
        return jsonify(message='Permission denied.'), 403

    data = request.get_json()
    if data is None or data['body'].strip() == '':
        return jsonify(message='Invalid item body.'), 400
    item.body = data['body']
    db.session.commit()
    return jsonify(message='Item updated.')


@todo_bp.route('/item/<int:item_id>/toggle', methods=['PATCH'])
def toggle_item(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user != item.author:
        return jsonify(message='Permission denied.'), 403

    item.done = not item.done
    db.session.commit()
    return jsonify(message='Item toggled.')


@todo_bp.route('/item/<int:item_id>/delete', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if current_user != item.author:
        return jsonify(message='Permission denied.'), 403

    db.session.delete(item)
    db.session.commit()
    return jsonify(message='Item deleted.')


@todo_bp.route('/item/clear', methods=['DELETE'])
def clear_items():
    items = Item.query.with_parent(current_user).filter_by(done=True).all()
    for item in items:
        db.session.delete(item)
    db.session.commit()
    return jsonify(message='All clear!')