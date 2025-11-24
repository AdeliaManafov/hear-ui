"""Custom calibration wrapper for regressor models.

This module defines the CalibratedRegressor class which must be importable
for unpickling calibrated models.
"""

import numpy as np


class CalibratedRegressor:
    """Wrapper for regressor with isotonic calibration.
    
    This class wraps a base regressor model with an isotonic calibrator
    to improve probability calibration.
    """
    
    def __init__(self, base_model, calibrator):
        """Initialize calibrated regressor.
        
        Args:
            base_model: The base sklearn model (e.g., Pipeline with RandomForestRegressor)
            calibrator: Fitted IsotonicRegression calibrator
        """
        self.base_model = base_model
        self.calibrator = calibrator
    
    def predict(self, X):
        """Make calibrated predictions.
        
        Args:
            X: Input features (DataFrame or array)
            
        Returns:
            Calibrated predictions (numpy array)
        """
        # Get base predictions and clip to [0, 1]
        base_pred = np.clip(self.base_model.predict(X), 0, 1)
        # Apply calibration
        return self.calibrator.transform(base_pred)
    
    def predict_proba(self, X):
        """Get prediction probabilities in sklearn format.
        
        Args:
            X: Input features
            
        Returns:
            Array of shape (n_samples, 2) with [1-prob, prob]
        """
        probs = self.predict(X)
        return np.vstack([1 - probs, probs]).T
    
    def __getattr__(self, name):
        """Delegate attribute access to base model if not found."""
        return getattr(self.base_model, name)
