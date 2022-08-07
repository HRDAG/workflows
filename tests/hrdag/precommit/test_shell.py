import pytest

from hrdag.precommit import shell


@pytest.fixture
def project_structure() -> dict:
    return {
        ".git": {},
        "a": "a-file",
        "subdir": {"subsubdir": {}},
    }


class TestFindIn:
    @staticmethod
    def test_found(project_path):
        child = shell.find_in(project_path, "a")
        assert child == project_path / "a"

    @staticmethod
    def test_not_found(project_path):
        child = shell.find_in(project_path, "b")
        assert child is None


@pytest.mark.usefixtures("set_cwd")
@pytest.mark.parametrize(
    "relative_working_dir", ["subdir/subsubdir", "subdir", "."]
)
class TestRepositoryRoot:
    @staticmethod
    def test_find_root(project_path):
        assert shell.repository_root() == project_path

    @staticmethod
    @pytest.mark.parametrize(
        "project_structure",
        [
            {
                "subdir": {
                    "subsubdir": {},
                }
            }
        ],
    )
    def test_no_root(project_path):
        with pytest.raises(
            SystemExit, match=r"^Must be used within git repository$"
        ):
            shell.repository_root()
