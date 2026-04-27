"""
Test utility functions for tutorials/tutorial_pydanticAI/pydanticai.example.
"""

import asyncio
import importlib.util
import logging
import os
import pathlib
import sys
import types
from dataclasses import dataclass
from types import SimpleNamespace
from unittest import mock

import helpers.hunit_test as hunitest

if importlib.util.find_spec("pydantic_ai") is None:

    class ModelRetry(Exception):
        """
        Minimal stub for pydantic_ai.ModelRetry.
        """

    pydantic_ai_stub = types.ModuleType("pydantic_ai")
    pydantic_ai_stub.ModelRetry = ModelRetry
    sys.modules["pydantic_ai"] = pydantic_ai_stub

import pydanticai_example_utils as peu
from pydantic_ai import ModelRetry

_LOG = logging.getLogger(__name__)


@dataclass
class _DocChunk:
    """
    Minimal chunk object for tests.
    """

    doc_id: str
    chunk_id: int
    text: str
    vector: list[float]


@dataclass
class _DocMatch:
    """
    Minimal ranked match object for tests.
    """

    doc_id: str
    chunk_id: int
    score: float
    text: str


# #############################################################################
# Test_init_logger
# #############################################################################


class Test_init_logger(hunitest.TestCase):
    """
    Test notebook logger initialization.
    """

    def test1(self) -> None:
        """
        Test initialization with an existing module logger.
        """
        # Prepare inputs.
        notebook_log = logging.getLogger("test_notebook")
        module_log = logging.getLogger("test_module")
        # Run test.
        with mock.patch.object(peu, "_LOG", module_log), mock.patch.object(
            peu.hnotebo, "config_notebook"
        ) as mock_config, mock.patch.object(
            peu.hdbg, "init_logger"
        ) as mock_init_logger, mock.patch.object(
            peu.hnotebo, "set_logger_to_print"
        ) as mock_set_logger:
            peu.init_logger(notebook_log)
        # Check outputs.
        mock_config.assert_called_once()
        mock_init_logger.assert_called_once_with(
            verbosity=logging.INFO, use_exec_path=False
        )
        self.assertEqual(
            mock_set_logger.call_args_list,
            [mock.call(notebook_log), mock.call(module_log)],
        )

    def test2(self) -> None:
        """
        Test initialization when the module logger must be recreated.
        """
        # Prepare inputs.
        notebook_log = logging.getLogger("test_notebook")
        expected = logging.getLogger(peu.__name__)
        # Run test.
        with mock.patch.object(peu, "_LOG", None), mock.patch.object(
            peu.hnotebo, "config_notebook"
        ), mock.patch.object(
            peu.hdbg, "init_logger"
        ), mock.patch.object(
            peu.hnotebo, "set_logger_to_print"
        ) as mock_set_logger:
            peu.init_logger(notebook_log)
        # Check outputs.
        self.assertEqual(
            mock_set_logger.call_args_list,
            [mock.call(notebook_log), mock.call(expected)],
        )
        self.assertEqual(peu._LOG, expected)


# #############################################################################
# Test__stable_index
# #############################################################################


class Test__stable_index(hunitest.TestCase):
    """
    Test deterministic token indexing.
    """

    def helper(self, token: str, dim: int) -> int:
        """
        Test helper for `_stable_index()`.

        :param token: input token
        :param dim: embedding dimension
        :return: stable index
        """
        # Run test.
        actual = peu._stable_index(token, dim=dim)
        # Check outputs.
        self.assertEqual(actual < dim, True)
        self.assertEqual(actual >= 0, True)
        return actual

    def test1(self) -> None:
        """
        Test that the same token maps deterministically.
        """
        # Prepare inputs.
        token = "atlas"
        dim = 256
        # Run test.
        actual1 = self.helper(token, dim)
        actual2 = self.helper(token, dim)
        # Check outputs.
        self.assertEqual(actual1, actual2)

    def test2(self) -> None:
        """
        Test that an empty token still maps inside bounds.
        """
        # Prepare inputs.
        token = ""
        dim = 8
        # Run test.
        actual = self.helper(token, dim)
        # Check outputs.
        self.assertEqual(actual < dim, True)


# #############################################################################
# Test_embed
# #############################################################################


class Test_embed(hunitest.TestCase):
    """
    Test deterministic text embeddings.
    """

    def test1(self) -> None:
        """
        Test embedding an empty string.
        """
        # Prepare inputs.
        text = ""
        # Run test.
        actual = peu.embed(text)
        # Check outputs.
        self.assertEqual(len(actual), 256)
        self.assertEqual(sum(actual), 0.0)

    def test2(self) -> None:
        """
        Test embedding normalization and token cleanup.
        """
        # Prepare inputs.
        text1 = "Atlas billing"
        text2 = "atlas BILLING!!"
        # Run test.
        actual1 = peu.embed(text1)
        actual2 = peu.embed(text2)
        norm = sum(x * x for x in actual1)
        # Check outputs.
        self.assert_equal(str(actual1), str(actual2))
        self.assertEqual(round(norm, 6), 1.0)


# #############################################################################
# Test_dot
# #############################################################################


class Test_dot(hunitest.TestCase):
    """
    Test vector dot products.
    """

    def helper(
        self, left: list[float], right: list[float], expected: float
    ) -> None:
        """
        Test helper for `dot()`.

        :param left: left vector
        :param right: right vector
        :param expected: expected dot product
        """
        # Run test.
        actual = peu.dot(left, right)
        # Check outputs.
        self.assertEqual(actual, expected)

    def test1(self) -> None:
        """
        Test a normal dot product.
        """
        # Prepare inputs.
        left = [1.0, 2.0, 3.0]
        right = [4.0, 5.0, 6.0]
        # Prepare outputs.
        expected = 32.0
        # Run test.
        self.helper(left, right, expected)

    def test2(self) -> None:
        """
        Test the dot product of empty vectors.
        """
        # Prepare inputs.
        left = []
        right = []
        # Prepare outputs.
        expected = 0
        # Run test.
        self.helper(left, right, expected)


# #############################################################################
# Test_chunk_docs
# #############################################################################


class Test_chunk_docs(hunitest.TestCase):
    """
    Test document chunking.
    """

    def test1(self) -> None:
        """
        Test chunking a short document into one chunk.
        """
        # Prepare inputs.
        docs = [{"doc_id": "billing", "text": "invoice details"}]
        # Run test.
        actual = peu.chunk_docs(docs, _DocChunk, max_chars=100)
        # Check outputs.
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0].doc_id, "billing")
        self.assertEqual(actual[0].chunk_id, 0)
        self.assertEqual(actual[0].text, "invoice details")

    def test2(self) -> None:
        """
        Test chunking a document into multiple parts.
        """
        # Prepare inputs.
        docs = [{"doc_id": "billing", "text": "abcdefgh"}]
        # Run test.
        actual = peu.chunk_docs(docs, _DocChunk, max_chars=3)
        # Check outputs.
        expected = ["abc", "def", "gh"]
        self.assert_equal(str([chunk.text for chunk in actual]), str(expected))


# #############################################################################
# Test_search_chunks
# #############################################################################


class Test_search_chunks(hunitest.TestCase):
    """
    Test chunk ranking and truncation.
    """

    def test1(self) -> None:
        """
        Test ranking chunks by query similarity.
        """
        # Prepare inputs.
        chunks = [
            _DocChunk("limits", 0, "storage limits", peu.embed("storage limits")),
            _DocChunk("billing", 0, "invoice billing", peu.embed("invoice billing")),
        ]
        # Run test.
        actual = peu.search_chunks(
            chunks,
            "invoice",
            _DocMatch,
            top_k=2,
        )
        # Check outputs.
        self.assertEqual(actual[0].doc_id, "billing")
        self.assertEqual(len(actual), 2)

    def test2(self) -> None:
        """
        Test limiting the number of ranked matches.
        """
        # Prepare inputs.
        chunks = [
            _DocChunk("a", 0, "billing", peu.embed("billing")),
            _DocChunk("b", 0, "invoice", peu.embed("invoice")),
            _DocChunk("c", 0, "support", peu.embed("support")),
        ]
        # Run test.
        actual = peu.search_chunks(chunks, "invoice", _DocMatch, top_k=1)
        # Check outputs.
        self.assertEqual(len(actual), 1)


# #############################################################################
# Test_search_docs
# #############################################################################


class Test_search_docs(hunitest.TestCase):
    """
    Test context-aware document search.
    """

    def test1(self) -> None:
        """
        Test searching through chunks stored in the run context.
        """
        # Prepare inputs.
        chunks = [
            _DocChunk("billing", 0, "invoice download", peu.embed("invoice download")),
            _DocChunk("security", 0, "enable 2fa", peu.embed("enable 2fa")),
        ]
        ctx = SimpleNamespace(deps=SimpleNamespace(chunks=chunks))
        # Run test.
        actual = peu.search_docs(ctx, "invoice", doc_match_cls=_DocMatch)
        # Check outputs.
        self.assertEqual(actual[0].doc_id, "billing")


# #############################################################################
# Test_enforce_sources
# #############################################################################


class Test_enforce_sources(hunitest.TestCase):
    """
    Test answer source validation.
    """

    def helper(self, result: SimpleNamespace, expected: str | SimpleNamespace) -> None:
        """
        Test helper for `enforce_sources()`.

        :param result: validator input
        :param expected: expected output or retry message
        """
        # Run test.
        if isinstance(expected, str):
            with self.assertRaises(ModelRetry) as cm:
                peu.enforce_sources(result)
            actual = str(cm.exception)
            # Check outputs.
            self.assert_equal(actual, expected)
        else:
            actual = peu.enforce_sources(result)
            # Check outputs.
            self.assertEqual(actual, expected)

    def test1(self) -> None:
        """
        Test a standalone answer with no sources.
        """
        # Prepare inputs.
        result = self._build_result("This answer is standalone.", [])
        # Run test.
        self.helper(result, result)

    def test2(self) -> None:
        """
        Test a document-backed answer with valid sources.
        """
        # Prepare inputs.
        sources = [self._build_source("billing", 0, "download invoices")]
        result = self._build_result("According to billing docs.", sources)
        # Run test.
        self.helper(result, result)

    def test3(self) -> None:
        """
        Test that document-backed answers require sources.
        """
        # Prepare inputs.
        result = self._build_result("According to the document.", [])
        # Prepare outputs.
        expected = "You referenced docs/policies but did not include sources."
        # Run test.
        self.helper(result, expected)

    def test4(self) -> None:
        """
        Test that too many sources raise a retry.
        """
        # Prepare inputs.
        sources = [
            self._build_source("doc1", 0, "quote1"),
            self._build_source("doc2", 0, "quote2"),
            self._build_source("doc3", 0, "quote3"),
            self._build_source("doc4", 0, "quote4"),
        ]
        result = self._build_result("Standalone answer.", sources)
        # Prepare outputs.
        expected = "Too many sources. Max 3."
        # Run test.
        self.helper(result, expected)

    def test5(self) -> None:
        """
        Test that duplicate sources raise a retry.
        """
        # Prepare inputs.
        sources = [
            self._build_source("doc1", 0, "quote"),
            self._build_source("doc1", 0, "quote"),
        ]
        result = self._build_result("Standalone answer.", sources)
        # Prepare outputs.
        expected = "Duplicate sources. Keep sources unique."
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
    def _build_source(
        doc_id: str, chunk_id: int, quote: str
    ) -> SimpleNamespace:
        """
        Build a source reference object.

        :param doc_id: document identifier
        :param chunk_id: chunk identifier
        :param quote: source quote
        :return: source reference
        """
        source = SimpleNamespace(doc_id=doc_id, chunk_id=chunk_id, quote=quote)
        return source


# #############################################################################
# Test_ask
# #############################################################################


class Test_ask(hunitest.TestCase):
    """
    Test async agent wrappers.
    """

    def test1(self) -> None:
        """
        Test that `ask()` returns the agent output.
        """
        # Prepare inputs.
        deps = SimpleNamespace(name="deps")
        expected = {"answer": "ok"}

        class _Agent:
            async def run(self, query: str, deps: object) -> SimpleNamespace:
                return SimpleNamespace(output=expected)

        agent = _Agent()
        # Run test.
        actual = asyncio.run(peu.ask("question", deps, agent))
        # Check outputs.
        self.assertEqual(actual, expected)


# #############################################################################
# Test_stream_demo
# #############################################################################


class Test_stream_demo(hunitest.TestCase):
    """
    Test streaming notebook output helpers.
    """

    def test1(self) -> None:
        """
        Test fallback streaming for agents without `run_stream`.
        """
        # Prepare inputs.
        expected = "Unit tests matter."

        class _Agent:
            async def run(self, query: str) -> SimpleNamespace:
                return SimpleNamespace(output=expected)

        stream_agent = _Agent()
        # Run test.
        with mock.patch("builtins.print") as mock_print:
            asyncio.run(peu.stream_demo(stream_agent))
        # Check outputs.
        mock_print.assert_called_once_with(expected)

    def test2(self) -> None:
        """
        Test streaming text chunks from `run_stream`.
        """
        # Prepare inputs.
        chunks = ["Unit ", "tests"]

        class _Stream:
            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc, tb):
                return False

            async def stream_text(self):
                for chunk in chunks:
                    yield chunk

        class _Agent:
            def run_stream(self, query: str) -> _Stream:
                return _Stream()

        stream_agent = _Agent()
        # Run test.
        with mock.patch("builtins.print") as mock_print:
            asyncio.run(peu.stream_demo(stream_agent))
        # Check outputs.
        expected = [
            mock.call("Unit ", end="", flush=True),
            mock.call("tests", end="", flush=True),
            mock.call("\n"),
        ]
        self.assertEqual(mock_print.call_args_list, expected)


# #############################################################################
# Test_in_scope
# #############################################################################


class Test_in_scope(hunitest.TestCase):
    """
    Test support-question guardrail classification.
    """

    def helper(self, question: str, expected: bool) -> None:
        """
        Test helper for `in_scope()`.

        :param question: user question
        :param expected: expected classification
        """
        # Run test.
        actual = peu.in_scope(question)
        # Check outputs.
        self.assertEqual(actual, expected)

    def test1(self) -> None:
        """
        Test an in-scope billing question.
        """
        # Prepare inputs.
        question = "How do I download an invoice?"
        # Prepare outputs.
        expected = True
        # Run test.
        self.helper(question, expected)

    def test2(self) -> None:
        """
        Test an out-of-scope creative question.
        """
        # Prepare inputs.
        question = "Write me a poem about the ocean."
        # Prepare outputs.
        expected = False
        # Run test.
        self.helper(question, expected)


# #############################################################################
# Test_run_guarded
# #############################################################################


class Test_run_guarded(hunitest.TestCase):
    """
    Test guarded agent execution.
    """

    def test1(self) -> None:
        """
        Test the out-of-scope guardrail response.
        """
        # Prepare inputs.
        answer_with_sources_cls = SimpleNamespace
        deps = SimpleNamespace()
        agent = SimpleNamespace()
        # Run test.
        actual = asyncio.run(
            peu.run_guarded(
                "Write me a poem about the ocean.",
                deps,
                agent,
                answer_with_sources_cls,
            )
        )
        # Check outputs.
        self.assertEqual(
            actual.answer,
            "I can only help with Atlas product documentation and support questions.",
        )
        self.assertEqual(len(actual.follow_up_questions), 1)

    def test2(self) -> None:
        """
        Test delegating an in-scope question to the agent.
        """
        # Prepare inputs.
        expected = {"answer": "Atlas support answer"}

        class _Agent:
            async def run(
                self, question: str, deps: object, message_history: object = None
            ) -> SimpleNamespace:
                return SimpleNamespace(output=expected)

        agent = _Agent()
        # Run test.
        actual = asyncio.run(
            peu.run_guarded(
                "How do I contact Atlas support?",
                SimpleNamespace(),
                agent,
                SimpleNamespace,
            )
        )
        # Check outputs.
        self.assertEqual(actual, expected)


# #############################################################################
# Test_load_docs
# #############################################################################


class Test_load_docs(hunitest.TestCase):
    """
    Test loading markdown documents from disk.
    """

    def test1(self) -> None:
        """
        Test loading and sorting markdown files.
        """
        # Prepare inputs.
        scratch_dir = pathlib.Path(self.get_scratch_space())
        (scratch_dir / "zeta.md").write_text("Zeta text", encoding="utf-8")
        (scratch_dir / "alpha.md").write_text("Alpha text", encoding="utf-8")
        # Run test.
        actual = peu.load_docs(scratch_dir)
        # Check outputs.
        self.assert_equal(
            str([doc["doc_id"] for doc in actual]), str(["alpha", "zeta"])
        )
        self.assertEqual(actual[0]["title"], "Alpha")
        self.assertEqual(actual[1]["text"], "Zeta text")

    def test2(self) -> None:
        """
        Test loading an empty directory.
        """
        # Prepare inputs.
        scratch_dir = pathlib.Path(self.get_scratch_space()) / "empty_docs"
        os.makedirs(scratch_dir, exist_ok=True)
        # Run test.
        actual = peu.load_docs(scratch_dir)
        # Check outputs.
        self.assert_equal(str(actual), str([]))
