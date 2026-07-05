from textnode import TextNode, TextType
from typing import List
import re

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    
    for old_node in old_nodes:     
        # append as it's if it's not raw text.
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # split the text by the delimiter
        sections = old_node.text.split(delimiter)
        
        # if the length is even, means delimeter is unclosed
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: matching delimiter '{delimiter}' not found.")
        
        for i in range(len(sections)):
            # skips empty strings (occurs at starts or ends with the delimeter)
            if sections[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(sections[i], text_type))
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^()]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"\[([^\[\]]*)\]\(([^()]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        
        # If there are no images in this text node, keep it as-is
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        
        for image_tup in images:
            image_alt = image_tup[0]
            image_url = image_tup[1]
            sections = original_text.split(f"![{image_alt}]({image_url})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            original_text = sections[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
            
    return new_nodes
        
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
            
        for link_tup in links:
            link_text = link_tup[0]
            link_url = link_tup[1]
            # Split exactly 1 time at the current link tag
            sections = original_text.split(f"[{link_text}]({link_url})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
                
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
            
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes
    