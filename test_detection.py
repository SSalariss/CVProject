from detection.yolo_detector import YOLODetector

detector = YOLODetector('detection/model/yolov5s.pt')
boxes = detector.detect('data/test1.png')

print("Bounding boxes rilevate:")
for box in boxes:
    print(box)  # x1, y1, x2, y2, conf, class
