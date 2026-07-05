import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_newlines(self):
        # Test extreme edge cases with extra consecutive empty spaces and lines
        md = "\n\n# This is a Heading\n\n\n\nThis is a paragraph.   \n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a Heading",
                "This is a paragraph.",
            ]
        )
        
    def test_block_to_block_types(self):
        # Test Headings
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        
        # Test Code Block
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        
        # Test Quote Block
        self.assertEqual(block_to_block_type("> line 1\n> line 2"), BlockType.QUOTE)
        
        # Test Unordered List
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED_LIST)
        
        # Test Ordered List
        self.assertEqual(block_to_block_type("1. first\n2. second"), BlockType.ORDERED_LIST)
        
        # Test Paragraph defaults
        self.assertEqual(block_to_block_type("Just a normal paragraph string."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1.missing a space"), BlockType.PARAGRAPH)
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        )
    
    def test_extract_title(self):
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")
        
        md_spaces = "#    Tolkien Fan Club   "
        self.assertEqual(extract_title(md_spaces), "Tolkien Fan Club")
        
    def test_extract_title_exception(self):
        md = "## This is an h2 header\nJust some text."
        with self.assertRaises(Exception):
            extract_title(md)    
if __name__ == "__main__":
    unittest.main()