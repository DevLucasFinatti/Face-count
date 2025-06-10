import cv2
import mediapipe as mp
import math
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('video.mp4')
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height  = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


def main():
  num_faces = 0
  with mp_face_mesh.FaceMesh(
      max_num_faces=40,
      refine_landmarks=True,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = face_mesh.process(image)

      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

      if results.multi_face_landmarks:
        if num_faces != len(results.multi_face_landmarks):
          num_faces = len(results.multi_face_landmarks)
          print(f"Número de rostos reconhecidos: {num_faces}")

        for face_landmarks in results.multi_face_landmarks:
          for idx, landmark in enumerate(face_landmarks.landmark):
            
            if not _normalized_to_pixel_coordinates(landmark.x, landmark.y, width, height):
              num_faces = num_faces - 1
              print(f"Número de rostos reconhecidos: {num_faces}")
              main()

          mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())

      # Flip the image horizontally for a selfie-view display.
      cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
      if cv2.waitKey(5) & 0xFF == ord('q'):
        break
    cap.release()

main()

          
          