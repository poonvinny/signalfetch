"""DataPoint — the universal return type for all SignalFetch agents.

Every agent, regardless of source, returns a list of DataPoints. This creates a
consistent interface for consumers and enables the semantic layer (ontology/) to
map DataPoints onto RDF/OWL concepts without knowing the underlying source.
"""

from __future__ import annotations

import datetime
from typing import Any

from pydantic import BaseModel, Field


class DataPoint(BaseModel):
    """A single observation of a financial or economic data series.

    This is the primary output type for all SignalFetch agents. It captures the
    observed value along with enough metadata to identify the series, understand
    the units, and trace the data back to its source.

    Attributes:
        source: Data provider name (e.g. "BLS", "IMF", "World Bank", "EDGAR").
        series_id: Provider-native series identifier (e.g. "LNS14000000" for BLS unemployment).
        name: Human-readable series name (e.g. "Unemployment Rate").
        value: The numeric observation value.
        unit: Unit of measurement (e.g. "percent", "USD billions", "index").
        frequency: Observation frequency (e.g. "monthly", "quarterly", "annual").
        date: The date or period-end date this observation covers.
        metadata: Catch-all for provider-specific fields (country codes, vintage dates,
                  footnotes, etc.) that don't belong in the core schema.
        retrieved_at: UTC timestamp of when this DataPoint was fetched. Auto-set.
    """

    source: str
    series_id: str
    name: str
    value: float
    unit: str
    frequency: str
    date: datetime.date
    metadata: dict[str, Any] = Field(default_factory=dict)
    retrieved_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    model_config = {"frozen": True}
