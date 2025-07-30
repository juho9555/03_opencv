import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.ion()  # 인터랙티브 모드 켜기

# Figure 및 subplot 구성
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# 웹캠 이미지용 subplot
frame_display = ax1.imshow(np.zeros((480, 640, 3), dtype=np.uint8))
ax1.set_title("Webcam")
ax1.axis('off')

# 히스토그램용 subplot 초기화
lines = []
colors = ['b', 'g', 'r']
for color in colors:
    line, = ax2.plot(np.zeros(256), color=color)
    lines.append(line)

# 히스토그램 축 설정
ax2.set_title("BGR Histogram")
ax2.set_xlabel("Pixel Intensity")  # x축 레이블
ax2.set_ylabel("Frequency")        # y축 레이블
ax2.set_xlim(0, 256)
ax2.set_ylim(0, 5000)  # 픽셀 개수 기준으로 설정 (적절히 조정 가능)

# 카메라 연결
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    frame = cv2.flip(frame, 1)  # 좌우 반전
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_display.set_data(rgb_frame)

    h, w, _ = frame.shape
    x, y = w // 2 - 50, h // 2 - 50
    roi = frame[y:y+100, x:x+100]
    
    # 각 채널(BGR)의 히스토그램 계산 (정규화 없이)
    for i, line in enumerate(lines):
        hist = cv2.calcHist([roi], [i], None, [256], [0, 256])
        hist = hist.ravel()
        line.set_ydata(hist)

    # y축 크기 자동 조정 (선택사항)
    ax2.set_ylim(0, max([np.max(line.get_ydata()) for line in lines]) * 1.1)

    fig.canvas.draw()
    fig.canvas.flush_events()

    if plt.get_fignums() == []:
        break

cap.release()
cv2.destroyAllWindows()
