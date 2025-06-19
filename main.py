import sys
import cv2
import numpy as np
import mediapipe as mp
import pywavefront
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication
from OpenGL.GL import *
from OpenGL.GLU import *

OBJ_MODELS = ['media/gas_mask/gas_mask.obj', 'media/plague_doctor_mask_bloody/plague_doctor_mask_bloody.obj']

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

class GLWidget(QGLWidget):
    def __init__(self):
        super().__init__()
        self.model_index = 0
        self.models = []
        self.load_models()
        self.cap = cv2.VideoCapture(0)
        self.landmarks = None
        self.frame = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def load_models(self):
        self.models = []
        for path in OBJ_MODELS:
            scene = pywavefront.Wavefront(path, collect_faces=True)
            self.models.append(scene)
        print(f'Carregados {len(self.models)} modelos.')

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1)
        self.frame = frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            self.landmarks = results.multi_face_landmarks[0].landmark
        else:
            self.landmarks = None

        self.update()  # chama paintGL()

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glClearColor(0, 0, 0, 1)
        self.texture = glGenTextures(1)

        # Ativando iluminação simples
        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)
        # glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 1, 0])  # luz vindo da frente
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
        # glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])
        # glEnable(GL_COLOR_MATERIAL)
        # glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        # glShadeModel(GL_SMOOTH)


    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h if h != 0 else 1, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Desenha textura da webcam no fundo
        if self.frame is not None:
            self.draw_background(self.frame)

        # Posiciona câmera virtual
        gluLookAt(0,0,5, 0,0,0, 0,1,0)

        # glColor3f(1, 0, 0)  # vermelho
        # glutWireCube(1)     # se você tiver GLUT, ou desenhe manualmente

        # Desenha o modelo 3D alinhado com a face
        if self.landmarks:
            # Pegando ponto do nariz para exemplo (landmark 1)
            nose = self.landmarks[1]
            x = (nose.x - 0.5) * 2  # normalizando para -1 a 1
            y = -(nose.y - 0.5) * 2

            glPushMatrix()
            glTranslatef(x, y, -3)  # afasta o modelo da câmera (que está em z=0)
            glScalef(0.5, 0.5, 0.5)
            self.draw_model(self.models[self.model_index])
            glPopMatrix()


    def draw_background(self, frame):
        h, w, _ = frame.shape

        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, frame)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, w, 0, h, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex2f(0, 0)
        glTexCoord2f(1, 1)
        glVertex2f(w, 0)
        glTexCoord2f(1, 0)
        glVertex2f(w, h)
        glTexCoord2f(0, 0)
        glVertex2f(0, h)
        glEnd()

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def draw_model(self, model):
        glColor3f(1, 1, 1)  # cor branca, sem luz não precisa variar
        for mesh in model.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    vertex = model.vertices[vertex_i]
                    glVertex3f(*vertex)
            glEnd()

    def change_model(self):
        self.model_index = (self.model_index + 1) % len(self.models)
        print("Modelo trocado para:", OBJ_MODELS[self.model_index])

    def close(self):
        self.cap.release()
        self.makeCurrent()
        glDeleteTextures([self.texture])

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Face 3D Overlay com PyOpenGL')
        self.glWidget = GLWidget()
        self.btn_change = QPushButton('Trocar Modelo 3D')
        self.btn_change.clicked.connect(self.glWidget.change_model)

        layout = QVBoxLayout()
        layout.addWidget(self.glWidget)
        layout.addWidget(self.btn_change)
        self.setLayout(layout)
        self.resize(800, 600)

    def closeEvent(self, event):
        self.glWidget.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
