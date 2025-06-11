# British Sign Language Recognizer
This project aims to help people learn and practice British Sign Language.

# Instruction
To start the webpage, enter this in the terminal:

```
cd bslweb
pip install -r requirements.txt
python manage.py runserver
```

# System Architecture
When the webpage is started, video frames are caputred from the user's webcam and pass to the backend. The captured frames are then passed into the pre-trained model and generate predicted alphabet with confidence score. The predicted results and captured frames are finally passed to the frontend, and display to the users.

### Object Detection Model
YOLOv12l is used as the object detection model. It trained with British Sign Language hand gesture photos with the following hyper-parameters.

* Epochs: 400
* Image size: 416
* Batch size: 16
  
The training is run on Google Colab with A100 GPU for higher computational efficiency.

### Video Frames
Video frames are captured by OpenCV.

### Web Framework
Django is used as the web framework to hold the system on a webpage.

### Functional Buttons
HTML and JavaScript are used to handle the functional buttons. When the users select their desired alphabet, a corresponding hint picture will be shown below. The picture can be hide with the "Hide demonstration" button, or switch to a full alphabet chart wit the "All alphabet image" button. On the right, there is also a "Random alphabet" button.

### Random Alphabet Mode
When users click on the "Start Random Alphabet" button, alphabet will be randomly generated. When the detector predicted the user performing the correct gesture with confidence score of above 0.8, it will generate the next alphabet. Users are able to back to the default mode by clicking it again.

# Limitation and Future Work
The system has been tested on different individuals and get a promising result. However, YOLO has lack of the ability of handling dynamic input, which makes the system here not able to handle dynamic gesture like 'H' and 'J'. <br>

This limitation is planned to solve by using mediapipe with LSTM. By capturing the coordinate of the user's gestures and utilize LSTM with its power of learning sequential data, a full functional British Sign Language Learning Tool can be developed and implemented to the society.


