from flask import Flask, escape, request,render_template,redirect,g


app = Flask(__name__)


#Hacer vectores y matrices
import numpy as np
import math


#-----------------------------
x = []
y = []
metodo = 24
rta = []

#Variables para los metodos
sumXY = 0.0
sumX2 = 0.0
sumX3 = 0.0
sumX4 = 0.0
sumatoriaX = 0.0
sumatoriaY = 0.0
sumX2Y = 0.0
promY = 0.0
st = 0.0
sr = 0.0


@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/tomarPuntos')
def tomarPuntos():
    return render_template('tomarPuntos.html')

@app.route('/instrucciones')
def instrucciones():
    return render_template('instrucciones.html')

    
@app.route('/graficaResultado',methods=['GET','POST'])
def graficaResultado():
    global x
    global y
    global metodo
    global rta
    if request.method == 'POST':
        #Agregar puntos y el metodo a resolver
        x = request.form.getlist('puntosX[]')
        y = request.form.getlist('puntosY[]')
        metodo = request.form['metodo']
        print("Puntos X", x)
        print("Puntos y", y)
        print("Metodo pedido",int(metodo))
        if(int(metodo) == 5):
            rta = regresionLinealGradoDos()
        
        return '200'
    
    return render_template('graficayresultado.html',x=x,y=y,metodo=metodo,rtas = rta)






# Metodos:

def metodo1():
    a = np.array([[2.0,4.3,6],[4,5,6],[3,1,-2]])
    b = np.array([18,24,4])
    rtas = np.linalg.solve(a,b)
    print(rtas[0])
    print(rtas[1])
    print(rtas[2])
    return 200

def metodo2():
    global x
    xe = x
    print("X vale = ",xe)
    return 200

def metodo3():
    return 45364


def regresionLinealGradoDos():
    global x
    global y
    global sumXY
    global sumX2 
    global sumX3
    global sumX4
    global sumatoriaX
    global sumatoriaY
    global sumX2Y
    global promY
    global st
    global sr

    for i in range(len(x)):
        sumXY += float(x[i])*float(y[i])
        sumX2 += pow(float(x[i]),2)
        sumX3 += pow(float(x[i]),3)
        sumX4 += pow(float(x[i]),4)
        sumatoriaX += float(x[i])
        sumatoriaY += float(y[i])
        sumX2Y += pow(float(x[i]),2)*float(y[i])

    a = np.array([[len(x),sumatoriaX,sumX2],[sumatoriaX,sumX2,sumX3],[sumX2,sumX3,sumX4]])
    b = np.array([sumatoriaY,sumXY,sumX2Y])
    print("Matriz a:")
    print(a)
    print("Array b:")
    print(b)
    gauss = np.linalg.solve(a,b)
    print("a0",gauss[0])
    print("a1",gauss[1])
    print("a2",gauss[2])

    promY = sumatoriaY/(len(y))

    for i in range(len(x)):
        st += pow(float(y[i])-promY,2)
        sr += pow(float(y[i])-gauss[0]-(gauss[1]*float(x[i]))-pow(float(x[i]),2)*gauss[2],2)

    sy =  math.sqrt(st/(len(x)-1))
    syx = math.sqrt(sr/(len(x)-3))
    r = math.sqrt((st-sr)/st)*100

    rta.append(gauss[0])
    rta.append(gauss[1])
    rta.append(gauss[2])
    rta.append(sy)
    rta.append(syx)
    rta.append(r)

    print("Rta = ",rta)

    return rta
        














#Redirect:
@app.route("/irInicio",methods=['GET','POST'])
def irInicio():
    if request.method == 'POST':
        return redirect("/")

@app.route("/irTomarPuntos",methods=['GET','POST'])
def irTomarPuntos():
    if request.method == 'POST':
        return redirect("/tomarPuntos")

@app.route("/irgraficaResultado",methods=['GET','POST'])
def irgraficaResultado():
    if request.method == 'POST':
        return redirect("/graficaResultado")

@app.route("/irInstrucciones",methods=['GET','POST'])
def irInstrucciones():
    if request.method == 'POST':
        return redirect("/instrucciones")





if __name__=="__main__":
    app.run(debug=True)