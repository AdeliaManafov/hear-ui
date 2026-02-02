"""Explainer registry - registers all available explainer implementations.

This module auto-registers all explainer implementations with the factory
so they can be discovered and used by the application.
"""

from .alternative_explainers import CoefficientExplainer, LIMEExplainer
from .explainer_interface import ExplainerFactory
from .shap_explainer_adapter import ShapExplainerAdapter

# Register all explainer implementations
ExplainerFactory.register("shap", ShapExplainerAdapter)
ExplainerFactory.register("coefficient", CoefficientExplainer)
ExplainerFactory.register("lime", LIMEExplainer)

# Aliases for convenience
ExplainerFactory.register("coef", CoefficientExplainer)
ExplainerFactory.register("linear", CoefficientExplainer)


def get_available_explainers() -> list[str]:
    """Get list of all registered explainer methods.

    Returns:
        List of method names
    """
    return ExplainerFactory.list_available_methods()


def create_explainer(method: str, model=None, **kwargs):
    """Create an explainer instance.

    Args:
        method: Explainer method name ("shap", "lime", "coefficient")
        model: Model instance
        **kwargs: Method-specific parameters

    Returns:
        Explainer instance

    Raises:
        ValueError: If method is not registered
    """
    return ExplainerFactory.create(method, model=model, **kwargs)
