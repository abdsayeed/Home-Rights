"""
Document Classification Model
Classifies legal documents into categories
"""
try:
    import tensorflow as tf
    from tensorflow.keras import layers, models
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("TensorFlow not available - using fallback mode")

import numpy as np
import json
import os


def build_document_classifier(vocab_size=10000, max_length=500, num_classes=6):
    """
    Build CNN-LSTM hybrid model for document classification
    
    Args:
        vocab_size: Size of vocabulary
        max_length: Maximum sequence length
        num_classes: Number of document categories
    
    Returns:
        Compiled Keras model
    """
    if not TENSORFLOW_AVAILABLE:
        raise ImportError("TensorFlow is required to build models")
    
    model = models.Sequential([
        # Embedding layer
        layers.Embedding(
            input_dim=vocab_size,
            output_dim=300,
            input_length=max_length,
            name='embedding'
        ),
        
        # CNN layers for local feature extraction
        layers.Conv1D(128, 5, activation='relu', name='conv1'),
        layers.MaxPooling1D(5, name='pool1'),
        
        layers.Conv1D(128, 5, activation='relu', name='conv2'),
        layers.MaxPooling1D(5, name='pool2'),
        
        layers.Conv1D(128, 5, activation='relu', name='conv3'),
        layers.GlobalMaxPooling1D(name='global_pool'),
        
        # Dense layers for classification
        layers.Dense(256, activation='relu', name='dense1'),
        layers.Dropout(0.5, name='dropout1'),
        
        layers.Dense(128, activation='relu', name='dense2'),
        layers.Dropout(0.3, name='dropout2'),
        
        # Output layer
        layers.Dense(num_classes, activation='softmax', name='output')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
    )
    
    return model


class DocumentClassifier:
    """Document classifier for legal documents"""
    
    def __init__(self, model_path=None):
        self.model = None
        self.tokenizer = None
        self.label_encoder = None
        self.max_length = 500
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def load_model(self, model_path):
        """Load trained model and artifacts"""
        if not TENSORFLOW_AVAILABLE:
            print("TensorFlow not available - using fallback classification")
            return False
        
        try:
            # Load model
            self.model = tf.keras.models.load_model(model_path)
            
            # Load tokenizer
            tokenizer_path = os.path.join(model_path, 'tokenizer.json')
            if os.path.exists(tokenizer_path):
                with open(tokenizer_path, 'r') as f:
                    tokenizer_json = json.load(f)
                self.tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(
                    tokenizer_json
                )
            
            # Load label encoder
            le_path = os.path.join(model_path, 'label_encoder.json')
            if os.path.exists(le_path):
                with open(le_path, 'r') as f:
                    le_data = json.load(f)
                self.label_encoder = le_data['classes']
            
            print(f"Model loaded from {model_path}")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def predict(self, text):
        """
        Predict document category
        
        Args:
            text: Document text
            
        Returns:
            dict with category, confidence, and probabilities
        """
        if not self.model or not self.tokenizer or not self.label_encoder:
            # Return mock prediction if model not loaded
            return self._mock_prediction(text)
        
        # Preprocess
        sequence = self.tokenizer.texts_to_sequences([text])
        padded = tf.keras.preprocessing.sequence.pad_sequences(
            sequence,
            maxlen=self.max_length,
            padding='post'
        )
        
        # Predict
        predictions = self.model.predict(padded, verbose=0)
        
        # Get results
        category_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][category_idx])
        category = self.label_encoder[category_idx]
        
        # Get all probabilities
        probabilities = {
            self.label_encoder[i]: float(predictions[0][i])
            for i in range(len(self.label_encoder))
        }
        
        return {
            'category': category,
            'confidence': confidence,
            'probabilities': probabilities
        }
    
    def _mock_prediction(self, text):
        """Mock prediction when model not loaded"""
        text_lower = text.lower()
        
        # Simple keyword-based classification
        if 'tenancy agreement' in text_lower or 'assured shorthold' in text_lower:
            category = 'tenancy_agreement'
            confidence = 0.85
        elif 'section 21' in text_lower:
            category = 'section_21_notice'
            confidence = 0.80
        elif 'section 8' in text_lower:
            category = 'section_8_notice'
            confidence = 0.82
        elif 'repair' in text_lower:
            category = 'repair_request'
            confidence = 0.75
        elif 'rent' in text_lower and 'statement' in text_lower:
            category = 'rent_statement'
            confidence = 0.78
        else:
            category = 'general_correspondence'
            confidence = 0.65
        
        categories = [
            'tenancy_agreement',
            'section_21_notice',
            'section_8_notice',
            'repair_request',
            'rent_statement',
            'general_correspondence'
        ]
        
        probabilities = {cat: 0.1 for cat in categories}
        probabilities[category] = confidence
        
        return {
            'category': category,
            'confidence': confidence,
            'probabilities': probabilities
        }
