from enum import Enum
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes
from htmlnode import ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    ram_blocks = markdown.split("\n\n")
    filtered_blocks = []
    
    for block in ram_blocks:
        # Strip leading and trailing whitespace from the block
        cleaned_block = block.strip()
        
        if cleaned_block != "":
            filtered_blocks.append(cleaned_block)
    return filtered_blocks

def block_to_block_type(block: str) -> BlockType:
    # Check for Headings ('#' followed by a space)
    if block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return BlockType.HEADING
    
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")
    
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE  
    
    
    # Check for Unordered Lists (Every line must start with '- ' or '* ')
    is_unordered = True
    for line in lines:
        if not (line.startswith("- ")):
            is_unordered = False
            break
    if is_unordered:
        return BlockType.UNORDERED_LIST
    
    # Check for Ordered Lists (Every line must start with '1. ', '2. ', etc.)
    is_ordered = True
    for i in range(len(lines)):
        expected_prefix = f"{i + 1}. "
        if not lines[i].startswith(expected_prefix):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            node = handle_paragraph(block)
            block_nodes.append(node)
        elif block_type == BlockType.HEADING:
            node = handle_heading(block)
            block_nodes.append(node)
        elif block_type == BlockType.CODE:
            node = handle_code(block)
            block_nodes.append(node)
        elif block_type == BlockType.QUOTE:
            node = handle_quote(block)
            block_nodes.append(node)
        elif block_type == BlockType.UNORDERED_LIST:
            node = handle_unordered_list(block)
            block_nodes.append(node)
        elif block_type == BlockType.ORDERED_LIST:
            node = handle_ordered_list(block)
            block_nodes.append(node)
    return ParentNode("div", block_nodes)
            
def handle_paragraph(block):
    lines = block.split("\n")
    cleaned_text = " ".join(lines)

    children = text_to_children(cleaned_text)
    return ParentNode("p", children)

def handle_heading(block):
    # Count the number of hashes
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
            
    # The actual heading text starts after the hashes and the space
    # e.g., "### My Heading" -> level is 3, prefix length is 4 ("### ")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def handle_code(block):
    # Per rule 2.4 in image_8525e5.jpg, code blocks don't do inline markdown parsing.
    # We strip the leading ```\n and trailing ```, then wrap it in text_node_to_html_node.
    from textnode import TextNode, TextType # import just in case
    text = block[4:-3]
    # Manually pass through standard raw text processing
    raw_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_node)
    return ParentNode("pre", [ParentNode("code", [child])])

def handle_quote(block):
    # Strip the leading '>' and spaces from every line
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.lstrip(">").strip())
    # Rejoin with newlines and process inline elements
    text = "\n".join(cleaned_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def handle_unordered_list(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        # Strip the leading '- '
        text = line[2:]
        children = text_to_children(text)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ul", li_nodes)

def handle_ordered_list(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        # Slice off the prefix dynamically (e.g. '1. ', '10. ') by finding the first dot
        dot_index = line.find(".")
        text = line[dot_index + 2:] # step past the dot and the space
        children = text_to_children(text)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ol", li_nodes)

def extract_title(markdown):
    lines = markdown.split("\n")
    
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
        
    raise Exception("No h1 header found in markdown file")
