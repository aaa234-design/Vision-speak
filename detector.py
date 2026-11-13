from functools import lru_cache
from pathlib import Path

from ultralytics import YOLO

MODEL_NAME = "yolov8s-worldv2.pt"

OBJECTS = [
    "person", "car", "bus", "truck", "motorcycle", "bicycle", "scooter", "train", "airplane", "boat",
    "traffic light", "stop sign", "parking meter", "bench", "chair", "sofa", "table", "desk", "bed", "wardrobe",
    "cabinet", "bookshelf", "door", "window", "refrigerator", "microwave", "oven", "toaster", "washing machine", "fan",
    "air conditioner", "television", "monitor", "laptop", "desktop computer", "keyboard", "computer mouse", "mobile phone", "tablet", "remote control",
    "camera", "headphones", "speaker", "microphone", "printer", "watch", "clock", "lamp", "light bulb", "bottle",
    "cup", "mug", "glass", "plate", "bowl", "spoon", "fork", "knife", "pot", "pan",
    "water jug", "food container", "backpack", "handbag", "suitcase", "wallet", "umbrella", "book", "notebook", "paper",
    "pen", "pencil", "scissors", "ruler", "calculator", " stapler", "toothbrush", "comb", "hair dryer", "soap bottle",
    "shoe", "sandal", "shirt", "jacket", "trousers", "hat", "helmet", "glasses", "ball", "football",
    "cat", "dog", "bird", "horse", "cow", "sheep", "potted plant", "flower", "banana", "apple"
]
# Fix accidental leading whitespace in one prompt while retaining exactly 100 entries.
OBJECTS = [name.strip() for name in OBJECTS]
assert len(OBJECTS) == 100 and len(set(OBJECTS)) == 100


@lru_cache(maxsize=1)
def load_model():
    model = YOLO(MODEL_NAME)
    model.set_classes(OBJECTS)
    return model


def detect(image, confidence=0.25, image_size=640):
    model = load_model()
    results = model.predict(
        source=image,
        conf=float(confidence),
        imgsz=int(image_size),
        device="cpu",
        verbose=False,
    )
    return results[0]
