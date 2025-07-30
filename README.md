# OpenCV
## OpenCV에서 웹캠 사용 정리
### 웹캠 실행 후 프레임 확인하기
```
import cv2

cap = cv2.VideoCapture(0)               # 웹캠 실행
if cap.isOpened():
    while True:
        ret, img = cap.read()           # 다음 프레임 읽기
        if ret:
            cv2.imshow('camera', img)   # 다음 프레임 이미지 표시
            if cv2.waitKey(1) != -1:    # 1ms 동안 키 입력 대기 
                break                   # 아무 키라도 입력이 있으면 중지
        else:
            print('no frame')
            break
else:
    print("can't open camera.")
cap.release()                           # 자원 반납
cv2.destroyAllWindows()
```
**핵심 포인트**  
- cv2.VideoCapture(0): 0번 장치는 기본 웹캠
- cv2.imwrite(): 프레임 저장
- cv2.waitKey(1): 키보드 입력 대기 (ms 단위)

### 웹캠 + 히스토그램 표시
#### 1. 이미지 캡쳐
```
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()
```

#### 2. GrayScale 변환
```
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```  

#### 3. 히스토그램 계산
```
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
```

#### 4. 이미지 + 히스토그램 한 화면에 출력
```
fig, ax = plt.subplots(1, 2)
ax[0].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) # 이미지
ax[1].plot(hist, color='gray')                       # 히스토그램
plt.show()
```
  
### 실시간으로 웹캠과 히스토그램 확인하기
#### 1. 프레임 읽고 그레이스케일 변환 및 히스토그램 계산
```
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
```

#### 2. Matplotlib 서브플롯 구성
```
fig, ax = plt.subplots(1, 2)
```

#### 3. 영상 및 히스토그램 실시간 갱신
```
ax[0].cla()                                          # 이전 이미지 제거
ax[0].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
ax[0].set_title('Webcam')

ax[1].cla()                                          # 이전 그래프 제거
ax[1].plot(hist, color='gray')
ax[1].set_title('Grayscale Histogram')

plt.pause(0.001)                                     # 화면 업데이트
```

#### 4. 종료 조건 및 리소스 해제
```
if cv2.waitKey(1) == 27:                             # ESC 키 눌리면 종료
    break

cap.release()
cv2.destroyAllWindows()
plt.close()
```  

## ROI 정리
### Roi란?
ROI (Region of Interest)는 이미지나 영상에서 **관심 있는 부분**만 잘라내어 처리하는 것  
  
📌 **Region of Interest (ROI)** = 관심 영역

### Roi를 사용하는 이유
이미지 전체가 아니라 **일부만 처리하고 싶을 때** 사용한다.  
예를 들면:  

- 번호판만 추출해서 문자 인식
- 도로에서 차선 영역만 처리
- 얼굴만 인식해서 필터적용
- 불필요한 계산 줄이기 (속도 향상)

### OpenCV에서 Roi 사용법
```
roi = img[y:y+h, x:x+w]
```
- x, y: 시작 좌표 (왼쪽 위 모서리)
- w, h: 가로, 세로 길이
예를 들어:
```
img = cv2.imread('car.jpg')
roi = img[100:200, 300:400] # y = 100~200, x = 300~400 영역만 잘라냄
```

### Roi의 장점
불필요한 영역을 무시하기 때문에 처리속도 향상  
필요한 영역에만 집중하기 때문에 정확도 향상  
메모리 사용량 감소  

### Roi를 사용할 때 주의할 점
Roi는 **복사본이 아님**  
```
roi = img[y:y+h, x:x+w]
```
이렇게 사용하면 원본의 일부를 참조하기 때문에 복사본이 필요하면 <mark>.copy()</mark>를 사용해야 함

  
## Contour 정리  
### Contour란?
Contour란 이미지 내에서 **경계선**을 따라 연결된 점들의 집합  
  
📌 **Contour** = 윤곽선

### OpenCV에서 컨투어 검출 함수
<p align="center">
<pre><code> contours, hierarchy = cv2.findContours(image, mode, method)</code></pre>
</p>

- image: 흑백을 입력해야함 (HSV여도 하나의 채널(H, S, V)를 뽑아서 이진화 한 후 사용해야 함.
- mode: 컨투어 검색모드 (cv2.RETR_EXTERNAL - 외곽 윤곽선만 찾음)
- methodL 근사화 방법 (cv2.CHAIN_APPROX_SIMPLE - 꼭짓점만 저장)

### 컨투어의 활용
- 객체 인식 및 추적
- 모양 분석 (면적, 둘레, 중심 등)
- 영역 분할 및 특징 추출

### 컨투어를 이용한 주요 계산
- 면적 (Area): cv2.contourArea(contour)
- 둘레 (Perimeter): cv2.arcLenth(contour, True)
- 모먼트 (Moments): cv2.moments(contour)  
      - 중심 좌표(무게중심) 계산에 사용  
      - <pre><code>M = cv2.moments(contour)
cx = int(M['m10'] / M['m00'])
cy = int(M['m01'] / M['m00'])</code></pre>
