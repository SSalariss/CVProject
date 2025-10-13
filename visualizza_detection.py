import cv2
import numpy as np
from detection.yolo_detector import YOLODetector

def resize_image(image, max_width=800, max_height=600):
    h, w = image.shape[:2]
    scale = min(max_width / w, max_height / h)
    if scale < 1.0:
        image = cv2.resize(image, (int(w * scale), int(h * scale)))
    return image, scale

def draw_boxes(image, boxes, scale=1.0):
    for box in boxes:
        x1, y1, x2, y2, conf, cls = box
        x1, y1, x2, y2 = int(x1 * scale), int(y1 * scale), int(x2 * scale), int(y2 * scale)
        label = f"Class {int(cls)} {conf:.2f}"
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
    return image

if __name__ == "__main__":
    img_path = "data/test1.png"
    detector = YOLODetector('detection/model/yolov5s.pt')
    boxes = detector.detect(img_path)

    image = cv2.imread(img_path)
    image_resized, scale = resize_image(image)

    image_with_boxes = draw_boxes(image_resized, boxes, scale)

    cv2.imshow("Detection YOLO", image_with_boxes)
    print("Premi un tasto per chiudere la finestra...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
