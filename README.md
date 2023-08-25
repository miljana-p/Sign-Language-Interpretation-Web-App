# A web application for sign language interpretation and training
A Flask-based web application that utilizes computer vision and machine learning to interpret sign language. Users can also train and test their sign language skills with the application.

![image](https://github.com/pyrite0/Sign-Language-Interpretation-Web-App/assets/142906679/43c1728d-c238-4a7e-8b89-f4ed5b26e293)

## Project Structure
This repository is organized into two main directories: [`app`](./app/) and [`database`](./database/).

**[`app`](./app/) Directory**

The app directory contains the core files for the Flask web application:

  - [`main.py`](./app/main.py): This is the primary entry point for the application.
  - [`train.py`](./app/train.py): Contains the functionalities for training tensorflow model used in application.
  - [`util.py`](./app/util.py): Houses utility functions essential for the overall operations of the application.

Inside the app directory, you'll also find the templates folder:

  - templates: This folder holds all the Flask HTML templates. It includes templates for the homepage ([`home.html`](./app/templates/home.html)), examples page ([`examples.html`](./app/templates/examples.html)), the interface for testing sign language skils ([`game.html`](./app/templates/game.html)), and the sign language interpretation page ([`interpretation.html`](./app/templates/interpretation.html)).

**[`database`](./database/) Directory**

The database directory focuses on the backend data storage and operations:

  - [`db-create.py`](./database/db-create.py): A script responsible for setting up the initial database structure.
  - [`db-populate.py`](./database/db-populate.py): Used for populating the database with initial data sets.
  - [`db-util.py`](./database/db-util.py): Provides utility functions for handling various database operations.
    
## Database Structure

Database is organized in three tables:

  - LanguageHighScore: Stores high scores for each language.
  - LanguageCharacters: Keeps track of characters for each language.
  - LanguageFrases: Stores recognized phrases for each language.

Within the database directory:

  - [`db-create.py`](./database/db-create.py): This script initializes the database and sets up the required tables.
  - [`db-populate.py`](./database/db-populate.py): Provides functions to populate the tables. While it's currently configured to populate with languages data for the application, it's flexible enough to handle other data sets.

The data stored in these tables will be utilized for training a TensorFlow model dedicated to sign language recognition.

## Model Training

**[`train.py`](./app/train.py)** is dedicated to training a sign language recognition model for different languages. Here's what it does:

  **Environment Setup:**
  
  - Initializes necessary modules like mediapipe, cv2, tensorflow, and utilities.
  - Retrieves the list of languages from the database.

  **Data Collection:**
  
  - For each language and their corresponding letters, directories are created to store captured images.
  - Uses mediapipe's holistic model to capture hand landmarks as the user shows different signs.
  - Each sign and its landmarks are saved to their corresponding directories. Visual feedback is provided to the user during the collection phase.

  **Data Loading & Preprocessing:**
  
  - Landmark data is loaded from the saved files.
  - Maps letters to numerical values for model training.
  - Splits data into training and (a very small) testing set.

  **Model Definition & Training:**
  
  - Defines a neural network model using tensorflow.keras.
  - The model consists of Dense layers and Dropout layers for regularization.
  - Trains the model using the training dataset and logs the training process.

  **Model Saving:**
      - After training, the model is saved for later use in the corresponding language's directory.
      
## Sign Language Interpretation
Application offers two primary modes for sign language interpretation: Image Interpretation and Real-time Video Interpretation

![image](https://github.com/pyrite0/Sign-Language-Interpretation-Web-App/assets/142906679/cddab37b-4f15-4803-94ad-4e8f076e6423)

1. Image Interpretation:

    How it Works:
   
      Users can upload an image that contains a sign gesture.
      The application processes the image, recognizes the sign, and then translates it into the corresponding character or word.
   

3. Real-time Video Interpretation:

    How it Works:
   
      The application accesses the device's camera to capture a live video feed.
      As users perform sign gestures, the application recognizes and interprets them in real-time, providing immediate feedback.
      Alongside the textual representation, users receive visual feedback highlighting the hand's key landmarks and the expected gesture movement.
   
## Sign Language Training

Application also aids in the learning and practice of Sign Language.

![image](https://github.com/pyrite0/Sign-Language-Interpretation-Web-App/assets/142906679/4c6a5494-d447-4019-927e-84858bb14bd9)

How it Works:
    
  As users practice their sign language gestures in front of the camera, the application provides real-time feedback on the accuracy and form of each sign.
  This immediate feedback mechanism allows learners to correct their gestures on the fly, ensuring effective learning.
