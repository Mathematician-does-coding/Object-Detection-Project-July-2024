import cv2

thres = 0.5 # Threshold to detect objects


#img = cv2.imread('humanface.png')
cap = cv2.VideoCapture(1)
cap.set(3,640)
cap.set(4,480)




classNames= []

classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssdlite_mobilenet_v3_large_320x320_coco.pbtxt'
weightsPath = 'frozen_inference_graph.pb'


net = cv2.dnn_DetectionModel(configPath, weightsPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean(127.5, 127.5, 127.5)
net.setInputSwapRB(True)

while True:
    success, img = cap.read()
    classIds, confs, bbox = net.detect(img, confThreshold=thres)
    print(classIds, bbox)

    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
            cv2.putText(img, classNames[classId - 1], (box[0] + 10, box[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, f'{confidence:.2f}', (box[0] + 50, box[1] + 50),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)


    cv2.imshow("Output",img)
    cv2.waitKey(1)