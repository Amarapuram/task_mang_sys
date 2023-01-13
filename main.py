from flask_mysqldb import MySQL
from flask import Flask, request,render_template,redirect,url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from forms import LoginForm,RegisterForm

app = Flask(__name__)

# Configuration
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Arohit621587'
MYSQL_DB = 'taskmng'

app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_DB'] = MYSQL_DB
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL()
# Initialize the extension
mysql.init_app(app)

app.config['SECRET_KEY'] = 'thisisasecret'

#configure login manager
login_manager = LoginManager()
login_manager.init_app(app)


# create a user model
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    # fetch user from MySQL database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user WHERE U_id=%s', (user_id,))
    user = cur.fetchone()
    if user:
        return User(user['U_id'])
    return None

@app.route('/', methods=['GET'])
def home():
    cur = mysql.connection.cursor()
    user = None
    if current_user.is_authenticated:
        cur.execute(f"select * from user where U_id = {current_user.id}")
        user = cur.fetchone()
    return render_template("index.html",current_user=current_user,user=user)

#admin route
@app.route("/admin",methods=["GET"])
def admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin")
    admin = cur.fetchall()
    return render_template("admin/admin.html",admin=admin)

#admin/users
@app.route("/admin/user",methods=["GET"])
def users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user")
    users = cur.fetchall()
    return render_template("admin/admin_user.html",users=users)

@app.route("/admin/user/add",methods=["GET","POST"])
def add_user():
    cur = mysql.connection.cursor()
    if request.method == "POST":
        U_name = request.form.get("U_name")
        U_email = request.form.get("U_email")
        U_password = request.form.get("U_password")
        U_status = request.form.get("U_status")
        # U_image = request.form.get("U_image")
        U_gender = request.form.get("U_gender")
        cur.execute("INSERT INTO user (U_name,U_email,U_password,U_status,U_gender) VALUES (%s,%s,%s,%s,%s)",(U_name,U_email,U_password,U_status,U_gender))
        mysql.connection.commit()
        return redirect(url_for("users"))
    return render_template("admin/user_add.html")

@app.route("/admin/user/update/<int:user_id>",methods=["GET","POST"])
def update_user(user_id):
    cur = mysql.connection.cursor()
    if request.method == "POST":
        U_name = request.form.get("U_name")
        U_email = request.form.get("U_email")
        U_status = request.form.get("U_status")
        # U_image = request.form.get("U_image")
        U_gender = request.form.get("U_gender")
        cur.execute("UPDATE user SET U_name = %s,U_email = %s,U_status =%s,U_gender=%s WHERE U_id = %s",(U_name,U_email,U_status,U_gender,user_id))
        mysql.connection.commit()
        return redirect(url_for("users"))
    cur.execute(f"SELECT * FROM user where U_id = {user_id}")
    user = cur.fetchall()   
    return render_template("admin/user_update.html",user = user[0]) 

@app.route("/admin/user/delete/<int:user_id>",methods=["GET"])
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE from user where U_id ={user_id}")
    mysql.connection.commit()
    return redirect(url_for("users"))

@app.route("/admin/project",methods=["GET"])
def project():
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * from project")
    projects=cur.fetchall()
    return "Hi"
#??
@app.route("/admin/project/add/<int:admin_id>",methods=["GET","POST"])
def add_project(admin_id):
    cur = mysql.connection.cursor()
    if request.method == "POST":
        P_name = request.form.get("P_name")
        P_status = request.form.get("P_status")
        P_desc = request.form.get("P_desc")
        cur.execute("INSERT INTO project (P_name,P_desc,P_status,a_id) VALUES (%s,%s,%s,%s)",(P_name,P_desc,P_status,admin_id))
        mysql.connection.commit()
        return redirect(url_for("project"))
    return render_template("admin/admin_projects.html",admin_id=1)

@app.route("/admin/project/update/<int:project_id>",methods=["GET","POST"])
def update_project(project_id):
    cur = mysql.connection.cursor()
    if request.method == "POST":
        P_name = request.form.get("P_name")
        P_status = request.form.get("P_status")
        P_desc = request.form.get("P_desc")
        cur.execute("UPDATE project SET P_name = %s,P_status = %s,P_desc =%s WHERE P_id = %s",(P_name,P_status,P_desc,project_id))      #?
        mysql.connection.commit()
        return redirect(url_for("project"))
    cur.execute(f"SELECT * FROM project where P_id = {project_id}")
    user = cur.fetchall()   
    return render_template("admin/admin_projects.html",user = user[0])  

@app.route("/admin/project/delete/<int:project_id>",methods=["GET"])
def delete_project(project_id):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE from user where U_id ={project_id}")
    mysql.connection.commit()
    return redirect(url_for("project"))

#admin/project/task

@app.route("/admin/project/<int:project_id>/task",methods=["GET"])
def task(project_id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM task WHERE T_P_id= {project_id}")
    task = cur.fetchall()
    return render_template("admin/tasks_disp.html",task=task)

@app.route("/admin/<int:admin_id>/project/<int:project_id>/task/add",methods=["GET","POST"])
def add_task(admin_id,project_id):
    cur = mysql.connection.cursor()
    if request.method == "POST":
        T_name = request.form.get("T_name")
        T_date = request.form.get("T_date")
        T_deadline = request.form.get("T_deadline")
        T_sender = request.form.get("T_sender")
        T_reciever = request.form.get("T_reciever")
        T_status = request.form.get("T_status")
        cur.execute("INSERT INTO task (T_name,T_date,T_deadline,T_sender,T_reciever,T_status,T_P_id,a_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(T_name,T_date,T_deadline,T_sender,T_reciever,T_status,project_id,admin_id))
        mysql.connection.commit()
        return redirect(url_for("project"))
    return render_template("admin/add_task.html",project_id=project_id,admin_id=admin_id)

@app.route("/admin/project/<int:project_id>/update/task/<int:task_id>",methods=["GET","POST"])
def update_task(project_id,task_id):
    cur = mysql.connection.cursor()
    if request.method == "POST":
        T_name = request.form.get("T_name")
        T_date = request.form.get("T_date")
        T_deadline = request.form.get("T_deadline")
        T_sender = request.form.get("T_sender")
        T_receiver = request.form.get("T_receiver")
        T_status = request.form.get("T_status")
        cur.execute("UPDATE task SET T_name = %s,T_date = %s,T_deadline =%s,T_sender=%s,T_receiver=%s,T_status=%s WHERE T_project = %s AND T_id = %s",(T_name,T_date,T_deadline,T_sender,T_receiver,T_status,project_id,task_id))
        mysql.connection.commit()
        return redirect(url_for("project"))
    return render_template("tasks_disp.html")


@app.route("/admin/project/<int:project_id>/delete/task/<int:task_id>",methods=["GET"])
def delete_task(project_id,task_id):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE from task where T_project= {project_id} AND T_id ={task_id}")
    mysql.connection.commit()
    return redirect(url_for("project"))


@app.route("/admin/<int:admin_id>/projects/tasks/<int:task_id>/comment",methods=["GET"])
def comment(admin_id, task_id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM comments WHERE Task_id={task_id}")
    project = cur.fetchall()
    return render_template("admin/cmt_disp.html",project=project,admin_id=admin_id,task_id=task_id)

@app.route("/admin/projects/tasks/<task_id>/comment/add",methods=["GET","POST"])
def add_comment(task_id):
    cur = mysql.connection.cursor()
    if request.method == "POST":
        C_by = request.form.get("C_by")
        C_to = request.form.get("C_to")
        C_time = request.form.get("C_time")
        C_text = request.form.get("C_text")
        cur.execute("INSERT INTO comments (C_by,C_to,C_time,C_text) VALUES (%s,%s,%s) WHERE Task_id=%s",(C_by,C_to,C_time,C_text,task_id))
        mysql.connection.commit()
        return redirect(url_for("project"))
    return render_template("admin/task_cmt.html")

@app.route("/admin/projects/tasks/<task_id>/delete/comment/<int:Comment_id>",methods=["GET"])
def delete_comment(task_id,Comment_id):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE from commments where Task_id= {task_id} AND C_id ={Comment_id}")
    mysql.connection.commit()
    return redirect(url_for("project"))

#User

@app.route("/user/project/",methods=["GET"])
def user_project():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM project,user_project,user WHERE project.P_id = user_project.P_id AND user_project.U_id = user.U_id")
    project = cur.fetchall()
    return render_template("User/user_project.html",project=project)

@app.route("/user/project/tasks",methods=["GET"])
def user_task():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM task,user_task,user WHERE task.Task_id = user_task.Task_id AND user_task.U_id = user.U_id")
    project = cur.fetchall()
    return render_template("User/user_tasks.html",project=project)
#user_task_update

@app.route("/user/project/task/update/<int:task_id>",methods=["GET","POST"])
def user_update_task(task_id):
    cur = mysql.connection.cursor()
    if request.method == "POST":
        T_status = request.form.get("T_status")
        cur.execute(f"UPDATE task SET T_status = %s WHERE Task_id ={task_id}" )
        mysql.connection.commit()
        return redirect(url_for("project"))
    return render_template("tasks_disp.html")

@app.route("/user/projects/tasks/<int:task_id>/comment",methods=["GET"])
def user_comment(task_id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM comments WHERE Task_id={task_id}")
    project = cur.fetchall()
    return render_template("User/user_comment_disp.html",project=project)

@app.route("/user/projects/tasks/<task_id>/comment/add",methods=["GET","POST"])
def user_add_comment(task_id):
    cur = mysql.connection.cursor()
    if request.method == "POST":
        C_by = request.form.get("C_by")
        C_to = request.form.get("C_to")
        C_time = request.form.get("C_time")
        C_text = request.form.get("C_text")
        cur.execute("INSERT INTO comments (C_by,C_to,C_time,C_text) VALUES (%s,%s,%s) WHERE Task_id=%s",(C_by,C_to,C_time,C_text,task_id))
        mysql.connection.commit()
        return redirect(url_for("project"))
    return render_template("user/user_comment.html")

@app.route("/user/projects/tasks/<task_id>/delete/comment/<int:Comment_id>",methods=["GET"])
def user_delete_comment(task_id,Comment_id):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE from commments where Task_id= {task_id} AND C_id ={Comment_id}")
    mysql.connection.commit()
    return redirect(url_for("project"))

#login-Register-logout
@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    cur = mysql.connection.cursor()
    if login_form.validate_on_submit():
        email = request.form.get("email")
        password = request.form.get("password")
        cur.execute(f"select * from user where U_email = '{email}'")
        user = cur.fetchone()
        if user and user["U_password"] == password:
            user_obj = User(user['U_id'])
            login_user(user_obj)
            return redirect(url_for("home"))
    return render_template("auth/login.html", form=login_form)

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
@app.route("/register",methods=["GET","POST"])
def register():
    cur = mysql.connection.cursor()
    if request.method == "POST":
        U_name = request.form.get("U_name")
        U_email = request.form.get("U_email")
        U_password = request.form.get("U_password")
        U_status = request.form.get("U_status")
        # U_image = request.form.get("U_image")
        U_gender = request.form.get("U_gender")
        print(U_name)
        print(U_email)
        print(U_password)
        print(U_status)
        print(U_gender)

        cur.execute("INSERT INTO user (U_name,U_email,U_password,U_status,U_gender) VALUES (%s,%s,%s,%s,%s)",(U_name,U_email,U_password,U_status,U_gender))
        mysql.connection.commit()
        return redirect(url_for("users"))
    return render_template("admin/user_add.html")

if __name__ == '__main__':
    app.run(debug=True)