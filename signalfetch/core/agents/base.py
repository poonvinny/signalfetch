"""Base agent class and orchestrator for SignalFetch.

Agents are the primary unit of data retrieval. Each agent is responsible for a single
data source (e.g. BLS, IMF, World Bank) and knows how to fetch DataPoints from it.

The Orchestrator holds a registry of agents and routes queries to the appropriate ones.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from signalfetch.core.models.datapoint import DataPoint


class BaseAgent(ABC):
    """Abstract base class for all SignalFetch data-source agents.

    Subclass this in macro/ or funds/ and implement `fetch`. Each agent represents
    a single external data source. Agents are stateless — they perform retrieval and
    return DataPoints; no caching or persistence.

    Class attributes:
        source: Human-readable identifier for the data source (e.g. "BLS", "IMF").
    """

    source: str

    @abstractmethod
    async def fetch(self, **kwargs: object) -> list[DataPoint]:
        """Retrieve DataPoints from the source.

        Args:
            **kwargs: Source-specific query parameters (series IDs, date ranges, etc.)

        Returns:
            A list of DataPoint instances. Never returns None; returns [] on no results.
        """
        ...

    async def search(self, query: str) -> list[DataPoint]:
        """Semantic search over the source (optional).

        Subclasses may override this to support natural-language queries, e.g. by
        delegating to an LLM to map the query to series IDs before calling fetch().

        Args:
            query: Natural-language description of the data requested.

        Returns:
            A list of matching DataPoints.
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not support search()")


class Orchestrator:
    """Routes queries across a registry of agents.

    The Orchestrator is the top-level entry point for consumers. It holds a set of
    registered agents and dispatches queries to the appropriate one(s).

    Future: add routing logic (by source name, by capability, LLM-assisted routing).
    """

    def __init__(self, agents: list[BaseAgent] | None = None) -> None:
        """
        Args:
            agents: Initial list of agents to register. Can be extended later via
                    register().
        """
        self._agents: dict[str, BaseAgent] = {}
        for agent in agents or []:
            self.register(agent)

    def register(self, agent: BaseAgent) -> None:
        """Add an agent to the registry.

        Args:
            agent: The agent to register. Its `source` attribute is used as the key.
        """
        self._agents[agent.source] = agent

    async def run(self, query: str) -> list[DataPoint]:
        """Run a natural-language query across all registered agents.

        Args:
            query: Natural-language description of the data requested.

        Returns:
            Aggregated list of DataPoints from all agents that support search().
        """
        raise NotImplementedError("Orchestrator.run() routing logic not yet implemented")
