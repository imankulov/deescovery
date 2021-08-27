import pytest

from deescovery.matchers import (
    MatchByCallableAttribute,
    MatchByPattern,
    MatchBySubclass,
)


@pytest.mark.parametrize(
    "patterns, package, result",
    [
        (["*.models"], "domain_package.models", True),
        (["*.models_*"], "domain_package.models", False),
        (["*.models_*"], "domain_package.models_user", True),
        (["*.models.*"], "domain_package.models", False),
        (["*.models", "*.models.*"], "domain_package.models", True),
    ],
)
def test_match_by_pattern_should_return_relevant_packages(patterns, package, result):
    matcher = MatchByPattern(patterns)
    assert matcher(package) == result


@pytest.mark.parametrize(
    "attribute, obj, result",
    [
        ("strip", "", True),  # instances match
        ("strip", str, False),  # classes don't match
        ("foo", "", False),  # non-existent attribute
    ],
)
def test_match_by_callable_attribute_should_return_relevant_objects(
    attribute, obj, result
):
    matcher = MatchByCallableAttribute(attribute)
    assert matcher(obj) == result


class StringSubclass(str):
    pass


@pytest.mark.parametrize(
    "obj, result",
    [
        # instances don't match
        (1, False),
        ("foo", False),
        # the class itself doesn't match
        (str, False),
        # subclasses match
        (StringSubclass, True),
    ],
)
def test_match_by_subclass_should_return_relevant_objects(obj, result):
    matcher = MatchBySubclass(str)
    assert matcher(obj) == result
