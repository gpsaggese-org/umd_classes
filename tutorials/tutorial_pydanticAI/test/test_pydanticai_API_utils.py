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


class Test__mask(hunitest.TestCase):
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
# Test_init_logger
# #############################################################################


class Test_init_logger(hunitest.TestCase):
    """
    Test notebook logger initialization.
    """

    def test1(self) -> None:
        """
        Test that notebook logging helpers are configured.
        """
        # Prepare inputs.
        notebook_log = logging.getLogger("test_notebook")
        utils_log = logging.getLogger("test_utils")
        # Run test.
        with mock.patch.object(put, "_LOG", utils_log), mock.patch.object(
            put.hnotebo, "config_notebook"
        ) as mock_config, mock.patch.object(
            put.hdbg, "init_logger"
        ) as mock_init_logger, mock.patch.object(
            put.hnotebo,
            "set_logger_to_print",
            return_value=None,
        ) as mock_set_logger:
            put.init_logger(notebook_log)
        # Check outputs.
        mock_config.assert_called_once()
        mock_init_logger.assert_called_once_with(
            verbosity=logging.INFO, use_exec_path=False
        )
        self.assertEqual(mock_set_logger.call_count, 2)

    def test2(self) -> None:
        """
        Test that logger configuration uses the notebook logger and module logger.
        """
        # Prepare inputs.
        notebook_log = logging.getLogger("test_notebook")
        utils_log = logging.getLogger("test_utils")
        # Run test.
        with mock.patch.object(put, "_LOG", utils_log), mock.patch.object(
            put.hnotebo, "config_notebook"
        ), mock.patch.object(
            put.hdbg, "init_logger"
        ), mock.patch.object(
            put.hnotebo,
            "set_logger_to_print",
            return_value=None,
        ) as mock_set_logger:
            put.init_logger(notebook_log)
        # Check outputs.
        self.assertEqual(
            mock_set_logger.call_args_list,
            [mock.call(notebook_log), mock.call(utils_log)],
        )


# #############################################################################
# Test_log_environment
# #############################################################################


class Test_log_environment(hunitest.TestCase):
    """
    Test environment logging for notebook setup.
    """

    def test1(self) -> None:
        """
        Test logging configured environment values.
        """
        # Prepare inputs.
        env_path = "/tmp/.env"
        model_id = "openai:gpt-5-nano"
        openai_api_key = "sk-1234567890"
        # Prepare outputs.
        expected = [
            mock.call("dotenv path: %s", env_path),
            mock.call("PYDANTIC_AI_MODEL: %s", model_id),
            mock.call("OPENAI_API_KEY: %s", "sk-...90"),
        ]
        # Run test.
        with mock.patch.object(put._LOG, "info") as mock_log, mock.patch.dict(
            put.os.environ, {"OPENAI_API_KEY": openai_api_key}, clear=False
        ):
            put.log_environment(env_path, model_id)
        # Check outputs.
        self.assertEqual(mock_log.call_args_list, expected)

    def test2(self) -> None:
        """
        Test logging missing environment values.
        """
        # Prepare inputs.
        env_path = ""
        model_id = ""
        # Prepare outputs.
        expected = [
            mock.call("dotenv path: %s", "<not found>"),
            mock.call("PYDANTIC_AI_MODEL: %s", ""),
            mock.call("OPENAI_API_KEY: %s", "<not set>"),
        ]
        # Run test.
        with mock.patch.object(put._LOG, "info") as mock_log, mock.patch.dict(
            put.os.environ, {}, clear=True
        ):
            put.log_environment(env_path, model_id)
        # Check outputs.
        self.assertEqual(mock_log.call_args_list, expected)


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

    def helper(self, result: SimpleNamespace, expected: str | SimpleNamespace) -> None:
        """
        Test helper for `validate_sources()`.

        :param result: validator input
        :param expected: expected output or retry message
        """
        # Run test.
        if isinstance(expected, str):
            with self.assertRaises(ModelRetry) as cm:
                put.validate_sources(result)
            actual = str(cm.exception)
            # Check outputs.
            self.assert_equal(actual, expected)
        else:
            actual = put.validate_sources(result)
            # Check outputs.
            self.assertEqual(actual, expected)

    def test1(self) -> None:
        """
        Test an answer with no document claim and no sources.
        """
        # Prepare inputs.
        result = self._build_result("This answer is standalone.", [])
        # Run test.
        self.helper(result, result)

    def test2(self) -> None:
        """
        Test an answer with document references and sources.
        """
        # Prepare inputs.
        sources = [self._build_source("doc1", "quoted text")]
        result = self._build_result("According to the document.", sources)
        # Run test.
        self.helper(result, result)

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
        # Prepare outputs.
        expected = "Duplicate sources found."
        # Run test.
        self.helper(result, expected)

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
        # Prepare outputs.
        expected = "Too many sources. Maximum allowed is 3."
        # Run test.
        self.helper(result, expected)

    def test5(self) -> None:
        """
        Test that document claims without sources raise ModelRetry.
        """
        # Prepare inputs.
        result = self._build_result("According to the documents.", [])
        # Prepare outputs.
        expected = "Answer references documents but sources are empty."
        # Run test.
        self.helper(result, expected)

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

    def test2(self) -> None:
        """
        Test reading an empty company from a run context.
        """
        # Prepare inputs.
        ctx = SimpleNamespace(deps=SimpleNamespace(company=""))
        # Prepare outputs.
        expected = ""
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

    def test2(self) -> None:
        """
        Test that the cached documents are reused.
        """
        # Prepare inputs.
        expected = {"cached": "document"}
        put._DOCUMENTS_CACHE = expected
        # Run test.
        actual = put.load_example_documents()
        # Check outputs.
        self.assertEqual(actual, expected)


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

    def test2(self) -> None:
        """
        Test that an empty document mapping returns no document ids.
        """
        # Prepare outputs.
        expected = []
        # Run test.
        with mock.patch.object(put, "load_example_documents", return_value={}):
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

    def helper(self, query: str, max_results: int) -> str:
        """
        Test helper for `search_documents()`.

        :param query: search query
        :param max_results: maximum number of snippets
        :return: search output
        """
        # Prepare inputs.
        put._DOCUMENTS_CACHE = None
        # Run test.
        actual = put.search_documents(query, max_results=max_results)
        return actual

    def test1(self) -> None:
        """
        Test a search query with matching snippets.
        """
        # Prepare inputs.
        query = "billing starter"
        max_results = 1
        # Run test.
        actual = self.helper(query, max_results)
        # Check outputs.
        self.assertIn("doc_id=billing", actual)
        self.assertIn("Starter", actual)

    def test2(self) -> None:
        """
        Test a search query with no matching snippets.
        """
        # Prepare inputs.
        query = "zzzzzz"
        max_results = 3
        # Prepare outputs.
        expected = "No matching snippets found."
        # Run test.
        actual = self.helper(query, max_results)
        # Check outputs.
        self.assert_equal(actual, expected)

    def test3(self) -> None:
        """
        Test that the result count respects the requested limit.
        """
        # Prepare inputs.
        query = ""
        max_results = 2
        # Run test.
        actual = self.helper(query, max_results)
        # Check outputs.
        self.assertEqual(len(actual.splitlines()), 2)


# #############################################################################
# Test_validate_document_sources
# #############################################################################


class Test_validate_document_sources(hunitest.TestCase):
    """
    Test source validation against local documents.
    """

    def helper(self, result: SimpleNamespace, expected: str | SimpleNamespace) -> None:
        """
        Test helper for `validate_document_sources()`.

        :param result: validator input
        :param expected: expected output or retry message
        """
        # Run test.
        if isinstance(expected, str):
            with self.assertRaises(ModelRetry) as cm:
                put.validate_document_sources(result)
            actual = str(cm.exception)
            # Check outputs.
            self.assert_equal(actual, expected)
        else:
            actual = put.validate_document_sources(result)
            # Check outputs.
            self.assertEqual(actual, expected)

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
        self.helper(result, result)

    def test2(self) -> None:
        """
        Test that an unknown document id raises ModelRetry.
        """
        # Prepare inputs.
        sources = [self._build_source("missing", "quoted text")]
        result = self._build_result("According to the documents.", sources)
        # Prepare outputs.
        expected = "Unknown doc_id 'missing'. Use ids from example_dataset."
        # Run test.
        self.helper(result, expected)

    def test3(self) -> None:
        """
        Test that a quote mismatch raises ModelRetry.
        """
        # Prepare inputs.
        sources = [self._build_source("billing", "not present in billing")]
        result = self._build_result("According to the documents.", sources)
        # Prepare outputs.
        expected = "Quote not found in cited document 'billing'."
        # Run test.
        self.helper(result, expected)

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

    def helper(self, prompt: str, expected: str) -> None:
        """
        Test helper for `run_agent()`.

        :param prompt: prompt sent to the agent
        :param expected: expected output
        """
        # Prepare inputs.
        agent = self._Agent()
        # Run test.
        actual = asyncio.run(put.run_agent(agent, prompt=prompt))
        # Check outputs.
        self.assert_equal(actual, expected)

    def test1(self) -> None:
        """
        Test running an async agent.
        """
        # Prepare inputs.
        prompt = "hello"
        # Prepare outputs.
        expected = "answer: hello"
        # Run test.
        self.helper(prompt, expected)

    def test2(self) -> None:
        """
        Test running an async agent with the default prompt.
        """
        # Prepare inputs.
        prompt = "Tell me about Tokyo"
        # Prepare outputs.
        expected = "answer: Tell me about Tokyo"
        # Run test.
        self.helper(prompt, expected)


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

    def helper(self, prompt: str, expected: dict[str, str]) -> None:
        """
        Test helper for `run_validator_example()`.

        :param prompt: prompt sent to the validator agent
        :param expected: expected output
        """
        # Prepare inputs.
        agent = self._Agent()
        # Run test.
        actual = asyncio.run(put.run_validator_example(agent, prompt=prompt))
        # Check outputs.
        self.assert_equal(str(actual), str(expected))

    def test1(self) -> None:
        """
        Test running the validator example helper.
        """
        # Prepare inputs.
        prompt = "cite docs"
        # Prepare outputs.
        expected = {"prompt": prompt}
        # Run test.
        self.helper(prompt, expected)

    def test2(self) -> None:
        """
        Test running the validator example helper with the default prompt.
        """
        # Prepare inputs.
        prompt = "Use local documents to explain Atlas billing plans and cite sources."
        # Prepare outputs.
        expected = {"prompt": prompt}
        # Run test.
        self.helper(prompt, expected)


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

    class _StreamingText:
        """
        Minimal async iterator for stream chunks.
        """

        def __init__(self, chunks: list[str]) -> None:
            self._chunks = chunks
            self._index = 0

        def __aiter__(self) -> "Test_run_streaming_demo._StreamingText":
            return self

        async def __anext__(self) -> str:
            if self._index >= len(self._chunks):
                raise StopAsyncIteration
            value = self._chunks[self._index]
            self._index += 1
            return value

    class _Stream:
        """
        Minimal async stream context manager.
        """

        def __init__(self, chunks: list[str], result: str) -> None:
            self._chunks = chunks
            self._result = result

        async def __aenter__(self) -> "Test_run_streaming_demo._Stream":
            return self

        async def __aexit__(self, exc_type, exc, tb) -> None:
            return None

        def stream_text(self) -> "Test_run_streaming_demo._StreamingText":
            return Test_run_streaming_demo._StreamingText(self._chunks)

        async def get_final_result(self) -> str:
            return self._result

    class _StreamWithDelta:
        """
        Minimal async stream context manager with delta support.
        """

        def __init__(self, chunks: list[str], result: str) -> None:
            self._chunks = chunks
            self._result = result

        async def __aenter__(self) -> "Test_run_streaming_demo._StreamWithDelta":
            return self

        async def __aexit__(self, exc_type, exc, tb) -> None:
            return None

        def stream_text(
            self, delta: bool = False
        ) -> "Test_run_streaming_demo._StreamingText":
            if not delta:
                raise AssertionError("Expected delta=True.")
            return Test_run_streaming_demo._StreamingText(self._chunks)

        async def get_final_result(self) -> str:
            return self._result

    class _StreamWithoutFinalResult:
        """
        Minimal async stream context manager without final-result support.
        """

        def __init__(self, chunks: list[str]) -> None:
            self._chunks = chunks

        async def __aenter__(
            self,
        ) -> "Test_run_streaming_demo._StreamWithoutFinalResult":
            return self

        async def __aexit__(self, exc_type, exc, tb) -> None:
            return None

        def stream_text(self) -> "Test_run_streaming_demo._StreamingText":
            return Test_run_streaming_demo._StreamingText(self._chunks)

    class _StreamingAgent:
        """
        Minimal agent with streaming support.
        """

        def run_stream(self, prompt: str) -> "Test_run_streaming_demo._Stream":
            return Test_run_streaming_demo._Stream(
                ["unit ", "tests"], "unit tests"
            )

    class _StreamingAgentWithDelta:
        """
        Minimal agent with delta-based streaming support.
        """

        def run_stream(
            self, prompt: str
        ) -> "Test_run_streaming_demo._StreamWithDelta":
            return Test_run_streaming_demo._StreamWithDelta(
                ["unit ", "tests"], "unit tests"
            )

    class _StreamingAgentWithoutFinalResult:
        """
        Minimal agent without final-result streaming support.
        """

        def run_stream(
            self, prompt: str
        ) -> "Test_run_streaming_demo._StreamWithoutFinalResult":
            return Test_run_streaming_demo._StreamWithoutFinalResult(
                ["unit ", "tests"]
            )

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

    def test2(self) -> None:
        """
        Test streaming execution when the streaming API is available.
        """
        # Prepare inputs.
        agent = self._StreamingAgent()
        # Run test.
        actual = asyncio.run(put.run_streaming_demo(agent))
        # Check outputs.
        self.assert_equal(actual, "unit tests")

    def test3(self) -> None:
        """
        Test streaming execution when `stream_text(delta=True)` is supported.
        """
        # Prepare inputs.
        agent = self._StreamingAgentWithDelta()
        # Run test.
        actual = asyncio.run(put.run_streaming_demo(agent))
        # Check outputs.
        self.assert_equal(actual, "unit tests")

    def test4(self) -> None:
        """
        Test streaming execution without `get_final_result()`.
        """
        # Prepare inputs.
        agent = self._StreamingAgentWithoutFinalResult()
        # Run test.
        actual = asyncio.run(put.run_streaming_demo(agent))
        # Check outputs.
        self.assert_equal(actual, "unit tests")


# #############################################################################
# Test_get_openai_model_class
# #############################################################################


class Test__get_openai_model_class(hunitest.TestCase):
    """
    Test OpenAI model class discovery.
    """

    def test1(self) -> None:
        """
        Test missing OpenAI model module.
        """
        # Prepare inputs.
        # Run test.
        with mock.patch.object(
            put.importlib.util, "find_spec", return_value=None
        ):
            actual = put._get_openai_model_class()
        # Check outputs.
        self.assertIsNone(actual)

    def test2(self) -> None:
        """
        Test discovery of the explicit model class from the OpenAI module.
        """
        # Prepare inputs.
        openai_module = SimpleNamespace(OpenAIModel=object)
        # Run test.
        with mock.patch.object(
            put.importlib.util,
            "find_spec",
            side_effect=[object(), object()],
        ), mock.patch.object(
            put.importlib, "import_module", return_value=openai_module
        ):
            actual = put._get_openai_model_class()
        # Check outputs.
        self.assertEqual(actual, object)

    def test3(self) -> None:
        """
        Test missing OpenAI submodule.
        """
        # Prepare inputs.
        # Run test.
        with mock.patch.object(
            put.importlib.util,
            "find_spec",
            side_effect=[object(), None],
        ):
            actual = put._get_openai_model_class()
        # Check outputs.
        self.assertIsNone(actual)

    def test4(self) -> None:
        """
        Test discovery of the chat-model class from the OpenAI module.
        """
        # Prepare inputs.
        openai_chat_model = object()
        openai_module = SimpleNamespace(OpenAIChatModel=openai_chat_model)
        # Run test.
        with mock.patch.object(
            put.importlib.util,
            "find_spec",
            side_effect=[object(), object()],
        ), mock.patch.object(
            put.importlib, "import_module", return_value=openai_module
        ):
            actual = put._get_openai_model_class()
        # Check outputs.
        self.assertEqual(actual, openai_chat_model)


# #############################################################################
# Test_build_explicit_openai_model
# #############################################################################


class Test_build_explicit_openai_model(hunitest.TestCase):
    """
    Test explicit OpenAI model construction.
    """

    class _Model:
        """
        Fake explicit OpenAI model class.
        """

        def __init__(
            self, model_name: str, api_key: str | None = None, base_url: str | None = None
        ) -> None:
            self.model_name = model_name
            self.api_key = api_key
            self.base_url = base_url

    class _ModelWithModelArg:
        """
        Fake explicit OpenAI model class with a `model` kwarg.
        """

        def __init__(
            self, model: str, api_key: str | None = None, base_url: str | None = None
        ) -> None:
            self.model = model
            self.api_key = api_key
            self.base_url = base_url

    class _ModelWithPositionalArg:
        """
        Fake explicit OpenAI model class with a positional model arg.
        """

        def __init__(self, model_name: str) -> None:
            self.model_name = model_name

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

    def test2(self) -> None:
        """
        Test explicit model construction with environment-backed kwargs.
        """
        # Prepare inputs.
        model_id = "openai:gpt-5-nano"
        # Run test.
        with mock.patch.object(
            put, "_get_openai_model_class", return_value=self._Model
        ), mock.patch.dict(
            put.os.environ,
            {"OPENAI_API_KEY": "token", "OPENAI_BASE_URL": "https://example.com"},
            clear=False,
        ):
            actual = put.build_explicit_openai_model(model_id)
        # Check outputs.
        self.assertEqual(actual.model_name, "gpt-5-nano")
        self.assertEqual(actual.api_key, "token")
        self.assertEqual(actual.base_url, "https://example.com")

    def test3(self) -> None:
        """
        Test explicit model construction with a `model` kwarg.
        """
        # Prepare inputs.
        model_id = "openai:gpt-5-nano"
        # Run test.
        with mock.patch.object(
            put, "_get_openai_model_class", return_value=self._ModelWithModelArg
        ), mock.patch.dict(put.os.environ, {}, clear=False):
            actual = put.build_explicit_openai_model(model_id)
        # Check outputs.
        self.assertEqual(actual.model, "gpt-5-nano")

    def test4(self) -> None:
        """
        Test explicit model construction with a positional model arg.
        """
        # Prepare inputs.
        model_id = "openai:gpt-5-nano"
        # Run test.
        with mock.patch.object(
            put,
            "_get_openai_model_class",
            return_value=self._ModelWithPositionalArg,
        ):
            actual = put.build_explicit_openai_model(model_id)
        # Check outputs.
        self.assertEqual(actual.model_name, "gpt-5-nano")

    def test5(self) -> None:
        """
        Test that an empty model id raises an assertion.
        """
        # Prepare inputs.
        model_id = ""
        # Run test and check output.
        with self.assertRaises(AssertionError):
            with mock.patch.object(
                put, "_get_openai_model_class", return_value=self._Model
            ):
                put.build_explicit_openai_model(model_id)


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

    class _ModelsModule:
        """
        Fake models module.
        """

        ModelSettings = object()

    class _UsageModule:
        """
        Fake usage module.
        """

        UsageLimits = object()

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

    def test2(self) -> None:
        """
        Test fallback class discovery from submodules.
        """
        # Prepare inputs.
        pydantic_ai_module = sys.modules["pydantic_ai"]
        if hasattr(pydantic_ai_module, "ModelSettings"):
            del pydantic_ai_module.ModelSettings
        if hasattr(pydantic_ai_module, "UsageLimits"):
            del pydantic_ai_module.UsageLimits
        # Prepare outputs.
        expected = (
            self._ModelsModule.ModelSettings,
            self._UsageModule.UsageLimits,
        )
        # Run test.
        with mock.patch.object(
            put.importlib,
            "import_module",
            side_effect=[
                pydantic_ai_module,
                self._ModelsModule,
                self._UsageModule,
            ],
        ):
            actual = put.get_settings_classes()
        # Check outputs.
        self.assert_equal(str(actual), str(expected))
