import cv2
import numpy as np

img = cv2.imread('../img/bad_rect.png')
img2 = img.copy()

# 그레이 스케일
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 스레시홀드로 바이너리 이미지를 만들어서 검은배경에 흰색 전경으로 반전시키기
ret, th = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)

#가장 바깥쪽 컨투어에 대해 모든 좌표 반환
contours, hierarchy = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

contour = contours[0]

# 전체 둘레의 0.05로 오차범위 지정
epsilon = 0.05 * cv2.arcLength(contour, True)
# 근사 컨투어 계산
approx = cv2.approxPolyDP(contour, epsilon, True)

cv2.drawContours(img, [contour], -1, (0, 255, 0), 3)
cv2.drawContours(img2, [approx], -1, (0, 255, 0), 3)


# 결과 출력 
cv2.imshow('contour', img)
cv2.imshow('approx', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()