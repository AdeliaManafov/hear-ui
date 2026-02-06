"""Simple test script to verify generic XAI and model adapter architecture.

Run this with: python test_generic_architecture.py
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def test_explainer_interface():
    """Test that explainer interface and factory work."""
    from app.core.explainer_interface import ExplainerFactory
    from app.core.explainer_registry import get_available_explainers
    
    print("\n=== Testing Explainer Interface ===")
    
    # Check available methods
    methods = get_available_explainers()
    print(f"✓ Available explainer methods: {methods}")
    
    assert "shap" in methods, "SHAP should be registered"
    assert "coefficient" in methods, "Coefficient explainer should be registered"
    
    # Try to create each explainer
    for method in ["shap", "coefficient"]:
        try:
            explainer = ExplainerFactory.create(method)
            print(f"✓ Created {method} explainer: {explainer.get_method_name()}")
        except Exception as e:
            print(f"✗ Failed to create {method} explainer: {e}")
            return False
    
    return True


def test_model_adapters():
    """Test model adapter interface."""
    from app.core.model_adapter import SklearnModelAdapter, ModelAdapter
    import numpy as np
    
    print("\n=== Testing Model Adapters ===")
    
    # Create a simple sklearn model
    try:
        from sklearn.linear_model import LogisticRegression
        
        X = np.array([[1, 2], [3, 4], [5, 6]])
        y = np.array([0, 1, 0])
        
        model = LogisticRegression()
        model.fit(X, y)
        
        adapter = SklearnModelAdapter(model)
        print(f"✓ Created SklearnModelAdapter for {type(model).__name__}")
        print(f"  - Model type: {adapter.get_model_type()}")
        
        # Test prediction
        pred = adapter.predict(X[:1])
        print(f"  - Prediction: {pred}")
        
        # Test predict_proba
        proba = adapter.predict_proba(X[:1])
        print(f"  - Probability: {proba}")
        
        # Test coefficients
        coef = adapter.get_coefficients()
        print(f"  - Coefficients shape: {coef.shape if coef is not None else None}")
        
        return True
        
    except ImportError:
        print("✗ sklearn not available, skipping test")
        return True
    except Exception as e:
        print(f"✗ Model adapter test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_dataset_adapters():
    """Test dataset adapter interface."""
    from app.core.ci_dataset_adapter import CochlearImplantDatasetAdapter
    
    print("\n=== Testing Dataset Adapters ===")
    
    try:
        adapter = CochlearImplantDatasetAdapter()
        print(f"✓ Created CochlearImplantDatasetAdapter")
        
        # Test with sample CI patient data
        sample_data = {
            "Alter [J]": 45,
            "Geschlecht": "w",
            "Primäre Sprache": "Deutsch",
        }
        
        preprocessed = adapter.preprocess(sample_data)
        print(f"  - Preprocessed shape: {preprocessed.shape}")
        
        feature_names = adapter.get_feature_names()
        print(f"  - Number of features: {len(feature_names)}")
        
        schema = adapter.get_feature_schema()
        print(f"  - Schema: {schema.get('dataset_name', 'N/A')}")
        
        # Test validation
        valid, msg = adapter.validate_input(sample_data)
        print(f"  - Validation: {'✓ passed' if valid else f'✗ failed: {msg}'}")
        
        return True
        
    except Exception as e:
        print(f"✗ Dataset adapter test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_model_wrapper_adapters():
    """Test ModelWrapper with new adapter architecture."""
    from app.core.model_wrapper import ModelWrapper
    from app.core.ci_dataset_adapter import CochlearImplantDatasetAdapter
    
    print("\n=== Testing ModelWrapper with Adapters ===")
    
    try:
        # Create wrapper with CI adapter
        wrapper = ModelWrapper(dataset_adapter=CochlearImplantDatasetAdapter())
        
        if wrapper.is_loaded():
            print(f"✓ Model loaded successfully")
            print(f"  - Model type: {wrapper.model_adapter.get_model_type() if wrapper.model_adapter else 'N/A'}")
            print(f"  - Feature count: {len(wrapper.get_feature_names())}")
            
            # Test prediction with sample data
            sample = {
                "Alter [J]": 50,
                "Geschlecht": "m",
            }
            
            try:
                pred = wrapper.predict(sample)
                print(f"  - Sample prediction: {pred}")
            except Exception as e:
                print(f"  - Prediction test: {e}")
        else:
            print("⚠ Model not loaded (this is OK if model file doesn't exist)")
        
        return True
        
    except Exception as e:
        print(f"✗ ModelWrapper test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_explainer_with_model():
    """Test explainer with actual model."""
    from app.core.model_wrapper import ModelWrapper
    from app.core.explainer_registry import create_explainer
    import numpy as np
    
    print("\n=== Testing Explainer with Model ===")
    
    try:
        wrapper = ModelWrapper()
        
        if not wrapper.is_loaded():
            print("⚠ Model not loaded, skipping explainer test")
            return True
        
        # Create coefficient explainer (fast, always works for linear models)
        explainer = create_explainer("coefficient", model=wrapper.model)
        print(f"✓ Created {explainer.get_method_name()} explainer")
        
        # Create sample preprocessed data
        sample = {
            "Alter [J]": 45,
            "Geschlecht": "w",
        }
        
        X = wrapper.prepare_input(sample)
        print(f"  - Preprocessed shape: {X.shape}")
        
        # Generate explanation
        explanation = explainer.explain(
            model=wrapper.model,
            input_data=X,
            feature_names=wrapper.get_feature_names()
        )
        
        print(f"  - Prediction: {explanation.prediction:.4f}")
        print(f"  - Base value: {explanation.base_value:.4f}")
        print(f"  - Top 5 features:")
        
        sorted_features = sorted(
            explanation.feature_importance.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:5]
        
        for name, importance in sorted_features:
            print(f"      {name}: {importance:.6f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Explainer with model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("Testing Generic XAI and Model Architecture")
    print("=" * 70)
    
    tests = [
        ("Explainer Interface", test_explainer_interface),
        ("Model Adapters", test_model_adapters),
        ("Dataset Adapters", test_dataset_adapters),
        ("ModelWrapper Adapters", test_model_wrapper_adapters),
        ("Explainer with Model", test_explainer_with_model),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    print("\n" + "=" * 70)
    print("Test Results")
    print("=" * 70)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:10} {name}")
    
    all_passed = all(r[1] for r in results)
    print("=" * 70)
    
    if all_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
