book.Decentralized_AI/decentralization_ai_summit_2023.md
book.Decentralized_AI/responsible_genai_f23.md

From /Users/saggese/src/notes1/notes
- crypto.How_to_Defi_Beginner.Coingecko.2021.txt
- crypto.Mastering_Bitcoin.Antonopoulos.2017.txt
- crypto.Mastering_Ethereum.Antonopoulos.2018.txt
- IN_PROGRESS.book.crypto.Hands_on_smart_contract_development_with_Solidity_and_Ethereum.2019.Solorio.txt
- IN_PROGRESS.course.cs.Decentralized_finance.Harvey.Coursera.txt
- IN_PROGRESS.course.cs.entrepreneurship_in_web3.Berkeley.txt
- IN_PROGRESS.crypto.DeFi_and_the_future_of_finance.Harvey.2021.txt
- IN_PROGRESS.crypto.How_to_Defi_Advanced.Coingecko.2021.txt
- IN_PROGRESS.finance.Token_economy_and_Web3.Voshmgir.2020.txt
- IN_PROGRESS.book.crypto.Solidity_programming_essentials.Modi.2022.txt

## Overlap between deai.map.md, defi.map.md, web3.map.md

Compared headers and subpoints across all 3 files (deai=15 sections,
defi=14, web3=14).

**Shared across all 3** (theme same, details vary by domain):
- Governance/DAOs — deai "AI governance via DAOs", defi/web3 "…DAOs".
  Common: treasury mgmt, delegation, attack vectors, voting.
- Tokenomics/incentives — ve-token models named explicit in deai + defi.
- Regulation — MiCA named in deai + defi. Securities law shared defi +
  web3.
- Security — different angle each (deai: poisoning/Sybil; defi:
  reentrancy/oracle manip; web3: audits/formal verification). Formal
  verification shared defi + web3.

**Strong pairwise overlap: defi ↔ web3** (~7 of 14 defi sections match a
web3 section):
- Blockchain/consensus fundamentals (PoW/PoS, EVM)
- Smart contract platforms
- Cross-chain bridges / interoperability
- Layer 2 scaling (rollups, state channels)
- Governance/DAOs, tokenomics, regulation (listed above)

These two clearly share a base "blockchain infra" layer. defi adds
finance-specific pieces web3 lacks (AMMs, DEXs, lending, stablecoins,
derivatives, MEV, risk/systemic risk). web3 adds infra pieces defi lacks
(NFTs, decentralized identity, decentralized storage/DA, node
economics/RPC/indexers, crypto primitives, privacy tooling).

**Moderate overlap: deai ↔ (defi + web3)** (~6 of 15 deai sections touch
the other two):
- Zero-knowledge — deai's ZKML echoes web3's ZK proofs / zk-rollup
  privacy section.
- Oracles — deai's "oracles feeding ML outputs on-chain" echoes defi's
  dedicated oracle section.
- Governance, tokenomics, regulation, security (as above).

deai's other 9 sections (federated learning, decentralized training,
compute/inference markets, differential privacy, SMC/HE,
provenance/watermarking, data marketplaces, multi-agent mechanism
design, open vs closed ecosystems) are AI-specific — no counterpart in
defi or web3.
