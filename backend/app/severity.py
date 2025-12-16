import pickle
import os
import logging


MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'rf_severity.pkl')


def predict_severity(features):
    """
    Given extracted features, predict severity and injury info using a trained classifier.
    Returns severity label and injury label.
    Features: list/array shaped as expected by your model.
    """
    try:
        # Check if model file exists
        if not os.path.exists(MODEL_PATH):
            logging.warning(f"Model file not found at {MODEL_PATH}. Using fallback prediction.")
            return predict_severity_fallback(features)
        
        with open(MODEL_PATH, 'rb') as f:
            clf = pickle.load(f)
        
        prediction = clf.predict([features])
        
        # Map prediction indices to severity and injury labels
        severity_map = {0: "low", 1: "medium", 2: "high"}
        injury_map = {0: "no_injury", 1: "minor_injury", 2: "possible_injury"}
        
        if hasattr(prediction[0], '__iter__'):
            s_idx, i_idx = prediction[0][0], prediction[0][1]
        else:
            s_idx, i_idx = prediction[0], 0
        
        severity = severity_map.get(s_idx, "medium")
        injury = injury_map.get(i_idx, "possible_injury")
        
        return severity, injury
        
    except Exception as e:
        logging.error(f"Severity prediction error: {str(e)}")
        return predict_severity_fallback(features)


def predict_severity_fallback(features):
    """
    Fallback prediction based on deformation score when model is not available.
    """
    try:
        # Extract deformation score (first feature)
        deformation = features[0] if features and len(features) > 0 else 0.5
        
        # Classify severity based on deformation
        if deformation > 0.7:
            severity = "high"
        elif deformation > 0.4:
            severity = "medium"
        else:
            severity = "low"
        
        # Classify injury based on deformation
        if deformation > 0.6:
            injury = "possible_injury"
        elif deformation > 0.3:
            injury = "minor_injury"
        else:
            injury = "no_injury"
        
        return severity, injury
        
    except Exception as e:
        logging.error(f"Fallback severity prediction error: {str(e)}")
        return "medium", "possible_injury"
