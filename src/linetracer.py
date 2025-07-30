import cv2
import numpy as np
import matplotlib.pylab as plt


cap = cv2.VideoCapture(0)  # 0번 카메라 연결

if cap.isOpened():
    while True:
        ret, frame = cap.read()  # 프레임 읽기
        if ret:
            flipped = cv2.flip(frame, 1)  # 좌우반전 (1: 좌우, 0: 상하, -1: 대칭)
            cv2.imshow('camera', flipped)  # 반전된 프레임 표시

            if cv2.waitKey(1) != -1:  # 아무 키나 누르면
                cv2.imwrite('photo.jpg', flipped)  # 반전된 프레임 저장
                break
        else:
            print('no frame!')
            break
else:
    print('no camera!')

# 이미지 읽기 및 출력
img = cv2.imread('./photo.jpg')
cv2.imshow('img', img)

# 히스토그램 계산 및 그리기
channels = cv2.split(img)
colors = ('b', 'g', 'r')
for (ch, color) in zip (channels, colors):
    hist = cv2.calcHist([ch], [0], None, [256], [0, 256])
    plt.plot(hist, color = color)

# 히스토그램 그래프 저장
plt.savefig('histo.jpg')

plt.show()



cap.release()
cv2.destroyAllWindows()