import cv2
from cvzone.PoseModule import PoseDetector
import time

# TO BE SET DURING DEVELOPMENT
debugging = True

last_printed_time = time.time()

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

webcam = cv2.VideoCapture(0)
detector = PoseDetector()


face_x_coord, face_y_coord, face_width, face_height = 0, 0, 0, 0


# TO BE USED FOR ADDING A BLACK BOX AROUND THE FACE
def detect_bounding_box_for_faces(vid, show_bbox=False):
    global face_x_coord, face_y_coord, face_width, face_height
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for x, y, w, h in faces:
        face_x_coord, face_y_coord, face_width, face_height = x, y, w, h
        if show_bbox:
            cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)

    return faces


# while loop to continuously read frames from the webcam
while True:

    result, video_frame = webcam.read()  # read frames from the video

    if result is False:
        break  # terminate the loop if the frame is not read successfully

    # img = detector.findPose(video_frame)


    img, bboxInfo = detector.findPosition(video_frame)
    
    if bboxInfo is not None:
        
        keypoints = bboxInfo["keypoints"]
        
        left_shoulder = keypoints[11]
        right_shoulder = keypoints[12]
        left_hip = keypoints[23]
        right_hip = keypoints[24]

        # Unpacking coordinates for each keypoint
        x_left_shoulder, y_left_shoulder = left_shoulder
        x_right_shoulder, y_right_shoulder = right_shoulder
        x_left_hip, y_left_hip = left_hip
        x_right_hip, y_right_hip = right_hip

        # Printing the coordinates of the keypoints
        print("Left Shoulder:", left_shoulder)
        print("Right Shoulder:", right_shoulder)
        print("Left Hip:", left_hip)
        print("Right Hip:", right_hip)
        
            # Drawing lines between keypoints for demonstration
        cv2.line(video_frame, left_shoulder, left_hip, (0, 255, 0), 2)
        cv2.line(video_frame, right_shoulder, right_hip, (0, 255, 0), 2)

        # Drawing circles at keypoints for visualization
        cv2.circle(video_frame, left_shoulder, 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(video_frame, right_shoulder, 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(video_frame, left_hip, 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(video_frame, right_hip, 5, (0, 0, 255), cv2.FILLED)

        
    # TRUE TO SHOW BOX FOR DEBUGGING
    faces = detect_bounding_box_for_faces(
        video_frame, True
    )  # detect the bounding box around the face

    cv2.imshow("Video Frame", video_frame)  # display the frame
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    if debugging:
        # print every 3 second
        current_time = time.time()
        if current_time - last_printed_time >= 3:
            print(
                f"Face x: {face_x_coord}, Face y: {face_y_coord}, Face width: {face_width}, Face height: {face_height}"
            )
            last_printed_time = current_time

webcam.release()
cv2.destroyAllWindows()
