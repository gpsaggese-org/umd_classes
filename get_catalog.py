#!/usr/bin/env -S uv run

# /// script
# dependencies = ["requests", "beautifulsoup4"]
# ///
# 
# Create a script get_catalog.py --target manning
# to scrape the content of the pages
# using https://www.manning.com/catalog?page=1
# 
# The output is a CSV like
# 
# Title, Author, Year, Link
# "Retrieval Augmented Generation, The Seminal Papers", "Ben Auffarth", "2026", "https://www.manning.com/books/retrieval-augmented-generation-the-seminal-papers"
# 
# - [ ] 2 Extend the script to O'Reilly using --target oreilly1
# 
# https://www.oreilly.com/pub/q/book_all_date_desc
# 
# Download the page, if tmp.get_catalog.oreilly.txt and then parse it
# 
# - [ ] 3 Extend the script to O'Reilly using --target oreilly2
# 
# https://www.oreilly.com/search/?q=*&type=book&publishers=O%27Reilly%20Media%2C%20Inc.&order_by=created_at&rows=100
# 
# same approach of specifying the number of pages

r"""
Scrape book catalog from Manning Publications.

Fetches book data from Manning's online catalog and exports to CSV format.

Examples:
    # Scrape first 2 pages from Manning catalog
    > get_catalog.py --target manning --pages 2 --output books.csv

    # Scrape 5 pages and write to stdout
    > get_catalog.py --target manning --pages 5
"""

import argparse
import csv
import logging
import sys
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

import helpers.hdbg as hdbg
import helpers.hparser as hparser
import helpers.hprint as hprint

_LOG = logging.getLogger(__name__)

# #############################################################################
# Constants
# #############################################################################

# Manning base URL for catalog.
MANNING_CATALOG_URL = "https://www.manning.com/catalog"

# Request timeout in seconds.
REQUEST_TIMEOUT = 30

# CSV column headers.
CSV_COLUMNS = ["Title", "Author", "Year", "Link"]

# #############################################################################
# Scraping functions
# #############################################################################


def _extract_book_data(book_elem) -> Tuple[str, str, str, str]:
    """
    Extract book information from a book element on Manning catalog.

    :param book_elem: BeautifulSoup element representing a book listing
    :return: Tuple of (title, author, year, link)
        - Empty strings used for missing fields
    """
    title = ""
    author = ""
    year = ""
    link = ""
    # Extract title and link.
    title_elem = book_elem.find("a", class_="product-link")
    if title_elem:
        title = title_elem.get_text(strip=True)
        link_attr = title_elem.get("href")
        if link_attr:
            link = (
                link_attr
                if link_attr.startswith("http")
                else f"https://www.manning.com{link_attr}"
            )
    # Extract author.
    author_elem = book_elem.find("p", class_="product-author")
    if author_elem:
        author_text = author_elem.get_text(strip=True)
        # Author text often looks like "by John Doe"
        if author_text.startswith("by "):
            author = author_text[3:]
        else:
            author = author_text
    # Extract year (if available).
    year_elem = book_elem.find("span", class_="product-year")
    if year_elem:
        year = year_elem.get_text(strip=True)
    return (title, author, year, link)


def _scrape_page(page_num: int) -> List[Tuple[str, str, str, str]]:
    """
    Scrape book data from a single page of Manning catalog.

    :param page_num: Page number to scrape (1-indexed)
    :return: List of tuples containing (title, author, year, link)
    """
    url = f"{MANNING_CATALOG_URL}?page={page_num}"
    _LOG.info("Scraping page %d from '%s'", page_num, url)
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    books = []
    # Find all book elements on the page.
    book_elements = soup.find_all("div", class_="product-item")
    _LOG.debug("Found %d books on page %d", len(book_elements), page_num)
    for book_elem in book_elements:
        book_data = _extract_book_data(book_elem)
        if book_data[0]:
            # Only add if title was extracted.
            books.append(book_data)
    return books


def _scrape_catalog(num_pages: int) -> List[Tuple[str, str, str, str]]:
    """
    Scrape book data from multiple pages of Manning catalog.

    :param num_pages: Number of pages to scrape
    :return: List of tuples containing (title, author, year, link)
    """
    all_books = []
    for page_num in range(1, num_pages + 1):
        books = _scrape_page(page_num)
        all_books.extend(books)
    return all_books


# #############################################################################
# Output functions
# #############################################################################


def _write_csv_output(
    books: List[Tuple[str, str, str, str]], output_file: str = ""
) -> None:
    """
    Write book data to CSV format.

    :param books: List of tuples containing (title, author, year, link)
    :param output_file: Output file path, or empty string to write to stdout
    """
    if output_file:
        _LOG.info("Writing %d books to '%s'", len(books), output_file)
        output_fh = open(output_file, "w", newline="")
    else:
        _LOG.info("Writing %d books to stdout", len(books))
        output_fh = sys.stdout
    writer = csv.writer(output_fh)
    # Write header.
    writer.writerow(CSV_COLUMNS)
    # Write data rows.
    for book_data in books:
        writer.writerow(book_data)
    if output_file:
        output_fh.close()


# #############################################################################
# CLI
# #############################################################################


def _parse() -> argparse.ArgumentParser:
    """
    Parse command line arguments.

    :return: ArgumentParser instance
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        type=str,
        choices=["manning"],
        required=True,
        help="Book catalog target",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=1,
        help="Number of pages to scrape",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Output CSV file path (empty for stdout)",
    )
    hparser.add_verbosity_arg(parser)
    return parser


def _main(parser: argparse.ArgumentParser) -> None:
    """
    Main entry point.

    :param parser: ArgumentParser instance
    """
    args = parser.parse_args()
    hdbg.init_logger(verbosity=args.log_level, use_exec_path=True)
    _LOG.debug(hprint.to_str("args.target args.pages args.output"))
    # Validate pages argument.
    hdbg.dassert_lte(
        1,
        args.pages,
        "Number of pages must be at least 1",
    )
    # Scrape catalog.
    if args.target == "manning":
        books = _scrape_catalog(args.pages)
    else:
        raise ValueError(f"Unknown target: {args.target}")
    # Write output.
    _write_csv_output(books, output_file=args.output)
    _LOG.info("Scraped %d books successfully", len(books))


if __name__ == "__main__":
    parser = _parse()
    _main(parser)
