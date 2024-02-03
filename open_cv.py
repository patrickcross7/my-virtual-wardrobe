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

    # lmList, bboxInfo = detector.findPosition(img)

    # TRUE TO SHOW BOX FOR DEBUGGING
    faces = detect_bounding_box_for_faces(
        video_frame, True
    )  # detect the bounding box around the face

    cv2.imshow("Video Frame", video_frame)  # display the frame
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    if debugging:
        # print every 1 second
        current_time = time.time()
        if current_time - last_printed_time >= 3:
            print(
                f"Face x: {face_x_coord}, Face y: {face_y_coord}, Face width: {face_width}, Face height: {face_height}"
            )
            last_printed_time = current_time

webcam.release()
cv2.destroyAllWindows()
