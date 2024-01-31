import cvzone
from cv2 import WINDOW_NORMAL
from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.4, maxHands=1)



ax = 447
ay = 63


cx =250
cy =350

dx = 110
dy = 55
def get_finger(list):
    x=0
    y= 600


    for fram in list:
        if fram[1] <= y :
         y = fram[1]
         x = fram[0]
    return x,y




def draw_points(image,point_list):
    for points in point_list:
        cv2.circle(img, (points[0], points[1]), 20, (0, 255, 255), -1)


start = True
draw_point = []
distance = 200

while True:
    # Get image frame
    success, img = cap.read()

    # Find the hand and its landmarks
    img = detector.findHands(img)


    lmList2, bbox2 = detector.findPosition(img, draw=False)


    if bbox2:
        fing = detector.fingersUp()
        if fing.count(1) > 0:
            x,y = get_finger(lmList2)
            distance, img, info = detector.findDistance(8, 12, img,False)
            print("distance here",distance)
            if dx >= y >= dy and cx <= x <= cy :
                start = False

                if distance <= 23:
                    cv2.circle(img, (x, y), 20, (0, 255, 255), -1)
                    draw_point.append([x,y])
                    draw_points(img, draw_point)

                print("matching here",x,y)


            if start == False and distance <=100:
                x, y = get_finger(lmList2)
                draw_point.append([x, y])
                cv2.circle(img, (x, y), 20, (0, 255, 255), -1)

        else:
            draw_point = []



    draw_points(img, draw_point)
    cv2.namedWindow('Image', WINDOW_NORMAL)
    imz = cv2.resize(img, (960, 600))
    if start:
        cv2.circle(imz, (ax, ay), 63, (0, 255, 255), -1)

    cv2.imshow("Image", imz)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
