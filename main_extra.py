import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PyQt6.QtGui import (
    QPainter,
    QPen,
    QBrush,
    QColor,
    QColorConstants
)
from PyQt6.QtCore import (
    Qt,
    QPointF,
    QRectF,
    QTimer,
    QPoint
)
from functools import partial
from matriz import Transformador

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Transformaciones")
        self.setGeometry(400, 200, 600, 400)
        self.tf = Transformador()
        self.inicializarPlano()
        self.inicializarReloj()
        # self.setCentralWidget(self.contenedor_plano)
        self.cambiarAlPlano()

    def inicializarPlano(self):
        self.hboxlayout_plano = QHBoxLayout()
        self.contenedor_plano = QWidget()
        self.contenedor_plano.setLayout(self.hboxlayout_plano)

        self.canvas_plano = QGraphicsView(self.contenedor_plano)
        self.canvas_plano.setMinimumWidth(150)
        self.canvas_plano.setGeometry(0, 0, 550, 400)
        self.canvas_scene_plano = QGraphicsScene()
        self.canvas_plano.setScene(self.canvas_scene_plano)

        self.sidebar = QWidget(self.contenedor_plano)
        self.sidebar.setFixedWidth(150)
        self.gridlayout = QGridLayout(self.sidebar)
        self.sidebar.setLayout(self.gridlayout)

        self.p_label = QLabel("P")
        self.px_edit = QLineEdit(self.sidebar)
        self.px_edit.setPlaceholderText("x")
        self.py_edit = QLineEdit(self.sidebar)
        self.py_edit.setPlaceholderText("y")
        self.p_boton = QPushButton("Dibujar", self.sidebar)
        self.p_boton.clicked.connect(self.dibujarP)

        self.c_label = QLabel("C")
        self.cx_edit = QLineEdit(self.sidebar)
        self.cx_edit.setPlaceholderText("x")
        self.cy_edit = QLineEdit(self.sidebar)
        self.cy_edit.setPlaceholderText("y")
        self.c_boton = QPushButton("Dibujar", self.sidebar)
        self.c_boton.clicked.connect(self.dibujarC)

        self.t_label = QLabel("T")
        self.tx_edit = QLineEdit(self.sidebar)
        self.tx_edit.setPlaceholderText("x")
        self.ty_edit = QLineEdit(self.sidebar)
        self.ty_edit.setPlaceholderText("y")
        self.t_boton = QPushButton("Trasladar", self.sidebar)
        self.t_boton.clicked.connect(self.trasladar)

        self.r_label = QLabel("R")
        self.r_edit = QLineEdit(self.sidebar)
        self.r_edit.setPlaceholderText("°")
        self.r_boton = QPushButton("Rotar", self.sidebar)
        self.r_boton.clicked.connect(self.rotar)

        self.s_label = QLabel("S")
        self.sx_edit = QLineEdit(self.sidebar)
        self.sx_edit.setPlaceholderText("x")
        self.sy_edit = QLineEdit(self.sidebar)
        self.sy_edit.setPlaceholderText("y")
        self.s_boton = QPushButton("Escalar", self.sidebar)
        self.s_boton.clicked.connect(self.escalar)

        self.p_prima_label = QLabel("P'")
        self.p_primax_edit = QLineEdit(self.sidebar)
        self.p_primax_edit.setPlaceholderText("x")
        self.p_primay_edit = QLineEdit(self.sidebar)
        self.p_primay_edit.setPlaceholderText("y")

        self.reloj_boton = QPushButton("Reloj", self.sidebar)
        self.reloj_boton.clicked.connect(self.cambiarAlReloj)

        self.gridlayout.addWidget(self.p_label, 0, 0)
        self.gridlayout.addWidget(self.px_edit, 0, 1)
        self.gridlayout.addWidget(self.py_edit, 0, 2)
        self.gridlayout.addWidget(self.p_boton, 0, 3, 1, 2)

        self.gridlayout.addWidget(self.c_label, 1, 0)
        self.gridlayout.addWidget(self.cx_edit, 1, 1)
        self.gridlayout.addWidget(self.cy_edit, 1, 2)
        self.gridlayout.addWidget(self.c_boton, 1, 3, 1, 2)

        self.gridlayout.addWidget(QLabel(""), 2, 0)
        self.gridlayout.addWidget(self.t_label, 3, 0)
        self.gridlayout.addWidget(self.tx_edit, 3, 1)
        self.gridlayout.addWidget(self.ty_edit, 3, 2)
        self.gridlayout.addWidget(self.t_boton, 3, 3, 1, 2)

        self.gridlayout.addWidget(self.r_label, 4, 0)
        self.gridlayout.addWidget(self.r_edit, 4, 1, 1, 2)
        self.gridlayout.addWidget(self.r_boton, 4, 3, 1, 2)

        self.gridlayout.addWidget(self.s_label, 5, 0)
        self.gridlayout.addWidget(self.sx_edit, 5, 1)
        self.gridlayout.addWidget(self.sy_edit, 5, 2)
        self.gridlayout.addWidget(self.s_boton, 5, 3, 1, 2)

        self.gridlayout.addWidget(QLabel(""), 6, 0)
        self.gridlayout.addWidget(self.p_prima_label, 7, 0)
        self.gridlayout.addWidget(self.p_primax_edit, 7, 1, 1, 2)
        self.gridlayout.addWidget(self.p_primay_edit, 7, 3, 1, 2)

        self.gridlayout.addWidget(self.reloj_boton, 8, 0, 1, 5)

        self.hboxlayout_plano.addWidget(self.canvas_plano)
        self.hboxlayout_plano.addWidget(self.sidebar)

        self.p_pen = QPen(QColorConstants.DarkBlue)
        self.p_brush = QBrush(QColorConstants.DarkBlue)
        self.c_pen = QPen(QColorConstants.DarkYellow)
        self.c_brush = QBrush(QColorConstants.DarkYellow)
        self.p_prima_pen = QPen(QColorConstants.DarkMagenta)
        self.p_prima_brush = QBrush(QColorConstants.DarkMagenta)

        self.p = QGraphicsEllipseItem(0.0, 0.0, 6.0, 6.0)
        self.p.setPen(self.p_pen)
        self.p.setBrush(self.p_brush)
        self.p.setVisible(False)

        self.c = QGraphicsEllipseItem(0.0, 0.0, 6.0, 6.0)
        self.c.setPen(self.c_pen)
        self.c.setBrush(self.c_brush)
        self.c.setVisible(False)

        self.p_prima = QGraphicsEllipseItem(0.0, 0.0, 6.0, 6.0)
        self.p_prima.setPen(self.p_prima_pen)
        self.p_prima.setBrush(self.p_prima_brush)
        self.p_prima.setVisible(False)

        self.canvas_scene_plano.addItem(self.p)
        self.canvas_scene_plano.addItem(self.c)
        self.canvas_scene_plano.addItem(self.p_prima)

        self.canvas_scene_plano.addEllipse(0, 0, 0, 0)
        self.canvas_scene_plano.addLine(0, -650, 0, 650)
        self.canvas_scene_plano.addLine(-650, 0, 650, 0)

    def dibujarP(self):
        self.p.setVisible(True)
        self.p.setX(int(self.px_edit.text()) - 3)
        self.p.setY(-int(self.py_edit.text()) - 3)

    def dibujarC(self):
        self.c.setVisible(True)
        self.c.setX(int(self.cx_edit.text()) - 3)
        self.c.setY(-int(self.cy_edit.text()) - 3)

    def trasladar(self):
        px = int(self.px_edit.text())
        py = int(self.py_edit.text())
        tx = int(self.tx_edit.text())
        ty = int(self.ty_edit.text())
        p_prima = self.tf.trasladar(px, py, tx, ty)
        p_primax = p_prima[0]
        p_primay = p_prima[1]
        self.p_prima.setVisible(True)
        self.p_prima.setX(p_primax - 3)
        self.p_prima.setY(-p_primay - 3)
        self.p_primax_edit.setText(str(p_primax))
        self.p_primay_edit.setText(str(p_primay))

    def rotar(self):
        px = int(self.px_edit.text())
        py = int(self.py_edit.text())
        angulo = int(self.r_edit.text())
        cx = int(self.cx_edit.text())
        cy = int(self.cy_edit.text())
        p_prima = self.tf.rotar(px, py, angulo, cx, cy)
        p_primax = p_prima[0]
        p_primay = p_prima[1]
        self.p_prima.setVisible(True)
        self.p_prima.setX(p_primax - 3)
        self.p_prima.setY(-p_primay - 3)
        self.p_primax_edit.setText(str(p_primax))
        self.p_primay_edit.setText(str(p_primay))

    def escalar(self):
        px = int(self.px_edit.text())
        py = int(self.py_edit.text())
        sx = int(self.sx_edit.text())
        sy = int(self.sy_edit.text())
        cx = int(self.cx_edit.text())
        cy = int(self.cy_edit.text())
        p_prima = self.tf.escalar(px, py, sx, sy, cx, cy)
        p_primax = p_prima[0]
        p_primay = p_prima[1]
        self.p_prima.setVisible(True)
        self.p_prima.setX(p_primax - 3)
        self.p_prima.setY(-p_primay - 3)
        self.p_primax_edit.setText(str(p_primax))
        self.p_primay_edit.setText(str(p_primay))

    def inicializarReloj(self):
        self.vboxlayout_reloj = QVBoxLayout()
        self.contenedor_reloj = QWidget()
        self.contenedor_reloj.setLayout(self.vboxlayout_reloj)

        self.canvas_reloj = QGraphicsView(self.contenedor_reloj)
        self.canvas_reloj.setMinimumWidth(150)
        self.canvas_reloj.setGeometry(0, 0, 600, 380)
        self.canvas_scene_reloj = QGraphicsScene()
        self.canvas_reloj.setScene(self.canvas_scene_reloj)

        self.bottombar = QWidget(self.contenedor_reloj)
        self.bottombar.setFixedHeight(40)
        self.bottombarlayout = QHBoxLayout(self.bottombar)
        self.bottombar.setLayout(self.bottombarlayout)
        self.vboxlayout_reloj.addWidget(self.bottombar)

        self.plano_boton = QPushButton("Plano", self.bottombar)
        self.plano_boton.clicked.connect(self.cambiarAlPlano)

        self.canvas_scene_reloj.addEllipse(0, 0, 0, 0)
        self.canvas_scene_reloj.addLine(0, -300, 0, 300)
        self.canvas_scene_reloj.addLine(-300, 0, 300, 0)

        self.c_reloj_pen = QPen(QColorConstants.DarkMagenta)
        self.c_reloj_brush = QBrush(QColorConstants.DarkMagenta)
        self.c_contorno_pen = QPen(QColorConstants.DarkMagenta)
        self.c_contorno_pen.setWidth(3)
        self.c_contorno_brush = QBrush(QColorConstants.Transparent)
        self.segundero_pen = QPen(QColorConstants.DarkCyan)
        self.segundero_pen.setWidth(2)
        self.segundero_brush = QBrush(QColorConstants.DarkCyan)

        self.c_reloj = QGraphicsEllipseItem(-3.0, -3.0, 6.0, 6.0)
        self.c_reloj.setPen(self.c_reloj_pen)
        self.c_reloj.setBrush(self.c_reloj_brush)

        self.c_contorno = QGraphicsEllipseItem(-100.0, -100.0, 200.0, 200.0)
        self.c_contorno.setPen(self.c_contorno_pen)
        self.c_contorno.setBrush(self.c_contorno_brush)

        self.segundero = QPointF(0.0, -100.0)
        self.segundero.setX(0.0)
        self.segundero.setY(-100.0)
        
        self.segundero_linea = QGraphicsLineItem(0, 0, 0, -100)
        self.segundero_linea.setPen(self.segundero_pen)

        self.seg_label = QLabel("Segundero")
        self.seg_xedit = QLineEdit()
        self.seg_yedit = QLineEdit()

        self.canvas_scene_reloj.addItem(self.c_reloj)
        self.canvas_scene_reloj.addItem(self.c_contorno)
        self.canvas_scene_reloj.addItem(self.segundero_linea)

        self.bottombarlayout.addWidget(self.seg_label)
        self.bottombarlayout.addWidget(self.seg_xedit)
        self.bottombarlayout.addWidget(self.seg_yedit)
        self.bottombarlayout.addWidget(self.plano_boton, 2)

        self.vboxlayout_reloj.addWidget(self.canvas_reloj)
        self.vboxlayout_reloj.addWidget(self.bottombar)

        self.segundos_timer = QTimer()
        self.segundos_timer.timeout.connect(self.moverSegundero)
        self.segundos_timer.start(1000)

    def cambiarAlReloj(self):
        self.contenedor_plano.setParent(None)
        self.contenedor_reloj.setParent(self)
        self.setCentralWidget(self.contenedor_reloj)

    def cambiarAlPlano(self):
        self.contenedor_reloj.setParent(None)
        self.contenedor_plano.setParent(self)
        self.setCentralWidget(self.contenedor_plano)

    def moverSegundero(self):
        x = self.segundero.x()
        y = self.segundero.y()
        nuevas_coordenadas = self.tf.rotar(x, y, 6)
        x = nuevas_coordenadas[0]
        y = nuevas_coordenadas[1]
        self.segundero.setX(x)
        self.segundero.setY(y)
        self.seg_xedit.setText(str(x))
        self.seg_yedit.setText(str(y))
        self.segundero_linea.setLine(0, 0, x, y)

def main():
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()