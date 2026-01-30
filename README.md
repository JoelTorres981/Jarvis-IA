# 🤖 ChatBot Integrado con Inteligencia Artificial

Proyecto desarrollado para la asignatura **Fundamentos de Inteligencia Artificial**  
Escuela Politécnica Nacional – Escuela de Formación de Tecnólogos  
Período Académico: **2025-B**

---
## Integrantes

- Emily Alejandra Galeas Tingo  
- Joel Eduardo Torres Mora

## 📌 Descripción del proyecto

Este proyecto consiste en el desarrollo de un **chatbot básico con Inteligencia Artificial**, capaz de interactuar con el usuario mediante **voz y texto**, utilizando un modelo de **aprendizaje automático supervisado** para la clasificación de intenciones.

El sistema integra:
- Un modelo local entrenado con **Scikit-learn**
- Reconocimiento y síntesis de voz
- Interfaz gráfica desarrollada en **Tkinter**
- Integración con la **API de Google Gemini**
- Automatización de búsquedas en Google

Además, permite la **configuración de parámetros**, visualización de **métricas del modelo** y la **prueba de nuevos casos**, cumpliendo con todos los requisitos académicos del proyecto.

---

## 🎯 Objetivo general

Desarrollar una aplicación funcional en Python que implemente un modelo de Inteligencia Artificial capaz de interactuar con el usuario mediante voz o texto.

---

## 🎯 Objetivos específicos

- Implementar una interfaz gráfica amigable para la interacción con el usuario.
- Entrenar y evaluar un modelo de IA para la clasificación de intenciones.
- Integrar servicios externos de IA generativa.
- Mostrar métricas del desempeño del modelo.
- Permitir la configuración de parámetros en tiempo real.

---

## 🧠 Modelo de Inteligencia Artificial

- **Tipo:** Clasificación supervisada multiclase  
- **Algoritmo:** Multinomial Naive Bayes  
- **Vectorización:** CountVectorizer  
- **Clases:**  
  - Saludo  
  - Despedida  
  - Google  
  - Wiki  

El modelo es entrenado localmente y evaluado mediante la métrica de **Exactitud (Accuracy)**.

---

## 📊 Métricas del modelo

- **Accuracy (Exactitud)**
- Número de ejemplos de entrenamiento

Las métricas se calculan automáticamente al finalizar el entrenamiento y se visualizan en la interfaz gráfica.

---

## ⚙️ Funcionalidades principales

- ✔ Interacción por voz y texto
- ✔ Entrenamiento del modelo
- ✔ Clasificación de intenciones
- ✔ Configuración de parámetros:
  - Velocidad de voz
  - Sensibilidad del micrófono
- ✔ Visualización de métricas
- ✔ Integración con Google Gemini
- ✔ Búsquedas automáticas en Google
- ✔ Prueba de nuevos casos

---

## 🖥️ Interfaz gráfica

La interfaz gráfica fue desarrollada con **Tkinter** y permite:
- Visualizar métricas del modelo
- Ajustar parámetros del sistema
- Interactuar con el chatbot por voz o texto

---
