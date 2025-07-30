import cv2

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

cap.release()
cv2.destroyAllWindows()