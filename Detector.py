import numpy as np
import cv2
import random
import time
from ultralytics import YOLO

def main():
    '''
    Train your model explicitly for n number of epochs using :
    yolo detect train data=path-to-your-data.yaml-file model=model-of-your-choice epochs=your-choice imgsz=preferably-640
    '''
    model = YOLO("runs\\detect\\train8\\weights\\best.pt") # Absolute path may be preferred
    classnames = ['Paper', 'Rock', 'Scissors']

    video_cap = cv2.VideoCapture('video.mp4')
    tutorial_cap = cv2.VideoCapture('tutorial.mp4')
    cap = cv2.VideoCapture(0)

    if not video_cap.isOpened() or not cap.isOpened() or not tutorial_cap.isOpened():
        print("Error: Video, tutorial, or camera feed could not be opened.")
        exit()

    ret, frame = cap.read()
    height, width, _ = frame.shape if ret else (0, 0, 0)
    q = False
    tutorial = True  
    hand_img = None
    your_score = 0
    cpu_score = 0
    while True:
        if tutorial:
            tutorial_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  
            while True:
                ret_tutorial, tutorial_frame = tutorial_cap.read()
                ret, frame = cap.read()

                if not ret_tutorial or not ret:
                    print("Error: Failed to read tutorial or camera feed.")
                    break

                tutorial_frame_resized = cv2.resize(tutorial_frame, (width, height))
                combined = np.hstack((tutorial_frame_resized, frame))
                cv2.imshow('Image', combined)

                if cv2.waitKey(1) == ord('t'):  # Press 't' to exit tutorial
                    tutorial = False
                    break

                if tutorial_cap.get(cv2.CAP_PROP_POS_FRAMES) == tutorial_cap.get(cv2.CAP_PROP_FRAME_COUNT):
                    tutorial_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        else:
            video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 
            while True:
                ret_video, video_frame = video_cap.read()
                ret, frame = cap.read() 

                if not ret_video or not ret:
                    print("Error: Failed to read video or camera feed.")
                    break

                video_frame_resized = cv2.resize(video_frame, (width, height))
                combined = np.hstack((video_frame_resized, frame))
                cv2.imshow('Image', combined)

                if cv2.waitKey(1) == ord('q'):
                    cap.release()
                    video_cap.release()
                    tutorial_cap.release()
                    cv2.destroyAllWindows()
                    q=True
                    break

                if video_cap.get(cv2.CAP_PROP_POS_FRAMES) == video_cap.get(cv2.CAP_PROP_FRAME_COUNT):
                    break
            if q:
                break
            #Class Prediction by Computer
            predicted_class = random.choice(classnames)
            detected_class = ''
            match_found = False
            detection_start_time = time.time()
            game_stat = 0 #1-Win ; 0:Loss ; 2:Draw
            while not match_found:
                ret, frame = cap.read()
                if not ret:
                    print("Live Capture Failed")
                    break

                results = model(frame, stream=True)
                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        # Class detection
                        cls = int(box.cls[0])
                        
                        detected_class = classnames[cls]
                        print(f"Computer : {predicted_class}")
                        print(f"You : {detected_class}")
                    
                        if predicted_class=='Paper':
                            
                            if detected_class=='Scissors':
                                game_stat = 1
                            elif detected_class=='Rock':
                                game_stat = 0
                            else:
                                game_stat = 2
                        elif predicted_class=='Scissors':
                        
                            if detected_class=='Rock':
                                game_stat = 1
                            elif detected_class=='Paper':
                                game_stat = 0
                            else:
                                game_stat = 2
                        elif predicted_class=='Rock':
                            if detected_class=='Paper':
                                game_stat = 1
                            elif detected_class=='Scissors':
                                game_stat = 0
                            else:
                                game_stat = 2
                        match_found=True
                        break
                    break
                if cv2.waitKey(1) == ord('q'):
                    cap.release()
                    video_cap.release()
                    tutorial_cap.release()
                    cv2.destroyAllWindows()
                    q = True
                    break
                if time.time() - detection_start_time > 6:
                    print("Detection timeout, restarting video loop.")
                    break
            
            if q:
                break
            cv2.imshow('Image', frame)
            color = (0,0,0)
            message = ''
            if game_stat==0:
                message = 'Lost'
                color = (0,0,255)
                cpu_score+=1
            elif game_stat==1:
                message = 'Won'
                color = (0,255,0)
                your_score+=1
            else:
                message = 'Draw'
                color = (255,0,0)
            if match_found:
                match_message = np.zeros_like(frame)
                cv2.putText(
                    match_message,
                    message,
                    ((width//2)-100, height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    4,
                    color,
                    4,
                )
                game_score = np.zeros_like(frame)
                cv2.putText(
                    game_score,
                    f'You : {detected_class} Computer : {predicted_class}',
                    ((width//2)-300, (height // 2) - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,255,255),
                    2,
                )
                cv2.imshow('Image', game_score)
                cv2.waitKey(3000)
                cv2.imshow('Image', match_message)
                cv2.waitKey(4000)  # Pause for 4 seconds

    score = np.zeros_like(frame)
    cv2.putText(
    score,
    f'''You : {your_score}  Computer : {cpu_score}''',
    ((width//2)-300, (height // 2) - 20),
    cv2.FONT_HERSHEY_DUPLEX,
    1,
    (0,255,0),
    2,
    )
    while True:
        cv2.imshow('Score',score)
        if cv2.waitKey(1) == ord('q'):

                    cv2.destroyAllWindows()
                    break
if __name__=='__main__':
    main()