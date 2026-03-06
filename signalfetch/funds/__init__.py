"""Fund data agents: SEC EDGAR filings, prospectus and PDF extraction.

Agents in this module download structured documents (fund filings, prospectuses)
from sources like EDGAR and use DocumentFetcher + an LLMProvider to extract
typed DataPoints. An LLM is required for this module.
"""
