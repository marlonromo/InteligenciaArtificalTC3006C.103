# -*- coding: utf-8 -*-
"""Modulo2UsoFramework.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JL6M69-zbkXltZ_XTq1pbY2KoYMrUWwX

## Create Dataset

Creamos un Dataset en base al DataSet obtenido de Kaggle "Student Study Hours",
donde el archivo .csv es "score_updated.csv", dentro de este Dataset podemos
observar la calificacion del estudiante en base a las horas estudiadas.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import pandas as pd
# Importemos nuestro google drive
from google.colab import drive

drive.mount("/content/gdrive")
!pwd # Print working directory

# Commented out IPython magic to ensure Python compatibility.
# Buscamos el el path donde esta nuestro csv
# %cd "/content/gdrive/MyDrive/"
!ls # List files located in defined folder

# Cargar el conjunto de datos desde score_updated.csv
data = pd.read_csv('score_updated.csv')
X = data['Hours'].values
y = data['Scores'].values

"""# CREAMOS LAS FUNCIONES PARA ENTRENAR Y PREDECIR"""

def update_w_and_b(X, y, w, b, alpha):
  '''Update parameters w and b during 1 epoch'''
  dl_dw = 0.0
  dl_db = 0.0
  N = len(X)
  for i in range(N):
    dl_dw += -2*X[i]*(y[i] - (w*X[i] + b))
    dl_db += -2*(y[i] - (w*X[i] + b))
  # update w and b
  w = w - (1/float(N))*dl_dw*alpha
  b = b - (1/float(N))*dl_db*alpha
  return w, b

def train(X, y, w, b, alpha, epochs):
  '''Loops over multiple epochs and prints progress'''
  print('Training progress:')
  for e in range(epochs):
    w, b = update_w_and_b(X, y, w, b, alpha)
  # log the progress
    if e % 400 == 0:
      avg_loss_ = avg_loss(X, y, w, b)
      # print("epoch: {} | loss: {}".format(e, avg_loss_))
      print("Epoch {} | Loss: {} | w:{}, b:{}".format(e, avg_loss_, round(w, 4), round(b, 4)))
  return w, b

def train_and_plot(X, y, w, b, alpha, epochs, x_max_plot):
  '''Loops over multiple epochs and plot graphs showing progress'''
  for e in range(epochs):
    w, b = update_w_and_b(X, y, w, b, alpha)
  # plot visuals for last epoch
    if e == epochs-1:
      avg_loss_ = avg_loss(X, y, w, b)
      x_list = np.array(range(0,x_max_plot)) # Set x range
      y_list = (x_list * w) + b # Set function for the model based on w & b
      plt.scatter(x=X, y=y)
      plt.plot(y_list, c='r')
      plt.title("Epoch {} | Loss: {} | w:{}, b:{}".format(e, round(avg_loss_,2), round(w, 4), round(b, 4)))
      plt.show()
  return w, b

def avg_loss(X, y, w, b):
  '''Calculates the MSE'''
  N = len(X)
  total_error = 0.0
  for i in range(N):
    total_error += (y[i] - (w*X[i] + b))**2
  return total_error / float(N)

def predict(x, w, b):
  return w*x + b

"""## ENTRENAMOS EL MODELO Y VISUALIZAMOS LOS DATOS."""

# Define initial w and b, learning rate alpha and number of epochs e, to train
# the model using features X and labels y
w = 0.0
b = 0.0
alpha = 0.001
epochs = 12000
# Train Model
w, b = train(X=X, y=y, w=0.0, b=0.0, alpha=0.001, epochs=12000)

# Define epoch numbers to plot to visualize progress
epoch_plots = [1, 2, 3, 11, 22, 33, epochs+1]
for epoch_plt in epoch_plots:
  w, b = train_and_plot(X, y, 0.0, 0.0, 0.001, epoch_plt, 10)

"""## HACEMOS LA PRIMERA PREDICCION EN BASE A 10 HORAS ESTUDIADAS

Como podemos observar, sin usar ningun framework podemos observar que la prediccion
fue muy buena, ya que si una persona estudia 10 horas obtiene un resultado de 100.8792.
"""

# Use trained model to make a prediction
x_new = 10
y_new = predict(x_new, w, b)
print('Para x={}, la predicción de y es y={}'.format(x_new, round(y_new,4)))

"""## A continuacion, vamos a implementarlo con el framework scikit-learn"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Cargar el conjunto de datos desde score_updated.csv
data = pd.read_csv('score_updated.csv')
X = data['Hours'].values.reshape(-1, 1)  # Requiere que X sea una matriz 2D
y = data['Scores'].values

# Inicializar y entrenar el modelo de regresión lineal
model = LinearRegression()
model.fit(X, y)

# Obtener los coeficientes (w y b)
w = model.coef_[0]
b = model.intercept_

# Realizar predicciones
x_new = np.array([[10]])  # Asegurarse de que sea una matriz 2D
y_new = model.predict(x_new)

# Visualizar el ajuste
plt.scatter(X, y, marker='o', c='b')
plt.plot(X, model.predict(X), c='r')
plt.title(f"Predicción de Regresión Lineal | w: {w}, b: {b}")
plt.xlabel('Hours')
plt.ylabel('Scores')
plt.show()

# Calcular el error cuadrático medio (MSE)
mse = mean_squared_error(y, model.predict(X))
print(f'Error Cuadrático Medio (MSE): {mse}')
print(f'Para x={x_new[0][0]}, la predicción de y es y={y_new[0]}')

"""**REPORTE:**

Para este momento de retroalimentacion, utilice un conjunto de datos de Students Study Hours,
donde contenia informacion sobre la hora que estudian los estudiantes al dia para obtener cierta
calificacion, cuando aplique la regresion lineal sin uso de un framework, me di cuenta que no hubo
necesidad de modificar alpha debido a que me dio una prediccion muy buena ya que si un estudiante
estudia 10 horas, va obtener una calificacion de 100.8792, al momento de usar la libreria de scikit-learn,
nos dimos cuenta que la prediccion obtuvimos 100.8767, a pesar que la diferencia es muy poca, se puede
considerar mas confiable ya que esta mas cerca del 100 que es la calificacion total, al igual obtuvimos
un MSE bajo donde no afecta mucho el resultado, asi que en conclusion, el usar la libreria de scikit-learn
te va dar predicciones mas cercanas y confiables al resultado esperado.

# A continuacion, vamos a probar calcular el Bias, Varianza, e implementar regularizacion para despues probarlo correctamente en nuestro reporte final. Esto va ser un breve codigo donde lo implementaremos de manera simple para tener un mejor entendimiento de su funcionamiento. Utilizando la libreria de Ridge
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Cargar el conjunto de datos desde score_updated.csv
data = pd.read_csv('score_updated.csv')
X = data['Hours'].values.reshape(-1, 1)  # Requiere que X sea una matriz 2D
y = data['Scores'].values

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inicializar y entrenar el modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)

# Obtener los coeficientes (w y b)
w = model.coef_[0]
b = model.intercept_

# Realizar predicciones
x_new = np.array([[10]])  # Asegurarse de que sea una matriz 2D
y_new = model.predict(x_new)

# Calcular el error cuadrático medio (MSE) en datos de entrenamiento
mse_train = mean_squared_error(y_train, model.predict(X_train))
print(f'Error Cuadrático Medio en Entrenamiento (Sesgo): {mse_train}')

# Calcular el MSE en datos de prueba (Varianza)
mse_test = mean_squared_error(y_test, model.predict(X_test))
print(f'Error Cuadrático Medio en Prueba (Varianza): {mse_test}')

# Aplicar Regularización Ridge (L2)
alpha = 0.1  # Hiperparámetro de regularización, puedes ajustarlo
ridge_model = Ridge(alpha=alpha)
ridge_model.fit(X_train, y_train)

# Calcular el MSE en datos de entrenamiento con regularización
mse_train_reg = mean_squared_error(y_train, ridge_model.predict(X_train))
print(f'Error Cuadrático Medio en Entrenamiento con Regularización: {mse_train_reg}')

# Calcular el MSE en datos de prueba con regularización
mse_test_reg = mean_squared_error(y_test, ridge_model.predict(X_test))
print(f'Error Cuadrático Medio en Prueba con Regularización: {mse_test_reg}')

# Visualizar el ajuste sin regularización
plt.scatter(X, y, marker='o', c='b')
plt.plot(X, model.predict(X), c='r', label=f"Predicción sin Regularización | w: {w}, b: {b}")
plt.title(f"Predicción de Regresión Lineal (Sin Regularización)")
plt.xlabel('Hours')
plt.ylabel('Scores')

# Visualizar el ajuste con regularización
plt.scatter(X_train, y_train, marker='o', c='b', label='Datos de Entrenamiento')
plt.plot(X, ridge_model.predict(X), c='g', label=f"Predicción con Regularización | alpha: {alpha}")
plt.title(f"Predicción de Regresión Lineal (Con Regularización)")
plt.xlabel('Hours')
plt.ylabel('Scores')

plt.legend(loc='best')
plt.show()

# Resultados de la predicción
print(f'Para x={x_new[0][0]}, la predicción de y es y={y_new[0]}')

"""En estas dos graficas podemos ver un claro ejemplo del uso de la prediccion de
regreison lineal con regularizacion y sin regularizacion, cuando no usamos regularizacion
el modelo se ajusta mucho a los datos de train, esto lo que puede ocasionar es que el
modelo pueda ser deficiente o overfitting. Y cuando usamos regularizacion lo que hace y
lo que se observa es que controla la complejidad del modelo y reduce el overfitting. Y
asi mismo permite que el modelo se ajuste a los datos de train de una mejor manera.
Basicamente la regularizacion ayuda a mejorar el modelo y reduce la probabilidad de
presentar un overfitting."""