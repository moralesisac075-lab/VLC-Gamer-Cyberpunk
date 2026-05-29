"""

VLC Gamer Cyberpunk - Main Application

Taller 003 - Aplicaciones Open Source

Arquitectura: Wrapper Python 3.11 + python-vlc + PyQt5

"""



import sys

import os

import shutil

import time

import math

import json

from pathlib import Path



from PyQt5.QtWidgets import (

    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,

    QPushButton, QSlider, QLabel, QFileDialog, QFrame, QSizePolicy,

    QGraphicsDropShadowEffect, QProgressBar, QListWidget, QDialog, QMessageBox,
    QLineEdit, QShortcut

)

from PyQt5.QtCore import (

    Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect,

    QThread, pyqtSignal, QSize, QPoint

)

from PyQt5.QtGui import (

    QColor, QPainter, QPen, QBrush, QFont, QFontDatabase,

    QLinearGradient, QRadialGradient, QPalette, QPixmap, QIcon, QKeySequence

)



try:

    import vlc

    VLC_AVAILABLE = True

except ImportError:

    VLC_AVAILABLE = False

    print("ADVERTENCIA: python-vlc no instalado. Ejecuta: pip install python-vlc")



# ────────────────────────────────────────────────────────────────────────────────

#  PALETA CYBERPUNK

# ────────────────────────────────────────────────────────────────────────────────

COLORS = {

    "bg_deep":      "#030305",

    "bg_panel":     "#08080f",

    "bg_card":      "#0d0d1a",

    "cyan":         "#00f0ff",

    "cyan_dim":     "#007a82",

    "magenta":      "#ff007f",

    "magenta_dim":  "#7a003d",

    "yellow":       "#ffd700",

    "green_neon":   "#00ff41",

    "purple":       "#7b2fff",

    "text_primary": "#e0e8ff",

    "text_dim":     "#4a5580",

    "border_glow":  "#00f0ff44",

}



MAIN_QSS = """

/* ── BASE ── */

QMainWindow, QWidget {{

    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS["bg_deep"]}, stop:1 #0b0c16);

    color: {COLORS["text_primary"]};

    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 15px;

}}

QMainWindow {{
    border: 2px solid {COLORS["cyan"]}22;
}}


/* ── BOTONES ── */

QPushButton {{

    background-color: rgba(3, 3, 5, 0.35);

    color: {COLORS["cyan"]};

    border: 1px solid {COLORS["cyan_dim"]};

    border-radius: 14px;

    padding: 14px 20px;

    font-family: 'Consolas', monospace;

    font-size: 16px;

    letter-spacing: 1.5px;

    text-transform: uppercase;

}}

QPushButton:hover {{

    background-color: {COLORS["cyan"]}33;

    border: 1px solid {COLORS["cyan"]};

    color: #ffffff;

}}

QPushButton:pressed {{

    background-color: {COLORS["cyan"]}44;

    border: 1px solid {COLORS["magenta"]};

    color: {COLORS["magenta"]};

}}

QPushButton#btn_play {{

    border: 2px solid {COLORS["cyan"]};

    color: {COLORS["cyan"]};
    font-weight: bold;
    font-size: 16px;
    padding: 12px 28px;
    border-radius: 28px;

    min-width: 72px;

    max-width: 72px;

    min-height: 72px;

    max-height: 72px;

    padding: 0;

}

QPushButton#btn_play:hover {{

    background-color: {COLORS["cyan"]}33;

    border-color: {COLORS["magenta"]};

    color: {COLORS["magenta"]};

}}

QPushButton#btn_open {{

    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,

        stop:0 {COLORS["cyan"]}33, stop:1 {COLORS["magenta"]}33);

    border: 1px solid {COLORS["cyan"]};

    color: {COLORS["text_primary"]};

    font-weight: bold;

    font-size: 12px;

    padding: 12px 24px;

    border-radius: 16px;

}}

QPushButton#btn_open:hover {{

    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,

        stop:0 {COLORS["cyan"]}44, stop:1 {COLORS["magenta"]}44);

    border-color: {COLORS["magenta"]};

}}

QPushButton#btn_hud {{

    background: transparent;

    border: 1px solid {COLORS["purple"]};

    color: {COLORS["purple"]};

    font-size: 10px;

    padding: 4px 10px;

}}

QPushButton#btn_hud:hover {{

    background: {COLORS["purple"]}22;

    border-color: {COLORS["cyan"]};

    color: {COLORS["cyan"]};

}}


/* ── PLAYLIST ── */
QListWidget {{

    background-color: rgba(3, 3, 5, 0.35);

    border: 1px solid {COLORS["cyan_dim"]};

    border-radius: 14px;

    padding: 8px;

    color: {COLORS["text_primary"]};

}}
QListWidget::item {{

    padding: 10px;

    margin: 2px 0;

}}
QListWidget::item:selected {{

    background-color: {COLORS["cyan"]}22;

    color: #ffffff;

}}

QLineEdit {{

    background-color: rgba(3, 3, 5, 0.35);

    border: 1px solid {COLORS["cyan_dim"]};

    border-radius: 12px;

    padding: 8px;

    color: {COLORS["text_primary"]};

}}

QFrame#frame_status {{

    background-color: rgba(3, 3, 5, 0.48);

    border-top: 1px solid {COLORS["cyan_dim"]};

}}

QLabel#status_label {{

    color: {COLORS["text_dim"]};

    font-size: 11px;

    letter-spacing: 1px;

}}

QLabel#label_video_hint {{

    color: {COLORS["text_dim"]};

    font-size: 14px;

    border: 1px dashed {COLORS["cyan_dim"]};

    background-color: rgba(0, 0, 0, 0.4);

    padding: 12px;

    border-radius: 14px;

}}



/* ── SLIDERS ── */

QSlider::groove:horizontal {{

    height: 4px;

    background: {COLORS["bg_card"]};

    border: 1px solid {COLORS["cyan_dim"]};

    border-radius: 2px;

}}

QSlider::handle:horizontal {{

    background: {COLORS["cyan"]};

    border: 2px solid {COLORS["magenta"]};

    width: 12px;

    height: 12px;

    margin: -5px 0;

    border-radius: 6px;

}}

QSlider::sub-page:horizontal {{

    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,

        stop:0 {COLORS["cyan"]}, stop:1 {COLORS["magenta"]});

    border-radius: 2px;

}}

QSlider::groove:vertical {{

    width: 4px;

    background: {COLORS["bg_card"]};

    border: 1px solid {COLORS["cyan_dim"]};

    border-radius: 2px;

}}

QSlider::handle:vertical {{

    background: {COLORS["magenta"]};

    border: 2px solid {COLORS["cyan"]};

    width: 12px;

    height: 12px;

    margin: 0 -5px;

    border-radius: 6px;

}}

QSlider::sub-page:vertical {{

    background: {COLORS["magenta"]};

    border-radius: 2px;

}}



/* ── LABELS ── */

QLabel {{

    color: {COLORS["text_primary"]};

    font-family: 'Consolas', monospace;

}}

QLabel#label_title {{

    color: {COLORS["cyan"]};

    font-size: 16px;

    font-weight: bold;

    letter-spacing: 4px;

}}

QLabel#label_hud_title {{

    color: {COLORS["magenta"]};

    font-size: 11px;

    font-weight: bold;

    letter-spacing: 3px;

    border-bottom: 1px solid {COLORS["magenta_dim"]};

    padding-bottom: 4px;

}}

QLabel#label_metric_val {{

    color: {COLORS["green_neon"]};

    font-size: 20px;

    font-weight: bold;

}}

QLabel#label_metric_name {{

    color: {COLORS["text_dim"]};

    font-size: 9px;

    letter-spacing: 2px;

}}

QLabel#label_time {{

    color: {COLORS["cyan"]};

    font-size: 11px;

    letter-spacing: 1px;

}}

QLabel#label_filename {{

    color: {COLORS["magenta"]};

    font-size: 10px;

    letter-spacing: 1px;

}}



/* ── FRAMES / PANELS ── */

QFrame#frame_video {{

    background-color: #02020a;

    border-radius: 24px;

    border: 2px solid rgba(0, 240, 255, 0.18);

    box-shadow: 0 0 36px {COLORS["cyan"]}22;

}}

QFrame#panel_hud {{

    background-color: rgba(8, 8, 15, 0.92);

    border: 1px solid {COLORS["magenta_dim"]};

    border-radius: 18px;

    padding: 16px;

}}

QFrame#panel_playlist {{

    background-color: rgba(8, 8, 15, 0.92);

    border: 1px solid {COLORS["cyan_dim"]};

    border-radius: 18px;

    padding: 16px;

}}

QFrame#frame_controls {{

    background-color: rgba(8, 8, 15, 0.96);

    border: 1px solid {COLORS["cyan_dim"]};

    border-radius: 18px;

    padding: 12px;

}}

QFrame#frame_header {{

    background-color: {COLORS["bg_panel"]};

    border-bottom: 1px solid {COLORS["cyan_dim"]};

}}



/* ── PROGRESS BARS (HUD) ── */

QProgressBar {{

    background: {COLORS["bg_card"]};

    border: 1px solid {COLORS["cyan_dim"]};

    border-radius: 8px;

    height: 12px;

    text-align: center;

    color: transparent;

}}

QProgressBar::chunk {{

    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,

        stop:0 {COLORS["cyan"]}, stop:1 {COLORS["magenta"]});

    border-radius: 2px;

}}

QProgressBar#bar_gpu {{

    background: {COLORS["bg_card"]};

    border: 1px solid {COLORS["green_neon"]}44;

}}

QProgressBar#bar_gpu::chunk {{

    background: {COLORS["green_neon"]};

}}

"""

# Reemplazar dinámicamente los tokens {COLORS["key"]} por sus valores
for _k, _v in COLORS.items():
    MAIN_QSS = MAIN_QSS.replace('{COLORS["' + _k + '"]}', _v)

# Corregir llaves dobles que se usaron para escapar en ediciones previas
MAIN_QSS = MAIN_QSS.replace('{{', '{').replace('}}', '}')





# ────────────────────────────────────────────────────────────────────────────────

#  WIDGET DE PARTÍCULAS (Canvas animado)

# ────────────────────────────────────────────────────────────────────────────────

class ParticleCanvas(QWidget):

    """Fondo animado de partículas tipo lluvia de Matrix / red cyberpunk."""



    def __init__(self, parent=None):

        super().__init__(parent)

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.setAttribute(Qt.WA_NoSystemBackground)

        self.particles = []

        self.grid_offset = 0

        self._init_particles()



        self.timer = QTimer(self)

        self.timer.timeout.connect(self._update)

        self.timer.start(33)  # ~30 FPS



    def _init_particles(self):

        import random

        self.particles = [

            {

                "x": random.uniform(0, 1),

                "y": random.uniform(0, 1),

                "speed": random.uniform(0.0005, 0.002),

                "size": random.uniform(1, 3),

                "alpha": random.uniform(0.2, 0.9),

                "color": random.choice([

                    QColor(0, 240, 255),    # cyan

                    QColor(255, 0, 127),    # magenta

                    QColor(123, 47, 255),   # purple

                    QColor(0, 255, 65),     # green

                ])

            }

            for _ in range(60)

        ]



    def _update(self):

        self.grid_offset = (self.grid_offset + 1) % 40

        for p in self.particles:

            p["y"] += p["speed"]

            if p["y"] > 1.0:

                import random

                p["y"] = 0.0

                p["x"] = random.uniform(0, 1)

                p["alpha"] = random.uniform(0.2, 0.9)

        self.update()



    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)



        w, h = self.width(), self.height()



        # Grid cyberpunk perspectiva

        painter.setOpacity(0.06)

        pen = QPen(QColor(0, 240, 255), 1)

        painter.setPen(pen)

        spacing = 40

        for x in range(0, w + spacing, spacing):

            painter.drawLine(x, 0, x, h)

        for y in range(-self.grid_offset, h + spacing, spacing):

            painter.drawLine(0, y, w, y)



        # Partículas

        for p in self.particles:

            c = QColor(p["color"])

            c.setAlphaF(p["alpha"])

            painter.setOpacity(p["alpha"])

            painter.setPen(Qt.NoPen)

            painter.setBrush(QBrush(c))

            px = int(p["x"] * w)

            py = int(p["y"] * h)

            size = p["size"]

            painter.drawEllipse(int(px - size), int(py - size),

                                int(size * 2), int(size * 2))



            # Estela

            trail = QColor(p["color"])

            trail.setAlphaF(p["alpha"] * 0.2)

            painter.setBrush(QBrush(trail))

            trail_h = size * 8

            painter.drawEllipse(int(px - size * 0.5),

                                int(py - trail_h),

                                int(size), int(trail_h))



        painter.end()





# ────────────────────────────────────────────────────────────────────────────────

#  PANEL HUD DE MÉTRICAS

# ────────────────────────────────────────────────────────────────────────────────

class GamerHUDPanel(QFrame):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setObjectName("panel_hud")

        self.setFixedWidth(260)

        self._build_ui()



        # Timer para simular métricas en tiempo real

        self.metric_timer = QTimer(self)

        self.metric_timer.timeout.connect(self._update_metrics)

        self.metric_timer.start(1500)



    def _build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(12, 12, 12, 12)

        layout.setSpacing(10)



        title = QLabel("⚡ GAMER HUD")

        title.setObjectName("label_hud_title")

        layout.addWidget(title)



        self.metrics = {}

        metric_defs = [

            ("CPU",  "cpu_bar",  "bar_cpu",  None),

            ("RAM",  "ram_bar",  "bar_ram",  None),

            ("GPU",  "gpu_bar",  "bar_gpu",  "bar_gpu"),

            ("FPS",  "fps_val",  None,       None),

            ("CODEC","cod_val",  None,       None),

            ("HWDEC","hwd_val",  None,       None),

        ]



        for label_text, key, bar_obj, bar_id in metric_defs:

            row = QVBoxLayout()

            row.setSpacing(2)



            name_lbl = QLabel(label_text)

            name_lbl.setObjectName("label_metric_name")

            row.addWidget(name_lbl)



            if bar_obj:

                bar = QProgressBar()

                if bar_id:

                    bar.setObjectName(bar_id)

                bar.setRange(0, 100)

                bar.setValue(0)

                bar.setMaximumHeight(8)

                row.addWidget(bar)

                self.metrics[key] = bar

            else:

                val_lbl = QLabel("--")

                val_lbl.setObjectName("label_metric_val")

                val_lbl.setAlignment(Qt.AlignLeft)

                row.addWidget(val_lbl)

                self.metrics[key] = val_lbl



            layout.addLayout(row)



        layout.addStretch()



        sep = QLabel("── CODEC INFO ──")

        sep.setObjectName("label_metric_name")

        sep.setAlignment(Qt.AlignCenter)

        layout.addWidget(sep)



        self.codec_info = QLabel("Formato: --\nRes: --\nBitrate: --")

        self.codec_info.setObjectName("label_metric_name")

        self.codec_info.setWordWrap(True)

        layout.addWidget(self.codec_info)



    def _update_metrics(self):

        import random

        if "cpu_bar" in self.metrics:

            self.metrics["cpu_bar"].setValue(random.randint(3, 15))

        if "ram_bar" in self.metrics:

            self.metrics["ram_bar"].setValue(random.randint(45, 65))

        if "gpu_bar" in self.metrics:

            self.metrics["gpu_bar"].setValue(random.randint(20, 45))

        if "fps_val" in self.metrics:

            self.metrics["fps_val"].setText(f"{random.randint(58, 60)}")

        if "cod_val" in self.metrics:

            self.metrics["cod_val"].setText("H.264")

        if "hwd_val" in self.metrics:

            self.metrics["hwd_val"].setText("AUTO")



    def update_codec_info(self, fmt="--", res="--", bitrate="--"):

        self.codec_info.setText(f"Formato: {fmt}\nRes: {res}\nBitrate: {bitrate}")





class PlaylistPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("panel_playlist")
        self.setFixedWidth(260)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        title = QLabel("▶ PLAYLIST")
        title.setObjectName("label_hud_title")
        layout.addWidget(title)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar playlist...")
        layout.addWidget(self.search_input)

        self.list_widget = QListWidget()
        self.list_widget.setObjectName("playlist_list")
        self.list_widget.setAlternatingRowColors(True)
        layout.addWidget(self.list_widget, stretch=1)

        buttons = QHBoxLayout()
        self.btn_add = QPushButton("AGREGAR")
        self.btn_remove = QPushButton("ELIMINAR")
        self.btn_clear = QPushButton("LIMPIAR")
        self.btn_save = QPushButton("GUARDAR")
        self.btn_load = QPushButton("CARGAR")
        for btn in (self.btn_add, self.btn_remove, self.btn_clear, self.btn_save, self.btn_load):
            btn.setFixedHeight(34)
            buttons.addWidget(btn)
        layout.addLayout(buttons)

        self.count_label = QLabel("0 archivos en la lista")
        self.count_label.setObjectName("label_metric_name")
        layout.addWidget(self.count_label)

        info = QLabel("Guarda tu playlist en playlist.json y arrastra archivos al reproductor.")
        info.setObjectName("label_metric_name")
        info.setWordWrap(True)
        layout.addWidget(info)

        layout.addStretch()


class TutorialDialog(QDialog):
    def __init__(self, parent=None, simple=False):
        super().__init__(parent)
        self.setWindowTitle("Tutorial - Cómo usar VLC Gamer Cyberpunk")
        self.setModal(True)
        self.resize(580, 360)
        # Si se solicita modo simple, usamos lenguaje más directo y breve
        if simple:
            self.pages = [
                {"title": "¡Hola!", "text": "Esta app pone música y videos. Pulsa ENTRAR y diviértete."},
                {"title": "Abrir", "text": "Pulsa '📁 ABRIR ARCHIVO' para seleccionar un video o canción."},
                {"title": "Reproducir", "text": "Pulsa ▶ para reproducir y ⏸ para pausar. Usa VOL para el sonido."},
                {"title": "Playlist", "text": "Añade músicas con AGREGAR y toca una para empezar a escuchar."},
            ]
        else:
            self.pages = [
                {
                    "title": "Bienvenido al VLC Gamer Cyberpunk",
                    "text": "Este tutorial te mostrará cómo usar la aplicación paso a paso. Pulsa SIGUIENTE para continuar."
                },
                {
                    "title": "Paso 1: Abrir archivo",
                    "text": "Usa el botón 'ABRIR ARCHIVO' para seleccionar tu video o audio. Puedes reproducir MP4, MKV, MP3, WAV y más."
                },
                {
                    "title": "Paso 2: Controles de reproducción",
                    "text": "Usa ▶ para reproducir/pausar, ⏮ y ⏭ para saltar 10 segundos, y STOP para detener. Ajusta el volumen con el control VOL."
                },
                {
                    "title": "Paso 3: Playlist",
                    "text": "Añade archivos a la playlist con AGREGAR, selecciona elementos y pulsa GUARDAR para conservar tu lista. Haz doble clic en una canción para reproducirla."
                },
                {
                    "title": "Paso 4: HUD y estilo",
                    "text": "Activa o desactiva el HUD con TOGGLE HUD. El panel de métricas muestra CPU, RAM, GPU y códec actual."
                },
            ]
        self.page_index = 0
        self._build_ui()
        self._update_page()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.title = QLabel()
        self.title.setObjectName("label_title")
        layout.addWidget(self.title)

        self.text = QLabel()
        self.text.setWordWrap(True)
        self.text.setAlignment(Qt.AlignTop)
        self.text.setStyleSheet("color: #e0e8ff; font-size: 13px; margin: 8px;")
        layout.addWidget(self.text, stretch=1)

        btn_row = QHBoxLayout()
        self.btn_prev = QPushButton("ANTERIOR")
        self.btn_next = QPushButton("SIGUIENTE")
        self.btn_close = QPushButton("SALIR")
        self.btn_prev.clicked.connect(self._prev_page)
        self.btn_next.clicked.connect(self._next_page)
        self.btn_close.clicked.connect(self.accept)
        btn_row.addWidget(self.btn_prev)
        btn_row.addWidget(self.btn_next)
        btn_row.addWidget(self.btn_close)
        layout.addLayout(btn_row)

    def _update_page(self):
        page = self.pages[self.page_index]
        self.title.setText(page["title"])
        self.text.setText(page["text"])
        self.btn_prev.setEnabled(self.page_index > 0)
        self.btn_next.setVisible(self.page_index < len(self.pages) - 1)
        self.btn_close.setText("CERRAR" if self.page_index == len(self.pages) - 1 else "SALIR")

    def _next_page(self):
        if self.page_index < len(self.pages) - 1:
            self.page_index += 1
            self._update_page()

    def _prev_page(self):
        if self.page_index > 0:
            self.page_index -= 1
            self._update_page()


class WelcomeDialog(QDialog):
    """Diálogo inicial que explica brevemente para qué sirve la app."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bienvenida - VLC Gamer Cyberpunk")
        self.setModal(True)
        self.resize(520, 240)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        title = QLabel("¡Bienvenido a VLC Gamer Cyberpunk ⚡")
        title.setObjectName("label_title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        info = QLabel("Esta aplicación reproduce videos y música de forma sencilla. Abre archivos, crea playlists y toca para reproducir. Está diseñada para que hasta los niños la entiendan.")
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info, stretch=1)

        btn_row = QHBoxLayout()
        self.btn_show = QPushButton("VER PARA QUÉ SIRVE")
        self.btn_enter = QPushButton("ENTRAR")
        btn_row.addStretch()
        btn_row.addWidget(self.btn_show)
        btn_row.addWidget(self.btn_enter)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self.btn_show.clicked.connect(self._open_simple_tutorial)
        self.btn_enter.clicked.connect(self.accept)

    def _open_simple_tutorial(self):
        dlg = TutorialDialog(self, simple=True)
        dlg.exec_()


# ────────────────────────────────────────────────────────────────────────────────

#  VENTANA PRINCIPAL

# ────────────────────────────────────────────────────────────────────────────────

class VLCCyberpunkPlayer(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("VLC GAMER CYBERPUNK  ⚡  v1.0")

        self.setMinimumSize(900, 580)

        self.resize(1100, 680)



        # Estado

        self.current_file = None

        self.is_playing = False

        self.hud_visible = True

        self.cache_dir = Path("vlc_media_cache")

        self.cache_dir.mkdir(exist_ok=True)

        self.playlist_file = Path("playlist.json")

        self.playlist = []



        # VLC

        if VLC_AVAILABLE:

            self.vlc_instance = vlc.Instance(

                "--quiet",

                "--no-video-title-show",

                "--no-snapshot-preview",

            )

            self.media_player = self.vlc_instance.media_player_new()

        else:

            self.vlc_instance = None

            self.media_player = None



        self._build_ui()

        self._apply_styles()

        self._start_timers()

        self._load_playlist()
        # Mostrar un consejo inicial claro y amigable
        try:
            self.show_hint("Pulsa '📁 ABRIR ARCHIVO' para empezar 🎵", 6000)
        except Exception:
            pass




    # ──────────────────────────────────────────────

    #  CONSTRUCCIÓN DE UI

    # ──────────────────────────────────────────────

    def _build_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        root = QVBoxLayout(central)

        root.setContentsMargins(0, 0, 0, 0)

        root.setSpacing(0)



        # Header

        self._build_header(root)



        # Cuerpo principal: video + HUD

        body = QHBoxLayout()

        body.setContentsMargins(6, 6, 6, 0)

        body.setSpacing(6)



        # Canvas de partículas (fondo)

        self.canvas = ParticleCanvas(central)

        self.canvas.lower()



        # Frame de video

        self.frame_video = QFrame()

        self.frame_video.setObjectName("frame_video")

        self.frame_video.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.frame_video.setAcceptDrops(True)

        self.video_overlay = QLabel("ARRASTRA Y SUELTA ARCHIVOS AQUÍ", self.frame_video)
        self.video_overlay.setObjectName("label_video_hint")
        self.video_overlay.setAlignment(Qt.AlignCenter)
        self.video_overlay.setWordWrap(True)
        self.video_overlay.setGeometry(self.frame_video.rect())
        self.video_overlay.show()

        if VLC_AVAILABLE and self.media_player:

            if sys.platform == "win32":

                self.media_player.set_hwnd(int(self.frame_video.winId()))

            else:

                self.media_player.set_xwindow(int(self.frame_video.winId()))

        body.addWidget(self.frame_video, stretch=1)



        # Panel HUD

        self.hud = GamerHUDPanel()

        body.addWidget(self.hud, stretch=0)

        self.playlist_panel = PlaylistPanel()
        self.playlist_panel.list_widget.itemDoubleClicked.connect(self._play_selected_playlist_item)
        self.playlist_panel.search_input.textChanged.connect(self._search_playlist)
        self.playlist_panel.btn_add.clicked.connect(self._add_to_playlist)
        self.playlist_panel.btn_remove.clicked.connect(self._remove_selected_playlist_item)
        self.playlist_panel.btn_clear.clicked.connect(self._clear_playlist)
        self.playlist_panel.btn_save.clicked.connect(self._save_playlist)
        self.playlist_panel.btn_load.clicked.connect(self._load_playlist)
        body.addWidget(self.playlist_panel, stretch=0)

        root.addLayout(body, stretch=1)



        # Controles

        self._build_controls(root)

        self._build_status_bar(root)


        # Posicionar canvas

        central.resizeEvent = self._on_resize



    def _build_header(self, root):

        header = QFrame()

        header.setObjectName("frame_header")

        header.setFixedHeight(64)

        h_layout = QHBoxLayout(header)

        h_layout.setContentsMargins(14, 0, 14, 0)



        # Logo / título

        title = QLabel("◈ VLC GAMER CYBERPUNK")

        title.setObjectName("label_title")

        h_layout.addWidget(title)

        h_layout.addStretch()



        # Nombre de archivo

        self.label_filename = QLabel("[ Sin archivo ]")

        self.label_filename.setObjectName("label_filename")

        h_layout.addWidget(self.label_filename)

        h_layout.addStretch()



        # Botón HUD toggle

        btn_hud = QPushButton("⚡ TOGGLE HUD")

        btn_hud.setObjectName("btn_hud")

        btn_hud.clicked.connect(self._toggle_hud)

        h_layout.addWidget(btn_hud)

        btn_tutorial = QPushButton("❔ TUTORIAL")

        btn_tutorial.setObjectName("btn_hud")

        btn_tutorial.clicked.connect(self._show_tutorial)

        h_layout.addWidget(btn_tutorial)



        # Botón abrir

        btn_open = QPushButton("📁 ABRIR ARCHIVO")

        btn_open.setObjectName("btn_open")

        btn_open.clicked.connect(self._open_file)

        h_layout.addWidget(btn_open)



        root.addWidget(header)



    def _build_controls(self, root):

        frame = QFrame()

        frame.setObjectName("frame_controls")

        frame.setFixedHeight(120)

        ctrl = QVBoxLayout(frame)

        ctrl.setContentsMargins(10, 6, 10, 6)

        ctrl.setSpacing(6)



        # Barra de progreso

        seek_row = QHBoxLayout()

        self.label_time = QLabel("00:00 / 00:00")

        self.label_time.setObjectName("label_time")

        self.label_time.setFixedWidth(160)

        seek_row.addWidget(self.label_time)



        self.slider_seek = QSlider(Qt.Horizontal)

        self.slider_seek.setRange(0, 1000)

        self.slider_seek.sliderMoved.connect(self._seek)

        seek_row.addWidget(self.slider_seek)

        ctrl.addLayout(seek_row)



        # Botones de control

        btn_row = QHBoxLayout()

        btn_row.setSpacing(8)

        btn_row.addStretch()



        self.btn_prev = QPushButton("⏮")

        self.btn_prev.setFixedSize(48, 48)

        self.btn_prev.clicked.connect(self._prev_10s)

        btn_row.addWidget(self.btn_prev)



        self.btn_play = QPushButton("▶")

        self.btn_play.setObjectName("btn_play")

        self.btn_play.setFixedSize(60, 60)

        self.btn_play.clicked.connect(self._toggle_play)

        btn_row.addWidget(self.btn_play)



        self.btn_next = QPushButton("⏭")

        self.btn_next.setFixedSize(48, 48)

        self.btn_next.clicked.connect(self._next_10s)

        btn_row.addWidget(self.btn_next)



        self.btn_stop = QPushButton("⏹ STOP")

        self.btn_stop.clicked.connect(self._stop)

        btn_row.addWidget(self.btn_stop)



        btn_row.addStretch()



        # Volumen

        vol_label = QLabel("VOL")

        vol_label.setObjectName("label_metric_name")

        btn_row.addWidget(vol_label)



        self.slider_vol = QSlider(Qt.Horizontal)

        self.slider_vol.setRange(0, 100)

        self.slider_vol.setValue(80)

        self.slider_vol.setFixedWidth(120)

        self.slider_vol.valueChanged.connect(self._set_volume)

        btn_row.addWidget(self.slider_vol)



        ctrl.addLayout(btn_row)

        root.addWidget(frame)

    def _show_tutorial(self):
        dialog = TutorialDialog(self)
        dialog.exec_()

    def _load_playlist(self):
        self.playlist = []
        if self.playlist_file.exists():
            try:
                with open(self.playlist_file, "r", encoding="utf-8") as handle:
                    data = json.load(handle)
                if isinstance(data, list):
                    self.playlist = [str(Path(x)) for x in data if x]
            except Exception:
                self.playlist = []
        self._update_playlist_ui()

    def _save_playlist(self):
        try:
            with open(self.playlist_file, "w", encoding="utf-8") as handle:
                json.dump(self.playlist, handle, indent=2, ensure_ascii=False)
            QMessageBox.information(self, "Playlist guardada", "Tu playlist se guardó en playlist.json")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo guardar la playlist:\n{e}")

    def _add_to_playlist(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Agregar archivos a la playlist", "",
            "Media (*.mp4 *.mkv *.avi *.mov *.mp3 *.flac *.wav *.webm);;All (*)"
        )
        if paths:
            for path in paths:
                if path not in self.playlist:
                    self.playlist.append(path)
            self._update_playlist_ui()

    def _remove_selected_playlist_item(self):
        item = self.playlist_panel.list_widget.currentItem()
        if item:
            path = item.text()
            if path in self.playlist:
                self.playlist.remove(path)
            self._update_playlist_ui()

    def _play_selected_playlist_item(self, item):
        if item:
            self._play_file(item.text())

    def _clear_playlist(self):
        self.playlist.clear()
        self._update_playlist_ui()

    def _search_playlist(self, text):
        for i in range(self.playlist_panel.list_widget.count()):
            item = self.playlist_panel.list_widget.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def _update_playlist_ui(self):
        self.playlist_panel.list_widget.clear()
        for path in self.playlist:
            self.playlist_panel.list_widget.addItem(path)
        self.playlist_panel.count_label.setText(f"{len(self.playlist)} archivos en la lista")
        self.status_label.setText(f"Ready | {len(self.playlist)} archivos en playlist")

    def _play_file(self, path):
        if not path:
            return
        self.current_file = path
        self.label_filename.setText(Path(path).name[:40])
        
        if hasattr(self, 'video_overlay'):
            self.video_overlay.hide()
        
        if VLC_AVAILABLE and self.media_player:
            media = self.vlc_instance.media_new(path)
            self.media_player.set_media(media)
            self.media_player.play()
            self.is_playing = True
            self.btn_play.setText("⏸")
            self.hud.update_codec_info("AUTO", "--", "--")
            if path not in self.playlist:
                self.playlist.append(path)
                self._update_playlist_ui()





    # ──────────────────────────────────────────────

    #  BARRA DE ESTADO

    # ──────────────────────────────────────────────

    def _build_status_bar(self, root):

        status_frame = QFrame()

        status_frame.setObjectName("frame_status")

        status_frame.setFixedHeight(36)

        status_layout = QHBoxLayout(status_frame)

        status_layout.setContentsMargins(10, 0, 10, 0)

        status_layout.setSpacing(15)


        self.status_label = QLabel("Ready | 0 archivos en playlist")

        self.status_label.setObjectName("status_label")


        status_layout.addWidget(self.status_label)

        # Etiqueta de ayuda visible y legible para niños
        self.tip_label = QLabel("")
        self.tip_label.setObjectName("status_tip")
        self.tip_label.setStyleSheet("font-size:13px; color: #d8f7ff; margin-left:12px;")
        status_layout.addWidget(self.tip_label, stretch=1)

        status_layout.addStretch()

        self.duration_label = QLabel("00:00 / 00:00")
        self.duration_label.setObjectName("status_label")
        status_layout.addWidget(self.duration_label)


        root.addWidget(status_frame)


    # ──────────────────────────────────────────────

    #  ESTILOS Y EFECTOS GLOW

    # ──────────────────────────────────────────────

    def _apply_styles(self):

        self.setStyleSheet(MAIN_QSS)

        self._add_glow(self.btn_play, QColor(0, 240, 255), 18)
        # Animación sutil para llamar la atención de los niños sobre el botón play
        try:
            self._start_play_pulse()
        except Exception:
            pass



    def _add_glow(self, widget, color, radius):

        effect = QGraphicsDropShadowEffect()

        effect.setColor(color)

        effect.setBlurRadius(radius)

        effect.setOffset(0, 0)

        widget.setGraphicsEffect(effect)

    def _start_play_pulse(self):
        effect = self.btn_play.graphicsEffect()
        if not isinstance(effect, QGraphicsDropShadowEffect):
            effect = QGraphicsDropShadowEffect()
            effect.setColor(QColor(0, 240, 255))
            effect.setBlurRadius(18)
            effect.setOffset(0, 0)
            self.btn_play.setGraphicsEffect(effect)

        self._pulse_anim = QPropertyAnimation(effect, b"blurRadius")
        self._pulse_anim.setStartValue(12)
        self._pulse_anim.setEndValue(30)
        self._pulse_anim.setDuration(900)
        self._pulse_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self._pulse_anim.setLoopCount(-1)
        self._pulse_anim.start()

    def show_hint(self, text, timeout=4000):
        try:
            self.tip_label.setText(text)
            QTimer.singleShot(timeout, lambda: self.tip_label.setText(""))
        except Exception:
            pass



    # ──────────────────────────────────────────────

    #  TIMERS

    # ──────────────────────────────────────────────

    def _start_timers(self):

        self.ui_timer = QTimer(self)

        self.ui_timer.timeout.connect(self._update_ui)

        self.ui_timer.start(500)



    def _update_ui(self):

        if not VLC_AVAILABLE or not self.media_player:

            return

        length = self.media_player.get_length()

        pos = self.media_player.get_position()

        if length > 0:

            cur = int(pos * length / 1000)

            tot = length // 1000

            self.label_time.setText(

                f"{cur//60:02d}:{cur%60:02d} / {tot//60:02d}:{tot%60:02d}"

            )

            self.slider_seek.blockSignals(True)

            self.slider_seek.setValue(int(pos * 1000))

            self.slider_seek.blockSignals(False)



    # ──────────────────────────────────────────────

    #  ANIMACIÓN HUD (QPropertyAnimation)

    # ──────────────────────────────────────────────

    def _toggle_hud(self):

        self.hud_anim = QPropertyAnimation(self.hud, b"maximumWidth")

        self.hud_anim.setDuration(400)

        self.hud_anim.setEasingCurve(QEasingCurve.InOutQuint)

        if self.hud_visible:

            self.hud_anim.setStartValue(260)

            self.hud_anim.setEndValue(0)

            self.hud_visible = False

        else:

            self.hud_anim.setStartValue(0)

            self.hud_anim.setEndValue(260)

            self.hud_visible = True

        self.hud_anim.start()



    # ──────────────────────────────────────────────

    #  CONTROLES DE REPRODUCCIÓN

    # ──────────────────────────────────────────────

    def _open_file(self):

        path, _ = QFileDialog.getOpenFileName(

            self, "Abrir archivo multimedia", "",

            "Media (*.mp4 *.mkv *.avi *.mov *.mp3 *.flac *.wav *.webm);;All (*)"

        )

        if path:

            self._play_file(path)




    def _toggle_play(self):

        if not VLC_AVAILABLE or not self.media_player:

            return

        if self.is_playing:

            self.media_player.pause()

            self.btn_play.setText("▶")

        else:

            self.media_player.play()

            self.btn_play.setText("⏸")

        self.is_playing = not self.is_playing



    def _stop(self):

        if VLC_AVAILABLE and self.media_player:

            self.media_player.stop()

        self.is_playing = False

        self.btn_play.setText("▶")

        self.slider_seek.setValue(0)

        self.label_time.setText("00:00 / 00:00")



    def _seek(self, value):

        if VLC_AVAILABLE and self.media_player:

            self.media_player.set_position(value / 1000.0)



    def _prev_10s(self):

        if VLC_AVAILABLE and self.media_player:

            t = max(0, self.media_player.get_time() - 10000)

            self.media_player.set_time(t)



    def _next_10s(self):

        if VLC_AVAILABLE and self.media_player:

            t = self.media_player.get_time() + 10000

            self.media_player.set_time(t)



    def _set_volume(self, val):

        if VLC_AVAILABLE and self.media_player:

            self.media_player.audio_set_volume(val)



    # ──────────────────────────────────────────────

    #  DRAG & DROP

    # ──────────────────────────────────────────────

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if Path(path).exists():
                files.append(path)
        
        if files:
            # Agrega archivos a la playlist
            for file_path in files:
                if file_path not in self.playlist:
                    self.playlist.append(file_path)
            
            # Reproduce el primer archivo
            if files:
                self._play_file(files[0])
            
            self._update_playlist_ui()
            event.accept()
        else:
            event.ignore()

    # ──────────────────────────────────────────────

    #  CANVAS RESIZE

    # ──────────────────────────────────────────────

    def _on_resize(self, event):

        self.canvas.setGeometry(0, 0,

                                self.centralWidget().width(),

                                self.centralWidget().height())



    def resizeEvent(self, event):

        super().resizeEvent(event)

        if hasattr(self, "canvas"):

            self.canvas.setGeometry(0, 0,

                                    self.centralWidget().width(),

                                    self.centralWidget().height())



    # ──────────────────────────────────────────────

    #  CIERRE SEGURO (limpieza de caché)

    # ──────────────────────────────────────────────

    def closeEvent(self, event):

        # 1. Detener reproducción y liberar instancia VLC

        if VLC_AVAILABLE and self.media_player:

            self.media_player.stop()

            del self.media_player

        if VLC_AVAILABLE and self.vlc_instance:

            del self.vlc_instance



        # 2. Purgar caché efímera

        try:

            if self.cache_dir.exists():

                shutil.rmtree(self.cache_dir)

        except Exception as e:

            print(f"[WARN] No se pudo limpiar caché: {e}")



        # 3. Limpiar thumbnails temporales VLC en APPDATA (Windows)

        try:

            appdata = Path(os.environ.get("APPDATA", ""))

            vlc_cache = appdata / "vlc"

            if vlc_cache.exists():

                for f in vlc_cache.glob("*.cache"):

                    f.unlink(missing_ok=True)

        except Exception:

            pass



        print("[VLC Cyberpunk] Caché purgada. Sesión terminada limpiamente.")

        event.accept()





# ────────────────────────────────────────────────────────────────────────────────

#  ENTRY POINT

# ────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setApplicationName("VLC Gamer Cyberpunk")

    window = VLCCyberpunkPlayer()

    window.show()

    sys.exit(app.exec_()) 

