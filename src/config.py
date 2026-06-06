"""Project configuration and filesystem paths."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
TEST_CASE_DIR = DATA_DIR / "test_cases"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
METRICS_DIR = OUTPUT_DIR / "metrics"
CHARTS_DIR = OUTPUT_DIR / "charts"
REPORTS_DIR = OUTPUT_DIR / "reports"
RANDOM_SEED = 42
BANK_NAME = "Emerald Credit Bank"


def ensure_directories() -> None:
    """Create the project output/data directories used by the pipeline."""
    for path in [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        TEST_CASE_DIR,
        METRICS_DIR,
        CHARTS_DIR,
        REPORTS_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)

