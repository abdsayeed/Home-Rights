TensorFlow Integration Guide
for HomeRights AI
Complete UK Tenant Rights Dataset & ML Implementation
Version 1.0 | February 2026
Abdullah Al Sayeed (B00956522)
Table of Contents
1. Introduction 3
2. UK Tenant Rights - Complete Dataset 5
2.1 Repairs and Maintenance 5
2.2 Deposits and Rent 8
2.3 Eviction Notices 11
2.4 Tenant Rights and Protections 14
3. TensorFlow Architecture 17
3.1 Document Classification Model 18
3.2 Named Entity Recognition 21
3.3 Pattern Detection System 24
4. Data Preparation 27
4.1 Data Collection Strategy 27
4.2 Annotation Guidelines 29
4.3 Preprocessing Pipeline 31
5. Model Training 34
5.1 Training Environment Setup 34
5.2 Training Procedures 36
5.3 Evaluation Metrics 39
6. Integration with Flask 42
6.1 Model Serving 42
6.2 API Endpoints 44
6.3 Real-time Processing 46
7. Implementation Code 48
8. Testing and Validation 58
9. Deployment 61
10. References 64
1. Introduction
This comprehensive guide provides step-by-step instructions for integrating TensorFlow
machine learning models into the HomeRights AI application. The document includes
complete UK tenant rights information structured for ML training, detailed model
architectures, training procedures, and integration code. The guide is organized into three
main parts:
• Part 1: UK Tenant Rights Dataset - Complete legal information about repairs, deposits,
evictions, and tenant protections, structured for machine learning training.
• Part 2: TensorFlow Models - Detailed architecture and training procedures for document
classification, entity extraction, and pattern detection.
• Part 3: Integration - Complete implementation code for integrating trained models with the Flask
backend API.
Key Features of This Implementation:
- Three specialized ML models working in concert
- Real-time document analysis and classification
- Entity extraction from legal documents
- Pattern detection for unfair clauses
- Comprehensive UK housing law coverage
- Production-ready Flask integration
2. UK Tenant Rights - Complete Dataset
This section provides comprehensive UK tenant rights information structured for machine
learning training. Each topic includes the legal basis, key points, common violations, and
relevant legislation. This data will be used to train the document classification and pattern
detection models.
2.1 Repairs and Maintenance
Legal Framework:
Topic: Landlord Repair Responsibilities
Legal Basis: Landlord and Tenant Act 1985, Section 11
Landlord Responsibilities:
• Structure and exterior (walls, roof, windows, doors, gutters, external pipes)
• Basins, sinks, baths, toilets
• Water and gas pipes, electrical wiring
• Heating and hot water installations
• Common areas in buildings with multiple flats
Tenant Responsibilities:
• Minor repairs (replacing light bulbs, batteries)
• Damage caused by tenant or their guests
• Reporting repairs promptly to landlord
Common Violations to Detect:
■ Clause stating tenant responsible for all repairs
■ Landlord refusing to do repairs
■ Long delays (>reasonable time) in completing repairs
■ Charging tenant for landlord's repair responsibilities
ML Training Example - Repairs:
Document Text:
"The Tenant shall be responsible for all repairs and maintenance to the Property including structural
repairs, plumbing, heating, and electrical systems."
Expected Classification: Tenancy Agreement
Detected Issue: Unfair repair responsibility clause
Severity: HIGH
Explanation: This clause violates Section 11 of the Landlord and Tenant Act 1985. The landlord is
legally responsible for structural repairs, plumbing, heating, and electrical systems.
Recommendation: This clause is likely unenforceable. Contact Shelter or Citizens Advice.
2.2 Deposits and Rent
Topic: Deposit Protection and Rent Regulations
Legal Basis: Housing Act 2004, Tenant Fees Act 2019, Deregulation Act 2015
<b>Requirement</b> <b>Details</b>
Maximum Deposit 5 weeks' rent (if annual rent is less than £50,000)
Protection Timeline 30 days from receiving deposit to protect it
Return Timeline 10 days (no disputes)
Prohibited Fees (Tenant Fees Act 2019):
■ Viewing fees
■ Administration fees
■ Reference fees
■ Check-in/check-out fees (beyond actual costs)
■ Renewal fees
Permitted Payments:
✓ Rent
✓ Refundable tenancy deposit (max 5 weeks)
✓ Refundable holding deposit (max 1 week, deducted from rent/deposit)
✓ Payments in default (late rent, lost keys, professional cleaning if specified)
✓ Early termination fees (if tenant requests early exit)
✓ Utilities and council tax (if specified in tenancy)
ML Training Example - Deposits:
Document Text:
"The Tenant shall pay a non-refundable deposit of £3,000 and an administration fee of £200 upon
signing this agreement. Monthly rent is £1,000."
Expected Classification: Tenancy Agreement
Detected Issues:
1. Non-refundable deposit (CRITICAL)
- All deposits must be refundable
- Deposit exceeds legal maximum (£3,000 vs £1,250 max for £1,000/month rent)
2. Administration fee (HIGH)
- Prohibited under Tenant Fees Act 2019
- Landlord/agent cannot charge administration fees
Recommendations:
• Demand return of excess deposit (£1,750)
• Request refund of administration fee (£200)
• Report to Trading Standards if fees not returned
• Potential fine for landlord: £5,000 (first offense), £30,000 (repeat)
2.3 Eviction Notices
Eviction procedures are strictly regulated in the UK. Landlords must follow specific legal
processes and cannot evict tenants without proper notice and, if necessary, a court order.
The Renters' Rights Act 2025 has made significant changes to eviction rules.
Section 21 Notice (No-Fault Eviction) - ABOLISHED
IMPORTANT UPDATE: Section 21 'no-fault' evictions were abolished under the Renters' Rights
Act 2025 (received Royal Assent 27 October 2025). Landlords can no longer evict tenants without
providing a specific reason.
Historical Information (for analyzing old documents):
• Minimum notice period was 2 months
• Could only be served after initial fixed term
• No reason needed to be given
• Must wait 4 months from tenancy start
• Invalid if deposit not protected
For ML Training: Documents mentioning Section 21 notices should be flagged as potentially
outdated (pre-2025) or invalid if dated after October 2025.
Section 8 Notice (Fault-Based Eviction)
Section 8 notices require the landlord to specify grounds for eviction. These remain valid under the
new legislation.
<b>Ground</b> <b>Reason</b> <b>Notice Period</b> <b>Mandatory</b>
Ground 1 Landlord needs property to live in (prior residence) Any reasonable Yes
Ground 2 Mortgage repossession required 2 months Yes
Ground 7 Death of tenant 1 month No
Ground 8 At least 2 months rent arrears 2 weeks Yes
Ground 10 Some rent arrears (at notice & hearing) 2 weeks No
Ground 11 Persistent late rent payment 2 weeks No
Ground 12 Breach of tenancy agreement 2 weeks No
Ground 14 Antisocial behaviour or criminal activity 2 weeks No
Ground 15 Deterioration of furniture/property 2 weeks No
Ground 17 False statement in tenancy application 2 weeks No
Common Eviction Notice Violations:
■ Section 21 notice after October 2025 (no longer legal)
■ Incorrect notice period (too short)
■ Missing required information (dates, grounds, etc.)
■ Invalid form used (not prescribed form)
■ Notice served during fixed term without break clause
■ Illegal eviction (changing locks, removing belongings)
■ Harassment or intimidation to force tenant to leave
■ Section 8 without valid grounds
■ Eviction without court order (except specific circumstances)
ML Training Example - Eviction Notice:
Document Text:
"NOTICE TO QUIT - Section 21
Date: January 15, 2026
You must leave the property at 123 Main Street within 28 days of this notice. No reason is required.
Failure to leave will result in immediate legal action."
Expected Classification: Section 21 Notice (Invalid)
Detected Issues:
1. Section 21 abolished (CRITICAL)
- Section 21 notices are no longer legal as of October 2025
- This notice dated January 2026 is invalid
2. Incorrect notice period (HIGH)
- Even when Section 21 was valid, minimum was 2 months (not 28 days)
3. Threatening language (MEDIUM)
- "Immediate legal action" is inappropriate
- Landlord must obtain court order before eviction
Recommendations:
• This notice is completely invalid and should be ignored legally
• Contact Shelter immediately for advice
• If landlord attempts illegal eviction, call police (999)
• Landlord may be liable for harassment/illegal eviction
• Continue paying rent and remain in property
2.4 Tenant Rights and Protections
UK tenants have extensive legal protections. Understanding these rights is essential for
detecting unfair clauses in tenancy agreements.
Core Tenant Rights:
✓ Right to live in a property that's safe and in good repair - Landlord must maintain structure,
heating, water, gas, and electricity
✓ Right to be protected from unfair eviction - Landlord must follow legal process, cannot change
locks or remove belongings
✓ Right to challenge unfair rent increases - Can apply to tribunal if increase is unfair
✓ Right to know who your landlord is - Must be provided with landlord's name and address
✓ Right to see an Energy Performance Certificate (EPC) - Property must have minimum E rating
✓ Right to a written tenancy agreement - Can request written terms
✓ Right to live in the property undisturbed - Landlord must give 24 hours notice for inspections
✓ Right to have deposit protected - In government-approved scheme within 30 days
✓ Right to be treated fairly regardless of protected characteristics - Equality Act 2010
protections
Common Unfair Terms to Detect:
Unfair Term Why It's Unfair Legal Basis
Blanket pet ban Can be challenged as unreasonable unless property unsuitability Renters' Rights Act 2025
Tenant liable for all repairs Landlord responsible for structure/installations Landlord and Tenant Act 1985 s11
No visitors allowed Unreasonable restriction on quiet enjoyment Derogation from Grant
Landlord can enter anytime 24 hours notice required except emergency Protection from Eviction Act 1977
Non-refundable charges All deposits must be refundable Housing Act 2004
Automatic rent increases above inflation Can be challenged as unfair Consumer Rights Act 2015
Tenant pays for professional cleaning Unless cleaning to original standard requiredTenant Fees Act 2019
Tenant responsible for structural repairs Landlord's statutory responsibility Landlord and Tenant Act 1985
Cannot report repairs without penalty Retaliatory eviction prohibited Deregulation Act 2015
ML Pattern Detection Rules for Implementation:
The following regex patterns and keywords should be used to detect unfair clauses:
PATTERN_RULES = { 'unfair_repairs': { 'patterns': [
r'tenant.*responsible.*all.*repair', r'tenant.*maintain.*structure',
r'tenant.*fix.*structural.*damage',
r'no.*landlord.*responsibility.*repair' ], 'severity': 'HIGH',
'legal_ref': 'Landlord and Tenant Act 1985 s11' }, 'unfair_deposit': {
'patterns': [ r'non-refundable.*deposit', r'deposit.*not.*return',
r'deposit.*exceed.*\d+.*week', r'deposit.*not.*protect' ], 'severity':
'CRITICAL', 'legal_ref': 'Housing Act 2004, Tenant Fees Act 2019' },
'illegal_fees': { 'patterns': [ r'administration.*fee',
r'reference.*check.*fee', r'viewing.*fee', r'renewal.*fee' ], 'severity':
'HIGH', 'legal_ref': 'Tenant Fees Act 2019' }, 'unfair_access': {
'patterns': [ r'landlord.*enter.*anytime',
r'no.*notice.*require.*inspection',
r'tenant.*must.*allow.*access.*immediately' ], 'severity': 'MEDIUM',
'legal_ref': 'Protection from Eviction Act 1977' }, 'invalid_eviction': {
'patterns': [ r'section 21.*notice', r'evict.*without.*court.*order',
r'leave.*immediately', r'24.*hour.*eviction' ], 'severity': 'CRITICAL',
'legal_ref': 'Renters Rights Act 2025' } }
3. TensorFlow Architecture
The HomeRights AI system uses three specialized TensorFlow models working together
to analyze legal documents. This section provides detailed architecture for each model.
System Overview:
• Model 1: Document Classifier - Identifies the type of legal document (tenancy agreement,
Section 8 notice, repair request, etc.)
• Model 2: Named Entity Recognition (NER) - Extracts key information like names, addresses,
dates, and monetary amounts
• Model 3: Pattern Detector - Identifies potentially unfair or illegal clauses using rule-based
patterns and ML
3.1 Document Classification Model
Purpose: Classify legal documents into predefined categories
Architecture: CNN-LSTM Hybrid Network
Input: Document text (up to 500 tokens)
Output: Document category + confidence score
<b>Category</b> <b>Description</b> <b>Key Features</b>
Tenancy Agreement Legally binding rental contract Contains terms, rent amount, deposit, obligations
Section 21 Notice No-fault eviction (pre-2025) Notice period, property address, dated before Oct 2025
Section 8 Notice Fault-based eviction Specifies grounds, notice period, hearing date
Repair Request Tenant repair notification Description of issue, urgency, access requirements
Rent Statement Payment records Amounts, dates, payment method, arrears if any
General Correspondence Other housing-related docs Letters, emails, notices not in above categories
TensorFlow Model Architecture: import tensorflow as tf from
tensorflow.keras import layers, models def
build_document_classifier(vocab_size=10000, max_length=500,
num_classes=6): """ CNN-LSTM hybrid model for document classification """
model = models.Sequential([ # Embedding layer
layers.Embedding(input_dim=vocab_size, output_dim=300,
input_length=max_length, name='embedding'), # CNN layers for local feature
extraction layers.Conv1D(128, 5, activation='relu', name='conv1'),
layers.MaxPooling1D(5, name='pool1'), layers.Conv1D(128, 5,
activation='relu', name='conv2'), layers.MaxPooling1D(5, name='pool2'),
layers.Conv1D(128, 5, activation='relu', name='conv3'),
layers.GlobalMaxPooling1D(name='global_pool'), # Dense layers for
classification layers.Dense(256, activation='relu', name='dense1'),
layers.Dropout(0.5, name='dropout1'), layers.Dense(128, activation='relu',
name='dense2'), layers.Dropout(0.3, name='dropout2'), # Output layer
layers.Dense(num_classes, activation='softmax', name='output') ])
model.compile( optimizer='adam', loss='categorical_crossentropy',
metrics=['accuracy', 'precision', 'recall'] ) return model # Create model
classifier = build_document_classifier() classifier.summary()
Training Specifications:
<b>Parameter</b> <b>Value</b> Batch Size 32 Learning Rate 0.001 Epochs 50 Train/Val/Test Split 70/15/15% Vocabulary Size 10,000 Max Sequence Length 500 tokens Embedding Dimension 300 Dropout Rate 0.5, 0.3 Expected Performance Metrics:
• Accuracy: >85% on test set
• Precision: >83% (minimize false positives)
• Recall: >82% (minimize false negatives)
• F1 Score: >82%
• Inference Time: <200ms per document
<b>Rationale</b>
Balance between memory and training stability
Adam optimizer default, works well for text
With early stopping (patience=5)
Standard split for sufficient training data
Covers legal terminology without overfitting
Captures full context of most documents
Standard for word embeddings
Prevents overfitting on legal jargon
3.2 Named Entity Recognition (NER)
Purpose: Extract structured information from unstructured legal text
Architecture: Transformer-based (spaCy with custom training)
Input: Raw document text
Output: Labeled entities with positions and categories
<b>Entity Type</b> <b>Examples</b> <b>Importance</b>
PERSON John Smith (landlord), Jane Doe (tenant) Identify parties in agreement
ADDRESS 123 Main Street, London SW1A 1AA Property identification
DATE 1 January 2025, 15/02/2026 Notice periods, tenancy start/end
MONEY £1,200, £5,000 deposit Rent amounts, fees, deposits
ORG ABC Property Management Ltd Management companies, agencies
LAW Section 11, Housing Act 2004 Legal references
DURATION 6 months, 2 years Fixed term lengths, notice periods
PERCENTAGE 5%, annual increase Rent increases, fees
spaCy NER Implementation: import spacy from spacy.training import Example
import random def train_legal_ner(training_data, output_path,
iterations=30): """ Train custom NER model for legal documents
training_data format: [ ("The landlord, John Smith, at 123 Main St...",
{"entities": [(14, 24, "PERSON"), (29, 40, "ADDRESS")]}), ... ] """ #
Create blank English model nlp = spacy.blank("en") # Add NER pipeline if
"ner" not in nlp.pipe_names: ner = nlp.add_pipe("ner") else: ner =
nlp.get_pipe("ner") # Add entity labels labels = ["PERSON", "ADDRESS",
"DATE", "MONEY", "ORG", "LAW", "DURATION", "PERCENTAGE"] for label in
labels: ner.add_label(label) # Disable other pipes during training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"] with
nlp.disable_pipes(*other_pipes): optimizer = nlp.begin_training() for
epoch in range(iterations): random.shuffle(training_data) losses = {} #
Batch training for text, annotations in training_data: doc =
nlp.make_doc(text) example = Example.from_dict(doc, annotations)
nlp.update([example], drop=0.5, losses=losses) print(f"Epoch {epoch +
1}/{iterations} - Loss: {losses['ner']:.4f}") # Save model
nlp.to_disk(output_path) print(f"Model saved to {output_path}") return nlp
# Usage example training_data = [ ("Landlord John Smith of 123 Main Street
receives £1200 monthly rent.", {"entities": [(9, 19, "PERSON"), (23, 38,
"ADDRESS"), (48, 53, "MONEY")]}), # ... more training examples ] legal_nlp
= train_legal_ner(training_data, "models/legal_ner")
Context-Aware Role Identification:
The NER model includes logic to infer whether a PERSON entity is a landlord or tenant based on
surrounding context:
def infer_person_role(entity, doc): """Determine if person is landlord or
tenant based on context""" # Get surrounding text (5 words before and
after) start = max(0, entity.start - 5) end = min(len(doc), entity.end + 5)
context = doc[start:end].text.lower() # Landlord indicators
landlord_keywords = ['landlord', 'lessor', 'owner', 'property manager',
'letting agent', 'receives rent', 'grants'] # Tenant indicators
tenant_keywords = ['tenant', 'lessee', 'occupier', 'renter', 'pays rent',
'rents'] landlord_score = sum(1 for kw in landlord_keywords if kw in
context) tenant_score = sum(1 for kw in tenant_keywords if kw in context)
if landlord_score > tenant_score: return 'landlord' elif tenant_score >
landlord_score: return 'tenant' else: return 'unknown'
4. Data Preparation
High-quality training data is crucial for model performance. This section outlines strategies
for collecting, annotating, and preprocessing UK housing law documents.
4.1 Data Collection Strategy
<b>Source</b> <b>Type</b> <b>Quantity Target</b> <b>Usage</b>
GOV.UK Example forms, guidance 200 documents Official templates, notices
Citizens Advice Sample documents 300 documents Real-world examples
Shelter Case studies, examples 250 documents Problem cases, disputes
Court Documents Public domain cases 150 documents Legal precedents
Synthetic Data Template-based generation 2000 documents Augmentation, variations
User Submissions Anonymized uploads 1000+ documents Real tenant documents
Synthetic Data Generation Script: import random from faker import Faker
fake = Faker('en_GB') def
generate_tenancy_agreement(template_type='standard'): """Generate
synthetic tenancy agreement""" data = { 'landlord_name': fake.name(),
'tenant_name': fake.name(), 'property_address': fake.address(),
'monthly_rent': random.choice([800, 950, 1100, 1250, 1400, 1600]),
'deposit': None, # Will calculate 'start_date':
fake.date_between(start_date='-1y', end_date='today'), 'term_months':
random.choice([6, 12, 18, 24]), } # Calculate deposit (should be max 5
weeks) data['deposit'] = int(data['monthly_rent'] * 1.15) # ~5 weeks #
Occasionally introduce violations for training if template_type ==
'problematic' and random.random() < 0.3: # Add unfair clauses if
random.random() < 0.5: data['deposit'] = int(data['monthly_rent'] * 3) #
Excessive! if random.random() < 0.5: data['admin_fee'] = 200 # Illegal fee!
template = f""" ASSURED SHORTHOLD TENANCY AGREEMENT This Agreement is made
on {data['start_date'].strftime('%d %B %Y')} BETWEEN: Landlord:
{data['landlord_name']} Tenant: {data['tenant_name']} Property:
{data['property_address']} Terms: 1. Rent: £{data['monthly_rent']} per
month, payable in advance 2. Deposit: £{data['deposit']} 3. Term:
{data['term_months']} months fixed term ... """ return template, data #
Generate training set for i in range(2000): doc_type =
random.choice(['standard', 'problematic']) agreement, metadata =
generate_tenancy_agreement(doc_type) # Save for training...
5. Model Training
Complete Training Script for Document Classifier: import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer from
tensorflow.keras.preprocessing.sequence import pad_sequences from
tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint from
sklearn.preprocessing import LabelEncoder from sklearn.model_selection
import train_test_split import numpy as np import json # Load training data
def load_training_data(data_path): with open(data_path, 'r') as f: data =
json.load(f) texts = [item['text'] for item in data] labels =
[item['category'] for item in data] return texts, labels # Prepare data
texts, labels = load_training_data('data/processed/training_data.json') #
Split data X_train, X_temp, y_train, y_temp = train_test_split( texts,
labels, test_size=0.3, random_state=42, stratify=labels ) X_val, X_test,
y_val, y_test = train_test_split( X_temp, y_temp, test_size=0.5,
random_state=42, stratify=y_temp ) # Tokenization tokenizer =
Tokenizer(num_words=10000, oov_token='') tokenizer.fit_on_texts(X_train)
X_train_seq = tokenizer.texts_to_sequences(X_train) X_val_seq =
tokenizer.texts_to_sequences(X_val) X_test_seq =
tokenizer.texts_to_sequences(X_test) # Padding max_length = 500
X_train_pad = pad_sequences(X_train_seq, maxlen=max_length,
padding='post') X_val_pad = pad_sequences(X_val_seq, maxlen=max_length,
padding='post') X_test_pad = pad_sequences(X_test_seq, maxlen=max_length,
padding='post') # Label encoding label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train) y_val_encoded =
label_encoder.transform(y_val) y_test_encoded =
label_encoder.transform(y_test) # One-hot encode y_train_cat =
tf.keras.utils.to_categorical(y_train_encoded) y_val_cat =
tf.keras.utils.to_categorical(y_val_encoded) y_test_cat =
tf.keras.utils.to_categorical(y_test_encoded) # Build model (using
function from section 3.1) model = build_document_classifier(
vocab_size=10000, max_length=500, num_classes=len(label_encoder.classes_)
) # Callbacks callbacks = [ EarlyStopping( monitor='val_loss', patience=5,
restore_best_weights=True, verbose=1 ), ModelCheckpoint(
'models/document_classifier_best.h5', monitor='val_accuracy',
save_best_only=True, verbose=1 ) ] # Train print("Starting training...")
history = model.fit( X_train_pad, y_train_cat, validation_data=(X_val_pad,
y_val_cat), epochs=50, batch_size=32, callbacks=callbacks, verbose=1 ) #
Evaluate test_loss, test_acc, test_prec, test_rec = model.evaluate(
X_test_pad, y_test_cat, verbose=0 ) print(f"\nTest Accuracy:
{test_acc:.4f}") print(f"Test Precision: {test_prec:.4f}") print(f"Test
Recall: {test_rec:.4f}") # Save final model and artifacts
model.save('models/document_classifier_final/') with
open('models/document_classifier_final/tokenizer.json', 'w') as f:
json.dump(tokenizer.to_json(), f) with
open('models/document_classifier_final/label_encoder.json', 'w') as f:
json.dump({ 'classes': label_encoder.classes_.tolist() }, f)
print("Training complete! Model saved.")
6. Integration with Flask
This section provides complete code for integrating the trained TensorFlow models with
your Flask backend API. The implementation includes model loading, prediction
endpoints, and real-time processing.
Flask ML Service Integration (app/services/ml_service.py): import
tensorflow as tf import numpy as np import json import spacy import re from
tensorflow.keras.preprocessing.sequence import pad_sequences import
pytesseract from PIL import Image import PyPDF2 class MLService:
_classifier_model = None _tokenizer = None _label_encoder = None _ner_model
= None @classmethod def initialize(cls, model_path='ml_models/'): """Load
all models on startup""" print("Loading ML models...") # Load document
classifier cls._classifier_model = tf.keras.models.load_model(
f'{model_path}/document_classifier_final/' ) # Load tokenizer with
open(f'{model_path}/document_classifier_final/tokenizer.json', 'r') as f:
tokenizer_json = json.load(f) cls._tokenizer =
tf.keras.preprocessing.text.tokenizer_from_json( tokenizer_json ) # Load
label encoder with
open(f'{model_path}/document_classifier_final/label_encoder.json', 'r') as
f: le_data = json.load(f) cls._label_encoder = le_data['classes'] # Load
NER model cls._ner_model = spacy.load(f'{model_path}/legal_ner/')
print("ML models loaded successfully!") @classmethod def
classify_document(cls, text): """Classify document type""" # Preprocess
sequence = cls._tokenizer.texts_to_sequences([text]) padded =
pad_sequences(sequence, maxlen=500, padding='post') # Predict predictions
= cls._classifier_model.predict(padded, verbose=0) # Get results
category_idx = np.argmax(predictions[0]) confidence =
float(predictions[0][category_idx]) category =
cls._label_encoder[category_idx] # Get all probabilities probabilities = {
cls._label_encoder[i]: float(predictions[0][i]) for i in
range(len(cls._label_encoder)) } return { 'category': category,
'confidence': confidence, 'probabilities': probabilities } @classmethod
def extract_entities(cls, text): """Extract named entities""" doc =
cls._ner_model(text) entities = { 'persons': [], 'addresses': [], 'dates':
[], 'amounts': [], 'organizations': [], 'laws': [] } for ent in doc.ents:
entity_data = { 'text': ent.text, 'label': ent.label_, 'start':
ent.start_char, 'end': ent.end_char } if ent.label_ == 'PERSON': # Infer
role role = cls._infer_person_role(ent, doc) entity_data['role'] = role
entities['persons'].append(entity_data) elif ent.label_ == 'ADDRESS':
entities['addresses'].append(entity_data) elif ent.label_ == 'DATE':
entities['dates'].append(entity_data) elif ent.label_ == 'MONEY':
entities['amounts'].append(entity_data) elif ent.label_ == 'ORG':
entities['organizations'].append(entity_data) elif ent.label_ == 'LAW':
entities['laws'].append(entity_data) return entities @classmethod def
detect_patterns(cls, text): """Detect potentially unfair clauses"""
patterns = { 'unfair_repairs': { 'patterns': [
r'tenant.*responsible.*all.*repair', r'tenant.*maintain.*structure',
r'no.*landlord.*responsibility.*repair' ], 'severity': 'HIGH',
'explanation': 'Landlord is responsible for structural repairs',
'legal_ref': 'Landlord and Tenant Act 1985 Section 11' }, 'unfair_deposit':
{ 'patterns': [ r'non-refundable.*deposit', r'deposit.*exceed.*\d+.*week',
r'deposit.*not.*protect' ], 'severity': 'CRITICAL', 'explanation':
'Deposit must be refundable and protected', 'legal_ref': 'Housing Act 2004,
Tenant Fees Act 2019' }, 'illegal_fees': { 'patterns': [
r'administration.*fee', r'reference.*check.*fee', r'viewing.*fee' ],
'severity': 'HIGH', 'explanation': 'These fees are prohibited',
'legal_ref': 'Tenant Fees Act 2019' }, 'invalid_eviction': { 'patterns': [
r'section 21.*notice', r'evict.*without.*court', r'leave.*immediately' ],
'severity': 'CRITICAL', 'explanation': 'Section 21 abolished, proper
process required', 'legal_ref': 'Renters Rights Act 2025' } }
detected_issues = [] text_lower = text.lower() for issue_type, config in
patterns.items(): for pattern in config['patterns']: matches =
list(re.finditer(pattern, text_lower, re.IGNORECASE)) for match in
matches: detected_issues.append({ 'issue': issue_type, 'severity':
config['severity'], 'matched_text': match.group(0), 'position':
match.span(), 'explanation': config['explanation'], 'legal_reference':
config['legal_ref'], 'recommendations':
cls._get_recommendations(issue_type) }) return detected_issues
@classmethod def _infer_person_role(cls, entity, doc): """Infer if person
is landlord or tenant""" start = max(0, entity.start - 5) end =
min(len(doc), entity.end + 5) context = doc[start:end].text.lower()
landlord_kw = ['landlord', 'lessor', 'owner', 'property manager'] tenant_kw
= ['tenant', 'lessee', 'occupier', 'renter'] if any(kw in context for kw in
landlord_kw): return 'landlord' elif any(kw in context for kw in
tenant_kw): return 'tenant' return 'unknown' @classmethod def
_get_recommendations(cls, issue_type): """Get recommendations for detected
issue""" recommendations = { 'unfair_repairs': [ 'Landlord must maintain
structure and installations', 'Request written clarification', 'Contact
local council housing team' ], 'unfair_deposit': [ 'Ensure deposit is
protected in approved scheme', 'Maximum deposit is 5 weeks rent', 'Contact
Shelter for advice' ], 'illegal_fees': [ 'Request refund of prohibited
fees', 'Report to Trading Standards', 'Landlord faces fines up to £30,000'
], 'invalid_eviction': [ 'Section 21 is no longer valid', 'Continue paying
rent normally', 'Call police if illegal eviction attempted', 'Contact
Citizens Advice immediately' ] } return recommendations.get(issue_type, [])
@classmethod def process_document(cls, file_path, file_type): """Complete
document processing pipeline""" # Extract text if file_type in ['jpg',
'jpeg', 'png']: text = cls._extract_text_from_image(file_path) elif
file_type == 'pdf': text = cls._extract_text_from_pdf(file_path) else:
raise ValueError(f"Unsupported file type: {file_type}") # Run all analysis
classification = cls.classify_document(text) entities =
cls.extract_entities(text) issues = cls.detect_patterns(text) return {
'extracted_text': text, 'classification': classification, 'entities':
entities, 'detected_issues': issues, 'summary':
cls._generate_summary(text, classification, issues) } @classmethod def
_extract_text_from_image(cls, image_path): """OCR extraction""" image =
Image.open(image_path) return pytesseract.image_to_string(image)
@classmethod def _extract_text_from_pdf(cls, pdf_path): """PDF text
extraction""" text = "" with open(pdf_path, 'rb') as file: reader =
PyPDF2.PdfReader(file) for page in reader.pages: text +=
page.extract_text() return text @classmethod def _generate_summary(cls,
text, classification, issues): """Generate plain English summary"""
category = classification['category'] confidence =
classification['confidence'] num_issues = len(issues) critical_issues = [i
for i in issues if i['severity'] == 'CRITICAL'] summary = f"This appears to
be a {category.replace('_', ' ')} " summary += f"(confidence:
{confidence*100:.1f}%). " if num_issues == 0: summary += "No significant
issues detected." else: summary += f"{num_issues} potential issue(s)
detected" if critical_issues: summary += f", including
{len(critical_issues)} critical issue(s)" summary += ". Review the detailed
analysis below." return summary
Flask API Endpoints (app/api/documents.py): from flask import Blueprint,
request, jsonify from flask_jwt_extended import jwt_required,
get_jwt_identity from app.services.ml_service import MLService from
werkzeug.utils import secure_filename import os bp = Blueprint('documents',
__name__) @bp.route('/upload', methods=['POST']) @jwt_required() def
upload_document(): """ Upload and analyze a legal document Request: - file:
Document file (PDF, JPG, PNG) - document_type: Optional hint Response: -
document_id: Unique identifier - extracted_text: OCR/extracted text -
classification: Document type + confidence - entities: Extracted structured
data - detected_issues: List of problems found - summary: Plain English
explanation """ try: # Validate file if 'file' not in request.files: return
jsonify({'error': 'No file provided'}), 400 file = request.files['file'] if
file.filename == '': return jsonify({'error': 'Empty filename'}), 400 #
Validate file type allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png'}
file_ext = file.filename.rsplit('.', 1)[1].lower() if file_ext not in
allowed_extensions: return jsonify({'error': 'Invalid file type'}), 400 #
Save file filename = secure_filename(file.filename) file_path =
os.path.join('/tmp', filename) file.save(file_path) # Process document
result = MLService.process_document(file_path, file_ext) # Store in
database from app.models.document import Document user_id =
get_jwt_identity() document = Document( user_id=user_id,
filename=filename, file_type=file_ext,
extracted_text=result['extracted_text'],
classification=result['classification'], entities=result['entities'],
detected_issues=result['detected_issues'] ) document_id = document.save()
# Clean up temp file os.remove(file_path) return jsonify({ 'document_id':
str(document_id), **result }), 200 except Exception as e: return
jsonify({'error': str(e)}), 500 @bp.route('/analyze', methods=['POST'])
@jwt_required() def analyze_text(): """ Analyze pasted text (no file
upload) Request: - text: Document text content - context: Optional context
hint Response: - classification: Document type - entities: Extracted
information - detected_issues: Problems found - summary: Plain English
explanation """ try: data = request.get_json() if not data or 'text' not in
data: return jsonify({'error': 'No text provided'}), 400 text =
data['text'] if len(text) < 10: return jsonify({'error': 'Text too
short'}), 400 # Run analysis classification =
MLService.classify_document(text) entities =
MLService.extract_entities(text) issues = MLService.detect_patterns(text)
summary = MLService._generate_summary(text, classification, issues) return
jsonify({ 'classification': classification, 'entities': entities,
'detected_issues': issues, 'summary': summary }), 200 except Exception as
e: return jsonify({'error': str(e)}), 500 @bp.route('/', methods=['GET'])
@jwt_required() def get_document(document_id): """Retrieve previously
analyzed document""" try: from app.models.document import Document user_id
= get_jwt_identity() document = Document.find_by_id(document_id, user_id)
if not document: return jsonify({'error': 'Document not found'}), 404
return jsonify(document.to_dict()), 200 except Exception as e: return
jsonify({'error': str(e)}), 500
Initialize ML Models in Flask App (app/__init__.py): from flask import
Flask from flask_cors import CORS from flask_jwt_extended import JWTManager
from app.services.ml_service import MLService def
create_app(config_name='development'): app = Flask(__name__)
app.config.from_object(f'app.config.{config_name.capitalize()}Config') #
Initialize extensions CORS(app) jwt = JWTManager(app) # Initialize MongoDB
from pymongo import MongoClient mongo_client =
MongoClient(app.config['MONGODB_URI']) app.db =
mongo_client[app.config['DB_NAME']] # Initialize ML models
print("Initializing ML models...")
MLService.initialize(model_path=app.config.get('ML_MODEL_PATH',
'ml_models')) # Register blueprints from app.api import auth, topics,
documents, support, chat app.register_blueprint(auth.bp,
url_prefix='/api/auth') app.register_blueprint(topics.bp,
url_prefix='/api/topics') app.register_blueprint(documents.bp,
url_prefix='/api/documents') app.register_blueprint(support.bp,
url_prefix='/api/support') app.register_blueprint(chat.bp,
url_prefix='/api/chat') @app.route('/health') def health_check(): return
{'status': 'healthy', 'ml_models_loaded': True}, 200 return app
10. Conclusion
This guide provides a complete implementation framework for integrating TensorFlow machine
learning models into the HomeRights AI application. The combination of document classification,
entity extraction, and pattern detection creates a powerful system for analyzing UK housing law
documents.
Key Achievements:
• Comprehensive UK tenant rights dataset structured for ML training
• Three specialized TensorFlow models working in concert
• Production-ready Flask integration code
• Real-time document analysis capabilities
• Automatic detection of unfair clauses and violations
Next Steps:
1. Collect and annotate training data from sources outlined in Section 4
2. Train models using scripts provided in Section 5
3. Integrate trained models with Flask backend using code from Section 6
4. Test with real documents and iterate based on results
5. Deploy to Azure with proper scaling configuration
The system is designed to continuously improve as more documents are processed and annotated,
making it increasingly valuable for UK tenants seeking to understand their housing rights.
11. References
• Housing Act 2004. Available from: https://www.legislation.gov.uk/ukpga/2004/34
• Landlord and Tenant Act 1985. Available from: https://www.legislation.gov.uk/ukpga/1985/70
• Tenant Fees Act 2019. Available from: https://www.legislation.gov.uk/ukpga/2019/4
• Renters' Rights Act 2025. Available from: https://www.legislation.gov.uk/ukpga/2025/26
• Protection from Eviction Act 1977. Available from: https://www.legislation.gov.uk/ukpga/1977/43
• GOV.UK (2025) Guide to the Renters' Rights Act.
https://www.gov.uk/government/publications/guide-to-the-renters-rights-act
• Citizens Advice (n.d.) Housing. https://www.citizensadvice.org.uk/housing/
• Shelter England (2023) Legal resources.
https://england.shelter.org.uk/professional_resources/legal
• TensorFlow Documentation. https://www.tensorflow.org/api_docs
• spaCy NLP Documentation. https://spacy.io/api