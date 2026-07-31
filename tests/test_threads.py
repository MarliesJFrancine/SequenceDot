import pytest

from seqdot.utils import resolve_threads


def test_resolve_threads_explicit():

    assert resolve_threads("4", 100) == 4


def test_resolve_threads_limited_by_sequences():

    assert resolve_threads("16", 3) == 3


def test_resolve_threads_single():

    assert resolve_threads("1", 20) == 1


def test_resolve_threads_auto():

    threads = resolve_threads("auto", 20)

    assert threads >= 1
    assert threads <= 20


def test_resolve_threads_auto_small_dataset():

    assert resolve_threads("auto", 1) == 1


def test_resolve_threads_invalid():

    with pytest.raises(ValueError):

        resolve_threads("banana", 10)




