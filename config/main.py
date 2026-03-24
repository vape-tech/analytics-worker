import logging
import os
from datetime import datetime
from typing import Optional

import pandas as pd
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class AnalyticsWorker:
    def __init__(self):
        self.data_dir = os.getenv("DATA_DIR", "data")
        self.output_dir = os.getenv("OUTPUT_DIR", "output")
        self._ensure_directories_exist()

    def _ensure_directories_exist(self):
        """Ensure that required directories exist."""
        for directory in [self.data_dir, self.output_dir]:
            os.makedirs(directory, exist_ok=True)

    def load_data(self, filename: str) -> Optional[pd.DataFrame]:
        """Load data from a CSV file."""
        filepath = os.path.join(self.data_dir, filename)
        try:
            return pd.read_csv(filepath)
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            return None

    def process_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Process the data by calculating the mean of each column."""
        return data.mean().to_frame().T

    def save_results(self, results: pd.DataFrame, filename: str) -> None:
        """Save the results to a CSV file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_dir, f"{filename}_{timestamp}.csv")
        results.to_csv(output_file, index=False)
        logger.info(f"Results saved to {output_file}")

    def run(self, filename: str) -> None:
        """Run the analytics worker."""
        logger.info("Starting analytics worker...")
        data = self.load_data(filename)
        if data is not None:
            results = self.process_data(data)
            self.save_results(results, filename)
        logger.info("Analytics worker completed.")

if __name__ == "__main__":
    worker = AnalyticsWorker()
    worker.run("example_data.csv")