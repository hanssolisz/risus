from flask import Flask, flash
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os



from flask import Markup

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'pagosdb'
mysql.init_app(app)


@app.route('/')
def index():
    _date = datetime.now()
    _year = _date.year
    _strYear = str(_year)
    _mes = _date.month
    print(_mes)
    _strMes = _mes

    if (_mes == 1):
        _strMes="01"
    if (_mes == 2):
        _strMes="02"
    if (_mes == 3):
        _strMes="03"
    if (_mes == 4):
        _strMes="04"
    if (_mes == 5):
        _strMes="05"
    if (_mes == 6):
        _strMes="06"
    if (_mes == 7):
        _strMes="07"
    if (_mes == 8):
        _strMes="08"
    if (_mes == 9):
        _strMes="09"



    conn = mysql.connect()
    cursor = conn.cursor()

    conn2 = mysql.connect()
    cursor2 = conn2.cursor()

    conn3 = mysql.connect()
    cursor3 = conn3.cursor()

    conn4 = mysql.connect()
    cursor4 = conn4.cursor()

    try:

        cursor.execute(
            "SELECT SUM(monto) as total, DATE_FORMAT(fecha, '%m')*1 as mes, DATE_FORMAT(fecha, '%Y') as year from pagos WHERE DATE_FORMAT(fecha, '%Y')=" + _strYear + " group by DATE_FORMAT(fecha, '%Y-%m')")
        rows = cursor.fetchall()
        dataitems = list()
        fld = {}
        i = 0
        ##################################
        for row in rows:
            fld["total"] = str(row[0])
            print(int(row[1]))

            if (int(row[1]) == 1):
                _mes = "Enero"
            if (int(row[1]) == 2):
                _mes = "Febrero"
            if (int(row[1]) == 3):
                _mes = "Marzo"
            if (int(row[1]) == 4):
                _mes = "Abril"
            if (int(row[1]) == 5):
                _mes = "Mayo"
            if (int(row[1]) == 6):
                _mes = "Junio"
            if (int(row[1]) == 7):
                _mes = "Julio"
            if (int(row[1]) == 8):
                _mes = "Agosto"
            if (int(row[1]) == 9):
                _mes = "Septiembre"
            if (int(row[1]) == 10):
                _mes = "Octubre"
            if (int(row[1]) == 11):
                _mes = "Noviembre"
            if (int(row[1]) == 12):
                _mes = "Diciembre"

            fld['mes'] = _mes
            fld['year'] = str(row[2])

            dataitems.append(fld.copy())
            ##################################
        print(dataitems)
        cursor.close()
        conn.close()
        # original json object
        # dataitems = [{"month": 'Jan', "temperature": 20, "color":'##3498db'},{"month": 'Feb', "temperature": 15, "color":'#e74c3c'}]
        # return render_template('chart3.html', dataitems=dataitems)
    except:
        print("Error: unable to fetch items")

    try:
        cursor2.execute("select SUM(monto) as total, apellidos as apellidos, especialista.pago_dental as dental, especialista.pago_estetica as estetica FROM pagos INNER JOIN especialista ON pagos.rut_especialista = especialista.rut WHERE DATE_FORMAT(fecha, '%Y-%m')='" + _strYear + "-" + _strMes + "' GROUP BY rut_especialista")
        rows2 = cursor2.fetchall()
        dataitems2 = list()
        fld2 = {}
        i = 0
        ##################################
        for row2 in rows2:
            fld2["total"] = str(row2[0])
            fld2['apellidos'] = str(row2[1])
            fld2['dental'] = int(row2[2])*row2[0]/100
            fld2['estetica'] = int(row2[3])*row2[0]/100


            dataitems2.append(fld2.copy())
            ##################################
        print(dataitems2)
        cursor2.close()
        conn2.close()

    except:
        print("Error: unable to fetch items")

    try:
        cursor3.execute("select SUM(monto) as total, cobertura as cobertura FROM pagos WHERE DATE_FORMAT(fecha, '%Y-%m')='" + _strYear + "-" + _strMes + "' GROUP BY cobertura")
        rows3 = cursor3.fetchall()
        dataitems3 = list()
        fld3 = {}
        i = 0
        ##################################
        for row3 in rows3:
            fld3["total"] = str(row3[0])
            fld3['cobertura'] = str(row3[1])

            dataitems3.append(fld3.copy())
            ##################################
        print(dataitems3)
        cursor3.close()
        conn3.close()

    except:
        print("Error: unable to fetch items")

    try:
            cursor4.execute(
                "select SUM(monto) as total, tipo as tipo FROM pagos WHERE DATE_FORMAT(fecha, '%Y-%m')='" + _strYear + "-" + _strMes + "' GROUP BY tipo")
            rows4 = cursor4.fetchall()
            dataitems4 = list()
            fld4 = {}
            i = 0
            ##################################
            for row4 in rows4:
                fld4["total"] = str(row4[0])
                fld4['tipo'] = str(row4[1])

                dataitems4.append(fld4.copy())
                ##################################
            print(dataitems4)
            cursor4.close()
            conn4.close()

    except:
            print("Error: unable to fetch items")


    return render_template('boletas/charts.html', dataitems=dataitems, _year=_year, dataitems2=dataitems2, dataitems3=dataitems3, dataitems4=dataitems4)


def nuevoPresupuesto():
    sql = "SELECT * FROM `especialista`"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    especialistas = cursor.fetchall()
    conn.commit()
    return render_template('boletas/nuevoPresupuesto.html', especialistas=especialistas)


@app.route('/actualizarPrestadores/', methods=['POST'])
def actualizarPrestadores():
    _rut = request.form['runespecialista']
    _nombres = request.form['nombres']
    _apellidos = request.form['apellidos']
    _especialidad = request.form['especialidad']
    _pago_dental = request.form['dental']
    _pago_estetica = request.form['estetica']
    _orden = request.form['orden']

    sql31 = "UPDATE `especialista` SET `rut`=%s, `nombres`=%s,`apellidos`=%s,`especialidad`=%s,`pago_dental`=%s,`pago_estetica`=%s WHERE id=%s"
    datosPrestadores = (_rut, _nombres, _apellidos, _especialidad, _pago_dental, _pago_estetica, _orden)
    conn31 = mysql.connect()
    cursor31 = conn31.cursor()
    cursor31.execute(sql31, datosPrestadores)
    conn31.commit()
    success_message = '¡Prestador/a modificado/a exitosamente!'
    flash(success_message)

    return redirect('/prestadores')


@app.route('/eliminarPrestadores/<int:id>')
def eliminarPrestador(id):
    conn5 = mysql.connect()
    cursor5 = conn5.cursor()
    cursor5.execute("DELETE FROM `especialista` WHERE id=%s", (id))
    conn5.commit()
    success_message = '¡Prestador/a eliminado/a exitosamente!'
    flash(success_message)
    return redirect('/prestadores')


@app.route('/nuevoPrestadores', methods=['POST'])
def nuevoPrestadores():
    _run = request.form['runespecialista']
    _nombres = request.form['nombres']
    _apellidos = request.form['apellidos']
    _especialidad = request.form['especialidad']
    _dental = request.form['dental']
    _estetica = request.form['estetica']

    sql3 = "INSERT INTO `especialista` (`rut`, `nombres`, `apellidos`, `especialidad`, `pago_dental`, `pago_estetica`, `id`) VALUES (%s, %s, %s, %s, %s, %s, NULL);"
    datosBoleta = (_run, _nombres, _apellidos, _especialidad, _dental, _estetica)
    conn3 = mysql.connect()
    cursor3 = conn3.cursor()
    cursor3.execute(sql3, datosBoleta)
    conn3.commit()

    success_message = '¡Prestador/a registrado/a exitosamente!'
    flash(success_message)

    return redirect('/prestadores')


@app.route('/prestadores')
def prestadores():
    sql = "SELECT * FROM `especialista`"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    especialistas = cursor.fetchall()
    conn.commit()

    return render_template('boletas/prestadores.html', especialistas=especialistas)


@app.route('/editarPrestadores/<int:id>')
def editarPrestadores(id):
    sql = "SELECT * FROM `especialista`"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    especialistas = cursor.fetchall()
    conn.commit()

    conn6 = mysql.connect()
    cursor6 = conn6.cursor()
    cursor6.execute(
        "SELECT rut, nombres, apellidos, especialidad, pago_dental, pago_estetica, id FROM especialista WHERE id=%s",
        (id))
    especialistasedit = cursor6.fetchall()
    conn6.commit()

    return render_template('/boletas/editarPrestadores.html', especialistasedit=especialistasedit,
                           especialistas=especialistas)


@app.route('/nuevaBoleta')
def nuevaBoleta():
    sql = "SELECT * FROM `especialista`"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    especialistas = cursor.fetchall()
    conn.commit()

    sql2 = "SELECT * FROM `pagos` ORDER by orden DESC limit 12"
    conn2 = mysql.connect()
    cursor2 = conn2.cursor()
    cursor2.execute(sql2)
    pagos = cursor2.fetchall()
    conn2.commit()

    return render_template('boletas/nuevaBoleta.html', especialistas=especialistas, pagos=pagos)


@app.route('/guardarBoleta', methods=['POST'])
def guardarBoleta():
    _boleta = request.form['boleta']
    _fecha = request.form['fecha']
    _especialista = request.form['especialista']
    _paciente = request.form['cliente']
    _tipo = request.form['tipo']
    _metodo = request.form['metodo']
    _monto = request.form['monto']
    _nombre_paciente = request.form['nombre_paciente']
    _cobertura = request.form['cobertura']
    _concepto = request.form['concepto']

    sql3 = "INSERT INTO `pagos` (`boleta`, `rut_paciente`, `rut_especialista`, `tipo`, `monto`, `fecha`, `metodo_pago`, `nombre_paciente`, `cobertura`, `concepto`, `orden`) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s, NULL);"
    datosBoleta = (
    _boleta, _paciente, _especialista, _tipo, _monto, _fecha, _metodo, _nombre_paciente, _cobertura, _concepto)
    conn3 = mysql.connect()
    cursor3 = conn3.cursor()
    cursor3.execute(sql3, datosBoleta)
    conn3.commit()

    sql0 = "SELECT * FROM `especialista`"
    conn0 = mysql.connect()
    cursor0 = conn0.cursor()
    cursor0.execute(sql0)
    especialistas = cursor0.fetchall()
    conn0.commit()

    sql20 = "SELECT * FROM `pagos` ORDER by orden DESC limit 12"
    conn20 = mysql.connect()
    cursor20 = conn20.cursor()
    cursor20.execute(sql20)
    pagos = cursor20.fetchall()
    conn20.commit()
    success_message = '¡Boleta registrada exitosamente!'
    flash(success_message)

    return render_template('boletas/nuevaBoleta.html', especialistas=especialistas, pagos=pagos)


@app.route('/registroBoletas')
def registroBoletas():
    sql = "SELECT * FROM `especialista`"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    especialistas = cursor.fetchall()
    conn.commit()

    sql4 = "SELECT boleta, rut_paciente, rut_especialista, monto, fecha, metodo_pago, orden, apellidos, tipo, nombre_paciente, concepto, cobertura FROM pagos INNER JOIN especialista ON pagos.rut_especialista = especialista.rut ORDER BY pagos.boleta DESC limit 500"
    conn4 = mysql.connect()
    cursor4 = conn4.cursor()
    cursor4.execute(sql4)
    pagos = cursor4.fetchall()
    conn4.commit()

    return render_template('boletas/registroBoletas.html', pagos=pagos, especialistas=especialistas)


@app.route('/editarBoleta/<int:orden>')
def editarBoleta(orden):
    sql06 = "SELECT * FROM `especialista`"
    conn06 = mysql.connect()
    cursor06 = conn06.cursor()
    cursor06.execute(sql06)
    especialistas = cursor06.fetchall()
    print(especialistas)
    conn06.commit()

    conn6 = mysql.connect()
    cursor6 = conn6.cursor()
    cursor6.execute(
        "SELECT boleta, rut_paciente, rut_especialista, monto, fecha, metodo_pago, orden, nombres, apellidos, especialidad, nombre_paciente, cobertura, concepto FROM pagos INNER JOIN especialista ON pagos.rut_especialista = especialista.rut WHERE pagos.orden=%s ORDER BY pagos.boleta DESC",
        (orden))
    consultaedit = cursor6.fetchall()
    print(consultaedit)
    conn6.commit()
    return render_template('/boletas/editarBoleta.html', consultaedit=consultaedit, especialistas=especialistas)


@app.route('/eliminarBoleta/<int:orden>')
def eliminarBoleta(orden):
    conn5 = mysql.connect()
    cursor5 = conn5.cursor()
    cursor5.execute("DELETE FROM `pagos` WHERE orden=%s", (orden))
    conn5.commit()
    success_message = '¡Registro eliminado exitosamente!'
    flash(success_message)
    return redirect('/registroBoletas')


@app.route('/actualizarBoleta/', methods=['POST'])
def actualizarBoleta():
    _boleta = request.form['boleta']
    _fecha = request.form['fecha']
    _especialista = request.form['especialista']
    _paciente = request.form['cliente']
    _tipo = request.form['tipo']
    _metodo = request.form['metodo']
    _monto = request.form['monto']
    _orden = request.form['orden']
    _nombre_paciente = request.form['nombre_paciente']
    _cobertura = request.form['cobertura']
    _concepto = request.form['concepto']

    sql31 = "UPDATE `pagos` SET `boleta`=%s,`rut_paciente`=%s,`rut_especialista`=%s,`tipo`=%s,`monto`=%s,`fecha`=%s,`metodo_pago`=%s,`nombre_paciente`=%s,`cobertura`=%s,`concepto`=%s WHERE orden=%s"
    datosBoleta1 = (
    _boleta, _paciente, _especialista, _tipo, _monto, _fecha, _metodo, _nombre_paciente, _cobertura, _concepto, _orden)
    conn31 = mysql.connect()
    cursor31 = conn31.cursor()
    cursor31.execute(sql31, datosBoleta1)
    conn31.commit()
    success_message = '¡Registro modificado exitosamente!'
    flash(success_message)

    return redirect('/registroBoletas')


@app.route('/nuevoPresupuesto')
def nuevoPresupuesto():
    sql7 = "SELECT * FROM `especialista`"
    conn7 = mysql.connect()
    cursor7 = conn7.cursor()
    cursor7.execute(sql7)
    especialistas7 = cursor7.fetchall()
    conn7.commit()

    return render_template('boletas/nuevoPresupuesto.html', especialistas=especialistas7)


@app.route('/buscarPorRut/', methods=['GET', 'POST'])
def buscarPorRut():
    _clienteBuscar = request.form['cliente']
    print(_clienteBuscar)
    sql32 = "SELECT * FROM `pagos` WHERE `rut_paciente`=%s"
    datosBuscar = (_clienteBuscar)
    conn32 = mysql.connect()
    cursor32 = conn32.cursor()
    cursor32.execute(sql32, datosBuscar)
    consultaBuscarRut = cursor32.fetchall()
    print(consultaBuscarRut)
    conn32.commit()

    return render_template('/boletas/registroBoletas.html', pagos=consultaBuscarRut)


if __name__ == '__main__':
    app.secret_key = "super secret key"
    app.run(debug=True)
