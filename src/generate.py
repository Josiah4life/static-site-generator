import os
from block_markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"Source markdown file not found: {from_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
        
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template HTML file not found: {template_path}")
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
    
    # convert markdown contents to an HTML string
    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    
    # extract the page title
    title = extract_title(markdown_content)
    
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    
    # Replace link origins using the basepath parameter
    final_html = final_html.replace('href="/"', f'href="{basepath}"')
    final_html = final_html.replace('src="/"', f'src="{basepath}"')
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)
        
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)
        
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # Iterate over every item inside the content directory
    for item in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        # If it's a file, check if it's markdown and convert it
        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                # Swap out the .md extension for .html (e.g., index.md -> index.html)
                # html_dest_path = dest_path.replace(".md", ".html")
                html_dest_path = dest_path[:-3] + ".html"
                generate_page(from_path, template_path, html_dest_path, basepath)
        
        # If it's a subdirectory, recursively crawl inside it
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)