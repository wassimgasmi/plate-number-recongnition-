from easyocr import Reader
import cv2

image = cv2.imread('cars/car6.jpg')
image = cv2.resize(image, (800, 600))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
edged = cv2.Canny(blur, 10, 200)
contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]

for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4:
        n_plate_cnt = approx
        break
(x, y, w, h) = cv2.boundingRect(n_plate_cnt)
license_plate = gray[y:y + h, x:x + w]

reader = Reader(['en'])
detection = reader.readtext(license_plate)
print(detection)

if len(detection) == 0:
    text = "Impossible to read the text from the license plate"
    cv2.putText(image, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 3)
    cv2.imshow('Image', image)
    cv2.waitKey(0)
else:
    cv2.drawContours(image, [n_plate_cnt], -1, (0, 255, 0), 3)
    text = f"{detection[0][1]} {detection[0][2] * 100:.2f}%"
    cv2.putText(image, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    # display the license plate and the output image
    print(text)
    cv2.imshow('license plate', license_plate)
    cv2.imshow('Image', image)
    cv2.waitKey(0)
