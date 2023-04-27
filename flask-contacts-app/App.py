from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)


# MySQL connection
app.config['MYSQL_HOST'] = '3.86.242.195'
app.config['MYSQL_USER'] = 'support'
app.config['MYSQL_PASSWORD'] = 'cub'
app.config['MYSQL_DB'] = 'socrud'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM miembros')
    data = cur.fetchall()
    return render_template('index.html', miembros=data)




@app.route('/add_member', methods=['POST'])
def add_member():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha = request.form['fecha']
        origen = request.form['origen']
        aeropuerto = request.form['aeropuerto']
        destino = request.form['destino']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO miembros (nombre, apellido, fecha, origen, aeropuerto, destino, precio) VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (nombre, apellido, fecha, origen, aeropuerto, destino, precio))
        mysql.connection.commit()
        flash('Miembro agregado correctamente')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_member(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM miembros WHERE id = %s', (int(id),))
    data = cur.fetchall()
    if not data: # si la lista esta vacia, mostrar error
        return "No se encontró miembro con ese ID"
    return render_template('edit-miembro.html', miembro=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_member(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha = request.form['fecha']
        origen = request.form['origen']
        aeropuerto = request.form['aeropuerto']
        destino = request.form['destino']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE miembros
        SET nombre = %s,
            apellido = %s,
            fecha = %s,
            origen = %s,
            aeropuerto = %s,
            destino = %s,
            precio = %s
        WHERE id = %s
        """, (nombre, apellido, fecha, origen, aeropuerto, destino, precio, id))
        mysql.connection.commit()
        flash('Miembro actualizado correctamente')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_member(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM miembros WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Miembro eliminado correctamente')
    return redirect(url_for('Index'))


@app.route('/integrantes')
def integrantes():
    return render_template('integrantes.html')




if __name__ == '__main__':
    app.run(port=5000, debug=True)
