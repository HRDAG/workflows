import os

import pytest

from hrdag.precommit import check_makefiles


@pytest.mark.usefixtures("set_cwd")
class TestMain:
    class TestAllOk:
        @staticmethod
        @pytest.fixture
        def project_structure():
            return {
                ".git": {},
                "task1": {"src": {}, "Makefile": "a makefile"},
                "task2": {"src": {}, "Makefile": "another makefile"},
                "task3": {},
                "task4": {},
            }

        @staticmethod
        def test_ok(runner):
            result = runner.invoke(check_makefiles.main)
            assert result.exit_code == 0
            assert result.stdout == ""
            assert result.stderr == ""

    class TestSomeNotOk:
        @staticmethod
        @pytest.fixture
        def project_structure():
            return {
                ".git": {},
                "task1": {"src": {}, "Makefile": "a makefile"},
                "task2": {"src": {}},
                "task3": {"src": {}, "Makefile": "another makefile"},
                "task4": {"src": {}},
            }

        @staticmethod
        def test_not_ok(runner):
            result = runner.invoke(check_makefiles.main)
            assert result.exit_code == 1
            assert result.stdout == ""
            assert result.stderr.split(os.linesep) == [
                "Missing Makefile:",
                "  task2",
                "  task4",
                "",
            ]
