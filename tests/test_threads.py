import os
import pytest

from seqdot.utils import resolve_threads


def test_resolve_threads_user():

    workers, mode = resolve_threads("4", 100)

    assert workers == 4
    assert mode == "user"


def test_resolve_threads_auto():

    workers, mode = resolve_threads("auto", 100)

    assert workers >= 1
    assert workers <= (os.cpu_count() or 1)
    assert mode == "auto"


def test_resolve_threads_capped():

    workers, mode = resolve_threads("1000", 3)

    assert workers == 3
    assert mode == "user"


def test_resolve_threads_zero():

    workers, mode = resolve_threads("0", 10)

    assert workers == 1
    assert mode == "user"


def test_resolve_threads_negative():

    workers, mode = resolve_threads("-5", 10)

    assert workers == 1
    assert mode == "user"










