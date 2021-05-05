import pathlib
from typing import List

from flask import Blueprint

from roman_discovery import ModuleRule, ObjectRule, discover
from roman_discovery.matchers import MatchByPattern, MatchByType


def test_module_rule_should_find_modules(collector: List, sample_project: pathlib.Path):
    rule = ModuleRule(
        name="Find controllers",
        module_matches=MatchByPattern(["*.controllers"]),
        module_action=collector.append,
    )
    discover("sample_project", rules=[rule])
    assert collector == ["sample_project.users.controllers"]


def test_object_module_rule_should_find_objects(
    collector: List, sample_project: pathlib.Path
):
    rule = ObjectRule(
        name="Find blueprints",
        module_matches=MatchByPattern(["*.controllers"]),
        object_matches=MatchByType(Blueprint),
        object_action=collector.append,
    )
    discover("sample_project", rules=[rule])
    assert len(collector) == 1
    assert collector[0].name == "users"
