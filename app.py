from flask import Flask,render_template,request,redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
mysql = MySQL(app)

app.config['SECRET_KEY'] = 'this is secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test2'

# index page
@app.route('/')
def index():
    return render_template("index.html")



# display patients information
@app.route('/show')
def show():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM question2')
    data = cursor.fetchall()

    return render_template("personal.html",data=data)


# add personal data form
@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == "POST":
        _fname = request.form['fname']
        _lname = request.form['lname']
        _birthday = request.form['birthday']
        _number = request.form['contact']
        _nic = request.form['nic']
        _note = request.form['note']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO question2 VALUES (NULL,% s, % s,% s, % s,% s,% s)',(_fname,_lname, _birthday, _number, _nic, _note,))
        mysql.connection.commit()
        cursor.close()

        redirect('/add')


    return render_template("pdform.html")


# update patient information
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM question2 WHERE id = % s', (id,))
    data = cursor.fetchone()

    if request.method == "POST":
        _fname = request.form['fname']
        _lname = request.form['lname']
        _birthday = request.form['birthday']
        _number = request.form['contact']
        _nic = request.form['nic']
        _note = request.form['note']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE question2 SET fist_name = %s,last_name = %s,birthday = %s,contact_number = %s,nic = %s,note = %s WHERE id = %s',(_fname,_lname,_birthday,_number,_nic,_note,id))
        mysql.connection.commit()
        cursor.close()

    return render_template("updatepdform.html",data=data)


# Delete patient information
@app.route('/delete/<id>',methods=['GET','POST'])
def delete(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM question2 WHERE id = %s',(id))
    mysql.connection.commit()
    return redirect('/show')


if __name__== "__main__":
    app.run(debug=True)