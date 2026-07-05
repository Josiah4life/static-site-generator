import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        #Check if dictionary attributes match expected output string
        node = HTMLNode(
            tag="a", 
            value="Boot.dev",
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), 
            ' href="https://www.google.com" target="_blank"'
        )
        
    def test_props_to_html_empty(self):
        #Check that a node with no props returns an empty string
        node = HTMLNode(tag="p", value="Hello world")
        self.assertEqual(node.props_to_html(), "")
        
    def test_repr(self):
        # Check that the string representation dumps data correctly
        node = HTMLNode(tag="h1", value="Title")
        # Checking if the string contains our tag/value
        self.assertTrue("HTMLNode" in repr(node))
        self.assertTrue("h1" in repr(node))
        self.assertTrue("Title" in repr(node))
    
    
    
    def test_leaf_to_html_p(self):
        # Starter test from assignment
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_raw_text(self):
        # Verify no tag just returns raw text string
        node = LeafNode(None, "Just some raw text.")
        self.assertEqual(node.to_html(), "Just some raw text.")

    def test_leaf_to_html_with_props(self):
        # Verify a link renders correctly with its attributes
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), 
            '<a href="https://www.google.com">Click me!</a>'
        )
    
    
    def test_to_html_with_children(self):
        # Starter test with single-level children
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        # Deep nesting test
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_many_children(self):
        # Mixing different leaf types and text inside a parent
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
        
        
if __name__ == "__main__":
    unittest.main()
    
