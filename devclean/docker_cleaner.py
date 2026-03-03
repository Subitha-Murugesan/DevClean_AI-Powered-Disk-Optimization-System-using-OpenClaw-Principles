import subprocess

def list_unused_images():
    result = subprocess.run(["docker", "images", "-f", "dangling=true", "-q"], capture_output=True, text=True)
    images = result.stdout.strip().split("\n")
    return [img for img in images if img]

if __name__ == "__main__":
    unused = list_unused_images()
    if unused:
        print("Unused Docker Images:")
        for img in unused:
            print(img)
    else:
        print("No unused Docker images found.")