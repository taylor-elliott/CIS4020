import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional


class Config:
    """Configuration loader and manager."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration from YAML file.

        Args:
            config_path: Path to config file. If None, uses default location.
        """
        if config_path is None:
            script_dir = Path(__file__).parent
            src_dir = script_dir.parent
            project_root = src_dir.parent
            self.config_path = str(project_root / "config" / "config.yaml")
        else:
            self.config_path = config_path

        self._config = self._load_config()
        self._project_root = self._get_project_root()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)
            return config if config is not None else {}
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Config file not found: {self.config_path}"
            )
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML config: {e}")

    def _get_project_root(self) -> Path:
        """Get project root directory."""
        # Config is in project_root/config/
        return Path(self.config_path).parent.parent

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key (supports nested keys with dots).

        Args:
            key: Configuration key (e.g., 'paths.raw_data')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value: Any = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def get_path(self, key: str) -> str:
        """
        Get absolute path from config.

        Args:
            key: Path key in config (e.g., 'paths.raw_data')

        Returns:
            Absolute path as string
        """
        relative_path = self.get(key)
        if relative_path is None:
            raise ValueError(f"Path not found in config: {key}")

        return str(self._project_root / relative_path)

    @property
    def raw_data_dir(self) -> str:
        """Get raw data directory path."""
        return self.get_path("paths.raw_data")

    @property
    def processed_data_dir(self) -> str:
        """Get processed data directory path."""
        return self.get_path("paths.processed_data")

    @property
    def processed_pima(self) -> str:
        result = self.get("processed", "processed_pima_diabetes.csv")
        return str(result)

    @property
    def processed_syn(self) -> str:
        result = self.get("processed", "processed_syn_diabetes.csv")
        return str(result)

    @property
    def log_dir(self) -> str:
        """Get logs directory path."""
        return self.get_path("paths.logs")

    @property
    def target_columns(self) -> List[str]:
        """Get target column schema."""
        result = self.get("columns.target", [])
        return result if isinstance(result, list) else []

    @property
    def columns_to_drop(self) -> List[str]:
        """Get columns to drop."""
        result = self.get("columns.drop", [])
        return result if isinstance(result, list) else []

    @property
    def column_rename_map(self) -> Dict[str, str]:
        """Get column rename mapping."""
        result = self.get("columns.rename", {})
        return result if isinstance(result, dict) else {}

    @property
    def log_level(self) -> str:
        """Get logging level."""
        result = self.get("logging.level", "INFO")
        return str(result)

    @property
    def log_format(self) -> str:
        """Get logging format."""
        default = "%(asctime)s - %(levelname)s - %(message)s"
        result = self.get("logging.format", default)
        return str(result)

    @property
    def console_output(self) -> bool:
        """Get console output setting."""
        result = self.get("logging.console_output", True)
        return bool(result)

    @property
    def file_output(self) -> bool:
        """Get file output setting."""
        result = self.get("logging.file_output", True)
        return bool(result)

    @property
    def output_prefix(self) -> str:
        """Get output file prefix."""
        result = self.get("processing.output_prefix", "processed_")
        return str(result)

    @property
    def save_index(self) -> bool:
        """Get save index setting."""
        result = self.get("processing.save_index", False)
        return bool(result)

    @property
    def preview_rows(self) -> int:
        """Get number of preview rows to show."""
        result = self.get("processing.show_preview_rows", 3)
        return int(result)

    @property
    def preview_full(self) -> int:
        result = self.get("processing.show_full_preview", True)
        return int(result)

    @property
    def continue_on_error(self) -> bool:
        """Get continue on error setting."""
        result = self.get("processing.continue_on_error", True)
        return bool(result)

    def __repr__(self) -> str:
        return f"Config(config_path='{self.config_path}')"
