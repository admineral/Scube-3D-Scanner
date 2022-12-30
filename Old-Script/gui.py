#!/bin/env python3

from PyQt5.QtWidgets import *
import scanner
import upload

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()

def start_button ():
    folder = scanner.run()
    print(folder)
    scene = upload.upload_and_send(folder)
    print(f"Fertig mit scene {scene}")

btn_quit = QPushButton('Schließen')
btn_quit.clicked.connect(app.quit)

btn_run = QPushButton('Starten')
btn_run.clicked.connect(start_button)

layout.addWidget(btn_run)
layout.addWidget(btn_quit)

window.setLayout(layout)
window.showFullScreen()

app.exec_()
