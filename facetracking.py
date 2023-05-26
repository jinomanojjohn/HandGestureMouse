import cv2
import mediapipe as mp


class faceTrack():
    def __init__(self, model=1, confidence=0.5):
        
        self.model = model
        self.confidence = confidence

        self.mpface = mp.solutions.face_detection.FaceDetection(
            model_selection=self.model,
            min_detection_confidence=self.confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def findFace(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.mpface.process(imgRGB)
        # print(results.multi_hand_landmarks)
        image_input = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # get results
        results = self.mpface.process(image_input)

        if not results.detections:
            print('No faces detected.')
            return False
        else:
            # for detection in results.detections:
            #     self.mpDraw.draw_detection(img, detection)
            return True
        # return img


# def main():
#     cap = cv2.VideoCapture(0)
#     detector = faceTrack()
#     while True:
#         success, img = cap.read()
#         img = detector.findFace(img)
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)


# if __name__ == "__main__":
#     main()