import torch

class YOLODetector:
    def __init__(self, model_path):
        # Carica modello yolov5s dal percorso specificato
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

    def detect(self, image_path):
        results = self.model(image_path)
        # Restituisce la lista di bounding box in formato numpy
        return results.xyxy[0].cpu().numpy()
