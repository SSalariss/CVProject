import cv2
import numpy as np
from detection.yolo_detector import YOLODetector

# Colori medi HSV di squadra e arbitro (rosso, blu, giallo)
color_team_a = np.array([0, 200, 200])      # rosso
color_team_b = np.array([120, 200, 200])    # blu
color_referee = np.array([30, 200, 200])    # giallo

distance_threshold = 60           # soglia classificazione colore
green_threshold = 0.3            # soglia percentuale pixel verdi per portiere

def resize_image(image, max_width=800, max_height=600):
    h, w = image.shape[:2]
    scale = min(max_width / w, max_height / h, 1.0)
    new_w, new_h = int(w * scale), int(h * scale)
    image_resized = cv2.resize(image, (new_w, new_h))
    return image_resized, scale

def is_green_present(roi_bgr, threshold=green_threshold):
    hsv_roi = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv_roi, lower_green, upper_green)
    green_ratio = np.sum(mask > 0) / mask.size
    return green_ratio > threshold

def get_mean_hsv(image, box):
    x1, y1, x2, y2 = [int(v) for v in box[:4]]
    roi = image[y1:y2, x1:x2]
    if roi.size == 0:
        return None, roi
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mean_color = hsv_roi.mean(axis=(0,1))
    return mean_color, roi

def classify_color(mean_hsv):
    if mean_hsv is None:
        return ('unknown', np.inf)
    distances = {
        'team_a': np.linalg.norm(mean_hsv - color_team_a),
        'team_b': np.linalg.norm(mean_hsv - color_team_b),
        'referee': np.linalg.norm(mean_hsv - color_referee),
    }
    min_class = min(distances, key=distances.get)
    min_dist = distances[min_class]
    if min_dist > distance_threshold:
        return ('unknown', min_dist)
    else:
        return (min_class, min_dist)

def draw_boxes(image, boxes, classes):
    color_map = {
        'team_a': (0,255,0),
        'team_b': (255,0,0),
        'referee': (0,255,255),
        'goalkeeper': (0,128,0),
        'unknown': (128,128,128)
    }
    for box, cls in zip(boxes, classes):
        x1, y1, x2, y2 = [int(v) for v in box[:4]]
        color = color_map.get(cls, (128,128,128))
        label = cls.upper()
        cv2.rectangle(image, (x1,y1), (x2,y2), color, 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    return image

def main():
    img_path = "data/test_image.jpg"
    detector = YOLODetector('detection/model/yolov5s.pt')

    image = cv2.imread(img_path)
    if image is None:
        print("Immagine non trovata.")
        return

    image_resized, scale = resize_image(image)
    
    boxes = detector.detect(image_resized)

    classes = []
    for box in boxes:
        mean_hsv, roi = get_mean_hsv(image_resized, box)
        # Se la ROI contiene abbastanza verde, assegna portiere
        if roi.size > 0 and is_green_present(roi):
            cls = 'goalkeeper'
        else:
            cls, dist = classify_color(mean_hsv)
        classes.append(cls)

    image_out = draw_boxes(image_resized, boxes, classes)

    cv2.imshow("Classificazione con filtro verde", image_out)
    print("Premi un tasto per chiudere la finestra...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
