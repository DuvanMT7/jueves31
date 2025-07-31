from flask import Flask, jsonify, request 
from flask_cors import CORS
import mysql.connector


app = Flask(__name__)  
CORS(app)

listaProyectos = []

resultadosPersona = []

db = mysql.connector.connect(
    host="localhost",
    user="root",           
    password="12345678duvanm",     
    database="sabadojulio" 
)
cursor = db.cursor(dictionary=True)
 

@app.route('/mensaje', methods=['GET'])
def mensaje():
    return 'Primera aplicacion Web'

@app.route('/listarProyectos', methods=['GET'])
def listar_proyectos():
    return jsonify(listaProyectos)

@app.route('/datosDeLaBase', methods=['GET'])
def datosBase():
     cursor.execute("SELECT * FROM persona")
     resultadosPersona = cursor.fetchall()
     return jsonify(resultadosPersona)

@app.route('/agregarPersonaBD', methods=['POST'])
def agregar():
    nuevaPersona = request.json.get('persona')
    resultadosPersona.append(nuevaPersona)
    cursor.execute("INSERT INTO persona (identificacion, nombre, edad) VALUES (%s, %s, %s)", 
            (nuevaPersona['identificacion'],nuevaPersona['nombre'], nuevaPersona['edad']))
    db.commit()
    return 'Se agrego una nueva persona'

@app.route('/buscarPersona/<identificacion>', methods=['GET'])
def buscar(identificacion):
    cursor.execute("SELECT * FROM persona where identificacion = %s",(identificacion,)) 
    resultadosPersona = cursor.fetchall()
    return jsonify(resultadosPersona)

@app.route('/actualizarPersona/<identificacion>', methods=['PUT'])
def actualizar(identificacion):
    datos_nuevos = request.json
    cursor.execute("UPDATE persona SET nombre=%s,edad=%s WHERE identificacion=%s",
    (datos_nuevos['nombre'], datos_nuevos['edad'], datos_nuevos['identificacion']))
    db.commit()
    return "Persona Actualizada"

@app.route('/eliminarPersona/<identificacion>', methods=['DELETE'])
def eliminar(identificacion):
    cursor.execute("DELETE FROM persona WHERE identificacion=%s", (identificacion,))
    db.commit()
    return "Persona Eliminada"
  
if __name__ == '__main__':
    app.run(debug=True) 

  

    