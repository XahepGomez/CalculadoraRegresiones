from flask import Flask, escape, request,render_template,redirect,g


app = Flask(__name__)


#Manejar los vectores y matrices
import numpy as np
import math

#-----------------------------
x = []
y = []
metodo = 24
rta = []

#Variables globales para los metodos
sumXY = 0.0
sumX2 = 0.0
sumX3 = 0.0
sumX4 = 0.0
sumX5 = 0.0
sumX6 = 0.0
sumatoriaX = 0.0
sumatoriaY = 0.0
sumX2Y = 0.0
sumX3Y = 0.0
promY = 0.0
promX = 0.0
st = 0.0
sr = 0.0
alpha = 0.0
beta = 0.0
sy = 0.0
syx = 0.0
r = 0.0

# Rende_templates, y recibir datos por el metodo post
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

        if(int(metodo) == 1):
            rta = RegresionLineal(x,y)
        elif(int(metodo) == 2):
            rta = TransformacionesLogaritmicas()
        elif(int(metodo) == 3):
            rta = EcuacionesDePotencias()
        elif(int(metodo) == 4):
            rta = RazonDeCrecimiento()
        elif(int(metodo) == 5):
            rta = RegresionLinealGradoDos()
        elif(int(metodo) == 6):
            rta = RegresionLinealGradoTres()
            print("Rta",rta)
        
        return '200'
    
    return render_template('graficayresultado.html',x=x,y=y,metodo=metodo,rtas = rta)











# Metodos:

def metodo1():
    a = np.array([[4,1,0],[1,4,1],[0,1,4]])
    b = np.array([-12,24,60])
    rtas = np.linalg.solve(a,b)
    print(rtas[0])
    print(rtas[1])
    print(rtas[2])
    return 200

#------------------- Método 1 -------------------
def RegresionLineal(puntoX,puntoY):
    global sumatoriaX
    global sumatoriaY
    global sumXY
    global sumX2
    global promY
    global promX
    global st
    global sr
    global sy
    global syx
    global r

    for i in range(len(puntoX)):
        sumatoriaX += float(puntoX[i])
        sumatoriaY += float(puntoY[i])
        sumXY += float(puntoX[i])*float(puntoY[i])
        sumX2 += pow(float(puntoX[i]),2) 

    promY = sumatoriaY/len(puntoX)
    promX = sumatoriaX/len(puntoX)

    a1 = ((len(puntoX)*sumXY)-(sumatoriaX*sumatoriaY))/(len(puntoX)* sumX2-(pow(sumatoriaX,2)))
    a0 = promY-(a1*promX)

    rta.append(a0)
    rta.append(a1)

    for i in range(len(puntoX)):
        st = (float(puntoY[i])-promY)*(float(puntoY[i])-promY)
        sr = pow(float(puntoY[i])-a0-(a1*float(puntoX[i])),2)

    sy = math.sqrt(st/(len(puntoX)-1))
    syx = math.sqrt(sr/(len(puntoX)-2))
    r = math.sqrt((st-sr)/st)*100

    rta.append(sy)
    rta.append(syx)
    rta.append(r)

    print("Rtas:",rta)

    return rta

#------------------- Método 2 -------------------
def TransformacionesLogaritmicas():

    global x
    global y

    logy=[]
    for i in range(len(x)):
        logy.append(math.log(float(y[i])))

    rta= RegresionLineal(x,logy)
    alpha=pow(math.e,float(rta[0]))
    beta=float(rta[1])

    rta.append(alpha)
    rta.append(beta)
    print("Rtas",rta)
    return rta

#------------------- Método 3 -------------------
def EcuacionesDePotencias():
    global x
    global y

    logy=[]
    logx=[]

    for i in range(len(x)):
        logy.append(math.log10(float(y[i])))
        logx.append(math.log10(float(x[i])))
   
    rta= RegresionLineal(logx,logy)

    alpha=math.pow(10,(rta[0]))
    beta=rta[1]

    rta.append(alpha)
    rta.append(beta)
    print("Rtas",rta)
    return rta

#------------------- Método 4 -------------------
def RazonDeCrecimiento():
    global x
    global y

    sobrex = []
    sobrey = []
    for i in range(len(x)):
        sobrex.append(1/float(x[i]))
        sobrey.append(1/float(y[i]))
    
    rta = RegresionLineal(sobrex,sobrey)

    alpha = 1/float(rta[0])
    beta = float(rta[1])/float(rta[0]) 
    rta.append(alpha)
    rta.append(beta)
    print("Rtas = ",rta)
    return rta

#------------------- Método 5 -------------------
def RegresionLinealGradoDos():
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
    
    print("Error ",math.fabs(len(x)-3))
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

#------------------- Método 6-------------------
def RegresionLinealGradoTres():
    print("Ejecutando el método")
    global x
    global y
    global sumXY
    global sumX2 
    global sumX3
    global sumX4
    global sumX5
    global sumX6
    global sumatoriaX
    global sumatoriaY
    global sumX2Y
    global sumX3Y
    global promY
    global st
    global sr
    global sy
    global syx
    global r
    
    for i in range(len(x)):
        
        sumXY += float(x[i])*float(y[i])
        sumX2 += pow(float(x[i]),2)
        sumX3 += pow(float(x[i]),3)
        sumX4 += pow(float(x[i]),4)
        sumX5 += pow(float(x[i]),5)
        sumX6 += pow(float(x[i]),6)
        sumatoriaX += float(x[i])
        sumatoriaY += float(y[i])
        sumX2Y += pow(float(x[i]),2)*float(y[i])
        sumX3Y += pow(float(x[i]),3)*float(y[i])

    a = np.array([[len(x),sumatoriaX,sumX2,sumX3],[sumatoriaX,sumX2,sumX3, sumX4],[sumX2,sumX3,sumX4,sumX5],[sumX3,sumX4,sumX5,sumX6]])
    b = np.array([sumatoriaY,sumXY,sumX2Y,sumX3Y])
    print("Matriz a:")
    print(a)
    print("Array b:")
    print(b)
    gauss = np.linalg.solve(a,b)
    print("a0",gauss[0])
    print("a1",gauss[1])
    print("a2",gauss[2])
    print("a3",gauss[3])

    promY = sumatoriaY/(len(y))

    for i in range(len(x)):
        st += pow(float(y[i])-promY,2)
        sr += pow(float(y[i])-gauss[0]-(gauss[1]*float(x[i]))-pow(float(x[i]),2)*gauss[2]-pow(float(x[i]),3)*gauss[3],2)

    sy =  math.sqrt(st/(len(x)-1))
    syx = math.sqrt(sr/(len(x)-3))
    r = math.sqrt((st-sr)/st)*100

    rta.append(gauss[0])
    rta.append(gauss[1])
    rta.append(gauss[2])
    rta.append(gauss[3])
    rta.append(sy)
    rta.append(syx)
    rta.append(r)

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