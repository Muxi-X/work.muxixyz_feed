from flask import jsonify

from ..models import Feed
from . import api
from ..decorator import login_required
from ..page import get_rows


PAGESIZE = 20

@api.route('/feed/list/<int:page>/', methods=['GET'], endpoint="getfeedlist")
@login_required(1)
def getfeedlist(uid,page):
    """
    在feedlist中不再筛选权限，而是在点击时的api中判定是否拥有权限
    """
    datas = get_rows(Feed, None, None, page, PAGESIZE, reverse=True)
    kindinit = datas['dataList'][0].get("source_kindid")
    for d in datas['dataList']:
        if d.get("source").get("kind_id") is not kindinit:
            kindinit = d.get("source").get("kind_id")
            d.update({"ifsplit": True})
        else:
            d.update({"ifsplit": False})
    
    return jsonify(datas)
    
    
@api.route('/feed/list/<int:userid>/personal/<int:page>/', methods=['GET'], endpoint="getuserfeedlist")
@login_required(1)
def getuserfeedlist(uid, userid, page):
    datas = get_rows(Feed, "userid", userid, page, PAGESIZE, reverse=True)    
    kindinit = datas['dataList'][0].get("source_kindid")
    for d in datas['dataList']:
        if d.get("source").get("kind_id") is not kindinit:
            kindinit = d.get("source").get("kind_id")
            d.update({"ifsplit": True})
        else:
            d.update({"ifsplit": False})
    
    return jsonify(datas)

