import logging
import sys
import types
from pathlib import Path
from unittest import mock

import pandas as pd

_BAMBOOAI_DIR = Path(__file__).resolve().parents[1]
_CLASS_ROOT = Path(__file__).resolve().parents[3]
if str(_BAMBOOAI_DIR) not in sys.path:
    sys.path.insert(0, str(_BAMBOOAI_DIR))
if str(_CLASS_ROOT) not in sys.path:
    sys.path.insert(0, str(_CLASS_ROOT))
if str(_CLASS_ROOT / "helpers_root") not in sys.path:
    sys.path.insert(0, str(_CLASS_ROOT / "helpers_root"))

# Avoid importing optional BambooAI runtime dependencies during unit-test
# collection. Individual tests patch `bambooai_utils.BambooAI` directly.
_BAMBOOAI_MODULE = types.ModuleType("bambooai")
_BAMBOOAI_MODULE.BambooAI = mock.Mock()
sys.modules.setdefault("bambooai", _BAMBOOAI_MODULE)

import helpers.hunit_test as hunitest

import bambooai_utils as butils

_LOG = logging.getLogger(__name__)


class Test__parse(hunitest.TestCase):
    """
    Test the BambooAI notebook argument parser.
    """

    def test1(self) -> None:
        """
        Test parser default values.
        """
        # Prepare outputs.
        expected_csv_path = str(butils._DEFAULT_CSV)
        expected_execution_mode = ""
        # Run test.
        args = butils._parse().parse_args([])
        # Check outputs.
        self.assert_equal(str(args.csv_path), expected_csv_path)
        self.assert_equal(args.execution_mode, expected_execution_mode)

    def test2(self) -> None:
        """
        Test parser accepts explicit notebook workflow arguments.
        """
        # Prepare inputs.
        argv = ["--csv-path", "custom.csv", "--execution-mode", "local"]
        # Prepare outputs.
        expected_csv_path = "custom.csv"
        expected_execution_mode = "local"
        # Run test.
        args = butils._parse().parse_args(argv)
        # Check outputs.
        self.assert_equal(str(args.csv_path), expected_csv_path)
        self.assert_equal(args.execution_mode, expected_execution_mode)


class Test__resolve_execution_mode(hunitest.TestCase):
    """
    Test execution mode resolution.
    """

    def test1(self) -> None:
        """
        Test that a non-empty execution mode is returned unchanged.
        """
        # Prepare inputs.
        mode = "local"
        # Prepare outputs.
        expected = "local"
        # Run test.
        actual = butils._resolve_execution_mode(mode)
        # Check outputs.
        self.assert_equal(actual, expected)

    def test2(self) -> None:
        """
        Test that an empty execution mode raises.
        """
        # Prepare inputs.
        mode = ""
        # Run test.
        with self.assertRaises(AssertionError):
            butils._resolve_execution_mode(mode)


class Test__setup_env(hunitest.TestCase):
    """
    Test environment setup for the notebook workflow.
    """

    def test1(self) -> None:
        """
        Test that dotenv loading is triggered during setup.
        """
        # Run test.
        with mock.patch("bambooai_utils.load_dotenv") as mock_load_dotenv:
            butils._setup_env()
        # Check outputs.
        mock_load_dotenv.assert_called_once_with()


class Test__load_dataframe(hunitest.TestCase):
    """
    Test CSV loading for the BambooAI notebook workflow.
    """

    def helper(self, df_in: pd.DataFrame) -> None:
        """
        Test helper for dataframe loading.

        :param df_in: dataframe to serialize and reload
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        csv_path = Path(scratch_dir) / "input.csv"
        df_in.to_csv(csv_path, index=False)
        # Prepare outputs.
        expected = df_in
        # Run test.
        actual = butils._load_dataframe(csv_path)
        # Check outputs.
        self.assert_equal(str(actual), str(expected))

    def test1(self) -> None:
        """
        Test loading a non-empty CSV file.
        """
        # Prepare inputs.
        df_in = pd.DataFrame(
            {
                "country": ["US", "CA"],
                "monthly_spend_usd": [10.0, 20.5],
            }
        )
        # Run test.
        self.helper(df_in)

    def test2(self) -> None:
        """
        Test loading a single-row CSV file.
        """
        # Prepare inputs.
        df_in = pd.DataFrame(
            {
                "country": ["US"],
                "monthly_spend_usd": [10.0],
            }
        )
        # Run test.
        self.helper(df_in)

    def test3(self) -> None:
        """
        Test that an empty CSV raises.
        """
        # Prepare inputs.
        scratch_dir = self.get_scratch_space()
        csv_path = Path(scratch_dir) / "input.csv"
        pd.DataFrame(columns=["country", "monthly_spend_usd"]).to_csv(
            csv_path, index=False
        )
        # Run test.
        with self.assertRaises(AssertionError):
            butils._load_dataframe(csv_path)


class Test__build_bamboo_agent(hunitest.TestCase):
    """
    Test BambooAI agent construction.
    """

    def test1(self) -> None:
        """
        Test that construction forwards the dataframe and feature flags.
        """
        # Prepare inputs.
        df = pd.DataFrame({"value": [1, 2]})
        expected_agent = mock.Mock()
        # Run test.
        with mock.patch("bambooai_utils.BambooAI") as mock_bambooai:
            mock_bambooai.return_value = expected_agent
            actual = butils._build_bamboo_agent(
                df,
                planning=False,
                vector_db=True,
                search_tool=True,
            )
        # Check outputs.
        self.assertIs(actual, expected_agent)
        mock_bambooai.assert_called_once()
        self.assertIs(mock_bambooai.call_args.kwargs["df"], df)
        self.assertEqual(mock_bambooai.call_args.kwargs["planning"], False)
        self.assertEqual(mock_bambooai.call_args.kwargs["vector_db"], True)
        self.assertEqual(mock_bambooai.call_args.kwargs["search_tool"], True)

    def test2(self) -> None:
        """
        Test that construction uses the default feature flags.
        """
        # Prepare inputs.
        df = pd.DataFrame({"value": [1, 2]})
        expected_agent = mock.Mock()
        # Run test.
        with mock.patch("bambooai_utils.BambooAI") as mock_bambooai:
            mock_bambooai.return_value = expected_agent
            actual = butils._build_bamboo_agent(df)
        # Check outputs.
        self.assertIs(actual, expected_agent)
        self.assertIs(mock_bambooai.call_args.kwargs["df"], df)
        self.assertEqual(mock_bambooai.call_args.kwargs["planning"], True)
        self.assertEqual(mock_bambooai.call_args.kwargs["vector_db"], False)
        self.assertEqual(mock_bambooai.call_args.kwargs["search_tool"], False)

    def test3(self) -> None:
        """
        Test that extra keyword arguments are forwarded.
        """
        # Prepare inputs.
        df = pd.DataFrame({"value": [1, 2]})
        expected_agent = mock.Mock()
        # Run test.
        with mock.patch("bambooai_utils.BambooAI") as mock_bambooai:
            mock_bambooai.return_value = expected_agent
            actual = butils._build_bamboo_agent(
                df,
                exploratory=True,
                custom_prompt_file="custom_prompts.yaml",
            )
        # Check outputs.
        self.assertIs(actual, expected_agent)
        self.assertEqual(mock_bambooai.call_args.kwargs["exploratory"], True)
        self.assertEqual(
            mock_bambooai.call_args.kwargs["custom_prompt_file"],
            "custom_prompts.yaml",
        )


class Test__run_agent(hunitest.TestCase):
    """
    Test BambooAI agent execution wrapper.
    """

    def test1(self) -> None:
        """
        Test that the wrapper calls the agent conversation method once.
        """
        # Prepare inputs.
        bamboo_ai = mock.Mock()
        # Run test.
        butils._run_agent(bamboo_ai)
        # Check outputs.
        bamboo_ai.pd_agent_converse.assert_called_once_with()

    def test2(self) -> None:
        """
        Test that the wrapper logs start and finish messages.
        """
        # Prepare inputs.
        bamboo_ai = mock.Mock()
        # Run test.
        with mock.patch.object(butils._LOG, "info") as mock_log_info:
            butils._run_agent(bamboo_ai)
        # Check outputs.
        actual = [call.args[0] for call in mock_log_info.call_args_list]
        expected = [
            "Starting BambooAI conversation.",
            "Finished BambooAI conversation.",
        ]
        self.assert_equal(str(actual), str(expected))


class Test__main(hunitest.TestCase):
    """
    Test the main BambooAI workflow orchestration.
    """

    def test1(self) -> None:
        """
        Test that main wires together parsing, loading, and execution.
        """
        # Prepare inputs.
        parser = mock.Mock()
        args = types.SimpleNamespace(
            log_level=logging.INFO,
            csv_path="input.csv",
            execution_mode="local",
        )
        parser.parse_args.return_value = args
        df = pd.DataFrame({"value": [1]})
        bamboo_agent = mock.Mock()
        # Run test.
        with mock.patch("bambooai_utils.hdbg.init_logger") as mock_init_logger:
            with mock.patch("bambooai_utils._setup_env") as mock_setup_env:
                with mock.patch(
                    "bambooai_utils._resolve_execution_mode",
                    return_value="local",
                ) as mock_resolve_execution_mode:
                    with mock.patch(
                        "bambooai_utils._load_dataframe", return_value=df
                    ) as mock_load_dataframe:
                        with mock.patch(
                            "bambooai_utils._build_bamboo_agent",
                            return_value=bamboo_agent,
                        ) as mock_build_bamboo_agent:
                            with mock.patch(
                                "bambooai_utils._run_agent"
                            ) as mock_run_agent:
                                butils._main(parser)
        # Check outputs.
        parser.parse_args.assert_called_once_with([])
        mock_init_logger.assert_called_once_with(
            verbosity=args.log_level, use_exec_path=True
        )
        mock_setup_env.assert_called_once_with()
        mock_resolve_execution_mode.assert_called_once_with(args.execution_mode)
        mock_load_dataframe.assert_called_once_with(Path(args.csv_path))
        mock_build_bamboo_agent.assert_called_once_with(df)
        mock_run_agent.assert_called_once_with(bamboo_agent)
