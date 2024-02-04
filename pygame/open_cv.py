import cv2
from cvzone.PoseModule import PoseDetector
import time


# create a opencv class to get the body landmarks


class open_cv_camera:
    def __init__(self, videoInput=0):
        self.webcam = cv2.VideoCapture(0)
        self.last_printed_time = time.time()
        self.detector = PoseDetector()
        self.face_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        width = int(self.webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(f"width: {width}, height: {height}")

    def release(self):
        self.webcam.release()
        cv2.destroyAllWindows()

    def __del__(self):
        self.release()
        self.release()

    def get_body_landmarks(
        self, show_bbox=False, debugging=False, show_video_frame=False
    ):
        current_time = time.time()

        result, video_frame = self.webcam.read()  # read frames from the video

        if result is False:
            print("There was an error reading the frame")
            return  # terminate the method if the frame is not read successfully

        self.detector.findPose(video_frame, draw=False)

        lmList, bboxInfo = self.detector.findPosition(
            video_frame, draw=False, bboxWithHands=False
        )

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
            x_right_shoulder, y_right_shoulder = (
                right_shoulder[0],
                right_shoulder[1],
            )
            x_left_elbow, y_left_elbow = left_elbow[0], left_elbow[1]
            x_right_elbow, y_right_elbow = right_elbow[0], right_elbow[1]
            x_left_hip, y_left_hip = left_hip[0], left_hip[1]
            x_right_hip, y_right_hip = right_hip[0], right_hip[1]
            x_left_ankle, y_left_ankle = left_ankle[0], left_ankle[1]
            x_right_ankle, y_right_ankle = right_ankle[0], right_ankle[1]

            if show_video_frame:
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
                    video_frame,
                    (x_left_shoulder, y_left_shoulder),
                    50,
                    (0, 0, 255),
                    cv2.FILLED,
                )
                cv2.circle(
                    video_frame,
                    (x_right_shoulder, y_right_shoulder),
                    50,
                    (0, 0, 255),
                    cv2.FILLED,
                )
                cv2.circle(
                    video_frame,
                    (x_left_hip, y_left_hip),
                    50,
                    (0, 0, 255),
                    cv2.FILLED,
                )
                cv2.circle(
                    video_frame,
                    (x_right_hip, y_right_hip),
                    50,
                    (0, 0, 255),
                    cv2.FILLED,
                )
                cv2.circle(
                    video_frame,
                    (x_left_ankle, y_left_ankle),
                    20,
                    (255, 255, 255),
                    cv2.FILLED,
                )
                cv2.circle(
                    video_frame,
                    (x_right_ankle, y_right_ankle),
                    20,
                    (255, 255, 255),
                    cv2.FILLED,
                )
                cv2.circle(
                    video_frame,
                    (x_left_elbow, y_left_elbow),
                    20,
                    (255, 0, 255),
                    cv2.FILLED,
                )
                cv2.circle(
                    video_frame,
                    (x_right_elbow, y_right_elbow),
                    20,
                    (255, 0, 255),
                    cv2.FILLED,
                )

        if show_video_frame:
            cv2.imshow("Video Frame", video_frame)  # display the frame

        landmarks = {}
        if lmList:
            landmarks = {
                "left_shoulder": (x_left_shoulder, y_left_shoulder),
                "right_shoulder": (x_right_shoulder, y_right_shoulder),
                "left_elbow": (x_left_elbow, y_left_elbow),
                "right_elbow": (x_right_elbow, y_right_elbow),
                "left_hip": (x_left_hip, y_left_hip),
                "right_hip": (x_right_hip, y_right_hip),
                "left_ankle": (x_left_ankle, y_left_ankle),
                "right_ankle": (x_right_ankle, y_right_ankle),
            }
        return landmarks

    def detect_bounding_box_for_faces(self, show_bbox=False):

        gray_image = cv2.cvtColor(self.webcam, cv2.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(
            gray_image, 1.1, 5, minSize=(40, 40)
        )
        for x, y, w, h in faces:
            face_x_coord, face_y_coord, face_width, face_height = x, y, w, h
            if show_bbox:
                cv2.rectangle(self.webcam, (x, y), (x + w, y + h), (0, 255, 0), 4)

        return faces


# # FOR TESTING PURPOSES
# cv_obj = open_cv_camera()

# while True:
#     landmark = cv_obj.get_body_landmarks(show_video_frame=True)

#     print(landmark)

#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break
