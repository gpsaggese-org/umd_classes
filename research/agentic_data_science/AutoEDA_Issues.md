# AutoEDA Agent - Issues Backlog

This document outlines all issues organized by EPIC for GitHub/Linear/Jira tracking.

---

## EPIC 1: Foundation & Infrastructure Setup

### Issue #1.1: Set up LangGraph and LangChain integration
**Epic:** Foundation
**Priority:** P0 (Critical)
**Complexity:** M
**Owner:** TBD

**Description:**
Add LangGraph and LangChain as project dependencies. Set up base module for initialization and configuration.

**Tasks:**
- [ ] Add `langraph` and `langchain` to `requirements.txt`
- [ ] Create `helpers/lang_graph_setup.py` with initialization
- [ ] Test with basic LangGraph StateGraph example
- [ ] Document version compatibility
- [ ] Create test fixtures for LangGraph testing

**Acceptance Criteria:**
- Dependencies install without conflicts
- Example LangGraph graph compiles and runs
- Test fixtures available for other issues

**Related Links:**
- https://github.com/causify-ai/helpers/issues/986

---

### Issue #1.2: Define core module structure for AutoEDA
**Epic:** Foundation
**Priority:** P0 (Critical)
**Complexity:** S
**Owner:** TBD

**Description:**
Create the package structure for the AutoEDA agent system.

**Tasks:**
- [ ] Create `helpers/hagentic_eda/` directory
- [ ] Create submodules: `state.py`, `graph.py`, `tools.py`, `prompts.py`, `utils.py`
- [ ] Create `__init__.py` with public API exports
- [ ] Create `README.md` documenting structure
- [ ] Add to `helpers/__init__.py` imports

**Acceptance Criteria:**
- `import helpers.hagentic_eda` works
- All submodules are discoverable
- Package structure follows helpers conventions

---

### Issue #1.3: Create integration tests setup
**Epic:** Foundation
**Priority:** P0 (Critical)
**Complexity:** M
**Owner:** TBD

**Description:**
Set up pytest fixtures and test infrastructure for AutoEDA testing.

**Tasks:**
- [ ] Create `helpers/test/test_hagentic_eda_fixtures.py`
- [ ] Create `helpers/test/input/hagentic_eda/` with sample datasets
  - [ ] Sample CSV (mixed types)
  - [ ] Sample Parquet
  - [ ] Sample Feather
  - [ ] Sample schema YAML/JSON files
- [ ] Create fixtures for DataFrame, schema, agent state
- [ ] Document fixture usage in test examples

**Acceptance Criteria:**
- Fixtures importable in tests
- Sample datasets load correctly
- Fixtures cover common scenarios

---

## EPIC 2: Agent State Management

### Issue #2.1: Define AgentState schema with Pydantic
**Epic:** Agent State Management
**Priority:** P0 (Critical)
**Complexity:** M
**Owner:** TBD

**Description:**
Create the core AgentState class using Pydantic for type safety and validation.

**File:** `helpers/hagentic_eda/state.py`

**Tasks:**
- [ ] Define `AgentState` class with:
  - `conversation_history`: List[Message]
  - `dataset_context`: DataFrameInfo
  - `analysis_phase`: Enum (setup, cleaning, analysis, reporting)
  - `generated_cells`: List[NotebookCell]
  - `error_log`: List[str]
  - `metadata`: Dict[str, Any]
- [ ] Use Pydantic V2 with field validators
- [ ] Add docstrings for all fields
- [ ] Create example AgentState in docstring

**Acceptance Criteria:**
- State instantiates with valid data
- Validation catches invalid inputs
- Field documentation clear

**Tests:**
- `helpers/test/test_hagentic_eda_state.py::TestAgentState`

---

### Issue #2.2: Define supporting schema classes
**Epic:** Agent State Management
**Priority:** P0 (Critical)
**Complexity:** M
**Owner:** TBD

**Description:**
Create Pydantic models for nested state structures.

**File:** `helpers/hagentic_eda/state.py`

**Tasks:**
- [ ] Create `DataFrameInfo` with:
  - `shape`: Tuple[int, int]
  - `columns`: List[str]
  - `dtypes`: Dict[str, str]
  - `null_counts`: Dict[str, int]
  - `sample_values`: Dict[str, List[Any]]
- [ ] Create `ColumnInfo` with:
  - `name`: str
  - `dtype`: str
  - `detected_type`: str (numeric, categorical, datetime, text)
  - `statistics`: Dict[str, float]
  - `issues`: List[str]
- [ ] Create `NotebookCell` with:
  - `id`: str (UUID)
  - `type`: Enum (code, markdown)
  - `content`: str
  - `result`: Optional[str]
  - `error`: Optional[str]
  - `timestamp`: datetime
- [ ] Create `Message` class for conversation history
  - `role`: Enum (user, assistant, system)
  - `content`: str
  - `timestamp`: datetime

**Acceptance Criteria:**
- All classes instantiate correctly
- Serialization/deserialization works
- Field types match expected usage

**Tests:**
- `helpers/test/test_hagentic_eda_state.py::TestDataFrameInfo`
- `helpers/test/test_hagentic_eda_state.py::TestColumnInfo`
- `helpers/test/test_hagentic_eda_state.py::TestNotebookCell`

---

### Issue #2.3: Implement state serialization utilities
**Epic:** Agent State Management
**Priority:** P1 (High)
**Complexity:** M
**Owner:** TBD

**Description:**
Create functions to serialize and deserialize agent state for persistence.

**File:** `helpers/hagentic_eda/state.py`

**Tasks:**
- [ ] Implement `serialize_state(state: AgentState) -> str`
  - Convert to JSON
  - Handle datetime serialization
  - Handle enums
- [ ] Implement `deserialize_state(data: str) -> AgentState`
  - Parse JSON
  - Reconstruct state
  - Validate on load
- [ ] Implement `save_state_to_file(state: AgentState, path: str)`
- [ ] Implement `load_state_from_file(path: str) -> AgentState`
- [ ] Create round-trip tests

**Acceptance Criteria:**
- State round-trips without data loss
- Datetime and enum preserved correctly
- File I/O works

**Tests:**
- `helpers/test/test_hagentic_eda_state.py::Test_serialize_state`
- `helpers/test/test_hagentic_eda_state.py::Test_deserialize_state`

---

### Issue #2.4: Add state management utilities
**Epic:** Agent State Management
**Priority:** P1 (High)
**Complexity:** L
**Owner:** TBD

**Description:**
Create helper methods for common state updates.

**File:** `helpers/hagentic_eda/state.py`

**Tasks:**
- [ ] `update_dataset_context(state: AgentState, df: pd.DataFrame) -> AgentState`
  - Infer schema from dataframe
  - Detect column types
  - Calculate statistics
- [ ] `log_error(state: AgentState, error: str) -> AgentState`
  - Add error to error_log
  - Include timestamp
  - Keep last N errors
- [ ] `add_cell_result(state: AgentState, cell: NotebookCell) -> AgentState`
  - Append to generated_cells
  - Update analysis progress
- [ ] `add_message(state: AgentState, role: str, content: str) -> AgentState`
  - Add to conversation_history
  - Include timestamp
- [ ] Unit tests for all utilities

**Acceptance Criteria:**
- Methods update state correctly
- No state mutations (immutable pattern)
- Tests pass with 100% coverage

**Tests:**
- `helpers/test/test_hagentic_eda_state.py::Test_update_dataset_context`
- `helpers/test/test_hagentic_eda_state.py::Test_log_error`
- `helpers/test/test_hagentic_eda_state.py::Test_add_cell_result`

---

## EPIC 3: LangGraph Agent Orchestration

### Issue #3.1: Define graph nodes
**Epic:** LangGraph Agent Orchestration
**Priority:** P0 (Critical)
**Complexity:** L
**Owner:** TBD

**Description:**
Implement all node functions for the LangGraph state machine.

**File:** `helpers/hagentic_eda/graph.py`

**Tasks:**
- [ ] `agent_node(state: AgentState) -> AgentState`
  - Call LLM with system prompt
  - Add response to conversation_history
  - Return updated state
- [ ] `tools_node(state: AgentState) -> AgentState`
  - Extract tool calls from agent response
  - Execute tools
  - Add results to conversation_history
- [ ] `generate_code_node(state: AgentState) -> AgentState`
  - Extract code from agent response
  - Validate code (no dangerous commands)
  - Format code
  - Create NotebookCell
  - Return state with cell ready for execution
- [ ] `update_context_node(state: AgentState) -> AgentState`
  - Process execution results
  - Update dataset_context if needed
  - Add results to conversation_history
- [ ] `handle_error_node(state: AgentState) -> AgentState`
  - Parse error message
  - Generate fix code
  - Log error
  - Create corrective cell

**Acceptance Criteria:**
- All nodes implement correct signature
- State transitions work
- Unit tests for each node

**Tests:**
- `helpers/test/test_hagentic_eda_graph.py::TestAgentNode`
- `helpers/test/test_hagentic_eda_graph.py::TestToolsNode`
- `helpers/test/test_hagentic_eda_graph.py::TestGenerateCodeNode`

---

### Issue #3.2: Define graph edges and routing logic
**Epic:** LangGraph Agent Orchestration
**Priority:** P0 (Critical)
**Complexity:** M
**Owner:** TBD

**Description:**
Create conditional routing functions and connect graph edges.

**File:** `helpers/hagentic_eda/graph.py`

**Tasks:**
- [ ] `should_use_tools(state: AgentState) -> bool`
  - Check if agent response contains tool calls
- [ ] `should_generate_code(state: AgentState) -> bool`
  - Check if agent response contains code blocks
- [ ] `should_handle_error(state: AgentState) -> bool`
  - Check if error occurred in last execution
- [ ] Build StateGraph:
  - START -> agent_node
  - agent_node -> tools_node (if should_use_tools)
  - agent_node -> generate_code_node (if should_generate_code)
  - agent_node -> END (if complete)
  - tools_node -> agent_node
  - generate_code_node -> INTERRUPT
- [ ] Test routing logic

**Acceptance Criteria:**
- Graph compiles without errors
- Routing conditions tested
- Graph visualization works

**Tests:**
- `helpers/test/test_hagentic_eda_graph.py::Test_should_use_tools`
- `helpers/test/test_hagentic_eda_graph.py::Test_graph_routing`

---

### Issue #3.3: Implement interrupt/resume for execution feedback
**Epic:** LangGraph Agent Orchestration
**Priority:** P0 (Critical)
**Complexity:** M
**Owner:** TBD

**Description:**
Set up interrupt/resume mechanism for notebook cell execution.

**File:** `helpers/hagentic_eda/graph.py`

**Tasks:**
- [ ] Configure `interrupt_after=[generate_code_node]` in graph
- [ ] Implement `resume_with_results(state: AgentState, results: Dict) -> AgentState`
  - Update cell result in state
  - Trigger update_context_node
  - Continue graph execution
- [ ] Implement `resume_with_error(state: AgentState, error: str) -> AgentState`
  - Log error
  - Trigger handle_error_node
- [ ] Test interrupt/resume cycle

**Acceptance Criteria:**
- Graph interrupts correctly
- Resume with results updates state
- Error handling works

**Tests:**
- `helpers/test/test_hagentic_eda_graph.py::Test_interrupt_resume`

---

### Issue #3.4: Set up state persistence with checkpointing
**Epic:** LangGraph Agent Orchestration
**Priority:** P1 (High)
**Complexity:** M
**Owner:** TBD

**Description:**
Implement checkpointing for state persistence across sessions.

**File:** `helpers/hagentic_eda/graph.py`

**Tasks:**
- [ ] Configure memory-based checkpointing in StateGraph
- [ ] Implement `save_checkpoint(state: AgentState, checkpoint_id: str)`
  - Serialize state
  - Save to file or database
- [ ] Implement `load_checkpoint(checkpoint_id: str) -> AgentState`
  - Restore from file or database
- [ ] Implement `list_checkpoints() -> List[str]`
  - Show available checkpoints
- [ ] Test state recovery

**Acceptance Criteria:**
- Checkpoints save/load correctly
- State recovery works
- Multiple checkpoints can exist

**Tests:**
- `helpers/test/test_hagentic_eda_graph.py::Test_checkpoint_save_load`

---

### Issue #3.5: Create graph visualization and documentation
**Epic:** LangGraph Agent Orchestration
**Priority:** P2 (Medium)
**Complexity:** M
**Owner:** TBD

**Description:**
Generate visual documentation of the graph structure.

**File:** `helpers/hagentic_eda/graph.py`

**Tasks:**
- [ ] Add `export_graph_mermaid() -> str`
  - Generate Mermaid diagram of state machine
- [ ] Add `export_graph_ascii() -> str`
  - Generate ASCII diagram
- [ ] Create `GRAPH_DOCUMENTATION.md`
  - Describe nodes and responsibilities
  - Document state transitions
  - Include diagrams
- [ ] Add examples of graph execution

**Acceptance Criteria:**
- Diagrams render correctly
- Documentation is clear and complete

---

## EPIC 4: System Prompt Engineering

### Issue #4.1: Design system prompt template structure
**Epic:** System Prompt Engineering
**Priority:** P1 (High)
**Complexity:** M
**Owner:** TBD

**Description:**
Create the foundational system prompt template with all major sections.

**File:** `helpers/hagentic_eda/prompts.py`

**Tasks:**
- [ ] Define prompt template with sections:
  - Role and capabilities
  - Workflow phases and transitions
  - Code generation guidelines
  - Data analysis best practices
  - Output format requirements
  - Context injection placeholders
- [ ] Create `SystemPromptTemplate` class
- [ ] Add example prompt with annotations
- [ ] Test token counting for context window

**Acceptance Criteria:**
- Template renders without errors
- All sections present and meaningful
- Total tokens under LLM context limit

**Tests:**
- `helpers/test/test_hagentic_eda_prompts.py::Test_system_prompt_template`

---

### Issue #4.2: Implement context formatting functions
**Epic:** System Prompt Engineering
**Priority:** P1 (High)
**Complexity:** M
**Owner:** TBD

**Description:**
Create functions to format and inject context into prompts.

**File:** `helpers/hagentic_eda/prompts.py`

**Tasks:**
- [ ] `format_dataframe_context(state: AgentState) -> str`
  - Summarize current data state
  - Include schema, size, sample values
- [ ] `format_error_context(state: AgentState) -> str`
  - Include last error and recovery suggestions
- [ ] `format_analysis_history(state: AgentState) -> str`
  - Recent conversation summary
  - Previous analysis steps
- [ ] `format_column_statistics(state: AgentState) -> str`
  - Summary statistics for all columns
- [ ] Test formatting with various state conditions

**Acceptance Criteria:**
- Formatted context is concise (< 2000 tokens)
- All information necessary for agent decision-making
- Edge cases handled (empty data, errors, etc.)

**Tests:**
- `helpers/test/test_hagentic_eda_prompts.py::Test_format_dataframe_context`
- `helpers/test/test_hagentic_eda_prompts.py::Test_format_error_context`

---

### Issue #4.3: Design phase-specific prompt variations
**Epic:** System Prompt Engineering
**Priority:** P1 (High)
**Complexity:** L
**Owner:** TBD

**Description:**
Create distinct prompts for each analysis phase.

**File:** `helpers/hagentic_eda/prompts.py`

**Tasks:**
- [ ] **Phase 1: "Read Schema and Infer Types"**
  - Focus: Understanding data structure
  - Tools: Inspection tools
  - Code: Schema parsing
- [ ] **Phase 2: "Propose EDA Plan"**
  - Focus: Planning analysis approach
  - Tools: Suggestion tools
  - Output: Analysis plan for user confirmation
- [ ] **Phase 3: "Run Full Analysis"**
  - Focus: Executing planned analyses
  - Tools: Analysis tools
  - Code: Data exploration and visualization
- [ ] **Phase 4: "Generate Report"**
  - Focus: Summarizing insights
  - Output: Final report and key findings
- [ ] Create `get_phase_prompt(phase: str) -> str` function

**Acceptance Criteria:**
- Each phase has distinct guidance
- Phase transitions are clear
- Prompts guide agent correctly

**Tests:**
- `helpers/test/test_hagentic_eda_prompts.py::Test_phase_specific_prompts`

---

### Issue #4.4: Create prompt testing framework
**Epic:** System Prompt Engineering
**Priority:** P2 (Medium)
**Complexity:** M
**Owner:** TBD

**Description:**
Create tests and utilities for prompt quality assurance.

**File:** `helpers/hagentic_eda/prompts.py`

**Tasks:**
- [ ] `count_tokens(prompt: str) -> int`
  - Use tiktoken or model's tokenizer
- [ ] `validate_prompt_structure(prompt: str) -> bool`
  - Check for required sections
- [ ] Create unit tests for prompt formatting
- [ ] Create smoke tests with LLM (token counting)
- [ ] Create example prompts with annotations

**Acceptance Criteria:**
- Tests pass
- Prompts under context limits
- Examples clear and runnable

**Tests:**
- `helpers/test/test_hagentic_eda_prompts.py::Test_prompt_validation`

---

## EPIC 5: Tool Definitions and Integration

### Issue #5.1: Implement inspection tools
**Epic:** Tool Definitions and Integration
**Priority:** P1 (High)
**Complexity:** L
**Owner:** TBD

**Description:**
Create tools for data inspection and exploration.

**File:** `helpers/hagentic_eda/tools.py`

**Tasks:**
- [ ] `get_dataframe_info(df: pd.DataFrame) -> Dict`
  - Schema, shape, samples
  - Return: {"shape": (n, m), "columns": [...], "dtypes": {...}, ...}
  - Use `@tool` decorator
- [ ] `get_column_statistics(df: pd.DataFrame, column: str) -> Dict`
  - Distribution, outliers, null count
  - Numeric: mean, std, min, max, quantiles
  - Categorical: value_counts, cardinality
- [ ] `detect_data_issues(df: pd.DataFrame) -> Dict`
  - Type mismatches, missing values
  - Return: {"issues": [...], "column_issues": {...}}
  - Use helpers.hpandas for analysis
- [ ] Add comprehensive docstrings for LLM
- [ ] Pydantic input validation

**Acceptance Criteria:**
- Tools callable by agent
- Output useful and actionable
- Docstrings clear for LLM understanding

**Tests:**
- `helpers/test/test_hagentic_eda_tools.py::Test_get_dataframe_info`
- `helpers/test/test_hagentic_eda_tools.py::Test_detect_data_issues`

---

### Issue #5.2: Implement suggestion tools
**Epic:** Tool Definitions and Integration
**Priority:** P1 (High)
**Complexity:** L
**Owner:** TBD

**Description:**
Create tools for generating analysis suggestions.

**File:** `helpers/hagentic_eda/tools.py`

**Tasks:**
- [ ] `suggest_cleaning_steps(detected_issues: Dict) -> List[str]`
  - Recommend data preparation steps
  - Handle missing values, outliers, type issues
- [ ] `suggest_visualizations(column_types: Dict) -> List[str]`
  - Recommend charts/plots based on column types
  - E.g., histogram for numeric, bar chart for categorical
- [ ] `suggest_features(dataset_info: Dict) -> List[str]`
  - Feature engineering ideas
  - Based on domain patterns in data
- [ ] Add use `@tool` decorator
- [ ] Add docstrings

**Acceptance Criteria:**
- Suggestions are specific and actionable
- Agent can act on recommendations
- Tools are useful in practice

**Tests:**
- `helpers/test/test_hagentic_eda_tools.py::Test_suggest_cleaning_steps`
- `helpers/test/test_hagentic_eda_tools.py::Test_suggest_visualizations`

---

### Issue #5.3: Implement analysis tools
**Epic:** Tool Definitions and Integration
**Priority:** P1 (High)
**Complexity:** L
**Owner:** TBD

**Description:**
Create tools for statistical analysis.

**File:** `helpers/hagentic_eda/tools.py`

**Tasks:**
- [ ] `run_statistical_test(df: pd.DataFrame, test_type: str, columns: List[str]) -> Dict`
  - Supported tests: t-test, chi-square, correlation, normality
  - Return: test statistic, p-value, interpretation
- [ ] `check_correlations(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame`
  - Pearson/Spearman correlation matrix
  - Handle missing values
- [ ] `summarize_distribution(df: pd.DataFrame, column: str) -> Dict`
  - Summary stats, skewness, kurtosis
- [ ] Pydantic input validation for all tools
- [ ] Use `@tool` decorator

**Acceptance Criteria:**
- Tools validate inputs
- Results formatted clearly
- Statistical calculations accurate

**Tests:**
- `helpers/test/test_hagentic_eda_tools.py::Test_run_statistical_test`
- `helpers/test/test_hagentic_eda_tools.py::Test_check_correlations`

---

### Issue #5.4: Integrate with helpers modules
**Epic:** Tool Definitions and Integration
**Priority:** P1 (High)
**Complexity:** M
**Owner:** TBD

**Description:**
Leverage existing helpers utilities in tools.

**File:** `helpers/hagentic_eda/tools.py`

**Tasks:**
- [ ] Use `hdataframe.py` utilities for:
  - DataFrame validation
  - Schema inference
- [ ] Use `hpandas.py` utilities for:
  - Pandas operations
  - Data quality checks
- [ ] Use `hplot.py` (if exists) or helpers utilities for:
  - Plotting recommendations
- [ ] Document all integration points
- [ ] Create tests ensuring helpers are called

**Acceptance Criteria:**
- Tools use helpers functions
- No code duplication
- Integration tested

---

### Issue #5.5: Create tool registry and documentation
**Epic:** Tool Definitions and Integration
**Priority:** P2 (Medium)
**Complexity:** M
**Owner:** TBD

**Description:**
Create registry of all tools for agent discovery.

**File:** `helpers/hagentic_eda/tools.py`

**Tasks:**
- [ ] Create `TOOL_REGISTRY: Dict[str, Callable]`
  - Maps tool names to functions
  - All inspection, suggestion, and analysis tools
- [ ] Generate tool documentation for LLM
  - Tool descriptions
  - Parameters and types
  - Example usage
- [ ] Create `get_tools() -> List[LangChain.Tool]`
  - Returns all tools for agent binding
- [ ] Create `TOOLS_DOCUMENTATION.md`
  - Human-readable tool reference
- [ ] Add examples for each tool

**Acceptance Criteria:**
- Registry complete and importable
- Agent can discover all tools
- Documentation is clear

---

## EPIC 6: Data Type Analysis Modules

### Issue #6.1: Time Series Analysis Module
**Epic:** Data Type Analysis Modules
**Priority:** P1 (High)
**Complexity:** L
**Owner:** Pranav + Harshit

**Description:**
Implement analysis functions for time series data.

**File:** `helpers/hagentic_eda/analysis_timeseries.py`

**Tasks:**
- [ ] `analyze_time_series_autocorr(ts: pd.Series, lags: int = 40) -> Dict`
  - ACF/PACF analysis
  - Return plot data and interpretations
- [ ] `detect_seasonality(ts: pd.Series) -> Dict`
  - Seasonal decomposition
  - Return seasonal component and summary
- [ ] `detect_trend(ts: pd.Series) -> Dict`
  - Trend analysis (linear, polynomial)
  - Return trend direction and strength
- [ ] `rolling_statistics(ts: pd.Series, window: int = 12) -> Dict`
  - Rolling mean and std
  - Return time series and plots
- [ ] `detect_change_points(ts: pd.Series) -> List[int]` (optional)
  - Change point detection using statistical methods

**Example Dataset:** Yahoo stock prices time series

**Acceptance Criteria:**
- Functions handle missing data gracefully
- Visualizations are clear
- Interpretations are meaningful

**Tests:**
- `helpers/test/test_hagentic_eda_analysis_timeseries.py`

---

### Issue #6.2: Categorical Analysis Module
**Epic:** Data Type Analysis Modules
**Priority:** P1 (High)
**Complexity:** L
**Owner:** Sai

**Description:**
Implement analysis functions for categorical data.

**File:** `helpers/hagentic_eda/analysis_categorical.py`

**Tasks:**
- [ ] `analyze_categorical_distribution(df: pd.DataFrame, column: str) -> Dict`
  - Frequency counts, cardinality
  - Top categories, long-tail analysis
- [ ] `categorical_time_series(df: pd.DataFrame, time_col: str, cat_col: str) -> Dict`
  - Category distribution over time
  - Return trends by category
- [ ] `crosstab_analysis(df: pd.DataFrame, col1: str, col2: str) -> Dict`
  - Association between categorical variables
  - Return crosstab and chi-square test
- [ ] `create_categorical_plots(df: pd.DataFrame, column: str) -> Dict`
  - Bar charts, pie charts
  - Return plot data

**Example Dataset:** Netflix shows (genre, country, etc.)

**Acceptance Criteria:**
- Handles high-cardinality variables gracefully
- Output is interpretable
- Performance acceptable for large datasets

**Tests:**
- `helpers/test/test_hagentic_eda_analysis_categorical.py`

---

### Issue #6.3: Scalar (Numeric) Analysis Module
**Epic:** Data Type Analysis Modules
**Priority:** P1 (High)
**Complexity:** L
**Owner:** Madhur

**Description:**
Implement analysis functions for numeric data.

**File:** `helpers/hagentic_eda/analysis_scalar.py`

**Tasks:**
- [ ] `analyze_distribution(df: pd.DataFrame, column: str) -> Dict`
  - Histogram, KDE, normality tests
  - Return distribution summary and plots
- [ ] `detect_outliers(df: pd.DataFrame, column: str, method: str = "iqr") -> Dict`
  - IQR, z-score, isolation forest methods
  - Return outlier indices and analysis
- [ ] `generate_summary_stats(df: pd.DataFrame) -> pd.DataFrame`
  - Mean, median, std, quantiles
  - For all numeric columns
- [ ] `correlation_matrix(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame`
  - Pearson and Spearman correlation
  - Return heatmap and significant pairs
- [ ] `pairwise_scatter_plots(df: pd.DataFrame, columns: List[str]) -> Dict`
  - Scatter plot data for column pairs
  - Return plot coordinates and metadata

**Example Dataset:** World population data

**Acceptance Criteria:**
- Outlier detection works with different methods
- Statistics are accurate
- Performance acceptable for large datasets

**Tests:**
- `helpers/test/test_hagentic_eda_analysis_scalar.py`

---

### Issue #6.4: Cross-Variable Analysis Module
**Epic:** Data Type Analysis Modules
**Priority:** P1 (High)
**Complexity:** L
**Owner:** Sahil + Sai

**Description:**
Implement analysis functions for relationships between variables.

**File:** `helpers/hagentic_eda/analysis_cross_variable.py`

**Tasks:**
- [ ] `correlate_time_series(df: pd.DataFrame, ts_columns: List[str]) -> Dict`
  - Correlation between multiple time series
  - Return correlation matrix
- [ ] `categorical_numeric_interaction(df: pd.DataFrame, cat_col: str, num_col: str) -> Dict`
  - Groups and aggregations
  - Return summary stats by category
- [ ] `conditional_distributions(df: pd.DataFrame, target_col: str, feature_col: str) -> Dict`
  - Distribution of target conditioned on feature
  - Return conditional distributions
- [ ] `feature_interaction_analysis(df: pd.DataFrame, col1: str, col2: str) -> Dict`
  - Interaction detection
  - Return interaction summary

**Example Dataset:** Boston house prices

**Acceptance Criteria:**
- Handles mixed data types
- Insights are actionable
- Performance acceptable

**Tests:**
- `helpers/test/test_hagentic_eda_analysis_cross_variable.py`

---

### Issue #6.5: Unified Analysis Orchestrator
**Epic:** Data Type Analysis Modules
**Priority:** P2 (Medium)
**Complexity:** L
**Owner:** TBD

**Description:**
Create orchestrator that routes to appropriate analysis module.

**File:** `helpers/hagentic_eda/analysis.py`

**Tasks:**
- [ ] Create `AnalysisOrchestrator` class
- [ ] `route_analysis(state: AgentState) -> List[Dict]`
  - Detect column types
  - Route to appropriate analysis modules
  - Aggregate results
- [ ] `generate_analysis_plan(state: AgentState) -> List[str]`
  - Plan analyses based on detected types
- [ ] `execute_analysis_plan(state: AgentState, plan: List[str]) -> Dict`
  - Run planned analyses
  - Aggregate results

**Acceptance Criteria:**
- All data types analyzed
- Results combined logically
- Plan is reasonable

**Tests:**
- `helpers/test/test_hagentic_eda_analysis.py`

---

## EPIC 7: Code Generation and Execution

### Issue #7.1: Code generation from agent responses
**Epic:** Code Generation and Execution
**Priority:** P1 (High)
**Complexity:** M
**Owner:** TBD

**Description:**
Extract and validate code from agent responses.

**File:** `helpers/hagentic_eda/code_generation.py`

**Tasks:**
- [ ] `extract_code_blocks(text: str) -> List[str]`
  - Parse agent response for code blocks
  - Support multiple code blocks
- [ ] `validate_code(code: str) -> Tuple[bool, Optional[str]]`
  - Syntax check
  - Security checks (blacklist dangerous commands)
  - Return validity and any errors
- [ ] `format_code(code: str) -> str`
  - Apply style conventions (black, isort)
  - Add helpful comments
- [ ] Create blacklist of dangerous functions
  - `os.system`, `shutil.rmtree`, `exec`, `eval`, etc.

**Acceptance Criteria:**
- Handles multiple code blocks
- Security checks effective
- Formatted code follows conventions

**Tests:**
- `helpers/test/test_hagentic_eda_code_generation.py::Test_extract_code_blocks`
- `helpers/test/test_hagentic_eda_code_generation.py::Test_validate_code`

---

### Issue #7.2: Notebook cell management
**Epic:** Code Generation and Execution
**Priority:** P1 (High)
**Complexity:** L
**Owner:** TBD

**Description:**
Create and manage notebook cells programmatically.

**File:** `helpers/hagentic_eda/notebook_management.py`

**Tasks:**
- [ ] `create_notebook_cell(content: str, cell_type: str = "code") -> NotebookCell`
  - Generate cell object with ID and timestamp
- [ ] `insert_cell(notebook: NotebookNode, cell: NotebookCell, position: int = -1)`
  - Add cell to notebook
- [ ] `execute_cell(cell: NotebookCell, kernel_client) -> Dict`
  - Run code in Jupyter kernel
  - Handle async execution
- [ ] `capture_output(execution_result) -> Dict`
  - Get stdout, stderr, return value
  - Parse display data

**Acceptance Criteria:**
- Cells execute correctly
- Output captured accurately
- Handles kernel errors

**Tests:**
- `helpers/test/test_hagentic_eda_notebook_management.py`

---

### Issue #7.3: Error handling and recovery
**Epic:** Code Generation and Execution
**Priority:** P1 (High)
**Complexity:** M
**Owner:** TBD

**Description:**
Parse errors and generate fixes.

**File:** `helpers/hagentic_eda/code_generation.py`

**Tasks:**
- [ ] `parse_error(traceback: str) -> Dict`
  - Extract error type, message, line number
  - Categorize error (syntax, runtime, import, etc.)
- [ ] `generate_fix(error_info: Dict, code: str) -> str`
  - Create corrective code
  - Add debugging statements
- [ ] `retry_with_fix(original_code: str, error: str) -> str`
  - Generate and return fix code
- [ ] Handle common errors:
  - Import errors (missing packages)
  - Name errors (undefined variables)
  - Type errors (wrong types)
  - Attribute errors (missing attributes)

**Acceptance Criteria:**
- Errors detected accurately
- Fixes are reasonable
- Agent can recover

**Tests:**
- `helpers/test/test_hagentic_eda_code_generation.py::Test_parse_error`
- `helpers/test/test_hagentic_eda_code_generation.py::Test_generate_fix`

---

### Issue #7.4: Cell execution tracking
**Epic:** Code Generation and Execution
**Priority:** P2 (Medium)
**Complexity:** M
**Owner:** TBD

**Description:**
Track execution history and generate reports.

**File:** `helpers/hagentic_eda/execution_tracking.py`

**Tasks:**
- [ ] `ExecutionLog` class with:
  - Cell ID, timestamp, duration
  - Status (success, error, timeout)
  - Input and output
- [ ] `track_execution(cell_id: str, result: Dict)`
  - Record execution details
- [ ] `get_execution_history() -> List[ExecutionLog]`
  - Return all execution history
- [ ] `generate_execution_report() -> str`
  - Summary of execution progress

**Acceptance Criteria:**
- Tracking is complete and accurate
- Reports are informative

**Tests:**
- `helpers/test/test_hagentic_eda_execution_tracking.py`

---

## EPIC 8: Jupyter Integration & Frontend

**Note:** This is a Phase 2 epic (weeks 7-9). Requires significant TypeScript/frontend work.

### Issue #8.1: Server Extension (Python)
**Priority:** P2 (Medium)
**Complexity:** L
**Owner:** TBD

### Issue #8.2: Frontend Extension (TypeScript)
**Priority:** P2 (Medium)
**Complexity:** XL
**Owner:** TBD

### Issue #8.3: Communication Bridge
**Priority:** P2 (Medium)
**Complexity:** L
**Owner:** TBD

---

## EPIC 9: Testing & Quality Assurance

### Issue #9.1: Unit tests for core modules
**Epic:** Testing & Quality Assurance
**Priority:** P1 (High)
**Complexity:** L
**Owner:** TBD

**Description:**
Write comprehensive unit tests for all modules.

**Tasks:**
- [ ] Tests for EPIC 2 (state management): 95%+ coverage
- [ ] Tests for EPIC 3 (graph logic): 90%+ coverage
- [ ] Tests for EPIC 5 (tools): 90%+ coverage
- [ ] Tests for EPIC 6 (analysis): 85%+ coverage
- [ ] Tests for EPIC 7 (code generation): 90%+ coverage
- [ ] Run coverage report: `pytest --cov=helpers.hagentic_eda`

**Acceptance Criteria:**
- All unit tests pass
- Coverage threshold met (85%+)
- No flaky tests

---

### Issue #9.2: Integration tests for full workflows
**Epic:** Testing & Quality Assurance
**Priority:** P1 (High)
**Complexity:** L
**Owner:** TBD

**Description:**
Test end-to-end agent execution workflows.

**Tasks:**
- [ ] Test with time series dataset
  - Agent should recognize time series
  - Perform appropriate analyses
  - Generate notebook
- [ ] Test with categorical dataset
- [ ] Test with numeric dataset
- [ ] Test error recovery workflow
- [ ] Test state persistence workflow

**Files:**
- `helpers/test/test_hagentic_eda_integration.py`

**Acceptance Criteria:**
- Workflows complete successfully
- State persists correctly
- Outputs are reasonable

---

### Issue #9.3: Performance and stress testing
**Epic:** Testing & Quality Assurance
**Priority:** P2 (Medium)
**Complexity:** M
**Owner:** TBD

**Description:**
Ensure agent performance is acceptable.

**Tasks:**
- [ ] Test with large datasets (100k+ rows)
- [ ] Measure agent latency per decision
- [ ] Identify bottlenecks
- [ ] Profile memory usage
- [ ] Test timeout handling

**Acceptance Criteria:**
- Performance within acceptable bounds
- No memory leaks
- Timeouts handled gracefully

---

### Issue #9.4: Test dataset curation
**Epic:** Testing & Quality Assurance
**Priority:** P1 (High)
**Complexity:** M
**Owner:** TBD

**Description:**
Create datasets for comprehensive testing.

**Tasks:**
- [ ] Time series: Yahoo stock data (CSV)
- [ ] Categorical: Netflix shows (Parquet)
- [ ] Numeric: World population (Feather)
- [ ] Mixed: Boston house prices
- [ ] Create schema files (YAML/JSON) for each
- [ ] Document dataset characteristics
- [ ] Place in `helpers/test/input/hagentic_eda/`

**Acceptance Criteria:**
- Datasets cover all data types
- Easy to load and use in tests
- Documented for reproducibility

---

## EPIC 10: Documentation & Examples

### Issue #10.1: API documentation
**Epic:** Documentation & Examples
**Priority:** P2 (Medium)
**Complexity:** M
**Owner:** TBD

**Description:**
Generate API documentation for all modules.

**Tasks:**
- [ ] Ensure all public functions have docstrings
- [ ] Format docstrings with examples
- [ ] Generate Sphinx docs: `sphinx-build -b html docs docs/_build`
- [ ] Publish to GitHub Pages
- [ ] Create docstring examples for:
  - State management
  - Graph execution
  - Tool usage
  - Analysis modules

**Acceptance Criteria:**
- All public APIs documented
- Examples in docstrings work
- Docs build without errors

---

### Issue #10.2: Tutorials and guides
**Epic:** Documentation & Examples
**Priority:** P2 (Medium)
**Complexity:** L
**Owner:** TBD

**Description:**
Create comprehensive tutorials and guides.

**Tasks:**
- [ ] **Getting Started Guide**
  - Installation
  - First AutoEDA analysis
  - Understanding outputs
- [ ] **Architecture Overview**
  - System design
  - Component relationships
  - Execution flow
- [ ] **Tutorial Notebooks**
  - Time series analysis walkthrough
  - Categorical analysis walkthrough
  - Numeric analysis walkthrough
- [ ] **Advanced Usage Guide**
  - Custom analysis modules
  - Extending the agent
  - Performance tuning

**Acceptance Criteria:**
- Tutorials follow project conventions
- Examples run successfully
- Instructions are clear

---

### Issue #10.3: Example AutoEDA analysis
**Epic:** Documentation & Examples
**Priority:** P2 (Medium)
**Complexity:** L
**Owner:** TBD

**Description:**
Create comprehensive example notebook showing full workflow.

**Tasks:**
- [ ] Select Kaggle dataset (e.g., stock prices)
- [ ] Create example notebook: `examples/autoeda_stock_analysis.ipynb`
- [ ] Show full workflow:
  - Data loading
  - Schema definition
  - Agent initialization
  - Interaction loop
  - Report generation
- [ ] Annotate with explanations
- [ ] Highlight key insights

**Acceptance Criteria:**
- Notebook is clear and runnable
- Insights are meaningful
- Demonstrates agent capabilities

---

## Summary of Dependencies

```
EPIC 1 (Foundation)
  └─> EPIC 2 (State Management)
      └─> EPIC 3 (Graph Orchestration)
          ├─> EPIC 4 (System Prompts)
          ├─> EPIC 5 (Tools)
          └─> EPIC 6 (Analysis)
              └─> EPIC 7 (Code Generation & Execution)
                  └─> EPIC 9 (Testing)
                      └─> EPIC 10 (Documentation)

EPIC 8 (Jupyter Integration) [Phase 2]
  └─> (Can run in parallel, but depends on all prior EPICs)
```

---

## Success Metrics

- All issues completed
- Code coverage 85%+
- All integration tests pass
- Documentation complete and clear
- Agent successfully analyzes provided datasets
- Performance acceptable (< 5s per decision)
