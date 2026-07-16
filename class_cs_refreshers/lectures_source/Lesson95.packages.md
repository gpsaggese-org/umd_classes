# Functionality Clusters

| Cluster | Function | Packages Ordered by Stars |
|---|---|---|
| **1. Game Theory / Nash Equilibrium Computation** | Compute Nash equilibria, solve normal and extensive form games | Gambit (559), Nashpy (370), Nash (370) |
| **2. Game Theory Applications / Strategy Simulation** | Iterated games, agent-based modeling, tournament simulations | Mesa (3,727), Axelrod (835) |
| **3. Game Theory & Economics Tools** | Game theory integrated with broader economic analysis | QuantEcon (2,368) |

# Cluster 1. Game Theory / Nash Equilibrium Computation

## Nashpy

- **Description**: Most popular dedicated game theory library for computing Nash equilibria in 2-player games
- **GitHub URL**: https://github.com/nashpy/nashpy
- **Documentation URL**: https://nashpy.readthedocs.io
- **GitHub stars**: 370

### Features

- Computes Nash equilibria for 2-player games
- Supports both normal form and extensive form games
- Simple API for defining games and finding equilibria

### Alternatives

- Gambit
- Nash

## Gambit

- **Description**: Comprehensive game theory library for n-player games and complex game structures
- **GitHub URL**: https://github.com/gambitproject/gambit
- **Documentation URL**: https://gambit.readthedocs.io
- **GitHub stars**: 559

### Features

- Handles n-player games and complex game structures
- Solves for various equilibrium types
- More heavyweight and feature-rich than Nashpy

### Alternatives

- Nashpy
- Nash

## Nash

- **Description**: Older package for finding Nash equilibria with support for multiple algorithms
- **GitHub URL**: https://github.com/drvinceknight/nashpy
- **GitHub stars**: 370

### Features

- Support for multiple algorithms
- Less actively maintained than Nashpy

### Alternatives

- Nashpy
- Gambit

# Cluster 2. Game Theory Applications / Strategy Simulation

## Axelrod

- **Description**: For iterated prisoner's dilemma and strategy simulations with large library of built-in strategies
- **GitHub URL**: https://github.com/Axelrod-Python/Axelrod
- **Documentation URL**: https://axelrod.readthedocs.io
- **GitHub stars**: 835

### Features

- Large library of built-in strategies
- Tournament simulations
- Focus on iterated games and evolutionary dynamics

### Alternatives

- Mesa
- QuantEcon

## Mesa

- **Description**: Agent-based modeling framework for simulating game theory scenarios and multi-agent systems
- **GitHub URL**: https://github.com/projectmesa/mesa
- **Documentation URL**: https://mesa.readthedocs.io
- **GitHub stars**: 3,727

### Features

- Can be used to simulate game theory scenarios
- More general-purpose than dedicated game theory libraries
- Full agent-based modeling capabilities

### Alternatives

- Axelrod
- QuantEcon

# Cluster 3. Game Theory & Economics Tools

## QuantEcon

- **Description**: Economics library with integrated game theory tools and broader economic analysis capabilities
- **GitHub URL**: https://github.com/QuantEcon/QuantEcon.py
- **Documentation URL**: https://quantecon.org
- **GitHub stars**: 2,368

### Features

- Includes game theory utilities alongside other economic tools
- Broader scope than pure game theory
- Integration with numerical economics and optimization

### Alternatives

- Nashpy
- Mesa
