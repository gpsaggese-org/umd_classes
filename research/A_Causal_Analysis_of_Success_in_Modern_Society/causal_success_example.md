# Example Walkthrough

**See `causal_success_example.ipynb` for the interactive notebook** with all code, plots, and output.

The notebook walks through:
1. Setup and theory
2. Creating population
3. Running simulation
4. Statistical analysis
5. Visualization
6. Correlation analysis (talent vs luck)
7. Top performers analysis
8. Double Machine Learning (causal effect)
9. Causal Forests (heterogeneous effects)
10. Policy comparison
11. Summary and implications

## Extensions to Consider

You could make talents evolve over time (success breeds confidence, failure erodes it). You could add explicit network structures instead of just a networking score. You could calibrate to real wealth or citation distributions. You could introduce different types of events (rare huge opportunities vs frequent small ones).

The framework is flexible. This is a starting point, not the final word.

## Common Questions and Troubleshooting

**Q: The simulation is taking forever. What's wrong?**

A: Most likely issue is n_periods or n_agents set too high. 100 agents and 80 periods should run in under a minute. If you're doing 1000 agents and 500 periods, that could take a while. Reduce the numbers to test, then scale up.

**Q: My Gini coefficient is way different from what's described here.**

A: First check your random seed. If seed=42, you should get very consistent results. If you're using a different seed or no seed, results will vary. Second, check your parameter values. Very low lucky_mean or very few n_periods can produce low Gini. Very high unlucky_mean can produce extreme Gini.

**Q: Correlations are negative or don't make sense.**

A: Make sure you're using log(capital) not raw capital for correlation analysis. Raw capital correlations are unstable due to outliers. Also verify your agents actually ran through simulation (check that lucky_events and unlucky_events are non-zero).

**Q: Import errors when running the notebook.**

A: Most likely you're missing EconML. Run `pip install econml` in your environment. Or if you're in Docker, rebuild the container after adding econml to requirements.txt.

**Q: Visualizations aren't showing up.**

A: Add `%matplotlib inline` at the top of the notebook. This tells Jupyter to display plots in the notebook instead of in separate windows.

**Q: Can I run this with 1000 agents?**

A: Yes, but it'll be slower. The computational complexity scales roughly linearly with n_agents, so 1000 agents takes about 10x as long as 100 agents. Still very doable, just be patient.

## Final Thoughts

This analysis shows something uncomfortable: in systems with multiplicative dynamics and randomness, merit explains surprisingly little of the outcome variation. Most of success is luck compounding over time.

That doesn't mean talent is irrelevant. It means among reasonably capable people (which is most people), who succeeds is largely a matter of who gets lucky. The winner is rarely the best, just the luckiest of the good enough.

For individuals, this suggests some humility. Your success probably owes more to fortunate timing and random breaks than you might like to admit. Your failures might be bad luck more than bad choices.

For policymakers, it suggests focusing on access and opportunity rather than trying to pick winners. When randomness dominates, you can't know in advance who will succeed, so you might as well help everyone and let the chips fall.

For researchers, it shows the power of agent-based simulation and causal inference. We can build simple models that generate complex emergent patterns and then rigorously test what's driving those patterns.
