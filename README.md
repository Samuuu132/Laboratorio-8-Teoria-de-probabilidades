Laboratorio 8 — Teoría de Probabilidades
MM3014 | Universidad del Valle de Guatemala
Autores:

Juan Salguero
Diego Gudiel


Descripción
Simulación Monte Carlo del proceso de llenado del álbum Panini del Mundial FIFA 2026.
El laboratorio cubre 2 etapas:

Etapa 3: Incorporación de presupuesto y costo
Etapa 4: Efecto del intercambio de repetidas


Archivos
├── etapa3.py        # Código Etapa 3
├── etapa4.py        # Código Etapa 4
└── Lab08Nuevo.ipynb # Notebook con ambas etapas

Requisitos
bashpip install numpy matplotlib

Cómo ejecutar
Opción 1 — Google Colab (recomendado)

Ir a colab.research.google.com
Subir el archivo Lab08Nuevo.ipynb
Ejecutar con Runtime → Run All

Opción 2 — VS Code

Abrir la carpeta del proyecto en VS Code
Abrir Lab08Nuevo.ipynb
Seleccionar el kernel de Python
Ejecutar con Run All

Opción 3 — Script directo
bashpython etapa3.py
python etapa4.py

Orden de ejecución en el notebook
Etapa 3 (etapa3.py)
CeldaLíneasContenido11 – 20Imports y parámetros222 – 57Simulación principal sobres sueltos359 – 76Visualización barras478 – 92Pregunta 1594 – 113Pregunta 2 — Caja6115 – 150Pregunta 3 — Mixta + comparación final
Etapa 4 (etapa4.py)
CeldaLíneasContenido11 – 17Imports y parámetros219 – 52Funciones sim_completar y prob_M_sobres354 – 70Parte A: simulación hasta completar472 – 100Parte A: histogramas5102 – 113Parte B: cálculo de probabilidades6115 – 131Parte B: gráfica de líneas7133 – 151Umbrales 50%, 75%, 90%8153 – 201Preguntas de análisis P1–P5

Notas importantes

Todas las simulaciones usan la semilla 2026 para garantizar reproducibilidad
Se recomienda usar Google Colab ya que la Etapa 4 tiene simulaciones pesadas
Las celdas deben ejecutarse en orden ya que cada una depende de las variables de la anterior
Si se reinicia el kernel hay que volver a correr desde la celda 1


Parámetros principales
ParámetroValorN (estampas)100S (estampas por sobre)7R (simulaciones)10,000Precio sobreQ 9.50Precio caja (104 sobres)Q 975.00PresupuestoQ 1,000.00Semilla2026
