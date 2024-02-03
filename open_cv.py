import cv2
from cvzone.PoseModule import PoseDetector
import time

# TO BE SET DURING DEVELOPMENT
debugging = False

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
    current_time = time.time()

    result, video_frame = webcam.read()  # read frames from the video

    if result is False:
        print("There was an error reading the frame")
        break  # terminate the loop if the frame is not read successfully

    detector.findPose(video_frame, draw=False)

    lmList, bboxInfo = detector.findPosition(
        video_frame, draw=False, bboxWithHands=False
    )

    # if current_time - last_printed_time >= 5:
    #     print(lmList)
    #     print("---------------------------------------")
    #     last_printed_time = current_time

    if lmList:

        left_shoulder = lmList[11]
        right_shoulder = lmList[12]

        left_elbow = lmList[13]
        right_elbow = lmList[14]

        left_hip = lmList[23]
        right_hip = lmList[24]

        left_ankle = lmList[27]
        right_ankle = lmList[28]

        # Unpacking coordinates for each keypoint
        x_left_shoulder, y_left_shoulder = left_shoulder[0], left_shoulder[1]
        x_right_shoulder, y_right_shoulder = right_shoulder[0], right_shoulder[1]

        x_left_elbow, y_left_elbow = left_elbow[0], left_elbow[1]
        x_right_elbow, y_right_elbow = right_elbow[0], right_elbow[1]

        x_left_hip, y_left_hip = left_hip[0], left_hip[1]
        x_right_hip, y_right_hip = right_hip[0], right_hip[1]

        x_left_ankle, y_left_ankle = left_ankle[0], left_ankle[1]
        x_right_ankle, y_right_ankle = right_ankle[0], right_ankle[1]

        # Printing the coordinates of the keypoints

        # print("RELEVANT JOINT INFO")
        # print(" ")
        # print("Left Shoulder:", left_shoulder)
        # print("Right Shoulder:", right_shoulder)
        # print("Left Hip:", left_hip)
        # print("Right Hip:", right_hip)
        # print("Left Ankle:", left_ankle)
        # print("Right Ankle:", right_ankle)

        # Drawing lines between keypoints for demonstration
        cv2.line(
            video_frame,
            (x_left_shoulder, y_left_shoulder),
            (x_left_hip, y_left_hip),
            (0, 255, 0),
            2,
        )
        cv2.line(
            video_frame,
            (x_right_shoulder, y_right_shoulder),
            (x_right_hip, y_right_hip),
            (0, 255, 0),
            2,
        )
        cv2.line(
            video_frame,
            (x_left_hip, y_left_hip),
            (x_left_ankle, y_left_ankle),
            (255, 255, 0),
            5,
        )
        cv2.line(
            video_frame,
            (x_right_hip, y_right_hip),
            (x_right_ankle, y_right_ankle),
            (255, 255, 0),
            5,
        )
        cv2.line(
            video_frame,
            (x_left_shoulder, y_left_shoulder),
            (x_left_elbow, y_left_elbow),
            (255, 0, 255),
            10,
        )
        cv2.line(
            video_frame,
            (x_right_shoulder, y_right_shoulder),
            (x_right_elbow, y_right_elbow),
            (255, 0, 255),
            10,
        )

        # Drawing circles at keypoints for visualization
        cv2.circle(
            video_frame, (x_left_shoulder, y_left_shoulder), 50, (0, 0, 255), cv2.FILLED
        )
        cv2.circle(
            video_frame,
            (x_right_shoulder, y_right_shoulder),
            50,
            (0, 0, 255),
            cv2.FILLED,
        )
        cv2.circle(video_frame, (x_left_hip, y_left_hip), 50, (0, 0, 255), cv2.FILLED)
        cv2.circle(video_frame, (x_right_hip, y_right_hip), 50, (0, 0, 255), cv2.FILLED)
        cv2.circle(
            video_frame, (x_left_ankle, y_left_ankle), 20, (255, 255, 255), cv2.FILLED
        )
        cv2.circle(
            video_frame, (x_right_ankle, y_right_ankle), 20, (255, 255, 255), cv2.FILLED
        )
        cv2.circle(
            video_frame, (x_left_elbow, y_left_elbow), 20, (255, 0, 255), cv2.FILLED
        )
        cv2.circle(
            video_frame, (x_right_elbow, y_right_elbow), 20, (255, 0, 255), cv2.FILLED
        )

    # TRUE TO SHOW BOX FOR DEBUGGING
    faces = detect_bounding_box_for_faces(
        video_frame, False
    )  # detect the bounding box around the face

    cv2.imshow("Video Frame", video_frame)  # display the frame

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    if debugging:
        # print every 3 second

        if current_time - last_printed_time >= 3:
            print(
                f"Face x: {face_x_coord}, Face y: {face_y_coord}, Face width: {face_width}, Face height: {face_height}"
            )
            last_printed_time = current_time

webcam.release()
cv2.destroyAllWindows()
