"""Tests for lsstprojectmeta.lsstdocument.handles
"""

import pytest

from lsstprojectmeta.lsstdocument.handles import DOCUMENT_HANDLE_PATTERN


@pytest.mark.parametrize(
    'text,expected_series,expected_serial', [
        ('LDM-151', 'LDM', '151'),
        ('LSE-163', 'LSE', '163'),
        ('LPM-231', 'LPM', '231'),
        ('DMTR-51', 'DMTR', '51'),
        ('DMTN-001', 'DMTN', '001'),
        ('SQR-001', 'SQR', '001'),
        ('SMTN-001', 'SMTN', '001'),
        ('ldm-151', 'ldm', '151'),
        ('lse-163', 'lse', '163'),
        ('lpm-231', 'lpm', '231'),
        ('dmtr-51', 'dmtr', '51'),
        ('dmtn-001', 'dmtn', '001'),
        ('sqr-001', 'sqr', '001'),
        ('smtn-001', 'smtn', '001')
    ])
def test_document_handle_pattern(text, expected_series, expected_serial):
    match = DOCUMENT_HANDLE_PATTERN.match(text)
    assert match.group('series') == expected_series
    assert match.group('serial') == expected_serial
