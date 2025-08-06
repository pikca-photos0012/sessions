import os
IMAGE_FOLDER = os.getenv("IMAGE_FOLDER", "generated_images")
SCORE_THRESHOLD = int(os.getenv("SCORE_THRESHOLD", 45))
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", 2))
IMAGEN_MODEL = os.getenv("IMAGEN_MODEL", "imagen-3.0-generate-002")
GENAI_MODEL = os.getenv("GENAI_MODEL", "gemini-2.0-flash")
