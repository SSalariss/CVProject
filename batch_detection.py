import os
import json
import cv2
from detection.yolo_detector import YOLODetector

def save_detection_results(image_name, boxes, output_path):
    results = []
    for box in boxes:
        x1, y1, x2, y2, conf, cls = box
        results.append({
            'image': image_name,
            'bbox': [float(x1), float(y1), float(x2), float(y2)],
            'confidence': float(conf),
            'class': int(cls)
        })
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

def draw_boxes(image, boxes):
    for box in boxes:
        x1, y1, x2, y2, conf, cls = box
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        label = f"Class {int(cls)} {conf:.2f}"
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image

def main():
    data_folder = 'data'
    output_folder = 'results'
    os.makedirs(output_folder, exist_ok=True)

    detector = YOLODetector('detection/model/yolov5s.pt')

    image_files = [f for f in os.listdir(data_folder)
                   if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

    for img_file in image_files:
        img_path = os.path.join(data_folder, img_file)
        print(f"Processing {img_file}...")

        boxes = detector.detect(img_path)

        json_path = os.path.join(output_folder, img_file + '.json')
        save_detection_results(img_file, boxes, json_path)

        # Visualizzazione (opzionale: disabilita se vuoi solo i file JSON)
        image = cv2.imread(img_path)
        if image is None:
            print(f"Immagine {img_file} non trovata o non leggibile.")
            continue
        image = draw_boxes(image, boxes)
        cv2.imshow("Detection", image)
        cv2.waitKey(500)  # mostra per 0.5 secondi

    cv2.destroyAllWindows()
    print("Batch detection completata.")

if __name__ == '__main__':
    main()
