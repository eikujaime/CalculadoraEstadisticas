import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QTabWidget, QFrame, QColorDialog, QInputDialog, QMenu, QAction, QWidget, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QColor
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Funciones para calcular estadísticas básicas
def calcular_media(vector):
    return np.mean(vector)

def calcular_mediana(vector):
    return np.median(vector)

def calcular_moda(vector):
    moda = stats.mode(vector)
    if isinstance(moda.mode, np.ndarray):
        return moda.mode.tolist()
    else:
        return moda.mode

def calcular_desviacion_estandar(vector):
    return np.std(vector, ddof=1)

def calcular_varianza(vector):
    return np.var(vector, ddof=1)

def generar_grafico_histograma(vector, ax):
    ax.hist(vector)
    ax.set_xlabel('Valor')
    ax.set_ylabel('Frecuencia')
    ax.set_title('Histograma')

def generar_grafico_boxplot(vector, ax):
    ax.boxplot(vector)
    ax.set_xlabel('Variable')
    ax.set_ylabel('Valor')
    ax.set_title('Boxplot')

def calcular_probabilidad_continua(media, desviacion_estandar, valor):
    prob = stats.norm.cdf(valor, loc=media, scale=desviacion_estandar)
    return prob

def generar_grafico_normal(media, desviacion_estandar, ax):
    x = np.linspace(media - 3*desviacion_estandar, media + 3*desviacion_estandar, 100)
    y = stats.norm.pdf(x, loc=media, scale=desviacion_estandar)
    ax.plot(x, y)
    ax.set_xlabel('Valor')
    ax.set_ylabel('Densidad')
    ax.set_title('Distribución Normal')

# Clase principal de la aplicación
class CalculadoraEstadisticas(QMainWindow):
    def __init__(self):
        super().__init__()

        self.datos_entrada = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Calculadora de Estadísticas y Probabilidades")
        self.setGeometry(100, 100, 1000, 800)

        # Crear el menú
        menu = self.menuBar()

        file_menu = menu.addMenu("Archivo")
        file_menu.addAction("Salir", self.close)

        config_menu = menu.addMenu("Configuración")
        config_menu.addAction("Cambiar Color de Fondo", self.cambiar_color_fondo)
        config_menu.addAction("Cambiar Color del Texto", self.cambiar_color_texto)

        data_menu = menu.addMenu("Datos")
        data_menu.addAction("Ingresar Datos", self.ingresar_datos)

        # Crear el marco principal con pestañas
        self.tabs = QTabWidget()

        # Crear la pestaña de resultados
        result_tab = QWidget()
        self.tabs.addTab(result_tab, "Resultados")

        # Crear la pestaña de gráficos
        graph_tab = QWidget()
        self.tabs.addTab(graph_tab, "Gráficos")

        # Crear el marco para los resultados
        result_layout = QVBoxLayout(result_tab)
        result_frame = QFrame()
        result_layout.addWidget(result_frame)

        # Crear etiquetas para mostrar los resultados
        self.media_label = QLabel("Media: ", result_frame)
        self.mediana_label = QLabel("Mediana: ", result_frame)
        self.moda_label = QLabel("Moda: ", result_frame)
        self.desviacion_label = QLabel("Desviación Estándar: ", result_frame)
        self.varianza_label = QLabel("Varianza: ", result_frame)
        self.probabilidad_continua_label = QLabel("Probabilidad Continua: ", result_frame)

        result_layout.addWidget(self.media_label)
        result_layout.addWidget(self.mediana_label)
        result_layout.addWidget(self.moda_label)
        result_layout.addWidget(self.desviacion_label)
        result_layout.addWidget(self.varianza_label)
        result_layout.addWidget(self.probabilidad_continua_label)

        # Crear el marco para los gráficos
        graph_layout = QVBoxLayout(graph_tab)
        self.graph_frame = QFrame()
        graph_layout.addWidget(self.graph_frame)

        # Botón para actualizar la interfaz
        actualizar_button = QPushButton("Actualizar", self)
        actualizar_button.clicked.connect(self.actualizar_interfaz)

        # Configurar el layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(actualizar_button)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def actualizar_interfaz(self):
        if not self.datos_entrada:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingrese datos antes de actualizar.")
            return

        vector = np.array(self.datos_entrada, dtype=float)

        # Calcular estadísticas
        media = calcular_media(vector)
        mediana = calcular_mediana(vector)
        moda = calcular_moda(vector)
        desviacion_estandar = calcular_desviacion_estandar(vector)
        varianza = calcular_varianza(vector)

        self.media_label.setText(f"Media: {media:.2f}")
        self.mediana_label.setText(f"Mediana: {mediana:.2f}")
        self.moda_label.setText(f"Moda: {moda}")
        self.desviacion_label.setText(f"Desviación Estándar: {desviacion_estandar:.2f}")
        self.varianza_label.setText(f"Varianza: {varianza:.2f}")

        # Calcular probabilidades
        probabilidad_continua = calcular_probabilidad_continua(media, desviacion_estandar, 5)
        self.probabilidad_continua_label.setText(f"Probabilidad Continua: {probabilidad_continua:.2f}")

        # Generar gráficos
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        generar_grafico_histograma(vector, axs[0, 0])
        generar_grafico_boxplot(vector, axs[0, 1])
        generar_grafico_normal(media, desviacion_estandar, axs[1, 0])
        x = np.random.normal(loc=0, scale=1, size=1000)
        y = np.random.normal(loc=0, scale=1, size=1000)
        axs[1, 1].scatter(x, y)
        axs[1, 1].set_title('Gráfico de Dispersión')
        axs[1, 1].set_xlabel('X')
        axs[1, 1].set_ylabel('Y')

        # Mostrar gráficos en la interfaz
        canvas = FigureCanvas(fig)
        canvas.draw()
        self.graph_frame.setLayout(QVBoxLayout())
        self.graph_frame.layout().addWidget(canvas)

    def cambiar_color_fondo(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet(f"background-color: {color.name()};")

    def cambiar_color_texto(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.media_label.setStyleSheet(f"color: {color.name()};")
            self.mediana_label.setStyleSheet(f"color: {color.name()};")
            self.moda_label.setStyleSheet(f"color: {color.name()};")
            self.desviacion_label.setStyleSheet(f"color: {color.name()};")
            self.varianza_label.setStyleSheet(f"color: {color.name()};")
            self.probabilidad_continua_label.setStyleSheet(f"color: {color.name()};")

    def ingresar_datos(self):
        datos_entrada = QInputDialog.getText(self, "Ingresar Datos", "Ingrese los datos separados por comas:")
        if datos_entrada[1]:
            try:
                self.datos_entrada = [float(x) for x in datos_entrada[0].split(',')]
                self.actualizar_interfaz()
            except ValueError:
                QMessageBox.warning(self, "Advertencia", "Por favor, ingrese números válidos separados por comas.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CalculadoraEstadisticas()
    ex.show()
    sys.exit(app.exec_())
