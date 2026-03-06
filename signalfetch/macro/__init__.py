"""Macro data agents: BLS, IMF, World Bank, OECD, Eurostat.

Each agent in this module targets a single public data source and subclasses
BaseAgent from core/agents/. Macro agents use APIFetcher or CrawlerFetcher from
core/fetchers/ and do NOT require an LLM.
"""
