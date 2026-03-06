# SignalFetch

A modular, open-source framework for retrieving and extracting publicly available financial and economic data.

## Vision

SignalFetch is a free alternative to Datastream/Bloomberg for public data. It provides a clean Python interface for fetching macro and fund data from sources like BLS, IMF, World Bank, OECD, Eurostat, and SEC EDGAR, with a semantic layer built on RDF/OWL as a macro/funds extension to FIBO.

## Architecture

```
signalfetch/
├── core/
│   ├── agents/        ← base agent class, orchestrator
│   ├── fetchers/      ← reusable fetch capabilities (API, crawler, document)
│   ├── llm/           ← LLM provider abstraction (Claude default)
│   └── models/        ← Pydantic DataPoint models
├── macro/             ← BLS, IMF, World Bank, OECD, Eurostat agents
├── funds/             ← EDGAR fund filings, prospectus/PDF extraction
├── ontology/          ← RDF/OWL, FIBO extension
└── mcp/               ← MCP server exposing agents as tools
```

## Key Principles

- **No storage** — pure retrieval and extraction, returns Python objects
- **LLM agnostic** — Claude is the default; swap via the `LLMProvider` interface
- **LLM optional** — only required for the `funds/` module (document extraction)
- **Python 3.11+**

## Install

```bash
pip install signalfetch                  # core + macro
pip install "signalfetch[funds]"         # + PDF extraction
pip install "signalfetch[ontology]"      # + RDF/OWL semantic layer
pip install "signalfetch[mcp]"           # + MCP server
pip install "signalfetch[dev]"           # + development tools
```
