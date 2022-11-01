from cProfile import label
import sys
from functools import partial
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGraphicsView,
    QGraphicsScene,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
    QLineEdit
)
from PyQt6.QtGui import (
    QPen,
    QColorConstants
)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Graficador")
        self.setGeometry(300, 100, 800, 500)

        contenedor = QWidget(self)
        self.setCentralWidget(contenedor)

        canvas = QGraphicsView(contenedor)
        canvas.setMinimumWidth(200)
        canvas.setGeometry(0, 0, 700, 400)
        self.escena = QGraphicsScene(contenedor)
        canvas.setScene(self.escena)

        bottombar = QWidget(contenedor)
        layout_bottombar = QGridLayout(bottombar)
        bottombar.setLayout(layout_bottombar)

        label_inicioint = QLabel("[", bottombar)

        self.edit_liminf = QLineEdit(bottombar)
        self.edit_liminf.setPlaceholderText("Inferior")

        label_coma = QLabel(", ", bottombar)

        self.edit_limsup = QLineEdit(bottombar)
        self.edit_limsup.setPlaceholderText("Superior")
        
        label_finint = QLabel("]", bottombar)

        self.edit_a = QLineEdit(bottombar)
        self.edit_a.setPlaceholderText("a")
        label_x3 = QLabel("x<sup>3</sup> + ", bottombar)

        self.edit_b = QLineEdit(bottombar)
        self.edit_b.setPlaceholderText("b")
        label_x2 = QLabel("x<sup>2</sup> + ", bottombar)

        self.edit_c = QLineEdit(bottombar)
        self.edit_c.setPlaceholderText("c")
        label_x1 = QLabel("x + ", bottombar)

        self.edit_d = QLineEdit(bottombar)
        self.edit_d.setPlaceholderText("d")

        boton_graficar = QPushButton("Graficar", bottombar)
        boton_graficar.clicked.connect(self.graficar)

        self.escena.addEllipse(0, 0, 0, 0)
        self.escena.addLine(0, -400, 0, 400)
        self.escena.addLine(700, 0, -700, 0)

        layout_bottombar.addWidget(label_inicioint, 0, 0)
        layout_bottombar.addWidget(self.edit_liminf, 0, 1)
        layout_bottombar.addWidget(label_coma, 0, 2)
        layout_bottombar.addWidget(self.edit_limsup, 0, 3)
        layout_bottombar.addWidget(label_finint, 0, 4)
        layout_bottombar.addWidget(QLabel(), 0, 5)
        layout_bottombar.addWidget(self.edit_a, 0, 6)
        layout_bottombar.addWidget(label_x3, 0, 7)
        layout_bottombar.addWidget(self.edit_b, 0, 8)
        layout_bottombar.addWidget(label_x2, 0, 9)
        layout_bottombar.addWidget(self.edit_c, 0, 10)
        layout_bottombar.addWidget(label_x1, 0, 11)
        layout_bottombar.addWidget(self.edit_d, 0, 12)
        layout_bottombar.addWidget(QLabel(), 0, 13)
        layout_bottombar.addWidget(boton_graficar, 0, 14)

        layout_contenedor = QVBoxLayout(contenedor)
        contenedor.setLayout(layout_contenedor)
        layout_contenedor.addWidget(canvas)
        layout_contenedor.addWidget(bottombar)

        self.pen_grafica = QPen(QColorConstants.DarkRed)

    def intentarConvertir(self, texto):
        try:
            return float(texto)
        except:
            return 0

    def graficar(self):
        self.escena.clear()
        liminf = self.intentarConvertir(self.edit_liminf.text())
        limsup = self.intentarConvertir(self.edit_limsup.text())
        a = self.intentarConvertir(self.edit_a.text())
        b = self.intentarConvertir(self.edit_b.text())
        c = self.intentarConvertir(self.edit_c.text())
        d = self.intentarConvertir(self.edit_d.text())
        ultimox = liminf
        ultimoy = a * ultimox ** 3 + b * ultimox ** 2 + c * ultimox + d
        for x in range(int(liminf) + 1, int(limsup) + 1):
            y = a * x ** 3 + b * x ** 2 + c * x + d
            self.escena.addLine(ultimox, -ultimoy, x, -y, self.pen_grafica)
            ultimox = x
            ultimoy = y
        self.escena.addLine(0, -self.escena.height() / 2, 0, self.escena.height() / 2)
        self.escena.addLine(self.escena.width() / 2, 0, -self.escena.width() / 2, 0)
        self.escena.update()

def main():
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()