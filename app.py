from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, jsonify
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
# static的那个应该是内置有的定义
@app.route('/node_modules/<path:filename>')
def node_modules_files(filename):
    return send_from_directory(app.config['STATIC_FOLDER']['node_modules'], filename)

# 配置 LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 用户数据文件路径
USERS_FILE = 'static/json/users.json'
# 创建一个空字典，用于存储植物名称和它们对应的类别
plant_categories = {}
files_directory = 'static/datasets/'

# 修改文件列表，以便包含完整的文件路径
files = [os.path.join(files_directory, 'environment.txt'),
         os.path.join(files_directory, 'category.txt'),
         os.path.join(files_directory, 'function.txt'),
         os.path.join(files_directory, 'difficulty.txt')]

#遍历文件列表，对每个文件执行以下操作
for file_name in files:
    # 以只读模式打开文件，并指定编码为 utf-8
    with open(file_name, 'r', encoding='utf-8') as file:
        # 逐行读取文件内容
        for line in file:
            # 将每行数据按逗号分割，并去除首尾的空格
            data = line.strip().split(',')
            # 类别是第一个元素
            category = data[0]
            # 植物名称列表是剩余的元素
            plants = data[1:]
            # 遍历植物名称列表
            for plant in plants:
                # 如果植物名称已经存在于字典中，则将类别添加到对应的列表中
                if plant in plant_categories:
                    plant_categories[plant].append(category)
                else:
                    # 否则，在字典中为该植物名称创建一个新的类别列表
                    plant_categories[plant] = [category]


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


def read_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    return process_data(data)

def process_data(data):
    # 按换行符分割数据，并去除首尾的空格
    lines = data.strip().split('\n')
    # 初始化结果列表
    result = []
    # 遍历每一行数据
    for line in lines:
        # 按逗号分割行数据
        items = line.split(',')
        # 将分割后的数据转换为字典，并添加到结果列表中
        result.append({"name": items[0], "value": len(items) - 1})
    # 返回结果列表
    return result

# 定义查询函数，根据植物名称查找其类别
def find_plant_category(plant_name):
    # 如果植物名称存在于字典中，则返回对应的类别列表
    if plant_name in plant_categories:
        return plant_categories[plant_name]
    else:
        # 否则返回 None
        return None

# 定义查询函数，根据类别查找对应的植物列表
def find_plants_by_category(category):
    # 使用列表推导式返回属于指定类别的所有植物名称
    return [plant for plant, categories in plant_categories.items() if category in categories]

# 定义查询函数，查找属于某个类别的所有植物
def find_plants_in_category(category):
    # 初始化一个空列表，用于存储属于指定类别的植物名称
    plants_in_category = []
    # 遍历字典中的植物名称和类别列表
    for plant, categories in plant_categories.items():
        # 如果指定类别存在于植物的类别列表中，则将该植物名称添加到列表中
        if category in categories:
            plants_in_category.append(plant)
    # 返回包含属于指定类别的植物名称的列表
    return plants_in_category

def read_plant_data():
    plant_data = {}
    for filename in os.listdir(files_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(files_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    parts = line.strip().split(',')
                    category = parts[0]
                    plants = parts[1:]
                    plant_data[category] = plants
    return plant_data

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
def distribution():
    return render_template('distribution.html')


# 子路由：种类
@app.route('/category.html')
@login_required
def category():
    return render_template('category.html')

@app.route('/card.html')
@login_required
def card():
    return render_template('card.html')

@app.route('/card_2.html')
@login_required
def card_2():
    return render_template('card_2.html')

@app.route('/chat.html')
@login_required
def 切换():
    return render_template('chat.html')

# 子路由：植物数据
@app.route('/get_plant_data')
def get_plant_data():
    # 读取植物数据并返回 JSON 格式
    plant_data = read_plant_data()
    return jsonify(plant_data)

# 子路由：植物数据
@app.route('/data/<filename>')
def data(filename):
    # 如果文件名不在指定的列表中，则返回 404 错误
    if filename not in ['category', 'function', 'environment', 'difficulty']:
        abort(404)
    file_path = os.path.join(files_directory, f'{filename}.txt')
    try:
        data = read_data(file_path)
        return jsonify(data)
    except FileNotFoundError:
        abort(404)

# 子路由：植物数据
@app.route('/search', methods=['GET', 'POST'])
def search():
    search_term = request.form.get('search_term', '')  # 使用 get 方法提供默认值
    categories = find_plant_category(search_term)
    plants = find_plants_by_category(search_term)

    if categories or plants:
        # 如果找到了植物或类别，渲染相应的模板
        if categories:
            return render_template('result.html', plant_name=search_term, categories=categories)
        else:
            return render_template('category_result.html', category=plants[0], plants=plants)
    else:
        # 如果既没有找到植物也没有找到类别，渲染未找到的页面
        return render_template('not_found.html', search_term=search_term)

if __name__ == '__main__':
    app.run(debug=True)
