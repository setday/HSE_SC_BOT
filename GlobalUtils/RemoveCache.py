import os

if __name__ == "__main__":
    to_remove = []  # Remove all python cache files
    for root, dirs, files in os.walk("."):
        for dir in dirs:
            if dir == "__pycache__":
                to_remove.append(os.path.join(root, dir))
    for dir in to_remove:
        for root, dirs, files in os.walk(dir):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir(dir)
