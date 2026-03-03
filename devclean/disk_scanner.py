import os

def scan_disk(root_path=None):
    if root_path is None:
        root_path = os.path.expanduser("~")  # Default to home directory
    
    large_files = []
    print(f"Scanning directory: {root_path}")
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Skip permission-denied directories
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                size = os.path.getsize(fp)
                if size > 50 * 1024 * 1024:  # files >50MB
                    large_files.append((fp, size))
            except (OSError, PermissionError):
                continue
    
    large_files.sort(key=lambda x: x[1], reverse=True)
    return large_files

if __name__ == "__main__":
    print("Scanning disk for large files...")
    results = scan_disk()
    if results:
        for f, s in results[:10]:
            print(f"{f}: {s/1024/1024:.2f} MB")
    else:
        print("No files larger than 50MB found.")