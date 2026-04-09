# budget-manager (IN PROGRESS)

A command-line personal finance tool that imports bank transaction history from CSV exports and provides spending analysis and budget planning.

## What it does (IN PROGRESS)

- Imports transaction CSVs exported from your bank
- Parses and cleans transaction descriptions to extract merchant names
- Categorizes transactions using a user-defined rules system with fallback to bank-provided categories
- Generates monthly income and expense summaries
- Budget generation, spending analysis, and an interactive CLI

## How it works (IN PROGRESS)

Transaction CSVs are parsed through a bank-specific parser that normalizes raw data into structured `Transaction` objects. Each transaction is cleaned, categorized, and grouped into monthly summaries. Categorization checks user-defined rules first, falling back to a mapping of the bank's own category labels if no rule matches.

User-defined rules live in `rules/` as .toml files and match against merchant names or raw transaction descriptions. `rules/pnc.toml` is an example of a working rule file.

## Supported Banks

- PNC Bank

## Requirements

- Python 3.11+
- rich

## Setup

```bash
pip install -e .
```

## Usage

## Architecture

- Parser is an abstract base class since bank CSVs are not formatted the same
- Categories are decided by user rules first and then fallback on bank-specific mappings. Allows for categorization of transactions based on user choices.
    - Transfers are given the UNCATEGORIZED category since they can vary in purpose, moving money to a different account or money being transferred from a roommate to pay rent are not similar enough so users can categorize these transactions themselves.
- Transaction objects are frozen dataclasses to ensure data is not changed as they are taken from transaction records that have already occurred.
- SummaryDict is a custom defaultdict used to store MonthlySummary objects. The missing dunder method is overwritten to handle the creation of a MonthlySummary when a missing key is provided.
- CategoryMap is a custom dict used to map bank categories to more general categories. The missing dunder method is overwritten to assign UNCATEGORIZED to categories that are not accounted for.
