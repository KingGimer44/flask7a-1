from flask import Flask

from flask import render_template
from flask import request

import pusher

import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
  host="185.232.14.52",
  database="u760464709_tst_sep",
  user="u760464709_tst_sep_usr",
  password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    con.close()
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    con.close()
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    con.close()
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula: {matricula} Nombre y Apellido: {nombreapellido}"
def notificarActualizacionReserva():
    pusher_client = pusher.Pusher(
        app_id="1714541",
        key="cda1cc599395d699a2af",
        secret="9e9c00fc36600060d9e2",
        cluster="us2",
        ssl=True
    )

    pusher_client.trigger("canalRegistrosTemperaturaHumedad", "registroTemperaturaHumedad", {})

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT * FROM sensor_log")
    con.close()
    
    registros = cursor.fetchall()

    return registros

# @app.route("/evento", methods=["GET"])
# def evento():
#     if not con.is_connected():
#         con.reconnect()

#     cursor = con.cursor()

#     args = request.args
  
#     sql = "INSERT INTO sensor_log (Temperatura, Humedad, Fecha_Hora) VALUES (%s, %s, %s)"
#     val = (args["temperatura"], args["humedad"], datetime.datetime.now())
#     cursor.execute(sql, val)
    
#     con.commit()
#     con.close()

#     pusher_client = pusher.Pusher(
#         app_id="1714541",
#         key="cda1cc599395d699a2af",
#         secret="9e9c00fc36600060d9e2",
#         cluster="us2",
#         ssl=True
#     )
    
#     pusher_client.trigger("conexion", "evento", request.args)

@app.route("/guardar", methods=["POST"])
def guardar():
    if not con.is_connected():
        con.reconnect()

    id          = request.form["id"]
    temperatura = request.form["temperatura"]
    humedad     = request.form["humedad"]
    fechahora   = datetime.datetime.now(pytz.timezone("America/Matamoros"))
    
    cursor = con.cursor()

    if id:
        sql = """
        UPDATE tst0_resevas SET
        Nombre_Apellido = %s,
        Telefono     = %s
        WHERE Id_Reserva = %s
        """
        val = (nombre_apellido, telefono, id)
    else:
        sql = """INSERT INTO tst0_resevas (Nombre_Apellido, Telefono, Fecha_Hora)
                                 VALUES (%s,          %s,      %s)"""
        val =                           (nombre_apellido, telefono, fechahora)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    notificarActualizacionReserva()

    return make_response(jsonify({}))
  
@app.route("/editar", methods=["GET"])
def editar():
    if not con.is_connected():
        con.reconnect()

    id = request.args["id"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Reserva, Nombre_Apellido, Telefono FROM tst0_resevas
    WHERE Id_Reserva = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/eliminar", methods=["POST"])
def eliminar():
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    DELETE FROM tst0_resevas
    WHERE Id_Reserva = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    notificarActualizacionTemperaturaHumedad()

    return make_response(jsonify({}))
