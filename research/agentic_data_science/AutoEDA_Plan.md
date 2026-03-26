# AutoEDA Agent - Implementation Plan

## Overview

This plan breaks down the AutoEDA agent specification into EPICs and Issues for
team implementation. The agent is a Jupyter-native, agentic framework for
autonomous data analysis using LangGraph for orchestration.

---

## EPIC 1: Foundation & Infrastructure Setup

**Goal:** Establish the core infrastructure and dependencies needed for the AutoEDA agent.

**Owner:** DevOps/Infrastructure Team

### Issue 1.1: Set up LangGraph and LangChain integration
- Add LangGraph and LangChain to project dependencies
- Create base module: `helpers/lang_graph_setup.py`
- Document version compatibility and requirements
- **Acceptance Criteria:**
  - Dependencies installed and tested
  - Example LangGraph state and graph work correctly

### Issue 1.2: Define core module structure for AutoEDA
- Create `helpers/hagentic_eda/` package with submodules
- Submodules: `state.py`, `graph.py`, `tools.py`, `prompts.py`, `utils.py`
- Create `__init__.py` with public exports
- **Acceptance Criteria:**
  - Module imports correctly
  - All submodules are discoverable

### Issue 1.3: Create integration tests setup
- Add pytest fixtures for AutoEDA agent testing
- Set up test data directory with sample datasets
- Create utility functions for test assertions
- **Acceptance Criteria:**
  - Fixtures work with pytest
  - Sample datasets load correctly

---

## EPIC 2: Agent State Management

**Goal:** Design and implement the agent state schema for tracking analysis progress, dataset context, and execution history.

**Owner:** Data Engineering Team

### Issue 2.1: Define AgentState schema with Pydantic
**File:** `helpers/hagentic_eda/state.py`
- Create `AgentState` class with fields:
  - `conversation_history`: List of messages
  - `dataset_context`: DataFrame metadata
  - `analysis_phase`: Current phase (setup, cleaning, analysis, reporting)
  - `generated_cells`: List of executed notebook cells
  - `error_log`: Error tracking for self-correction
- Use Pydantic for validation
- **Acceptance Criteria:**
  - State instantiates correctly
  - All fields have proper type hints
  - Validation catches invalid inputs

### Issue 2.2: Define supporting schema classes
**File:** `helpers/hagentic_eda/state.py`
- Create `DataFrameInfo`: shape, columns, dtypes, null_counts, sample_values
- Create `ColumnInfo`: name, dtype, detected_type, statistics, issues
- Create `NotebookCell`: id, type (code/markdown), content, result, error
- **Acceptance Criteria:**
  - Classes serialize/deserialize correctly
  - Example instances created successfully

### Issue 2.3: Implement state serialization utilities
**File:** `helpers/hagentic_eda/state.py`
- Create `serialize_state()` function for persistence
- Create `deserialize_state()` function for recovery
- Test with sample state objects
- **Acceptance Criteria:**
  - State round-trips correctly (serialize -> deserialize)
  - JSON output is readable

### Issue 2.4: Add state management utilities
**File:** `helpers/hagentic_eda/state.py`
- Implement `update_dataset_context()` to infer schema
- Implement `log_error()` for error tracking
- Implement `add_cell_result()` for cell execution tracking
- Write unit tests
- **Acceptance Criteria:**
  - Unit tests pass
  - Methods update state correctly

---

## EPIC 3: LangGraph Agent Orchestration

**Goal:** Define and implement the LangGraph state machine that orchestrates agent reasoning, tool use, and code generation.

**Owner:** Agent Core Team

### Issue 3.1: Define graph nodes
**File:** `helpers/hagentic_eda/graph.py`
- Implement `agent_node`: Main reasoning with LLM
- Implement `tools_node`: Execute LangChain tools
- Implement `generate_code_node`: Extract code from agent response
- Implement `update_context_node`: Update dataset understanding from results
- Implement `handle_error_node`: Process and fix execution errors
- **Acceptance Criteria:**
  - All nodes implement proper signatures
  - State transitions work correctly

### Issue 3.2: Define graph edges and routing logic
**File:** `helpers/hagentic_eda/graph.py`
- Create `should_use_tools()` conditional function
- Create `should_generate_code()` conditional function
- Create `should_handle_error()` conditional function
- Connect: START -> agent -> tools/generate_code/END
- Connect: tools -> agent, generate_code -> INTERRUPT, RESUME -> update_context
- **Acceptance Criteria:**
  - All edges connect correctly
  - Conditional routing works with test inputs

### Issue 3.3: Implement interrupt/resume for execution feedback
**File:** `helpers/hagentic_eda/graph.py`
- Implement `interrupt_after` configuration for generate_code node
- Add resume logic to handle execution results
- Test interrupt/resume cycle
- **Acceptance Criteria:**
  - Graph interrupts after code generation
  - Resume with execution results updates state

### Issue 3.4: Set up state persistence with checkpointing
**File:** `helpers/hagentic_eda/graph.py`
- Configure memory-based checkpointing
- Create `save_checkpoint()` and `load_checkpoint()` utilities
- Test state recovery from checkpoints
- **Acceptance Criteria:**
  - Checkpoints save/load correctly
  - State persists across sessions

### Issue 3.5: Create graph visualization and documentation
**File:** `helpers/hagentic_eda/graph.py`
- Add method to export graph structure (Mermaid diagram)
- Generate ASCII diagram of state machine
- Document node responsibilities and transitions
- **Acceptance Criteria:**
  - Diagram renders correctly
  - Documentation is clear

---

## EPIC 4: System Prompt Engineering

**Goal:** Design comprehensive system prompts that guide agent behavior across analysis phases.

**Owner:** AI Research Team

### Issue 4.1: Design system prompt template structure
**File:** `helpers/hagentic_eda/prompts.py`
- Create base prompt with sections:
  - Role and capabilities
  - Workflow phases (setup, cleaning, analysis, reporting)
  - Code generation guidelines (style, imports, comments)
  - Context injection points
  - Output format requirements
- **Acceptance Criteria:**
  - Template renders without errors
  - All sections present and meaningful

### Issue 4.2: Implement context formatting functions
**File:** `helpers/hagentic_eda/prompts.py`
- Create `format_dataframe_context()` for current data state
- Create `format_error_context()` for error recovery
- Create `format_analysis_history()` for conversation tracking
- Test with sample data and errors
- **Acceptance Criteria:**
  - Formatted context is concise and complete
  - Functions handle edge cases (empty data, no errors, etc.)

### Issue 4.3: Design phase-specific prompt variations
**File:** `helpers/hagentic_eda/prompts.py`
- Phase 1: "Read Schema and Infer Types" prompt
- Phase 2: "Propose EDA Plan" prompt
- Phase 3: "Run Full Analysis" prompt
- Phase 4: "Generate Report" prompt
- **Acceptance Criteria:**
  - Each phase has distinct guidance
  - Phase transitions are clear

### Issue 4.4: Create prompt testing framework
**File:** `helpers/hagentic_eda/prompts.py`
- Write unit tests for prompt formatting
- Add smoke tests with LLM (token counting, context length)
- Create example prompts with annotations
- **Acceptance Criteria:**
  - Tests pass
  - Prompts under context limits

---

## EPIC 5: Tool Definitions and Integration

**Goal:** Define tools the agent can invoke for data inspection, suggestions, and analysis.

**Owner:** Data Science & Helpers Integration Team

### Issue 5.1: Implement inspection tools
**File:** `helpers/hagentic_eda/tools.py`
- `get_dataframe_info(df)`: Returns schema, shape, samples
- `get_column_statistics(df, column)`: Distribution, outliers, null count
- `detect_data_issues(df)`: Identify type mismatches, missing values
- Use `@tool` decorator from LangChain
- Write docstrings for LLM understanding
- **Acceptance Criteria:**
  - Tools callable by agent
  - Output useful and actionable

### Issue 5.2: Implement suggestion tools
**File:** `helpers/hagentic_eda/tools.py`
- `suggest_cleaning_steps(detected_issues)`: Recommend data prep
- `suggest_visualizations(column_types)`: Recommend charts/plots
- `suggest_features(dataset_info)`: Feature engineering ideas
- **Acceptance Criteria:**
  - Suggestions are specific and data-driven
  - Agent can act on recommendations

### Issue 5.3: Implement analysis tools
**File:** `helpers/hagentic_eda/tools.py`
- `run_statistical_test(df, test_type, columns)`: Hypothesis testing
- `check_correlations(df, method)`: Pearson/Spearman correlation
- Pydantic input validation for all tools
- **Acceptance Criteria:**
  - Tools validate inputs
  - Results formatted clearly

### Issue 5.4: Integrate with helpers modules
**File:** `helpers/hagentic_eda/tools.py`
- Leverage `hdataframe.py` for DataFrame operations
- Leverage `hpandas.py` for pandas utilities
- Leverage `hplot.py` (if exists) for visualization suggestions
- Document integration points
- **Acceptance Criteria:**
  - Tools use helpers functions
  - No code duplication

### Issue 5.5: Create tool registry and documentation
**File:** `helpers/hagentic_eda/tools.py`
- Create `TOOL_REGISTRY` dict mapping tool names to functions
- Generate tool documentation for LLM
- Create examples for each tool
- **Acceptance Criteria:**
  - Registry complete
  - Agent can discover all tools

---

## EPIC 6: Data Type Analysis Modules

**Goal:** Implement specialized analysis for different data types (time series, categorical, scalar, cross-variable).

**Owner:** Analytics Team (split by data type)

### Issue 6.1: Time Series Analysis Module (Owner: Pranav + Harshit)
**File:** `helpers/hagentic_eda/analysis_timeseries.py`
- `analyze_time_series_autocorr()`: ACF/PACF plots
- `detect_seasonality()`: Decomposition and seasonal detection
- `detect_trend()`: Trend analysis
- `rolling_statistics()`: Moving mean/std
- `detect_change_points()`: Change point detection (optional)
- **Acceptance Criteria:**
  - Functions handle missing data gracefully
  - Visualizations are clear

### Issue 6.2: Categorical Analysis Module (Owner: Sai)
**File:** `helpers/hagentic_eda/analysis_categorical.py`
- `analyze_categorical_distribution()`: Frequency counts, cardinality
- `time_series_categorical()`: Category distribution over time
- `crosstab_analysis()`: Association between variables
- `create_categorical_plots()`: Visualizations
- **Acceptance Criteria:**
  - Handles high-cardinality variables
  - Output is interpretable

### Issue 6.3: Scalar (Numeric) Analysis Module (Owner: Madhur)
**File:** `helpers/hagentic_eda/analysis_scalar.py`
- `analyze_distribution()`: Histogram, KDE, normality tests
- `detect_outliers()`: IQR, z-score, isolation forest methods
- `generate_summary_stats()`: Mean, median, std, quantiles
- `correlation_matrix()`: Pearson and Spearman
- `pairwise_scatter_plots()`: Visualization
- **Acceptance Criteria:**
  - Outlier detection works with different methods
  - Statistics are accurate

### Issue 6.4: Cross-Variable Analysis Module (Owner: Sahil + Sai)
**File:** `helpers/hagentic_eda/analysis_cross_variable.py`
- `correlate_time_series()`: Correlation between time series
- `categorical_numeric_interaction()`: Groups and aggregations
- `conditional_distributions()`: Conditional analysis
- `feature_interaction_analysis()`: Interaction detection
- **Acceptance Criteria:**
  - Handles mixed data types
  - Insights are actionable

### Issue 6.5: Unified Analysis Orchestrator
**File:** `helpers/hagentic_eda/analysis.py`
- Create `AnalysisOrchestrator` class
- Route to appropriate analysis module based on detected types
- Aggregate results into unified report
- **Acceptance Criteria:**
  - All data types analyzed
  - Results combined logically

---

## EPIC 7: Code Generation and Execution

**Goal:** Enable the agent to generate and execute Python code in notebook cells with error recovery.

**Owner:** Execution Engine Team

### Issue 7.1: Code generation from agent responses
**File:** `helpers/hagentic_eda/code_generation.py`
- `extract_code_blocks()`: Parse agent response for code
- `validate_code()`: Syntax check and security checks
- `format_code()`: Apply style conventions
- **Acceptance Criteria:**
  - Handles multiple code blocks
  - Blacklist checks for dangerous commands

### Issue 7.2: Notebook cell management
**File:** `helpers/hagentic_eda/notebook_management.py`
- `create_notebook_cell()`: Generate cell object
- `insert_cell()`: Add to notebook programmatically
- `execute_cell()`: Run code in kernel
- `capture_output()`: Get stdout, stderr, results
- **Acceptance Criteria:**
  - Cells execute correctly
  - Output captured accurately

### Issue 7.3: Error handling and recovery
**File:** `helpers/hagentic_eda/code_generation.py`
- `parse_error()`: Extract error type and message
- `generate_fix()`: Create corrective code
- `retry_with_fix()`: Run corrective code
- **Acceptance Criteria:**
  - Errors detected accurately
  - Agent can recover from common errors

### Issue 7.4: Cell execution tracking
**File:** `helpers/hagentic_eda/execution_tracking.py`
- Track execution history: timestamps, duration, status
- Store results and metadata
- Generate execution reports
- **Acceptance Criteria:**
  - Tracking is complete and accurate

---

## EPIC 8: Jupyter Integration & Frontend

**Goal:** Create the browser-to-kernel bridge and JupyterLab extension.

**Owner:** Frontend/Integration Team

**Note:** This requires JupyterLab extension development (TypeScript) which is a major undertaking. Consider this phase 2.

### Issue 8.1: Server Extension (Python)
- Backend service hosting LangGraph agent
- WebSocket server for communication
- Kernel interaction layer

### Issue 8.2: Frontend Extension (TypeScript)
- JupyterLab extension initialization
- UI for interacting with agent
- Notebook cell manipulation through `@jupyterlab/notebook`

### Issue 8.3: Communication Bridge
- JSON message format specification
- Bidirectional WebSocket handling
- Synchronization between UI and kernel state

---

## EPIC 9: Testing & Quality Assurance

**Goal:** Comprehensive testing framework for the AutoEDA agent.

**Owner:** QA Team

### Issue 9.1: Unit tests for core modules
- Test state management (EPIC 2)
- Test graph logic (EPIC 3)
- Test tools (EPIC 5)
- Test analysis modules (EPIC 6)
- Target: 85%+ code coverage
- **Acceptance Criteria:**
  - All unit tests pass
  - Coverage threshold met

### Issue 9.2: Integration tests for full workflows
- Test end-to-end agent execution
- Test with sample datasets (time series, categorical, scalar)
- Test error recovery and state persistence
- **Acceptance Criteria:**
  - Workflows complete successfully
  - State persists correctly

### Issue 9.3: Performance and stress testing
- Test with large datasets
- Measure agent latency
- Identify bottlenecks
- **Acceptance Criteria:**
  - Performance within acceptable bounds
  - No memory leaks

### Issue 9.4: Test dataset curation
- Create sample CSV, Parquet, Feather files
- Create schema files (JSON/YAML)
- Document dataset characteristics
- **Acceptance Criteria:**
  - Datasets cover all data types
  - Easy to use in tests

---

## EPIC 10: Documentation & Examples

**Goal:** Create comprehensive documentation and example notebooks.

**Owner:** Documentation Team

### Issue 10.1: API documentation
- Docstrings for all public functions
- Generate Sphinx/MkDocs docs
- Publish to GitHub Pages
- **Acceptance Criteria:**
  - All public APIs documented
  - Examples in docstrings

### Issue 10.2: Tutorials and guides
- Getting started guide
- Architecture overview document
- Step-by-step tutorial notebooks
- Advanced usage guide
- **Acceptance Criteria:**
  - Tutorials follow project conventions
  - Examples run successfully

### Issue 10.3: Example AutoEDA analysis
- Create example notebook showing full workflow
- Demonstrate on Kaggle datasets (stock prices, Netflix, etc.)
- Annotate key insights
- **Acceptance Criteria:**
  - Notebook is clear and runnable
  - Insights are meaningful

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-3)
- EPIC 1: Infrastructure setup
- EPIC 2: State management
- EPIC 3: LangGraph orchestration
- Deliverable: Basic graph structure compiling and running

### Phase 2: Intelligence (Weeks 4-6)
- EPIC 4: System prompts
- EPIC 5: Tools
- EPIC 6: Analysis modules
- Deliverable: Agent can perform basic analysis

### Phase 3: Execution & Integration (Weeks 7-9)
- EPIC 7: Code generation and execution
- EPIC 9: Testing (unit + integration)
- Deliverable: End-to-end agent workflow with sample datasets

### Phase 4: Polish & Documentation (Weeks 10-12)
- EPIC 8: Jupyter integration (if time permits)
- EPIC 9: Performance testing
- EPIC 10: Documentation and examples
- Deliverable: Production-ready agent with comprehensive docs

### Phase 5: Future Work
- Advanced features (text analysis, clustering, etc.)
- Full JupyterLab extension
- Cloud deployment options

---

## Success Criteria (End State)

1. **Functional Agent**: Autonomously analyzes datasets end-to-end
2. **State Management**: Persists progress and recovers from errors
3. **Extensible**: New analysis types can be added easily
4. **Well-Tested**: 85%+ code coverage, integration tests pass
5. **Well-Documented**: API docs, tutorials, and examples provided
6. **Production-Ready**: Error handling, logging, and monitoring in place

---

## Team Assignments Summary

| EPIC | Owner | Skills |
|------|-------|--------|
| 1 | DevOps | Infrastructure, CI/CD |
| 2 | Data Eng | Python, Pydantic, Data structures |
| 3 | Agent Core | LangGraph, Python, State machines |
| 4 | AI Research | Prompt engineering, LLM understanding |
| 5 | Data Science + Helpers | Statistics, Data analysis, Integration |
| 6 | Analytics (split) | Domain expertise per data type |
| 7 | Execution | Python, Jupyter, Error handling |
| 8 | Frontend | TypeScript, JupyterLab, WebSockets |
| 9 | QA | Testing, pytest, Performance |
| 10 | Docs | Technical writing, Examples |
