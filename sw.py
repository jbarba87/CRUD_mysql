from flask import Flask, render_template, request, url_for, redirect
import mysql.connector as mysql

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWD = "jorge"



def sql_consulta(database, command):
  db = mysql.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWD, database = database)
  cursor = db.cursor()
  cursor.execute(command)
  result = cursor.fetchall()
  db.close()
  return result

def sql_ejecucion(database, command):
  db = mysql.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASSWD, database = database)
  cursor = db.cursor()
  cursor.execute(command)
  db.commit()
  db.close()

app = Flask(__name__)

@app.route("/")
def index():
  re = sql_consulta("bookstore", "select *  from empleado;")
  return render_template("lista.html", list=re)

@app.route("/formulario")
def formulario():
  return render_template("form.html")

@app.route("/agregar", methods = ['POST'])
def agregar():
  if request.method == 'POST':
    idempleado = request.form['txtId']
    apellido = request.form['txtApellido']
    nombre = request.form['txtNombre']
    direccion = request.form['txtCiudad']
    email = request.form['txtCorreo']
    re = sql_ejecucion("bookstore", "insert into empleado (idempleado, apellido, nombre, direccion, email) values ('"+ idempleado + "', '" + apellido + "', '" + nombre + "', '" + direccion + "', '"+ email +"');")
    return redirect("/")


@app.route("/form2/<int:index>")
def form2(index):
  sql_command = "select * from empleado where idempleado =" + str(index) + ';'
  re = sql_consulta("bookstore", sql_command)
  return render_template("form2.html", res = re)

@app.route("/form2/update", methods = ['POST'])
def update():
  if request.method == 'POST':
    idempleado = request.form['txtId']
    apellido = request.form['txtApellido']
    nombre = request.form['txtNombre']
    direccion = request.form['txtCiudad']
    email = request.form['txtCorreo']
    
    sql_command = "update empleado set apellido='" + apellido + "', nombre='" + nombre + "', direccion='" + direccion + "', email='" + email + "' where idempleado=" + idempleado + ';'
    print(sql_command)
    sql_ejecucion("bookstore", sql_command)
  return redirect(url_for('index'))
 
@app.route("/delete/<int:index>")
def delete(index):
  print("Not Implemented yet")
  return redirect("/")


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
