import cv2
import numpy as np
import matplotlib.pyplot as plt

# 인터렉티브 모드, 그래프를 실시간 업데이트 시킬때 필요함(코드가 멈추지 않고 실행되게)
plt.ion()

# 웹캠은 왼쪽, 히스토그램은 오른쪽에 표시
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 웹캠 영상 출력용
frame_display = ax1.imshow(np.zeros((480, 640, 3), dtype=np.uint8))
ax1.set_title("Centerline Detection")
ax1.axis('off')

# HSV 히스토그램 출력용 (3개 채널)
ax2.set_title("HSV Histogram")
ax2.set_xlim([0, 256])
ax2.set_ylim([0, 5000]) 
lines = []
colors = ['r', 'g', 'b']
for i, color in enumerate(colors):
    line, = ax2.plot([], [], color=color)
    lines.append(line)
# 범례 생성(HSV 설명)
ax2.legend(['H', 'S', 'V'])

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

while True:
    ret, frame = cap.read() # ret은 프레임 읽기 성공 여부를 알려주는 불른값
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 검정색 선을 뽑기 위해 역이진화 (검정=255)
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    # Contour 검출
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 가장 큰 컨투어만 추출
    if contours:
        largest = max(contours, key=cv2.contourArea)
        cv2.drawContours(frame, [largest], -1, (0, 255, 0), 2)

        # 중심 좌표 추출 (모멘트)
        M = cv2.moments(largest)
        if M["m00"] != 0:  # M["m00"]은 contour의 면적을 의미 (중심좌표를 구할때 사용)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

    # HSV 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 히스토그램 계산 (H, S, V 각 채널 별로)
    hist_h = cv2.calcHist([hsv], [0], None, [256], [0, 256])
    hist_s = cv2.calcHist([hsv], [1], None, [256], [0, 256])
    hist_v = cv2.calcHist([hsv], [2], None, [256], [0, 256])

    # 정규화 (히스토그램 그래프가 너무 커서 적당히 줄이기)
    hist_h = cv2.normalize(hist_h, hist_h, 0, 3000, cv2.NORM_MINMAX)
    hist_s = cv2.normalize(hist_s, hist_s, 0, 3000, cv2.NORM_MINMAX)
    hist_v = cv2.normalize(hist_v, hist_v, 0, 3000, cv2.NORM_MINMAX)

    x = np.arange(256)
    lines[0].set_data(x, hist_h.flatten())
    lines[1].set_data(x, hist_s.flatten())
    lines[2].set_data(x, hist_v.flatten())

    ax2.set_xlim([0, 256])
    ax2.set_ylim([0, 3000])

    # RGB로 변환하여 실시간 업데이트
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_display.set_data(rgb_frame)

    fig.canvas.draw()
    fig.canvas.flush_events()

    # 창 닫으면 종료
    if plt.get_fignums() == []:
        break

cap.release()
cv2.destroyAllWindows()
