import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os
import asyncio

class DiffService:
    @staticmethod
    def compare_images(actual_path: str, expected_path: str, diff_output_path: str, run_id: str):
        """
        Compare two images and return similarity score and issues list.
        """
        if not os.path.exists(actual_path) or not os.path.exists(expected_path):
            raise FileNotFoundError("One of the images does not exist")

        img1 = cv2.imread(actual_path)
        img2 = cv2.imread(expected_path)
        
        # Ensure sizes match
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        
        h_min, w_min = min(h1, h2), min(w1, w2)
        img1 = cv2.resize(img1, (w_min, h_min))
        img2 = cv2.resize(img2, (w_min, h_min))
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Compute SSIM
        (score, diff) = ssim(gray1, gray2, full=True)
        diff = (diff * 255).astype("uint8")
        
        # Threshold the difference image
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        
        # Find contours
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        
        # Create overlay image
        overlay = img1.copy()
        
        issues = []
        for i, c in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(c)
            # Filter small changes
            if w * h < 100: 
                continue
                
            cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(overlay, str(i+1), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            issues.append({
                "id": i + 1,
                "bbox": {"x": x, "y": y, "width": w, "height": h},
                "area": w * h,
                "type": "visual_diff"
            })
            
        cv2.imwrite(diff_output_path, overlay)
        
        return {
            "score": score,
            "issues": issues,
            "diff_path": diff_output_path
        }

diff_service = DiffService()
