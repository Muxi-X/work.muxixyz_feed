'''coding = utf-8'''
from flask import jsonify, request
from . import api
from ..models import User
#from ..decorator import login_required
#from werkzeug.security import generate_password_hash, check_password_hash
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@api.route('/auth/login/', methods=['POST'])
def login():
    usrname = request.get_json().get('username')
    usr = User.query.filter_by(name=usrname).first()
    if usr is None:
        response = jsonify({
            "msg": 'user not existed!'})
        response.status_code = 401
        return response
    token = usr.generate_confirmation_token(usr)
    response = jsonify({
        "token": token})
    response.status_code = 200
    return response
