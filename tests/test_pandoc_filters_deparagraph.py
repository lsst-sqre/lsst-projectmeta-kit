"""Test the metasrc-deparagraph Pandoc filter.

The filter is implemented in metasrc.pandoc.filters.deparagraph, but we
test it through the metasrc-deparagraph entrypoint.
"""

import pypandoc
import pytest


@pytest.mark.parametrize(
    'sample,expected', [
        # Should strip <p> tag from single paragraph.
        ('Hello world!', 'Hello world!\n'),
        # Should leave <p> tags for multiple paragraphs.
        ('Hello.\n\nWorld!', '<p>Hello.</p>\n<p>World!</p>\n')
    ])
def test_deparagraph(sample, expected):
    output = pypandoc.convert_text(
        sample, 'html5', format='latex',
        extra_args=['--filter=metasrc-deparagraph'])
    assert output == expected
