from flask import Flask, render_template,request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

#Rutas de la Aplicación 
@app.route('/')
def home():
    cursor=db.database.cursor()
    cursor.execute("SELECT * FROM Docentes")
    myresult = cursor.fetchall()
    #Convertir datos a diccionario para tener la clave de c/u
    insertObject = []
    columNames = [column[0] for column in cursor.description]
    for record in myresult:
         insertObject.append(dict(zip(columNames,record)))
    cursor.close()
    return render_template('index.html' , data=insertObject)

#Ruta para guardar datos en la BD
@app.route('/Docentes', methods=['POST'])
def addDocente():
    nombreDocente = request.form['nombreDocente']
    apellidoDocente = request.form['apellidoDocente']
    telefonoDocente = request.form['telefonoDocente']
    facultadDocente = request.form['facultadDocente']
    materiaDocente = request.form['materiaDocente']
    
    if nombreDocente and apellidoDocente and telefonoDocente and facultadDocente and materiaDocente:
        cursor = db.database.cursor()
        sql= "INSERT INTO Docentes (nombreDocente,apellidoDocente,telefonoDocente,facultadDocente,materiaDocente) VALUES (%s,%s,%s,%s,%s)" 
        data = (nombreDocente,apellidoDocente,telefonoDocente,facultadDocente,materiaDocente)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('home'))       

@app.route('/delete/<string:idDocente>') 
def deleteDocente(idDocente):
    cursor = db.database.cursor()
    sql = "DELETE FROM Docentes WHERE idDocente= %s"
    data = (idDocente,)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('home')) 

@app.route('/edit/<string:idDocente>', methods=['POST'])
def editDocente(idDocente):
    
    nombreDocente = request.form['nombreDocente']
    apellidoDocente = request.form['apellidoDocente']
    telefonoDocente = request.form['telefonoDocente']
    facultadDocente = request.form['facultadDocente']
    materiaDocente = request.form['materiaDocente']
    
    if nombreDocente and apellidoDocente and telefonoDocente and facultadDocente and materiaDocente:
        cursor = db.database.cursor()
        sql = "UPDATE Docentes SET nombreDocente = %s , apellidoDocente = %s, telefonoDocente = %s, facultadDocente = %s, materiaDocente = %s WHERE idDocente = %s"
        data = (nombreDocente,apellidoDocente,telefonoDocente,facultadDocente,materiaDocente,idDocente)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)