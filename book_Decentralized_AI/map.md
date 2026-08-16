# Decentralized AI, DeFi, and Web3: Unified Course Topics

- Union of `deai.map.md`, `defi.map.md`, `web3.map.md` (35 unique chapters from
  45 total entries, per the overlap analysis in `README.md`)
- Each chapter lists its source file(s) in parentheses
- Chapters found in more than one source file merge their subtopics

## Foundations and Infrastructure

- **Blockchain consensus foundations** (defi + web3)
  - UTXO vs account models
  - Proof-of-work vs proof-of-stake
  - Finality, chain reorganizations
  - BFT-style consensus (Tendermint/HotStuff)
  - Liveness vs safety tradeoffs

- **Distributed ledger fundamentals** (web3)
  - Merkle trees
  - Hash chains
  - State machines
  - Byzantine fault tolerance

- **Smart contract platforms and security** (defi + web3)
  - EVM execution model, WASM-based chains
  - Gas models, account abstraction
  - Reentrancy
  - Oracle manipulation
  - Formal verification

- **Layer 2 and scaling architectures** (defi + web3)
  - Optimistic/zk-rollups
  - Sidechains, state channels
  - Sharding
  - Fee markets, composability across layers

- **Cross-chain interoperability and bridges** (defi + web3)
  - Bridge trust models, wrapped assets, bridge exploits
  - Light clients, IBC-style protocols
  - Atomic swaps
  - Rollup-native messaging

- **Cryptographic primitives for Web3** (web3)
  - Digital signatures, hash functions
  - Zero-knowledge proofs
  - Threshold signatures

- **Web3 infrastructure and node economics** (web3)
  - RPC providers
  - Indexers (The Graph)
  - Validator/staking economics

## Decentralized AI

- **Federated learning** (deai)
  - FedAvg aggregation
  - Personalization, non-IID data
  - Communication overhead

- **Decentralized training** (deai)
  - Data/model parallelism across untrusted nodes
  - Communication-efficient SGD
  - Bandwidth limits

- **Decentralized compute and inference markets** (deai)
  - Bittensor, Gensyn, Together
  - Incentive design for compute-sharing networks

- **Blockchain-AI integration** (deai)
  - On-chain agents
  - Smart-contract-triggered inference
  - Oracles feeding ML outputs on-chain

- **Zero-knowledge ML (ZKML)** (deai)
  - zk-SNARKs for verifiable inference
  - Proof-of-training
  - Trustless model correctness

- **Differential privacy** (deai)
  - DP-SGD
  - Privacy budgets
  - Accuracy tradeoffs in decentralized settings

- **Secure multiparty computation and homomorphic encryption** (deai)
  - Privacy-preserving collaborative training and inference

- **Model and data provenance** (deai)
  - Watermarking
  - Dataset lineage
  - Tamper-evident training records

- **Decentralized data marketplaces** (deai)
  - Data DAOs
  - Tokenized datasets
  - Incentive-compatible data sharing

- **Multi-agent systems and mechanism design** (deai)
  - Cooperative and competitive learning
  - Incentive alignment
  - Self-play economics

- **Open-source vs closed-source ecosystems** (deai)
  - Licensing, trust
  - Evaluation, e.g. DecodingTrust
  - Reproducibility

## Decentralized Finance

- **Automated market makers (AMMs)** (defi)
  - Constant-product/constant-sum curves
  - Concentrated liquidity
  - Impermanent loss

- **Decentralized exchanges and order flow** (defi)
  - Order-book DEXs, aggregators
  - MEV-aware routing
  - Slippage

- **Lending and borrowing protocols** (defi)
  - Overcollateralization
  - Interest-rate models
  - Liquidation mechanics
  - Flash loans

- **Stablecoins and monetary design** (defi)
  - Fiat-collateralized, crypto-backed, algorithmic pegs
  - Depeg risk (Terra/UST case study)

- **Derivatives and synthetic assets** (defi)
  - Perpetual futures
  - Options protocols
  - Synthetic exposure
  - Funding rates

- **MEV and transaction ordering** (defi)
  - Sandwich attacks
  - Front-running
  - PBS, proposer-builder separation
  - MEV redistribution

- **Oracle design and data integrity** (defi)
  - Chainlink-style feeds
  - TWAPs
  - Oracle manipulation attacks
  - Latency/trust tradeoffs

## Web3 and Digital Ownership

- **Decentralized identity and credentials** (web3)
  - DIDs, verifiable credentials
  - Soulbound tokens
  - Self-sovereign identity

- **NFTs and digital ownership** (web3)
  - Token standards (ERC-721/1155)
  - Provenance, royalties
  - On-chain vs off-chain metadata

- **Decentralized storage and data availability** (web3)
  - IPFS, Arweave, Filecoin
  - Data availability sampling

- **Privacy-preserving Web3** (web3)
  - zk-rollups for privacy
  - Mixers
  - Confidential transactions
  - Regulatory tension

## Cross-Cutting: Governance, Incentives, Security, Regulation

- **Governance and DAOs** (deai + defi + web3)
  - Voting mechanisms, token-weighted voting
  - Delegation
  - Treasury management, compute treasury management
  - Governance attack vectors
  - Legal wrapper models

- **Tokenomics and incentive design** (deai + defi + web3)
  - Token issuance, emission schedules
  - Reward mechanisms for compute/data contributors
  - ve-token-style models
  - Liquidity mining, protocol-owned liquidity
  - Incentive alignment, game-theoretic attack analysis

- **Robustness and security in AI networks** (deai)
  - Poisoning attacks
  - Sybil resistance
  - Adversarial nodes in federated/decentralized systems

- **Security and auditing** (web3)
  - Vulnerability classes
  - Formal verification
  - Bug bounties
  - Post-mortem case studies

- **Risk management and systemic risk** (defi)
  - Protocol composability ("money legos")
  - Contagion
  - Collateral cascades
  - Stress testing

- **Regulation** (deai + defi + web3)
  - Accountability vs decentralization tension
  - AI Act/MiCA-adjacent frameworks
  - Securities classification/law
  - AML/KYC in permissionless systems
  - Custody, CBDCs vs permissionless chains
  - Enterprise blockchain use cases
  - Alignment with `responsible_genai_f23.md`
