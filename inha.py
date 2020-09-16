import cv2
import numpy as np
import serial

PORT = 'COM30'
BaudRate = 9600
ARD= serial.Serial(PORT,BaudRate)


#가격리스트 DB open
cost = open("cost.txt", 'r')
#list화
costlist = [line.strip() for line in cost.readlines()]

#웹캠 구동
VideoSignal = cv2.VideoCapture(0)
# YOLO 가중치 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet("yolov2-food100.weights","yolov2-food100.cfg")

# YOLO NETWORK 재구성
classes = []
with open("obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]

while True:
    # 웹캠 시작
    ret, frame = VideoSignal.read()
    h, w, c = frame.shape

    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
    True, crop=False)
    YOLO_net.setInput(blob)
    outs = YOLO_net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:

        for detection in out:

            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                # 물체감지
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                dw = int(detection[2] * w)
                dh = int(detection[3] * h)
                # Rectangle coordinate
                x = int(center_x - dw / 2)
                y = int(center_y - dh / 2)
                boxes.append([x, y, dw, dh])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)
    #가격합산변수 초기화
    total=0
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            score = confidences[i]
            total+=int(costlist[class_ids[i]])
            print(label)
            print(total)
            # 경계상자와 클래스 정보 이미지에 입력
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
            cv2.putText(frame, label, (x, y - 20), cv2.FONT_ITALIC, 0.5, 
            (255, 255, 255), 1)
            
    #결과 이미지 show        
    cv2.imshow("YOLOv3", frame)
    
    if total!=0:
        Trans=str(total)
        Trans= Trans.encode('utf-8')
        ARD.write(Trans)
        while True :
            if ARD.readable() :
                break
            
    if cv2.waitKey(100) > 0:
        break
        
cost.close()
