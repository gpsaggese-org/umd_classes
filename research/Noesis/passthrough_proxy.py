"""
Passthrough proxy for the Noesis Server.

`Gateway` exposes one `call()` API that dispatches a prompt to a registered
provider and logs the raw request/response pair together with provider,
model, latency, and cost metadata.

Import as:

import research.Noesis.passthrough_proxy as rnopapro
"""

import dataclasses
import logging
import time
from typing import Callable, Dict, List

import helpers.hdbg as hdbg
import helpers.hprint as hprint

_LOG = logging.getLogger(__name__)


# #############################################################################
# Constants
# #############################################################################


# A provider's call function stands in for the real network call to a
# provider's SDK/API (e.g., OpenAI, Anthropic). It takes `(model, prompt)`
# and returns the raw response text. Tests inject a deterministic stand-in
# so no network call happens; a real deployment would wrap the provider's
# SDK here.
ProviderCallFn = Callable[[str, str], str]


# #############################################################################
# ProviderConfig
# #############################################################################


@dataclasses.dataclass
class ProviderConfig:
    """
    Register one LLM provider behind the gateway's single `call()` API.

    E.g., `ProviderConfig("openai_mock", echo_fn, 0.01)` registers a provider
    named "openai_mock" that charges 0.01 per character of prompt+response
    text.
    """

    # Short name callers pass to `Gateway.call()` to select this provider.
    name: str
    # Stand-in for the real provider SDK call (see `ProviderCallFn`).
    call_fn: ProviderCallFn
    # Crude placeholder pricing model: $ per character of prompt+response
    # text. This can be swapped for real per-token provider pricing once
    # one is needed.
    cost_per_char: float

    def __init__(
        self, name: str, call_fn: ProviderCallFn, cost_per_char: float
    ) -> None:
        hdbg.dassert_ne(name, "", "ProviderConfig needs a non-empty name")
        self.name = name
        self.call_fn = call_fn
        hdbg.dassert_lte(
            0.0,
            cost_per_char,
            "ProviderConfig.cost_per_char must be non-negative: %s",
            cost_per_char,
        )
        self.cost_per_char = cost_per_char


# #############################################################################
# RequestLogEntry
# #############################################################################


@dataclasses.dataclass
class RequestLogEntry:
    """
    Storage schema for one logged prompt/response pair.

    One entry is appended per `Gateway.call()`, matched or not: every
    request is logged regardless of provider outcome.
    """

    # Monotonically increasing id, unique within one `Gateway` instance.
    request_id: int
    # Name of the provider that served the request.
    provider: str
    # Model identifier forwarded to the provider.
    model: str
    # Raw, unscrubbed prompt text sent to the provider.
    prompt: str
    # Raw, unscrubbed response text returned by the provider.
    response: str
    # Wall-clock time the provider call took, in seconds.
    latency_in_secs: float
    # Estimated cost of the request, in dollars (see `ProviderConfig`).
    cost: float


# #############################################################################
# Gateway
# #############################################################################


class Gateway:
    """
    Passthrough proxy.

    One `call()` API dispatches a prompt to a registered provider and logs
    the raw request/response pair; `get_log()` / `query_log()` make every
    logged pair queryable.
    """

    def __init__(
        self, *, clock_fn: Callable[[], float] = time.perf_counter
    ) -> None:
        """
        :param clock_fn: monotonic clock used to measure call latency
            - Default: `time.perf_counter`
            - Tests inject a deterministic fake clock instead
        """
        self._providers: Dict[str, ProviderConfig] = {}
        self._log: List[RequestLogEntry] = []
        self._next_request_id = 0
        self._clock_fn = clock_fn

    def register_provider(self, provider_config: ProviderConfig) -> None:
        """
        Register a provider so `call()` can route requests to it.

        :param provider_config: provider to add behind the gateway's API
        """
        _LOG.debug(hprint.to_str("provider_config"))
        hdbg.dassert_not_in(
            provider_config.name,
            self._providers,
            "Provider '%s' is already registered",
            provider_config.name,
        )
        self._providers[provider_config.name] = provider_config

    def call(self, provider_name: str, model: str, prompt: str) -> str:
        """
        Route `prompt` to `provider_name`/`model` and log the exchange.

        :param provider_name: name of a provider registered via
            `register_provider()`
        :param model: model identifier to forward to the provider's
            `call_fn`
        :param prompt: raw prompt text to send
        :return: raw response text returned by the provider
        """
        _LOG.debug(hprint.to_str("provider_name model"))
        hdbg.dassert_in(
            provider_name,
            self._providers,
            "Unknown provider '%s'; registered providers: %s",
            provider_name,
            sorted(self._providers.keys()),
        )
        provider_config = self._providers[provider_name]
        # Time only the provider call itself, not the logging bookkeeping.
        start_time = self._clock_fn()
        response = provider_config.call_fn(model, prompt)
        latency_in_secs = self._clock_fn() - start_time
        cost = round(
            provider_config.cost_per_char * (len(prompt) + len(response)), 6
        )
        entry = RequestLogEntry(
            self._next_request_id,
            provider_name,
            model,
            prompt,
            response,
            latency_in_secs,
            cost,
        )
        self._next_request_id += 1
        self._log.append(entry)
        _LOG.debug("return=%s", response)
        return response

    def get_log(self) -> List[RequestLogEntry]:
        """
        :return: every logged request/response pair, in call order
        """
        return list(self._log)

    def query_log(
        self, *, provider: str = "", model: str = ""
    ) -> List[RequestLogEntry]:
        """
        Return logged entries filtered by provider and/or model.

        :param provider: keep only entries logged for this provider
            - Default: "" (no provider filter)
        :param model: keep only entries logged for this model
            - Default: "" (no model filter)
        :return: matching entries, in call order
        """
        entries = self._log
        if provider:
            entries = [entry for entry in entries if entry.provider == provider]
        if model:
            entries = [entry for entry in entries if entry.model == model]
        return list(entries)
