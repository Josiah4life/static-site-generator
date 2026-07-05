import os
import shutil
from copystatic import copy_directory_recursive
from generate import generate_page, generate_pages_recursive

def main():
    
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        
    source_dir = "static"
    dest_dir = "public"

    # Clean build check: delete 'public/' if it already exists
    if os.path.exists(dest_dir):
        print(f"Cleaning old build... removing {dest_dir}/")
        shutil.rmtree(dest_dir)

    print("Beginning site generation pipeline...")
    
    # Re-copy everything fresh from 'static' to 'public'
    copy_directory_recursive(source_dir, dest_dir)
    # generate_pages_recursive("content", "template.html", "public", )
    generate_pages_recursive("content", "template.html", dest_dir, basepath)
    # generate_page("content/index.md", "template.html", "public/index.html")
    
    print("Static site successfully generated and deployed to production directory!")if __name__ == "__main__":
    main()