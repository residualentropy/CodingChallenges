import sys

print("Loading OpenCV... ", end="")
sys.stdout.flush()
import cv2
print(f"version {cv2.__version__} loaded.")
