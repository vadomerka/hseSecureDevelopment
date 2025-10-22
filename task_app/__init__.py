import os

# Ensure uploads directory exists for tests and runtime
os.makedirs(os.path.join(os.getcwd(), "uploads"), exist_ok=True)
