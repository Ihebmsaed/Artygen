# events/utils.py
from nudenet import NudeDetector

# Initialize the NudeDetector
detector = NudeDetector()

def is_image_appropriate(image):
    # Convert the image to bytes
    image_bytes = image.read()
    
    # Use the detector to check for nudity
    result = detector.detect(image_bytes)
    print(result)

    # Check if there are results and handle accordingly
    if not result:  # No results returned
        return True  # Assume safe if no detections

    # Check the confidence scores for each result
    for detection in result:
        if 'score' in detection and detection['score'] >= 0.5:  # Threshold for nudity
            return False  # Nudity detected

    return True  # No nudity detected
