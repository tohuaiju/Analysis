from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)

# 静态文件路由
app.config['STATIC_FOLDER'] = {
    'static': 'static',
    'node_modules': 'node_modules'
}
@app.route('/node_modules/<path:filename>')
def node_modules_files(filename):
    return send_from_directory(app.config['STATIC_FOLDER']['node_modules'], filename)

# 配置 MySQL 数据库连接字符串
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://EaseAty:123@EaseAty.mysql.pythonanywhere-services.com/EaseAty$sql'
# 关闭 Flask-SQLAlchemy 的追踪修改功能，以提高性能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy
db = SQLAlchemy(app)

# 初始化 LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # 检查密码是否匹配
            login_user(user)
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error_message='Invalid username or password')
    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    return 'Welcome to your profile!'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# 首页，主路由
@app.route("/index_0.html")
def index():
    return render_template('index_0.html')

# 第一个子路由
@app.route('/random-access.html')
def random_access():
    return render_template('random-access.html')

# 第二个子路由
@app.route('/taxonomic-relationships.html')
def Taxonomic_relationships():
    return render_template('taxonomic-relationships.html')

# 第三个子路由
@app.route('/distribution_map.html')
def distribution_map():
    return render_template('distribution_map.html')

# 第四个子路由
@app.route('/search.html')
def search():
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
