# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT
import logging
import requests
import os
from typing import Annotated
from langchain_core.tools import tool
from .decorators import log_io

logger = logging.getLogger(__name__)


class BrightDataCrawler:
    """Bright Data crawler that mimics the original Crawler interface"""

    def __init__(self):
        self.api_token = os.getenv("BRIGHT_DATA_API_KEY")
        self.unlocker_zone = "unblocker"

        if not self.api_token:
            raise ValueError("BRIGHT_DATA_API_KEY environment variable is required")

    def _api_headers(self):
        return {
            "authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def crawl(self, url: str):
        """Crawl URL using Bright Data and return an object with to_markdown() method"""
        try:
            response = requests.post(
                "https://api.brightdata.com/request",
                json={
                    "url": url,
                    "zone": self.unlocker_zone,
                    "format": "raw",
                    "data_format": "markdown",
                },
                headers=self._api_headers(),
                timeout=120,
            )
            logger.info(f"Bright Data response status: {response.status_code}")
            logger.info(f"Bright Data response headers: {response.headers}")
            logger.info(f"Bright Data response content length: {len(response.text)}")
            logger.info(
                f"Bright Data response content (first 200 chars): {response.text[:200]}"
            )
            response.raise_for_status()
            status_code = response.status_code
            logger.info(f"Bright Unlocker was called - Status: {status_code}")
            if status_code == 200:
                logger.info("Bright Unlocker called successfully")
            return CrawledArticle(response.text)

        except requests.exceptions.RequestException as e:
            raise Exception(f"Bright Data API request failed: {str(e)}")


class CrawledArticle:
    """Article object that mimics the original Crawler's article interface"""

    def __init__(self, markdown_content: str):
        self._content = markdown_content

    def to_markdown(self) -> str:
        """Return the markdown content"""
        return self._content


@tool
@log_io
def crawl_tool(
    url: Annotated[str, "The url to crawl."],
) -> str:
    """Use this to crawl a url and get a readable content in markdown format."""
    try:
        crawler = BrightDataCrawler()
        article = crawler.crawl(url)
        return f"URL: {url}\n\nContent:\n{article.to_markdown()[:1000]}"
    except BaseException as e:
        error_msg = f"Failed to crawl. Error: {repr(e)}"
        logger.error(error_msg)
        return error_msg
