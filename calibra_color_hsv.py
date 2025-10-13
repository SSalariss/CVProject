import cv2
import numpy as np

selected_colors = []

def mouse_callback(event, x, y, flags, param):
    global roi_start, roi_end, drawing, image, clone
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        roi_start = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        temp_image = clone.copy()
        cv2.rectangle(temp_image, roi_start, (x, y), (0,255,0), 2)
        cv2.imshow("Seleziona HSV", temp_image)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        roi_end = (x, y)
        x1, y1 = min(roi_start[0], roi_end[0]), min(roi_start[1], roi_end[1])
        x2, y2 = max(roi_start[0], roi_end[0]), max(roi_start[1], roi_end[1])
        roi = clone[y1:y2, x1:x2]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mean_hsv = hsv_roi.mean(axis=(0,1))
        selected_colors.append(mean_hsv)
        print(f"Colore medio HSV selezionato: {mean_hsv}")

if __name__ == "__main__":
    drawing = False
    roi_start, roi_end = None, None
    image = cv2.imread('data/test_image.jpg')
    if image is None:
        print("Immagine non trovata")
        exit()
    
    # Ridimensiona immagine per comodità
    max_width, max_height = 800, 600
    h, w = image.shape[:2]
    scale = min(max_width / w, max_height / h, 1.0)
    new_w, new_h = int(w * scale), int(h * scale)
    image = cv2.resize(image, (new_w, new_h))
    
    clone = image.copy()
    cv2.namedWindow("Seleziona HSV")
    cv2.setMouseCallback("Seleziona HSV", mouse_callback)
    print("Seleziona rettangoli con il mouse sulle divise (premi 'q' per uscire)...")

    while True:
        cv2.imshow("Seleziona HSV", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    print("\nColori medi HSV selezionati:")
    for i, c in enumerate(selected_colors):
        print(f"{i+1}: {c}")
