#!/usr/bin/env python
# 上面这一句是可执行文件时，直接调用路径中的Python

# author:Sole_idol
# filename: manage.py
# datetime:2020/8/19 7:59
"""
05 - ORM系统练习
"""
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
# 数据库迁移
from flask_migrate import Migrate,MigrateCommand


app = Flask(__name__)
# 定义manager对象
manager = Manager(app)
# 数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://demon:123456@localhost:3306/school'
# 每次请求结束后都会自动提交数据库中的数据
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 创建一个db实例
db = SQLAlchemy(app)
# 数据库迁移
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)  # 这里的 db 是自己随便起的名字，迁移时用的db就是他



class Student(db.Model):
    '''
    定义表结构
    '''
    
    # 指定一个表名
    __tablename__ = 'student'
    # 字段定义
    id = db.Column(db.Integer, primary_key=True)  # 指定主键后，自动指定自增
    name = db.Column(db.String(20), nullable=False, unique=True)  # 不为空，不重复
    gender = db.Column(db.Enum('男', '女', '保密'))
    city = db.Column(db.String(10), nullable=False)  # 不允许为空
    birthday = db.Column(db.Date, default='1990-01-01')
    bio = db.Column(db.Text)
    money = db.Column(db.Float)


class User(db.Model):
    '''
    简单用户表
    '''
    # 指定一个表名
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)  # 指定主键后，自动指定自增
    name = db.Column(db.String(20), nullable=False)  # 不为空
    gender = db.Column(db.Enum('男', '女', '保密'))
    math = db.Column(db.Integer, default=80)


@manager.command
def init_db():
    '''
        创建数据库中的表
    '''
    db.create_all()


# 创建的用户数据实例
u1 = User(name='jack', gender='男', math=98)
u2 = User(name='merry', gender='女', math=67)
u3 = User(name='Bob', gender='男', math=78)
u4 = User(name='tom', gender='男', math=48)
u5 = User(name='honny', gender='男', math=76)
u6 = User(name='alex', gender='女', math=83)
u7 = User(name='sole', gender='男', math=90)
u8 = User(name='idol', gender='男', math=91)


@manager.command
def insert_data():
    '''
    插入数据
    '''
    
    # 插入一条数据
    db.session.add(u1)
    db.session.add(u2)
    
    # 插入多条数据
    db.session.add_all([u3, u4, u5, u6, u7, u8])
    db.session.commit()


@manager.command
def del_db(id):
    '''
    删除数据
    :return:
    '''
    u = User.query.get(int(id))
    db.session.delete(u)
    print('已删除用户：', u)
    db.session.commit()


@manager.command
def update_db():
    '''
    修改数据
    :return:
    '''
    # 普通修改  (未成功！！！)
    u3.name = '王哈哈'
    db.session.commit()
    
    # 根据查询结果修改
    u = User.query.filter_by(id=3)
    # 下面参数symchronize_session=False是关闭同步会话
    u.update({'gender': '保密'}, symchronize_session=False)
    db.session.commit()


@manager.command
def sel_db():
    '''
    查询用户信息
    :return:
    '''
    # 查找id=10的用户
    user = User.query.get(3)
    print('\n************************\n', user.id, ' ---> ', user.name)
    # 删选过滤出id=7的用户    filter_by只能赋予关键字一个等于的值，不能给一个范围，filter可以给一个范围
    user2 = User.query.filter_by(id=7).one()  # <User 7>
    print('\n************************\n', user2.id, ' ---> ', user2.name)
    print(user2)
    # 过滤删选2
    user3 = User.query.filter(User.id < 5).order_by('math')
    uu3 = user3.all()
    print('\n************************\n')
    print('user3:', user3, '\nuu3:', uu3)
    # 打印结果：user3: SELECT user.id AS user_id, user.name AS user_name, user.gender AS user_gender
    # FROM user
    # WHERE user.id < %(id_1)s ORDER BY user.name
    
    # uu3: [<User 3>, <User 1>, <User 2>, <User 4>]
    print('\n************************\n')
    for user in user3:
        print(user.id, ' ---> ', user.name)
    
    # 按量取出数据：limit / offset
    print('\n************************\n')
    # 这里面limit不支持两个参数
    user4 = User.query.filter(User.id > 2).limit(3).offset(2)
    for user in user4:
        print(user.id, ' ---> ', user.name)
    
    # 计数：count
    num = User.query.filter(User.id > 3).count()
    print('\n************************\n')
    print(f'id>3的有{num}个')
    
    # 检查是否存在
    print('\n************************\n')
    # 不能使用get获取的对象，他没有exists()
    # ex = User.query.get(5).exists()
    # print(ex)
    ex = User.query.filter_by(name='jack').exists()
    res = db.session.query(ex).scalar()
    print(ex)  # ex的打印结果：EXISTS (SELECT 1 FROM "user" WHERE "user".name = :name_1)
    
    print(res)
    
    print('\n************************\n')
    t1 = User.query.filter_by(id=7)
    t2 = User.query.get(7)
    print('t1:', t1)
    '''t1: SELECT user.id AS user_id, user.name AS user_name, user.gender AS user_gender
    FROM user
    WHERE user.id = %(id_1)s
    '''
    print('t2:', t2)  # t2: <User 7>
    
    # 排序order_by
    print('\n************************\n')
    # 按数学成绩 升序 (默认)
    # user5 = User.query.order_by('math')
    # 按数学成绩 降序
    user5 = User.query.order_by(db.desc(User.math))
    for u in user5:
        print(f'{u.id} --> {u.name} --> {u.math}')


@app.route('/', methods=('POST', 'GET'))
def main():
    return render_template('base1.html')


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8080, debug=True)
    manager.run()
