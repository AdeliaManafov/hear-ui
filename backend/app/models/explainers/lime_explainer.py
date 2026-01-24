from lime import lime_tabular
import numpy as np

class LimeExplainer:
    def __init__(self, model, feature_names):
        self.model = model
        self.feature_names = feature_names

    def prepare_training_data(self, training_data):
        self.explainer = lime_tabular.LimeTabularExplainer(
            training_data=training_data,
            feature_names=self.feature_names,
            class_names=['nicht_empfohlen', 'empfohlen'],
            mode='classification'
        )

    def explain(self, input_data):
        # Format the input data
        data_array = np.array([
            input_data.age,
            input_data.hearing_loss_duration,
            1 if input_data.implant_type == "type_a" else 0  # Anpassung je nach Ihren Daten
        ]).reshape(1, -1)

        explanation = self.explainer.explain_instance(
            data_array[0],
            self.model.predict_proba,
            num_features=len(self.feature_names)
        )

        return {
            feature: {
                'importance': abs(importance),
                'direction': 'positive' if importance > 0 else 'negative'
            }
            for feature, importance in explanation.as_list()
        }