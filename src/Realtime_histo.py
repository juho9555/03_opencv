import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.ion()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

frame_display = ax1.imshow(np.zeros((480, 640, 3), dtype=np.uint8))
ax1.set_title("Webcam")
ax1.axis('off')

# HSV 히스토그램용 subplot 초기화
lines = []
colors = ['m', 'c', 'y']  # H, S, V
labels = ['Hue', 'Saturation', 'Value']  # 범례용 텍스트

for color in colors:
    line, = ax2.plot(np.zeros(256), color=color)
    lines.append(line)

ax2.set_title("HSV Histogram")
ax2.set_xlabel("Pixel Intensity")
ax2.set_ylabel("Frequency")
ax2.set_xlim(0, 256)
ax2.set_ylim(0, 5000)

# 범례 추가
ax2.legend(labels, loc='upper right')

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_display.set_data(rgb_frame)

    h, w, _ = frame.shape
    x, y = w // 2 - 50, h // 2 - 50
    cv2.rectangle(frame, (x, y), (x+100, y+100), (0, 255, 0), 2)
    roi = frame[y:y+100, x:x+100]

    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    h_channel, s_channel, v_channel = cv2.split(hsv_roi)

    for i, channel in enumerate([h_channel, s_channel, v_channel]):
        hist = cv2.calcHist([channel], [0], None, [256], [0, 256])
        lines[i].set_ydata(hist.ravel())

    ax2.set_ylim(0, max([np.max(line.get_ydata()) for line in lines]) * 1.1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_display.set_data(rgb_frame)
    fig.canvas.draw()
    fig.canvas.flush_events()

    if plt.get_fignums() == []:
        break

cap.release()
cv2.destroyAllWindows()
