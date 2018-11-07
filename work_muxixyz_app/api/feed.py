from flask import jsonify

from ..models import User, Feed, User2Project
from . import api
from ..decorator import login_required
from ..page import get_rows


PAGESIZE = 40
NOBODY=0
NORMAL=1
ADMIN=3
SUPERADMIN=7
nodata = {
    "dataList": [],
    "hasNext": False,
    "pageMax": 0,
    "pageNum": 0,
    "rowsNum": 0
}


@api.route('/feed/list/<int:page>/', methods=['GET'], endpoint="getfeedlist")
@login_required(1)
def getfeedlist(uid,page):
    """
    在feedlist中不再筛选权限，而是在点击时的api中判定是否拥有权限
    """
    user = User.query.filter_by(id=uid).first() or None
    # 用户未查询到，返回空
    if not user:
        return jsonify(nodata),404 
    # 用户权限为NOBODY，返回空
    if user.role is NOBODY:
        return jsonify(nodata),401
    else:
        # 查询数据
        datas = get_rows(Feed, None, None, page, PAGESIZE, reverse=True)
        if len(datas['dataList']) is 0:
            return jsonify(nodata)

        kindinit = datas['dataList'][0].get("source").get("kind_id")
        dayinit = datas['dataList'][0].get("timeday")
        for d in datas['dataList']:
            if d.get("source").get("kind_id") != kindinit:
                kindinit = d.get("source").get("kind_id")
                d.update({"ifsplit": True})
            elif d.get("timeday") != dayinit:
                dayinit = d.get("timeday")
                d.update({"ifsplit": True})
            else:
                d.update({"ifsplit": False})
        
        # 为管理员，则返回所有数据
        if user.role is ADMIN or user.role is SUPERADMIN:
            return jsonify(datas)
        # 为普通用户，则查询用户所在的project ids,从所有的datas中删去不在的数据，再返回
        elif user.role is NORMAL:
            reliations = User2Project.query.filter_by(user_id=uid).all()
            pids = [r.project_id for r in reliations]

            for d in datas['dataList']:
                if d.get("source").get("project_id") in pids:
                    datas['dataList'].remove(d)
            datas['rowsNum'] = len(datas['dataList'])
            return jsonify(datas)
    
    
@api.route('/feed/list/<int:userid>/personal/<int:page>/', methods=['GET'], endpoint="getuserfeedlist")
@login_required(1)
def getuserfeedlist(uid, userid, page):
    user = User.query.filter_by(id=uid).first() or None
    # 用户未查询到，返回空
    if not user:
        print("nouser")
        return jsonify(nodata),404 
    # 用户权限为NOBODY，返回空
    if user.role is NOBODY:
        return jsonify(nodata),401
    else:
        # 查询数据,此处以userid为筛选条件 <=============== DIFFERENCE HERE
        datas = get_rows(Feed, "userid", userid, page, PAGESIZE, reverse=True)    
        if len(datas['dataList']) is 0:
            return jsonify(nodata)

        kindinit = datas['dataList'][0].get("source").get("kind_id")
        dayinit = datas['dataList'][0].get("timeday")
        for d in datas['dataList']:
            if d.get("source").get("kind_id") != kindinit:
                kindinit = d.get("source").get("kind_id")
                d.update({"ifsplit": True})
            elif d.get("timeday") != dayinit:
                dayinit = d.get("timeday")
                d.update({"ifsplit": True})
            else:
                d.update({"ifsplit": False})
        
        # 为管理员，则返回所有数据
        if user.role is ADMIN or user.role is SUPERADMIN:
            return jsonify(datas)
        # 为普通用户，则查询用户所在的project ids,从所有的datas中删去不在的数据，再返回
        elif user.role is NORMAL:
            reliations = User2Project.query.filter_by(user_id=uid).all()
            pids = [r.project_id for r in reliations]

            for d in datas['dataList']:
                if d.get("source").get("project_id") in pids:
                    datas['dataList'].remove(d)
            datas['rowsNum'] = len(datas['dataList'])
            return jsonify(datas)
