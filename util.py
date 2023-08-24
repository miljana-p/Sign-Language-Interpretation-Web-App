import cv2
import numpy as np
import os
import tensorflow
import mediapipe as mp

mp_holistics = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

def load_model_from_folder(name):
    folder_path = os.path.join('data_collection', name)
    model_path = os.path.join(folder_path, 'signLanguage.h5')
    if not os.path.exists(model_path):
        return None
    model = tensorflow.keras.models.load_model(model_path)
    return model

def landmarksOnScreen(image, points):
    mp_drawing.draw_landmarks(image, points.left_hand_landmarks, mp_holistics.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=3),
                              mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))
    mp_drawing.draw_landmarks(image, points.right_hand_landmarks, mp_holistics.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=3),
                              mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2))

def buildLandmarkArray(image, holistic):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    points = holistic.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    landmarkArrayLeft = np.zeros(21 * 3)
    if points.left_hand_landmarks:
        landmarkArrayLeft = (
            np.array(list(map(lambda lm: [lm.x, lm.y, lm.z], points.left_hand_landmarks.landmark)))).flatten()
    landmarkArrayRight = np.zeros(21 * 3)
    if points.right_hand_landmarks:
        landmarkArrayRight = (
            np.array(list(map(lambda lm: [lm.x, lm.y, lm.z], points.right_hand_landmarks.landmark)))).flatten()
    return points, np.concatenate([landmarkArrayRight, landmarkArrayLeft])