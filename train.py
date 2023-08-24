import os
import mediapipe as mp
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import TensorBoard
from db_util import get_libraries
from util import buildLandmarkArray, landmarksOnScreen

cap = cv2.VideoCapture(0)
mp_holistics = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

Languages= get_libraries()
for l in Languages:
    for letter in l[1]:
        try:
            os.makedirs(os.path.join('data_collection', l[0], letter))
        except:
            pass
    
    cap = cv2.VideoCapture(0)
    l[1]+=['Blanko', 'Cancel', 'Skip', 'Save']
    with mp_holistics.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        for letter in l[1]:
            for imageNum in range(51):
                _, image = cap.read()
                points, landmarkArray = buildLandmarkArray(image, holistic)

                landmarksOnScreen(image, points)
                
                cv2.putText(image, 'Images for ' + letter + ' num ' + str(imageNum), (30, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
                
                cv2.putText(image, 'Language: ' + l[0], (30, 70), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                if imageNum == 0:
                    cv2.putText(image, 'Get Ready', (200, 200),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4, cv2.LINE_AA)
                    cv2.imshow('Image with landmarks', image)
                    cv2.waitKey(3000)
                else:
                    cv2.waitKey(100)
                    cv2.imshow('Image with landmarks', image)
                    p = os.path.join('data_collection', l[0], letter, str(imageNum))
                    np.save(p, landmarkArray)
                    cv2.waitKey(600)

                if cv2.waitKey(1) == ord('q') or cv2.getWindowProperty('Image with landmarks', cv2.WND_PROP_VISIBLE) < 1:
                    break

    cap.release()
    cv2.destroyAllWindows()
    sequences, results = [], []

    result_map = {key: num for num, key in enumerate(l[1])}
    for letter in l[1]:
        for imgNum in range(50):
            res = np.load(os.path.join('data_collection', l[0], letter, "{}.npy".format(imgNum+1)))
            sequences.append(res)
            results.append(result_map[letter])

    x = np.array(sequences, object)
    y = to_categorical(results).astype(int)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.005)

    log_dir = os.path.join('Logs')
    tb_callback=TensorBoard(log_dir=log_dir)
    model = Sequential()
    model.add(Dense(256, activation='selu', input_dim=126))
    model.add(Dropout(0.5))
    model.add(Dense(128, activation='selu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='selu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(l[1]) + 4, activation='softmax'))

    model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

    x_train = x_train.astype(np.float32)
    x_test = x_test.astype(np.float32)

    model.fit(x_train, y_train, epochs=300, callbacks=[tb_callback])
    model.save(os.path.join('data_collection', l[0], "signLanguage.h5"))
