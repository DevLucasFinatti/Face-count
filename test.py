import cv2
import mediapipe as mp
import math
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


def main():
  num_faces = 0
  with mp_face_mesh.FaceMesh(
    max_num_faces=40,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
  ) as face_mesh:
      while cap.isOpened():
        success, image = cap.read()
        if not success:
          print("Ignoring empty camera frame.")
          continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        num_faces = 0  # zera a contagem antes de verificar

        if results.multi_face_landmarks:
          num_faces = len(results.multi_face_landmarks)

          for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
              image=image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_TESSELATION,
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )

        # fazer o espelhamento antes de renderizar o texto, se não fica espelhado tbm
        flipped_image = cv2.flip(image, 1)
        
        if num_faces > 0:
          cv2.putText(
            flipped_image,
            f'Rostos detectados: {num_faces}',
            (10, 30),                          # posição x y
            cv2.FONT_HERSHEY_SIMPLEX,          # fonte
            0.6,                               # escala 
            (0, 255, 0),                       # cor
            1,                                 # espessura
            cv2.LINE_AA
          )
        else:
          cv2.putText(
            flipped_image,
            f'Rostos detectados: {num_faces}',
            (10, 30),                          # posição x y
            cv2.FONT_HERSHEY_SIMPLEX,          # fonte
            0.6,                               # escala 
            (0, 0, 255),                       # cor
            1,                                 # espessura
            cv2.LINE_AA
          )

        cv2.imshow('MediaPipe Face Mesh', flipped_image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
          break

  cap.release()
  cv2.destroyAllWindows()

main()
