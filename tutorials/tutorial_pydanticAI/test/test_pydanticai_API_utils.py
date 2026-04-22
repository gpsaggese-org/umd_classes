"""
Test utility functions for tutorials/tutorial_pydanticAI/pydanticai.API.
"""

import asyncio
import importlib.util
import logging
import sys
import types
from types import SimpleNamespace
from unittest import mock

import helpers.hunit_test as hunitest

if importlib.util.find_spec("pydantic_ai") is None:

    class ModelRetry(Exception):
        """
        Minimal stub for pydantic_ai.ModelRetry.
        """

    class RunContext:
        """
        Minimal stub for pydantic_ai.RunContext.
        """

        def __class_getitem__(cls, item: object) -> type["RunContext"]:
            """
            Support type annotations that use RunContext[Any].

            :param item: type argument
            :return: RunContext class
            """
            return cls

    pydantic_ai_stub = types.ModuleType("pydantic_ai")
    pydantic_ai_stub.ModelRetry = ModelRetry
    pydantic_ai_stub.RunContext = RunContext
    sys.modules["pydantic_ai"] = pydantic_ai_stub

import pydanticai_API_utils as put
from pydantic_ai import ModelRetry

_LOG = logging.getLogger(__name__)


# #############################################################################
# Test_mask
# #############################################################################


class Test_mask(hunitest.TestCase):
    """
    Test secret masking for notebook environment output.
    """

    def helper(self, value: str | None, expected: str) -> None:
        """
        Test helper for `_mask()`.

        :param value: value to mask
        :param expected: expected masked value
        """
        # Run test.
        actual = put._mask(value)
        # Check outputs.
        self.assert_equal(actual, expected)

    def test1(self) -> None:
        """
        Test masking a missing value.
        """
        # Prepare inputs.
        value = None
        # Prepare outputs.
        expected = "<not set>"
        # Run test.
        self.helper(value, expected)

    def test2(self) -> None:
        """
        Test masking an empty value.
        """
        # Prepare inputs.
        value = ""
        # Prepare outputs.
        expected = "<not set>"
        # Run test.
        self.helper(value, expected)

    def test3(self) -> None:
        """
        Test masking a short value.
        """
        # Prepare inputs.
        value = "secret"
        # Prepare outputs.
        expected = "******"
        # Run test.
        self.helper(value, expected)

    def test4(self) -> None:
        """
        Test masking a normal secret value.
        """
        # Prepare inputs.
        value = "sk-1234567890"
        # Prepare outputs.
        expected = "sk-...90"
        # Run test.
        self.helper(value, expected)


# #############################################################################
# Test_get_weather
# #############################################################################


class Test_get_weather(hunitest.TestCase):
    """
    Test deterministic weather output.
    """

    def helper(self, city: str, expected: str) -> None:
        """
        Test helper for `get_weather()`.

        :param city: city name
        :param expected: expected weather response
        """
        # Run test.
        actual = put.get_weather(city)
        # Check outputs.
        self.assert_equal(actual, expected)

    def test1(self) -> None:
        """
        Test weather output for a normal city.
        """
        # Prepare inputs.
        city = "Tokyo"
        # Prepare outputs.
        expected = "The weather in Tokyo is sunny."
        # Run test.
        self.helper(city, expected)

    def test2(self) -> None:
        """
        Test weather output for an empty city.
        """
        # Prepare inputs.
        city = ""
        # Prepare outputs.
        expected = "The weather in  is sunny."
        # Run test.
        self.helper(city, expected)


# #############################################################################
# Test_build_missing_sources_retry
# #############################################################################


class Test_build_missing_sources_retry(hunitest.TestCase):
    """
    Test construction of the missing-sources retry exception.
    """

    def test1(self) -> None:
        """
        Test that the helper builds a ModelRetry instance.
        """
        # Prepare outputs.
        expected = "Answer references documents but sources are empty."
        # Run test.
        actual = put.build_missing_sources_retry()
        # Check outputs.
        self.assertIsInstance(actual, ModelRetry)
        self.assert_equal(str(actual), expected)


# #############################################################################
# Test_validate_sources
# #############################################################################


class Test_validate_sources(hunitest.TestCase):
    """
    Test answer source validation.
    """

    def test1(self) -> None:
        """
        Test an answer with no document claim and no sources.
        """
        # Prepare inputs.
        result = self._build_result("This answer is standalone.", [])
        # Run test.
        actual = put.validate_sources(result)
        # Check outputs.
        self.assertEqual(actual, result)

    def test2(self) -> None:
        """
        Test an answer with document references and sources.
        """
        # Prepare inputs.
        sources = [self._build_source("doc1", "quoted text")]
        result = self._build_result("According to the document.", sources)
        # Run test.
        actual = put.validate_sources(result)
        # Check outputs.
        self.assertEqual(actual, result)

    def test3(self) -> None:
        """
        Test that duplicate sources raise ModelRetry.
        """
        # Prepare inputs.
        sources = [
            self._build_source("doc1", "quoted text"),
            self._build_source("doc1", "quoted text"),
        ]
        result = self._build_result("Standalone answer.", sources)
        # Run test and check output.
        with self.assertRaises(ModelRetry) as cm:
            put.validate_sources(result)
        actual = str(cm.exception)
        expected = "Duplicate sources found."
        self.assert_equal(actual, expected)

    def test4(self) -> None:
        """
        Test that too many sources raise ModelRetry.
        """
        # Prepare inputs.
        sources = [
            self._build_source("doc1", "quote1"),
            self._build_source("doc2", "quote2"),
            self._build_source("doc3", "quote3"),
            self._build_source("doc4", "quote4"),
        ]
        result = self._build_result("Standalone answer.", sources)
        # Run test and check output.
        with self.assertRaises(ModelRetry) as cm:
            put.validate_sources(result)
        actual = str(cm.exception)
        expected = "Too many sources. Maximum allowed is 3."
        self.assert_equal(actual, expected)

    def test5(self) -> None:
        """
        Test that document claims without sources raise ModelRetry.
        """
        # Prepare inputs.
        result = self._build_result("According to the documents.", [])
        # Run test and check output.
        with self.assertRaises(ModelRetry) as cm:
            put.validate_sources(result)
        actual = str(cm.exception)
        expected = "Answer references documents but sources are empty."
        self.assert_equal(actual, expected)

    @staticmethod
    def _build_result(
        answer: str, sources: list[SimpleNamespace]
    ) -> SimpleNamespace:
        """
        Build a validator input object.

        :param answer: answer text
        :param sources: source references
        :return: validator input
        """
        result = SimpleNamespace(answer=answer, sources=sources)
        return result

    @staticmethod
    def _build_source(doc_id: str, quote: str) -> SimpleNamespace:
        """
        Build a source reference object.

        :param doc_id: document identifier
        :param quote: source quote
        :return: source reference
        """
        source = SimpleNamespace(doc_id=doc_id, quote=quote)
        return source


# #############################################################################
# Test_company_name
# #############################################################################


class Test_company_name(hunitest.TestCase):
    """
    Test dependency access for the company-name tool.
    """

    def test1(self) -> None:
        """
        Test reading the company from a run context.
        """
        # Prepare inputs.
        ctx = SimpleNamespace(deps=SimpleNamespace(company="OpenAI"))
        # Prepare outputs.
        expected = "OpenAI"
        # Run test.
        actual = put.company_name(ctx)
        # Check outputs.
        self.assert_equal(actual, expected)


# #############################################################################
# Test_load_example_documents
# #############################################################################


class Test_load_example_documents(hunitest.TestCase):
    """
    Test loading local example documents.
    """

    def test1(self) -> None:
        """
        Test that tutorial documents are loaded.
        """
        # Prepare inputs.
        put._DOCUMENTS_CACHE = None
        # Run test.
        actual = put.load_example_documents()
        # Check outputs.
        self.assertIn("billing", actual)
        self.assertIn("Starter: $20 per month", actual["billing"])


# #############################################################################
# Test_get_available_document_ids
# #############################################################################


class Test_get_available_document_ids(hunitest.TestCase):
    """
    Test document-id discovery.
    """

    def test1(self) -> None:
        """
        Test that document ids are returned in sorted order.
        """
        # Prepare outputs.
        expected = sorted(put.load_example_documents())
        # Run test.
        actual = put.get_available_document_ids()
        # Check outputs.
        self.assert_equal(str(actual), str(expected))


# #############################################################################
# Test_search_documents
# #############################################################################


class Test_search_documents(hunitest.TestCase):
    """
    Test local document search snippets.
    """

    def test1(self) -> None:
        """
        Test a search query with matching snippets.
        """
        # Prepare inputs.
        query = "billing starter"
        # Run test.
        actual = put.search_documents(query, max_results=1)
        # Check outputs.
        self.assertIn("doc_id=billing", actual)
        self.assertIn("Starter", actual)

    def test2(self) -> None:
        """
        Test a search query with no matching snippets.
        """
        # Prepare inputs.
        query = "zzzzzz"
        # Prepare outputs.
        expected = "No matching snippets found."
        # Run test.
        actual = put.search_documents(query)
        # Check outputs.
        self.assert_equal(actual, expected)


# #############################################################################
# Test_validate_document_sources
# #############################################################################


class Test_validate_document_sources(hunitest.TestCase):
    """
    Test source validation against local documents.
    """

    def test1(self) -> None:
        """
        Test a valid source quote.
        """
        # Prepare inputs.
        sources = [
            self._build_source(
                "billing",
                "Starter: $20 per month, 5 data sources, email support.",
            )
        ]
        result = self._build_result("According to the documents.", sources)
        # Run test.
        actual = put.validate_document_sources(result)
        # Check outputs.
        self.assertEqual(actual, result)

    def test2(self) -> None:
        """
        Test that an unknown document id raises ModelRetry.
        """
        # Prepare inputs.
        sources = [self._build_source("missing", "quoted text")]
        result = self._build_result("According to the documents.", sources)
        # Run test and check output.
        with self.assertRaises(ModelRetry) as cm:
            put.validate_document_sources(result)
        actual = str(cm.exception)
        expected = "Unknown doc_id 'missing'. Use ids from example_dataset."
        self.assert_equal(actual, expected)

    def test3(self) -> None:
        """
        Test that a quote mismatch raises ModelRetry.
        """
        # Prepare inputs.
        sources = [self._build_source("billing", "not present in billing")]
        result = self._build_result("According to the documents.", sources)
        # Run test and check output.
        with self.assertRaises(ModelRetry) as cm:
            put.validate_document_sources(result)
        actual = str(cm.exception)
        expected = "Quote not found in cited document 'billing'."
        self.assert_equal(actual, expected)

    @staticmethod
    def _build_result(
        answer: str, sources: list[SimpleNamespace]
    ) -> SimpleNamespace:
        """
        Build a validator input object.

        :param answer: answer text
        :param sources: source references
        :return: validator input
        """
        result = SimpleNamespace(answer=answer, sources=sources)
        return result

    @staticmethod
    def _build_source(doc_id: str, quote: str) -> SimpleNamespace:
        """
        Build a source reference object.

        :param doc_id: document identifier
        :param quote: source quote
        :return: source reference
        """
        source = SimpleNamespace(doc_id=doc_id, quote=quote)
        return source


# #############################################################################
# Test_run_agent
# #############################################################################


class Test_run_agent(hunitest.TestCase):
    """
    Test async agent helper execution.
    """

    class _Agent:
        """
        Minimal async agent used by tests.
        """

        async def run(self, prompt: str) -> SimpleNamespace:
            """
            Return a fake run result.

            :param prompt: prompt sent to the agent
            :return: fake run result
            """
            result = SimpleNamespace(output=f"answer: {prompt}")
            return result

    def test1(self) -> None:
        """
        Test running an async agent.
        """
        # Prepare inputs.
        agent = self._Agent()
        prompt = "hello"
        # Prepare outputs.
        expected = "answer: hello"
        # Run test.
        actual = asyncio.run(put.run_agent(agent, prompt=prompt))
        # Check outputs.
        self.assert_equal(actual, expected)


# #############################################################################
# Test_run_validator_example
# #############################################################################


class Test_run_validator_example(hunitest.TestCase):
    """
    Test validator example helper execution.
    """

    class _Agent:
        """
        Minimal async validator agent used by tests.
        """

        async def run(self, prompt: str) -> SimpleNamespace:
            """
            Return a fake validator run result.

            :param prompt: prompt sent to the agent
            :return: fake run result
            """
            result = SimpleNamespace(output={"prompt": prompt})
            return result

    def test1(self) -> None:
        """
        Test running the validator example helper.
        """
        # Prepare inputs.
        agent = self._Agent()
        prompt = "cite docs"
        # Prepare outputs.
        expected = {"prompt": prompt}
        # Run test.
        actual = asyncio.run(put.run_validator_example(agent, prompt=prompt))
        # Check outputs.
        self.assert_equal(str(actual), str(expected))


# #############################################################################
# Test_run_streaming_demo
# #############################################################################


class Test_run_streaming_demo(hunitest.TestCase):
    """
    Test streaming helper fallback behavior.
    """

    class _Agent:
        """
        Minimal agent without streaming support.
        """

        async def run(self, prompt: str) -> SimpleNamespace:
            """
            Return a fake fallback run result.

            :param prompt: prompt sent to the agent
            :return: fake run result
            """
            result = SimpleNamespace(output=f"fallback: {prompt}")
            return result

    def test1(self) -> None:
        """
        Test fallback execution when streaming is unavailable.
        """
        # Prepare inputs.
        agent = self._Agent()
        # Run test.
        actual = asyncio.run(put.run_streaming_demo(agent))
        # Check outputs.
        self.assert_equal(actual.output, "fallback: What are unit tests?")


# #############################################################################
# Test_get_openai_model_class
# #############################################################################


class Test_get_openai_model_class(hunitest.TestCase):
    """
    Test OpenAI model class discovery.
    """

    def test1(self) -> None:
        """
        Test missing OpenAI model module.
        """
        # Run test.
        with mock.patch.object(
            put.importlib.util, "find_spec", return_value=None
        ):
            actual = put._get_openai_model_class()
        # Check outputs.
        self.assertIsNone(actual)


# #############################################################################
# Test_build_explicit_openai_model
# #############################################################################


class Test_build_explicit_openai_model(hunitest.TestCase):
    """
    Test explicit OpenAI model construction.
    """

    def test1(self) -> None:
        """
        Test missing model class fallback.
        """
        # Prepare inputs.
        model_id = "openai:gpt-5-nano"
        # Run test.
        with mock.patch.object(
            put, "_get_openai_model_class", return_value=None
        ):
            actual = put.build_explicit_openai_model(model_id)
        # Check outputs.
        self.assertIsNone(actual)


# #############################################################################
# Test_get_settings_classes
# #############################################################################


class Test_get_settings_classes(hunitest.TestCase):
    """
    Test settings class discovery.
    """

    class _ModelSettings:
        """
        Fake model settings class.
        """

    class _UsageLimits:
        """
        Fake usage limits class.
        """

    def test1(self) -> None:
        """
        Test direct class discovery from the pydantic_ai module.
        """
        # Prepare inputs.
        pydantic_ai_module = sys.modules["pydantic_ai"]
        pydantic_ai_module.ModelSettings = self._ModelSettings
        pydantic_ai_module.UsageLimits = self._UsageLimits
        # Prepare outputs.
        expected = (self._ModelSettings, self._UsageLimits)
        # Run test.
        actual = put.get_settings_classes()
        # Check outputs.
        self.assert_equal(str(actual), str(expected))
        del pydantic_ai_module.ModelSettings
        del pydantic_ai_module.UsageLimits
