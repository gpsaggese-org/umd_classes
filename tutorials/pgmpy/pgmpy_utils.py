"""
Utility functions for pgmpy tutorial notebooks.

- Notebooks should call these functions instead of writing raw logic inline.
- This helps keep the notebooks clean, modular, and easier to debug.

Import as:

import tutorials.pgmpy.pgmpy_utils as tpgpguti
"""

import pandas as pd
import logging
from itertools import product
from sklearn.model_selection import train_test_split
from pycaret.classification import compare_models

def draw_pgmpy_model(model, filename="model.png", prog="dot"):
    """
    Draw a pgmpy model using Graphviz and display it in a notebook.
    Requires pygraphviz + graphviz system packages.

    :param model: pgmpy DiscreteBayesianNetwork model
    :param filename: output filename for the PNG image
    :param prog: graphviz program to use (default: "dot")
    :return: graphviz object
    """
    from IPython.display import Image, display

    g = model.to_graphviz()
    g.draw(filename, prog=prog)
    display(Image(filename=filename))
    return g


def factor_to_dataframe(factor, value_col="probability"):
    """
    Convert a pgmpy Factor to a pandas DataFrame.

    :param factor: pgmpy DiscreteFactor object
    :param value_col: name of the column for probability values
    :return: pandas DataFrame with factor variables and values
    """
    variables = factor.variables
    states = [
        factor.state_names.get(v, list(range(factor.cardinality[i])))
        for i, v in enumerate(variables)
    ]
    assignments = list(product(*states))
    df = pd.DataFrame(assignments, columns=variables)
    df[value_col] = factor.values.flatten()
    return df
