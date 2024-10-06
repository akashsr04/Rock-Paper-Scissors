import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow.keras as tf
import cv2 

import cv2
import mediapipe

cap = cv2.VideoCapture(0)
if not cap.isOpened():
  print('Camera Not Opened')
else:
  while True:
    ret, frame=cap.read()
    if not ret:
      print("Could not Capture Frame")
      break
    else:
      print(frame)
      cv2.namedWindow('LiveStream',cv2.WINDOW_NORMAL)
      cv2.imshow('LiveStream',frame)
    if cv2.waitKey(1) == ord('q'):
      break
print("Program execution finished")
cap.release()
cv2.destroyAllWindows()


