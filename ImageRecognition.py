import torch
import sys
import cv2
import numpy as np
from pathlib import Path

sys.path.append("yolov5")

from yolov5.models.common import DetectMultiBackend
from yolov5.utils.general import non_max_suppression
from yolov5.utils.torch_utils import select_device
from yolov5.utils.augmentations import letterbox

# load model from local weights
weights = "weights/yolov5s.pt"
device = select_device("cpu")

model = DetectMultiBackend(weights, device=device)
stride = model.stride
names = model.names

def recognise(path: str, verbose=True):
    """
    Recognize objects in an image using YOLOv5
    
    Args:
        path: Path to image file
        verbose: Print detection results
        
    Returns:
        List of detections with class names and confidence scores
    """
    detections = []
    
    try:
        # load image
        img = cv2.imread(path)
        if img is None:
            print(f"Error: Could not load image from {path}")
            return detections

        # preprocess
        img_resized = letterbox(img, stride=stride, auto=True)[0]
        img_resized = img_resized.transpose((2,0,1))[::-1]
        img_resized = np.ascontiguousarray(img_resized)

        img_tensor = torch.from_numpy(img_resized).to(device)
        img_tensor = img_tensor.float() / 255
        img_tensor = img_tensor.unsqueeze(0)

        # inference
        pred = model(img_tensor)

        # apply NMS
        pred = non_max_suppression(pred)

        if verbose:
            print(f"\n📸 Image: {path}")
            print("Detected Objects:")
        
        # Process detections
        for det in pred[0]:
            x1, y1, x2, y2, conf, cls = det
            class_name = names[int(cls)]
            confidence = float(conf)
            
            detection_info = {
                'class': class_name,
                'confidence': confidence,
                'bbox': (float(x1), float(y1), float(x2), float(y2))
            }
            detections.append(detection_info)
            
            if verbose:
                print(f"  • {class_name}: {confidence:.2%} confidence")
        
        if not detections and verbose:
            print("  No objects detected")
            
    except Exception as e:
        print(f"Error during recognition: {e}")
    
    return detections