from . import db
from flask import jsonify
from sqlalchemy.sql import text

# db.session.query(Table).filter()有bug,导致生成的sql语句为
# select * from table where false = 1;
# 因此无法查询到任何数据，故在需要使用filter的地方直接使用sql语句查询

def get_rows(Table, Record, Value, pageNum, pageSize, reverse=False):
    if Record is None:
        rows = db.session.query(Table).count()
    else:
        sql = "select count(*) from " + str(Table.__tablename__) + " where " + str(Record) + " = " + str(Value)
        ret = db.session.execute(sql).first()
        rows = ret[0]

    yu = rows % pageSize
    chu = rows // pageSize
    if yu is 0:
        pageMax = chu
    else:
        pageMax = chu + 1

    hasNext = True
    if pageNum >= pageMax:
        hasNext = False
    if Record is not None:
        if reverse:
            sql = "select * from " + str(Table.__tablename__) + " where " + str(Record) + " = " + str(Value) + \
                  " order by id desc limit " + str(pageSize) + " offset " + str((pageNum-1)*pageSize)
            dataList = db.session.query(Table).from_statement(text(sql)).all()
        else:
            sql = "select * from " + str(Table.__tablename__) + " where " + str(Record) + " = " + str(Value) + \
                  " limit " + str(pageSize) + " offset " + str((pageNum-1)*pageSize)
            dataList = db.session.query(Table).from_statement(text(sql)).all()
    else:
        if reverse:
            dataList = db.session.query(Table).order_by("id desc").limit(pageSize).offset((pageNum-1)*pageSize)
        else:
            dataList = db.session.query(Table).limit(pageSize).offset((pageNum-1)*pageSize)

    # return dict
    dictList = []
    for d in dataList:
        dictList.append(d.to_dict())


    return {
        'pageNum': pageNum,
        'pageMax': pageMax,
        'hasNext': hasNext,
        'rowsNum': len(dictList),
        'dataList': dictList,
    }

