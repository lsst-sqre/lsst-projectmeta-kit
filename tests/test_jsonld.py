"""Tests for the lsstprojectmeta.jsonld module.
"""

import datetime
from lsstprojectmeta.jsonld import encode_jsonld


def test_datetime_encoding():
    """Test that a datetime.datetime can be encoded.
    """
    test_date = datetime.datetime(2018, 1, 1, hour=12, minute=0, second=0,
                                  tzinfo=datetime.timezone.utc)
    jsonld_doc = {'date': test_date}

    expected = '{"date": "2018-01-01T12:00:00Z"}'

    assert expected == encode_jsonld(jsonld_doc)


def test_datetime_encoding_no_tz():
    """Test that a datetime.datetime with no timezone can be encoded.
    """
    test_date = datetime.datetime(2018, 1, 1, hour=12, minute=0, second=0)
    jsonld_doc = {'date': test_date}

    expected = '{"date": "2018-01-01T12:00:00Z"}'

    assert expected == encode_jsonld(jsonld_doc)
