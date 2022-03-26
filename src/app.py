from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

from config import config
from validaciones import *

app = Flask(__name__)


conexion = MySQL(app)


# @cross_origin
@app.route('/bom', methods=['GET'])
def listar_cursos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, network_layer, vendor, template, vendor_part, item_master, sap_number, description, comment, count, price FROM bom order by id asc"
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursos = []
        for fila in datos:
            curso = {
                    'id': fila[0],
                    'network_layer': fila[1],
                    'vendor': fila[2],
                    'template': fila[3],
                    'vendor_part': fila[4],
                    'item_master': fila[5],
                    'sap_number': fila[6],
                    'description': fila[7],
                    'comment': fila[8],
                    'count': fila[9],
                    'price': fila[10]
                    }
            cursos.append(curso)
        return jsonify({'BOM': cursos, 'mensaje': "Cursos listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/bom/<template>', methods=['GET'])
def leer_curso(template):
    #print(template)
    try:
        #cursos = leer_curso_bd(template)
        
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM bom WHERE template = '{0}'".format(template)
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursos = []
        if datos != None:
            
            for fila in datos:
                i=+1
                curso = {
                        'id': fila[0],
                        'network_layer': fila[1],
                        'vendor': fila[2],
                        'template': fila[3],
                        'vendor_part': fila[4],
                        'item_master': fila[5],
                        'sap_number': fila[6],
                        'description': fila[7],
                        'comment': fila[8],
                        'count': fila[9],
                        'price': fila[10]
                        }
                cursos.append(curso)
        
        if cursos != None:
            return jsonify({'BOM': cursos, 'mensaje': " Se encontraron los componentes", 'exito': True})
        else:
            return jsonify({'mensaje': "Curso no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})



def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
