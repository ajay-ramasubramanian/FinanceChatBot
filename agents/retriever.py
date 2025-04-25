# agents/retriever.py
import os
import logging
from datetime import datetime, timedelta
from sec_edgar_downloader import Downloader
import shutil

class SECRetriever:
    """Agent responsible for retrieving SEC filings using sec-edgar-downloader."""

    def __init__(self, company_name="YourCompanyName", email="your.email@example.com", output_dir="data/filings"):
        self.output_dir = output_dir
        self.company_name = company_name
        self.email = email
        # Initialize the downloader, specifying the root download location
        self.dl = Downloader(self.company_name, self.email, self.output_dir)
        self.logger = logging.getLogger(__name__)
        os.makedirs(self.output_dir, exist_ok=True) # Ensure base directory exists

    def get_filings(self, ticker, years=1, forms=["10-K", "10-Q"], limit=10):
        """
        Retrieve recent filings for a company using sec-edgar-downloader.

        Args:
            ticker (str): The company ticker symbol.
            years (int): How many years of history to retrieve.
            forms (list): List of SEC form types to download (e.g., ["10-K", "10-Q"]).
            limit (int): The maximum total number of filings to return.

        Returns:
            list: A list of file paths to the primary HTML document for each downloaded filing.
                Returns an empty list if no filings are found or an error occurs.
        """
        ticker = ticker.upper()
        self.logger.info(f"Retrieving latest {limit} {forms} filings for {ticker} from past {years} years.")

        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * years)
        after_date_str = start_date.strftime("%Y-%m-%d")
        before_date_str = end_date.strftime("%Y-%m-%d")

        download_count = 0
        max_per_form = limit # Aim to download up to 'limit' for each form initially

        # Clear previous downloads for this ticker to ensure freshness (optional)
        ticker_download_path = os.path.join(self.output_dir, "sec-edgar-filings", ticker)
        if os.path.exists(ticker_download_path):
            self.logger.info(f"Removing previous downloads for {ticker} at {ticker_download_path}")
            try:
                shutil.rmtree(ticker_download_path)
            except OSError as e:
                self.logger.error(f"Error removing directory {ticker_download_path}: {e}")


        for form in forms:
            try:
                # Download filings. download_details=True gets the primary HTML document.
                num_downloaded = self.dl.get(
                    form,
                    ticker,
                    after=after_date_str,
                    before=before_date_str,
                    download_details=True, # VERY IMPORTANT: Gets the primary HTML document
                    limit=max_per_form      # Limit downloads per form type
                )
                self.logger.info(f"Downloaded {num_downloaded} '{form}' filings for {ticker}.")
                download_count += num_downloaded

            except Exception as e:
                self.logger.error(f"Error downloading '{form}' filings for {ticker}: {e}")
                # Continue to the next form type even if one fails

        # After downloads, find the paths to the actual primary documents
        if download_count > 0:
            primary_doc_paths = self._find_primary_document_paths(ticker_download_path)
            self.logger.info(f"Found {len(primary_doc_paths)} primary document paths for {ticker}.")
            # Sort paths (descending seems reasonable, hoping structure implies date)
            # and apply the overall limit
            primary_doc_paths.sort(reverse=True)
            return primary_doc_paths[:limit]
        else:
            self.logger.warning(f"No filings were successfully downloaded for {ticker}.")
            return []

    def _find_primary_document_paths(self, ticker_path):
        """
        Recursively finds paths to the primary HTML document within the download structure.
        sec-edgar-downloader usually saves it as 'primary-document.html' or 'filing-details.html'.
        """
        primary_docs = []
        # Expected filenames used by sec-edgar-downloader with download_details=True
        expected_filenames = ["primary-document.html", "filing-details.html"]

        if not os.path.exists(ticker_path):
            self.logger.warning(f"Ticker download path does not exist: {ticker_path}")
            return []

        for root, dirs, files in os.walk(ticker_path):
            for filename in expected_filenames:
                if filename in files:
                    full_path = os.path.join(root, filename)
                    primary_docs.append(full_path)
                    # Assuming one primary doc per accession number directory
                    break # Move to the next directory

        return primary_docs

