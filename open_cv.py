import cv2

from cvzone.PoseModule import PoseDetector


face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

webcam = cv2.VideoCapture(0)
detector = PoseDetector()


# TO BE USED FOR ADDING A BLACK BOX AROUND THE FACE
def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for x, y, w, h in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return faces


# while loop to continuously read frames from the webcam
while True:

    result, video_frame = webcam.read()  # read frames from the video

    if result is False:
        break  # terminate the loop if the frame is not read successfully

    img = detector.findPose(video_frame)

    lmList, bboxInfo = detector.findPosition(img)

    cv2.imshow("Video Frame", img)  # display the frame
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

webcam.release()
cv2.destroyAllWindows()
