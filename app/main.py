import random
from database.db_util import change_HighScore, get_HighScore, get_Signs, get_libraries, saveFrase
from flask import Flask, render_template, Response, jsonify, request
import cv2
import numpy as np
import mediapipe as mp
from util import load_model_from_folder, landmarksOnScreen, buildLandmarkArray
import time

app = Flask(__name__)
mp_holistics = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
status = False
cap = cv2.VideoCapture(0)

sequence = "Here Recognied Letters will be shown"

current_image=None

randomLetter=""
recognizedLetter=""
currentScore=0
timer=60
highScore=0
isTrainigOn=False


@app.route("/")
@app.route("/home")
def home():
    data = get_libraries()
    return render_template('home.html', data=data)

@app.route("/examples")
def examples():
    return render_template('examples.html')

@app.route("/train/<name>")
def train(name):
    global highScore
    highScore=get_HighScore(name)
    return render_template('game.html', name=name, highScore=highScore, randomLetter=randomLetter, recognizedLetter=recognizedLetter, currentScore=currentScore, timer=timer)

@app.route("/<name>")
def interpretation(name):
    return render_template('interpretation.html', name=name, sequence=sequence)

def camera_interpretation(name, letters, interval=3):
    letters+=['Blanko', 'Cancel', 'Save', 'Skip']
    model = load_model_from_folder(name)
    threshold = 0.9
    cap = cv2.VideoCapture(0)
    global sequence
    sequence = ""
    last = ""
    last_check_time = time.time()
    with mp_holistics.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            _, image = cap.read()
            current_time = time.time()
            points, landmarkArray = buildLandmarkArray(image, holistic)
            landmarksOnScreen(image, points)
            if current_time - last_check_time >= interval:
                res = model.predict(np.expand_dims(landmarkArray, axis=0))[0]
                if res[np.argmax(res)] >= threshold:
                    recognized_letter = letters[np.argmax(res)]
                    if last != recognized_letter:
                        if recognized_letter=='Blanko':
                            sequence += '_'
                        elif recognized_letter=='Cancel':
                            cv2.putText(image, 'CANCEL', (200, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
                            cv2.waitKey(3000)
                            sequence=''
                        elif recognized_letter=='Save':
                            cv2.putText(image, 'SAVE', (200, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
                            cv2.waitKey(3000)
                            saveFrase(name, sequence)
                            sequence=''
                        elif recognized_letter!='Skip'and recognized_letter!='R':
                            sequence+=recognized_letter
                        last = recognized_letter
                else:
                    recognized_letter = None
                last_check_time = current_time

            _, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
         
@app.route("/interpretationImage/<name>")
def start_image_interpretation(name):
    letters = get_Signs(name)
    return Response(image_interpretation(name, letters), mimetype='multipart/x-mixed-replace; boundary=frame')
   
def image_interpretation(name, letters):
    letters+=['Blanko', 'Cancel', 'Skip', 'Save']
    model = load_model_from_folder(name)
    threshold = 0.5
    global sequence
    sequence = ""
    global current_image
    print(type(current_image))
    with mp_holistics.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        points, landmarkArray = buildLandmarkArray(current_image, holistic)
        landmarksOnScreen(current_image, points)
        res = model.predict(np.expand_dims(landmarkArray, axis=0))[0]
        if res[np.argmax(res)] >= threshold:
            recognized_letter = letters[np.argmax(res)]
            sequence=recognized_letter
            print(recognized_letter)
        else:
            recognized_letter = None
        _, buffer = cv2.imencode('.jpg', current_image)
        current_image = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + current_image + b'\r\n')
        
def camera_game(name, letters, game_duration=60):
    randomLetters=letters.copy()
    letters+=['Blanko', 'Cancel', 'Skip', 'Save']
    global randomLetter, recognizedLetter, currentScore, timer, isTrainigOn
    isTrainigOn=True
    randomLetter = random.choice(randomLetters)
    model = load_model_from_folder(name)
    timer=game_duration
    currentScore = 0
    threshold = 0.9
    cap = cv2.VideoCapture(0)
    last_check_time = time.time()
    with mp_holistics.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened() and timer>0:
            _, image = cap.read()
            current_time = time.time()
            points, landmarkArray = buildLandmarkArray(image, holistic)
            landmarksOnScreen(image, points)
            if current_time - last_check_time >=1:
                timer = timer-1
                res = model.predict(np.expand_dims(landmarkArray, axis=0))[0]
                if res[np.argmax(res)] >= threshold:
                    recognizedLetter = letters[np.argmax(res)]
                    if recognizedLetter=='Skip':
                        cv2.putText(image, 'SKIP', (200, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
                        randomLetter = random.choice(randomLetters)
                    elif recognizedLetter !='Cancel'or recognizedLetter != 'Skip' or recognizedLetter != 'Save':
                        if recognizedLetter == randomLetter:
                            currentScore += 1
                            randomLetter = random.choice(randomLetters)
                else:
                    recognizedLetter = None
                last_check_time = time.time()
            
            _, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
    isTrainigOn=False
    change_HighScore(name, currentScore)
    
@app.route("/game/<name>")
def start_game(name):
    letters = get_Signs(name)
    return Response(camera_game(name, letters), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/interpretation/<name>")
def start_interpretation(name):
    letters = get_Signs(name)
    return Response(camera_interpretation(name, letters), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/change_image',  methods = ['POST'])
def change_image():
    global current_image
    image_data = request.data
    nparr = np.frombuffer(image_data, np.uint8)
    current_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return jsonify(ok=True)

@app.route('/get_sequence')
def get_sequence():
    global sequence
    return jsonify(sequence=sequence)

@app.route('/get_data')
def get_data():
    global randomLetter, recognizedLetter, currentScore, timer, highScore, isTrainigOn
    return jsonify(randomLetter=randomLetter, recognizedLetter=recognizedLetter, currentScore=currentScore, timer=timer, highScore=highScore, isTrainigOn=isTrainigOn)