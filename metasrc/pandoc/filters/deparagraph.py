"""Pandoc filter to remove the outer Para wrapper and replace it with a
Plain wrapper.
"""

from panflute import toJSONFilter, Para, Plain


def deparagraph(element, doc):
    """Panflute filter function that converts content wrapped in a Para to
    Plain.

    Only lone paragraphs are affected. Para elements with siblings (like a
    second Para) are left unaffected.
    """
    if isinstance(element, Para):
        # Check if siblings exist; don't process the paragraph in that case.
        if element.next is not None:
            return element
        elif element.prev is not None:
            return element

        # Remove the Para wrapper from the lone paragraph.
        # `Plain` is a container that isn't rendered as a paragraph.
        return Plain(*element.content)


def main():
    """Setuptools entrypoint for the deparagraph CLI."""
    toJSONFilter(deparagraph)
