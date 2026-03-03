from disk_scanner import scan_disk
#from docker_cleaner import list_unused_images

def generate_report():
    print("\n=== DevClean Report ===\n")

    print("Top Large Files:")
    results = scan_disk()
    if results:
        for f, s in results[:5]:
            print(f"{f} - {s/1024/1024:.2f} MB")
    else:
        print("No large files found in home directory.")

    # docker_imgs = list_unused_images()
    # print("\nUnused Docker Images:")
    # if docker_imgs:
    #     for img in docker_imgs:
    #         print(img)
    # else:
    #     print("None found")

    print("\nSuggested Actions:")
    print("- Delete large unused files")
    print("- Remove dangling Docker images")

if __name__ == "__main__":
    generate_report()