import os
import tempfile
import shutil
import pandas as pd
import pytest
from src.utils.file import (
    load_csv,
    get_dataframe,
    get_first_dataframe,
    get_all_dataframes,
    combine_dataframes,
)


@pytest.fixture
def test_data_dir():
    """Create temporary directory with test CSV files."""
    test_dir = tempfile.mkdtemp()
    # Create sample CSV files
    sample_data1 = pd.DataFrame(
        {"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]}
    )
    sample_data2 = pd.DataFrame(
        {"A": [10, 11, 12], "B": [13, 14, 15], "C": [16, 17, 18]}
    )
    csv_file1 = os.path.join(test_dir, "test1.csv")
    csv_file2 = os.path.join(test_dir, "test2.csv")
    sample_data1.to_csv(csv_file1, index=False)
    sample_data2.to_csv(csv_file2, index=False)
    yield {
        "dir": test_dir,
        "file1": csv_file1,
        "file2": csv_file2,
        "data1": sample_data1,
        "data2": sample_data2,
    }
    shutil.rmtree(test_dir)


class TestLoadCSV:
    """Test cases for load_csv function."""

    def test_load_csv_success(self, test_data_dir):
        """Test loading a valid CSV file."""
        df = load_csv(test_data_dir["file1"])
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert list(df.columns) == ["A", "B", "C"]

    def test_load_csv_file_not_found(self, test_data_dir):
        """Test loading a non-existent CSV file."""
        with pytest.raises(FileNotFoundError):
            load_csv(os.path.join(test_data_dir["dir"], "nonexistent.csv"))

    def test_load_csv_empty_file(self, test_data_dir):
        """Test loading an empty CSV file."""
        empty_file = os.path.join(test_data_dir["dir"], "empty.csv")
        with open(empty_file, "w") as f:
            f.write("")
        with pytest.raises(pd.errors.EmptyDataError):
            load_csv(empty_file)


class TestGetDataframe:
    """Test cases for get_dataframe function."""

    def test_get_dataframe_success(self, test_data_dir):
        """Test getting a specific CSV file."""
        df = get_dataframe("test1.csv", test_data_dir["dir"])
        assert isinstance(df, pd.DataFrame)
        pd.testing.assert_frame_equal(df, test_data_dir["data1"])

    def test_get_dataframe_directory_not_found(self):
        """Test getting dataframe from non-existent directory."""
        with pytest.raises(FileNotFoundError):
            get_dataframe("test1.csv", "/nonexistent/directory")

    def test_get_dataframe_not_a_directory(self, test_data_dir):
        """Test getting dataframe when path is not a directory."""
        with pytest.raises(NotADirectoryError):
            get_dataframe("test1.csv", test_data_dir["file1"])


class TestGetFirstDataframe:
    """Test cases for get_first_dataframe function."""

    def test_get_first_dataframe_success(self, test_data_dir):
        """Test getting first CSV file from directory."""
        df = get_first_dataframe(test_data_dir["dir"])
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3

    def test_get_first_dataframe_no_csv(self, test_data_dir):
        """Test getting first CSV when no CSV files exist."""
        empty_dir = os.path.join(test_data_dir["dir"], "empty")
        os.makedirs(empty_dir)
        result = get_first_dataframe(empty_dir)
        assert result is None


class TestGetAllDataframes:
    """Test cases for get_all_dataframes function."""

    def test_get_all_dataframes_success(self, test_data_dir):
        """Test getting all CSV files from directory."""
        dfs = get_all_dataframes(test_data_dir["dir"])
        assert len(dfs) == 2
        assert all(isinstance(df, pd.DataFrame) for df in dfs)

    def test_get_all_dataframes_empty_directory(self, test_data_dir):
        """Test getting all CSVs from empty directory."""
        empty_dir = os.path.join(test_data_dir["dir"], "empty")
        os.makedirs(empty_dir)
        dfs = get_all_dataframes(empty_dir)
        assert len(dfs) == 0


class TestCombineDataframes:
    """Test cases for combine_dataframes function."""

    def test_combine_dataframes_success(self, test_data_dir):
        """Test combining all CSV files."""
        combined = combine_dataframes(test_data_dir["dir"])
        assert isinstance(combined, pd.DataFrame)
        assert len(combined) == 6  # 3 rows from each file

    def test_combine_dataframes_no_csv(self, test_data_dir):
        """Test combining when no CSV files exist."""
        empty_dir = os.path.join(test_data_dir["dir"], "empty")
        os.makedirs(empty_dir)
        result = combine_dataframes(empty_dir)
        assert result is None

    def test_combine_dataframes_ignore_index(self, test_data_dir):
        """Test combining with and without ignoring index."""
        combined_reset = combine_dataframes(
            test_data_dir["dir"], ignore_index=True
        )
        combined_keep = combine_dataframes(
            test_data_dir["dir"], ignore_index=False
        )
        assert list(combined_reset.index) == list(range(6))
        assert len(combined_keep) == 6
