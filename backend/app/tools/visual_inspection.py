"""Visual inspection tool for UI validation."""

from typing import Dict, Any
import cv2
import numpy as np
from PIL import Image
import io
import base64
from pathlib import Path
import tempfile

class VisualInspectionTool:
    """Tool for visual inspection and validation."""

    async def execute(
        self,
        image_data: str,
        validation_type: str = "screenshot",
        reference_image: str = None,
        threshold: float = 0.8
    ) -> Dict[str, Any]:
        """Execute visual inspection."""
        try:
            if validation_type == "screenshot":
                return await self._validate_screenshot(image_data)
            elif validation_type == "comparison":
                return await self._compare_images(image_data, reference_image, threshold)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported validation type: {validation_type}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _validate_screenshot(self, image_data: str) -> Dict[str, Any]:
        """Validate screenshot quality and content."""
        try:
            # Convert base64 to image
            image = self._base64_to_image(image_data)
            
            # Basic image quality checks
            checks = {
                "resolution": self._check_resolution(image),
                "blur_detection": self._check_blur(image),
                "contrast": self._check_contrast(image)
            }
            
            success = all(check["success"] for check in checks.values())
            return {
                "success": success,
                "checks": checks
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _compare_images(
        self,
        image_data: str,
        reference_data: str,
        threshold: float
    ) -> Dict[str, Any]:
        """Compare two images for similarity."""
        try:
            # Convert base64 to images
            image = self._base64_to_image(image_data)
            reference = self._base64_to_image(reference_data)
            
            # Ensure same size
            if image.size != reference.size:
                image = image.resize(reference.size)
            
            # Convert to numpy arrays
            img_array = np.array(image)
            ref_array = np.array(reference)
            
            # Calculate similarity
            similarity = self._calculate_similarity(img_array, ref_array)
            
            return {
                "success": similarity >= threshold,
                "similarity": similarity,
                "threshold": threshold
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _base64_to_image(self, base64_str: str) -> Image.Image:
        """Convert base64 string to PIL Image."""
        image_data = base64.b64decode(base64_str)
        return Image.open(io.BytesIO(image_data))

    def _check_resolution(self, image: Image.Image) -> Dict[str, Any]:
        """Check image resolution."""
        width, height = image.size
        min_width = 800
        min_height = 600
        
        return {
            "success": width >= min_width and height >= min_height,
            "width": width,
            "height": height,
            "message": f"Resolution: {width}x{height}"
        }

    def _check_blur(self, image: Image.Image) -> Dict[str, Any]:
        """Check image blur level."""
        # Convert to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Calculate Laplacian variance
        blur_value = cv2.Laplacian(gray, cv2.CV_64F).var()
        threshold = 100
        
        return {
            "success": blur_value >= threshold,
            "blur_value": blur_value,
            "threshold": threshold,
            "message": f"Blur value: {blur_value}"
        }

    def _check_contrast(self, image: Image.Image) -> Dict[str, Any]:
        """Check image contrast."""
        # Convert to grayscale numpy array
        gray = np.array(image.convert('L'))
        
        # Calculate contrast
        contrast = gray.std()
        threshold = 30
        
        return {
            "success": contrast >= threshold,
            "contrast": contrast,
            "threshold": threshold,
            "message": f"Contrast value: {contrast}"
        }

    def _calculate_similarity(
        self,
        image1: np.ndarray,
        image2: np.ndarray
    ) -> float:
        """Calculate similarity between two images."""
        # Convert to grayscale
        gray1 = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_RGB2GRAY)
        
        # Calculate SSIM (Structural Similarity Index)
        score = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)[0][0]
        return float(score) 