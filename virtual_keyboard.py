import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

initHand = mp.solutions.hands
mainHand = initHand.Hands()
draw = mp.solutions.drawing_utils

keys = [["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P", "^", "$"],
        ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M", "%", "*"],
        ["W", "X", "C", "V", "B", "N", ",", ";", ":", "!", ".", "?"]]

finalText = ""
clicked = False

def handLandmarks(colorImg):
    landmarkList = []
    landmarkPositions = mainHand.process(colorImg)
    landmarkChek = landmarkPositions.multi_hand_landmarks
    if landmarkChek:
        for hand in landmarkChek:
            for index, landmark in enumerate(hand.landmark):  # Change here
                landmarkList.append([index, int(landmark.x*1280), int(landmark.y*720)])
    return landmarkList


def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size

        if button.text == "Space" or button.text == "Delete":
            cv2.rectangle(img, button.pos, (x + w, y + h), (64, 64, 64), cv2.FILLED)
            text_x = x + int(w * 0.35) - 50
            text_y = y + int(h * 0.65)
            cv2.putText(img, button.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
        else:
            cv2.rectangle(img, button.pos, (x + w, y + h), (64, 64, 64), cv2.FILLED)
            cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size

buttonList = []
for i in range(len(keys)):
    print(i)
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

buttonList.append(Button([50, 350], "Space", [885, 85]))
buttonList.append(Button([950, 350], "Delete", [285, 85]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    lmlist = handLandmarks(img)
    img = drawAll(img, buttonList)

    if lmlist:
        for button in buttonList:
            x,y = button.pos
            w, h = button.size

            if x<lmlist[8][1]<x+w and y<lmlist[8][2]<y+h:
                if button.text == "Space" or button.text == "Delete":
                    cv2.rectangle(img, button.pos, (x + w, y + h), (128, 128, 128), cv2.FILLED)
                    text_x = x + int(w * 0.35) - 50
                    text_y = y + int(h * 0.65)
                    cv2.putText(img, button.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                else:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (128, 128, 128), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                if lmlist[8][2] < lmlist[7][2] and lmlist[12][2] < lmlist[11][2] and not clicked:
                    if button.text == "Space" or button.text == "Delete":
                        cv2.rectangle(img, button.pos, (x + w, y + h), (192, 192, 192), cv2.FILLED)
                        text_x = x + int(w * 0.35) - 50
                        text_y = y + int(h * 0.65)
                        cv2.putText(img, button.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        if button.text == "Space":
                            finalText += " "
                        else:
                            finalText = finalText[:-1]
                    else:
                        cv2.rectangle(img, button.pos, (x + w, y + h), (192, 192, 192), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 25, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        finalText += button.text
                    clicked = True
                if lmlist[8][2] < lmlist[7][2] and lmlist[12][2] > lmlist[11][2]:
                    clicked = False

    cv2.rectangle(img, (50, 580), (1235, 680), (64, 64, 64), cv2.FILLED)
    cv2.putText(img, finalText, (60, 645), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    cv2.imshow('Virtual Keyboard', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()