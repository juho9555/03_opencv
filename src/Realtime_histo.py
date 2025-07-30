import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.ion()  # 인터랙티브 모드 (실시간 업데이트용)

# Matplotlib 창 구성
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
frame_display = ax1.imshow(np.zeros((480, 640, 3), dtype=np.uint8))
ax1.set_title("Webcam (Center_line Contour)")
ax1.axis('off')

# HSV 히스토그램 초기화
colors = ['m', 'c', 'y']  # H: magenta, S: cyan, V: yellow
labels = ['Hue', 'Saturation', 'Value']
lines = [ax2.plot(np.zeros(256), color=color)[0] for color in colors]

ax2.set_title("HSV Histogram")
ax2.set_xlabel("Pixel Intensity")
ax2.set_ylabel("Frequency")
ax2.set_xlim(0, 256)
ax2.set_ylim(0, 1000)
ax2.legend(labels, loc='upper right')

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 마스크 생성 (검정색 범위): H, S, V 각각 임계값 조정
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])
    mask = cv2.inRange(hsv, lower_black, upper_black)

    # 윤곽선 찾기
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    roi = None

    if contours:
        # 가장 큰 contour 선택 (중앙선일 확률 높음)
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # ROI 추출
        roi = frame[y:y+h, x:x+w]

        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        h_channel, s_channel, v_channel = cv2.split(hsv_roi)

        for i, channel in enumerate([h_channel, s_channel, v_channel]):
            hist = cv2.calcHist([channel], [0], None, [256], [0, 256])
            lines[i].set_ydata(hist.ravel())

        # Y축 자동조절
        ax2.set_ylim(0, max([np.max(line.get_ydata()) for line in lines]) * 1.1)

    # 웹캠 이미지 업데이트
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_display.set_data(rgb_frame)
    fig.canvas.draw()
    fig.canvas.flush_events()

    if plt.get_fignums() == []:  # 창 닫으면 종료
        break

cap.release()
cv2.destroyAllWindows()
