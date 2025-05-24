# ============================================
# Preparación del entorno de trabajo
# ============================================

rm(list=ls())
# Librerías necesarias para el análisis
library(tidyverse)    # Manipulación y visualización de datos (ggplot2, dplyr, readr, etc.)
library(caret)        # Entrenamiento y evaluación de modelos de clasificación y regresión
library(rpart)        # Árboles de decisión (Decision Tree)
library(rpart.plot)   # Visualización de árboles de decisión
library(kernlab)      # Modelos SVM (Support Vector Machines)
library(pROC)         # Curvas ROC y cálculo de AUC
library(PRROC)        # Curvas PR (Precision-Recall) y cálculo de AUC
library(glmnet)       # Modelos de regresión regularizada
library(ggplot2)


# Seleccionar archivo
dataset <- read.csv(file.choose())

# Preparación de los datos
# Elimino la columna "ID"
dataset_noid <- dataset %>% select(-ID)

# Variables predictoras (X) y variable respuesta (y)
x <- as.matrix(dataset_noid[, 2:ncol(dataset_noid)])  
y <- factor(dataset_noid$Diagnosis)                  # Convertir Diagnosis a factor (variable objetivo)

# ============================================
# Selección del método supervisado
# ============================================

##Las SVM es muy poderosas cuando los datos no se pueden separar de manera simple, ya que buscan un hiperplano que maximice el 
##margen entre las clases, lo que lo hace muy precisa, aunque a veces requieren más tiempo de computación 
##y ajuste de parámetros. Por otro lado, los Árboles de Decisión son bastante fáciles de interpretar, 
##lo que me ayuda a entender cómo el modelo toma sus decisiones. Sin embargo, tienden a sobreajustarse si no 
##se cuidan bien, especialmente con datos más complejos o ruidosos. En general, 
##SVM es más sólida, especialmente para datos complejos 
##como los de WDBC, mientras que los Árboles de Decisión puede ser útil si se busca algo más 
##simple y explicativo, aunque en términos de rendimiento, probablemente no superen al otro enfoque.

# ============================================
# Procesamiento del dataframe
# ============================================

# Dividir el conjunto de datos en entrenamiento y prueba
set.seed(1995)  # Semilla para la reproducción de resultados
trainIndex <- createDataPartition(dataset_noid$Diagnosis, p = 0.8, list = FALSE)
trainData <- dataset_noid[trainIndex, ]
testData <- dataset_noid[-trainIndex, ]

# Convertir la columna de diagnóstico a factor
dataset_noid$Diagnosis <- as.factor(dataset_noid$Diagnosis)



# ============================================
# Modelo SVM (Support Vector Machine)
# ============================================

# Crear un modelo de SVM radial utilizando el paquete caret
# Parámetro C por defecto es 1, pero lo ajusto para encontrar un balance entre un margen amplio y una clasificación correcta de las muestras

svmModelRadial <- train(Diagnosis ~ ., 
                        data = trainData, 
                        method = "svmRadial", 
                        trControl = trainControl(method = "cv", number = 10),  # Usamos validación cruzada
                        preProcess = c("center", "scale"),  # Preprocesamiento para estandarizar los datos
                        tuneGrid = expand.grid(sigma = seq(0.05, 0.1, length = 10), C = seq(0, 2, length = 20)),  # Parametros C y sigma a ajustar
                        prob.model = TRUE)  # Para obtener probabilidades

# Ver los detalles del modelo SVM radial
svmModelRadial

# Graficar los resultados del modelo
plot(svmModelRadial)

# Realizar predicciones en el conjunto de prueba utilizando el modelo entrenado
predictions_svm_radial <- predict(svmModelRadial, newdata = testData)
predictions_svm_radial

#No sé por qué si se se corre todo a la vez da problemas con la matriz de confusión.
#Pero seleccionando cada comando uno a uno si que funciona desde el anterior comando hacia adelante

##Convertir las variables a factores con los mismos niveles
predictions_svm_radial <- factor(predictions_svm_radial, levels = levels(testData$Diagnosis))
testData$Diagnosis <- factor(testData$Diagnosis)  

# Evaluar el modelo utilizando la matriz de confusión
confMatrix_svm_radial <- confusionMatrix(predictions_svm_radial, testData$Diagnosis)
print(confMatrix_svm_radial)

# Mostrar precisión global del modelo
print(confMatrix_svm_radial$overall['Accuracy'])  # Precisión global

# Mostrar métricas de la clase como sensibilidad, especificidad, etc.
print(confMatrix_svm_radial$byClass)  # Sensibilidad, especificidad, etc.

# Obtener probabilidades para la clasificación con el modelo radial
probabilities_svm_radial <- predict(svmModelRadial, newdata = testData, type = "prob")
print(probabilities_svm_radial)


##En este análisis del modelo SVM (Máquinas de Vectores de Soporte) con núcleo radial, 
##se observa el desempeño del modelo en función de los parámetros de ajuste como el valor 
##de sigma y el parámetro C. El modelo fue evaluado mediante una validación cruzada de 10 
##pliegues sobre un conjunto de datos que comprende 569 muestras distribuidas entre dos 
##clases: 'B' (benigno) y 'M' (maligno), con un total de 26 variables predictoras. 
##Además, los datos fueron previamente centrados y escalados.

##Al revisar los resultados, podemos observar que con valores de C y sigma específicos, 
##el modelo alcanza altos niveles de precisión. Por ejemplo, cuando el parámetro C es 
##1.5789474 y sigma es 0.05000000, la precisión alcanza un 97.15% (accuracy) y un Kappa 
##de 0.939, lo que indica una excelente concordancia entre las predicciones y las observaciones 
##reales. A medida que se ajustan los valores de sigma y C, se observa una ligera variabilidad 
##en los resultados, pero en general, las métricas de rendimiento siguen siendo muy altas, 
##con valores de precisión y Kappa superiores al 95% en la mayoría de las combinaciones de 
##estos parámetros.

##Los resultados indican que el modelo SVM radial tiene un buen desempeño general para la 
##clasificación de las muestras, alcanzando una precisión y Kappa que indican una clasificación 
##casi perfecta. 


# ============================================
# Usar un modelo de Árbol de Decisión
# ============================================

dtModel <- train( Diagnosis ~ .,           # Variable objetivo
                  data = trainData,        # Conjunto de entrenamiento
                  method = "rpart",        # Método: Árbol de Decisión
                  trControl = trainControl( # Validación cruzada con 10 pliegues
                    method = "cv",         # Método de validación cruzada
                    number = 10            # Número de pliegues
                  ),
                  preProcess = c("center", "scale"), # Preprocesamiento: centrar y escalar
                  tuneLength = 10         # Ajuste automático de los hiperparámetros
)

# Mostrar los resultados del modelo entrenado
print(dtModel)

# Visualizacion en pantalla:: Graficar la variación de las métricas con los hiperparámetros
plot(dtModel)

# Visualizacion en pantalla: Graficar el árbol de decisión usando rpart.plot
rpart.plot(dtModel$finalModel)

# Evaluar el modelo con el conjunto de prueba
predictions_raw <- predict(dtModel, newdata = testData, type = "raw")  # Predicciones de clases

# Mostrar las predicciones
print(predictions_raw)

# Evaluar la precisión del modelo utilizando la matriz de confusión
confMatrix <- confusionMatrix(predictions_raw, testData$Diagnosis)
print(confMatrix)

# Obtener las probabilidades de cada clase
probabilities_dt <- predict(dtModel, newdata = testData, type = "prob")
print(probabilities_dt)

# Mostrar métricas de precisión global y por clase
print(confMatrix$overall['Accuracy'])  # Precisión global
print(confMatrix$byClass)  # Métricas de clase (sensibilidad, especificidad, etc.)

## El modelo de Árbol de Decisión se usó con 
## validación cruzada con 10 pliegues mostró una bunea clasificación 
## de tumores benignos (B) y malignos (M). La precisión global alcanzada fue de 92.92%, 
## lo que significa que el modelo clasificó correctamente el 92.92% de las observaciones en 
## el conjunto de prueba. Esta alta precisión se ve respaldada por un valor de Kappa de 0.8484, 
## lo que indica una excelente concordancia entre las predicciones y las etiquetas reales, 
## superando el valor esperado por azar.

## La sensibilidad, que refleja la capacidad del modelo para identificar correctamente los 
## tumores malignos (clase positiva en este caso), fue del 94.37%. Esto significa que el modelo 
## identificó el 94.37% de los casos de tumores malignos, lo cual es crucial en un contexto médico 

##En cuanto a otros indicadores importantes, el valor de "Pos Pred Value" y "Neg Pred Value" 
##(que reflejan la precisión en la clasificación de las clases positiva y negativa, respectivamente) 
##fueron del 94.37% y 90.48%, lo que indica la fiabilidad del modelo al hacer sus predicciones. 
##Además, la precisión balanceada fue de 92.42%, lo que demuestra que el modelo tiene un buen 
##rendimiento tanto en la identificación de tumores benignos como malignos, sin sesgo hacia ninguna 
##de las clases.

##El modelo también mostró una "Prevalencia" de 62.83%, lo que refleja la proporción de tumores 
##benignos en el conjunto de datos, mientras que la "Detection Rate" y la "Detection Prevalence" 
##fueron ambas de 59.29%, lo que sugiere que el modelo fue capaz de detectar correctamente el 
##59.29% de los casos en el conjunto de prueba. 


# ============================================
# Curva ROC
# ============================================

# Obtener las probabilidades de cada clase con el Árbol de Decisión
probabilities_dt <- predict(dtModel, newdata = testData, type = "prob")
print(probabilities_dt)

# Obtener las probabilidades para la clasificación con el modelo SVM Radial
probabilities_svm_radial <- predict(svmModelRadial, newdata = testData, type = "prob")
print(probabilities_svm_radial)

# Calcular las curvas ROC para el modelo de Árbol de Decisión
roc_dt <- roc(testData$Diagnosis, probabilities_dt[, 2])  # Probabilidad para la clase "M", positiva
auc_dt <- auc(roc_dt)
cat("AUC Árbol de Decisión:", auc_dt, "\n")

# Calcular las curvas ROC para el modelo SVM Radial
roc_svm_radial <- roc(testData$Diagnosis, probabilities_svm_radial[, 2])  # Probabilidad para la clase "M", positiva
auc_svm_radial <- auc(roc_svm_radial)
cat("AUC SVM Radial:", auc_svm_radial, "\n")

# Graficar las curvas ROC
plot(roc_dt, col = "blue", main = "Curvas ROC para Árbol de Decisión y SVM Radial", lwd = 2)
plot(roc_svm_radial, col = "red", add = TRUE, lwd = 2)

# Agregar leyenda
legend("bottomright", 
       legend = c(paste("AUC Árbol de Decisión:", round(auc_dt, 2)), 
                  paste("AUC SVM Radial:", round(auc_svm_radial, 2))),
       col = c("blue", "red"), lwd = 2)


# ============================================
# Curva Precision-Recall
# ============================================


# Calcular la curva PR para el modelo de Árbol de Decisión
pr_dt <- pr.curve(scores.class0 = probabilities_dt[, 2], 
                  weights.class0 = testData$Diagnosis == "M", 
                  curve = TRUE, max.compute = TRUE, min.compute = TRUE, rand.compute = TRUE)

# Calcular la curva PR para el modelo SVM Radial
pr_svm_radial <- pr.curve(scores.class0 = probabilities_svm_radial[, 2], 
                          weights.class0 = testData$Diagnosis == "M", 
                          curve = TRUE, max.compute = TRUE, min.compute = TRUE, rand.compute = TRUE)

# Graficar las curvas PR
plot(pr_dt, col = "blue", lwd = 2, rand.plot = TRUE, fill.area = TRUE)
plot(pr_svm_radial, col = "red", add = TRUE, lwd = 2, rand.plot = TRUE, fill.area = TRUE)

# Agregar leyenda
legend("bottomright", 
       legend = c(paste("PR-Curve Árbol de Decisión:", round(pr_dt$auc.integral, 2)), 
                  paste("PR-Curve SVM Radial:", round(pr_svm_radial$auc.integral, 2))),
       col = c("blue", "red"), lwd = 2)


## En el análisis de desempeño de los modelos de clasificación, el SVM 
## muestra un rendimiento superior al Árbol de Decisión en varias métricas clave. En primer lugar,
## la sensibilidad del modelo SVM es prácticamente perfecta, con un valor cercano a 1, lo que
## indica que logra identificar correctamente casi todos los casos positivos (malignos) en el conjunto 
## de datos. En contraste, el Árbol de Decisión presenta una sensibilidad ligeramente inferior, con
## un valor de 0.94, lo que sugiere que tiene una tasa de falsos negativos mayor. Además, en las 
## curvas ROC, que muestran la capacidad de los modelos para discriminar entre clases, el SVM se aleja 
## significativamente de la línea de aleatoriedad, lo que sugiere una clasificación altamente efectiva.
## Por otro lado, el Árbol de Decisión no se aleja tanto de esta línea, lo que indica un rendimiento
## relativamente peor en términos de separación entre las clases. En cuanto a la Precision-Recall 
## curve, el SVM muestra una precisión perfecta (1), mientras que el Árbol de Decisión comienza 
## con una precisión de 0.75. A medida que se aumenta el recall en el Árbol de Decisión, la 
## precisión mejora progresivamente hasta alcanzar un valor de 0.94. Sin embargo, a medida que el 
## recall llega a 1, ambos modelos muestran una caída abrupta en la precisión, con el Árbol de Decisión 
## sufriendo una mayor caída. En resumen, el modelo SVM no solo ofrece una mayor sensibilidad, sino que 
## también demuestra un rendimiento más estable en las curvas ROC y PR, lo que lo convierte en una opción 
## más fiable y precisa en comparación con el Árbol de Decisión.
