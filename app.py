from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps
import json
import os

# 初始化 Flask 应用
app = Flask(__name__)
app.secret_key = 'secret_key_babalababa'

# 配置静态文件路径
app.config['STATIC_FOLDER'] = {
    'static': 'static',
    'node_modules': 'node_modules'
}

# 配置 LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 用户数据文件路径
USERS_FILE = 'static/json/users.json'

# 如果用户数据文件不存在，则创建一个空文件
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump([], f)

# 定义用户类
class User(UserMixin):
    def __init__(self, id, username, email, password, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin


# 创建管理员用户
admin_user = User(id=0, username='admin', email='admin@example.com', password='password')
admin_user.is_admin = True  # 将管理员用户标记为管理员

# 装饰器：检查是否为管理员
def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin:
            return func(*args, **kwargs)
        else:
            abort(403)  # 禁止访问
    return decorated_function

# 登录用户加载函数
# 这里的问题，怪不得我的管理一直无法登录
@login_manager.user_loader
def load_user(user_id):
    if user_id == '0':
        return admin_user
    else:
        users = load_users()
        for user_data in users:
            if str(user_data['id']) == user_id:
                return User(**user_data)
    return None


# 加载用户数据
def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

# 保存用户数据
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

# 首页路由
@app.route('/')
def home():
    return render_template('login.html')

# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            admin_user.is_admin = True  # 将管理员用户标记为管理员
            login_user(admin_user)

            return redirect(url_for('manage_users'))

        users = load_users()
        for user_data in users:
            if user_data['username'] == username and user_data['password'] == password:
                user = User(**user_data)
                login_user(user)
                return redirect(url_for('index'))

        return render_template('login.html', error_message='用户名或密码错误')

    return render_template('login.html')

# 注册路由
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        users = load_users()
        max_user_id = max([user['id'] for user in users]) if users else 0
        for user_data in users:
            if user_data['username'] == username:
                return render_template('login.html', error_message='Username already exists')
            if user_data['email'] == email:
                return render_template('login.html', error_message='Email already exists')

        new_user_id = max_user_id + 1
        new_user = {'id': new_user_id, 'username': username, 'email': email, 'password': password}
        users.append(new_user)
        save_users(users)

        return redirect(url_for('login'))

    return render_template('login.html')

# 注销路由
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# 个人面板路由
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# 用户管理路由
@app.route('/manage_users')
def manage_users():
    if current_user.is_authenticated and current_user.is_admin:
        users = load_users()
        return render_template('manage_users.html', users=users)
    else:
        return redirect(url_for('login'))

# 删除用户路由
@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.is_authenticated and current_user.is_admin:
        users = load_users()
        for idx, user in enumerate(users):
            if user['id'] == user_id:
                del users[idx]
                save_users(users)
                return redirect(url_for('manage_users'))
        return 'User not found'
    else:
        return 'Access Denied'

# 子路由：首页
@app.route("/index.html")
@login_required
def index():
    return render_template('index.html')

# 子路由：数据随机展示
@app.route('/random-access.html')
@login_required
def random_access():
    return render_template('random-access.html')

# 子路由：分类关系
@app.route('/taxonomic-relationships.html')
@login_required
def taxonomic_relationships():
    return render_template('taxonomic-relationships.html')

# 子路由：植被分布
@app.route('/distribution.html')
@login_required
def search():
    return render_template('distribution.html')


# 子路由：种类
@app.route('/category.html')
@login_required
def category():
    return render_template('category.html')

if __name__ == '__main__':
    app.run(debug=True)
