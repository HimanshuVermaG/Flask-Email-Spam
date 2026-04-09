import os
import string
import pickle
import nltk
from flask import Flask, render_template, request, jsonify
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# ---------------------------------------------------------------------------
# NLTK bootstrap – download required data silently on first run
# ---------------------------------------------------------------------------
nltk.download('punkt',     quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

# ---------------------------------------------------------------------------
# Text pre-processing  (mirrors the notebook's transform_text function)
# ---------------------------------------------------------------------------
_ps = PorterStemmer()
_stop_words = set(stopwords.words('english'))

def transform_text(text: str) -> str:
    """Lowercase → tokenise → keep alphanumeric → remove stopwords → stem."""
    tokens = nltk.word_tokenize(text.lower())
    cleaned = [
        _ps.stem(tok)
        for tok in tokens
        if tok.isalnum() and tok not in _stop_words and tok not in string.punctuation
    ]
    return " ".join(cleaned)

# ---------------------------------------------------------------------------
# Load artefacts (vectorizer + model)
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.abspath(__file__))

def _load(filename):
    path = os.path.join(ROOT, filename)
    with open(path, 'rb') as f:
        return pickle.load(f)

try:
    tfidf = _load('vectorizer.pkl')
    model = _load('model.pkl')
    MODEL_READY = True
except Exception as exc:
    print(f"[ERROR] Could not load model artefacts: {exc}")
    tfidf = model = None
    MODEL_READY = False

# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Accepts both:
      • application/x-www-form-urlencoded  (regular form POST)
      • application/json                   (fetch/XHR from JS)
    Returns JSON: { prediction, label, confidence, message }
    """
    # --- Parse input --
    if request.is_json:
        data = request.get_json(silent=True) or {}
        text = data.get('message', '').strip()
    else:
        text = request.form.get('message', '').strip()

    # --- Validate --
    if not text:
        return jsonify(success=False, error="Please enter a message before analysing."), 400

    if not MODEL_READY:
        return jsonify(success=False, error="Model artefacts could not be loaded. Check server logs."), 500

    # --- Pipeline --
    processed   = transform_text(text)
    vectorised  = tfidf.transform([processed])
    prediction  = int(model.predict(vectorised)[0])          # 0 = ham, 1 = spam

    # Confidence – use predict_proba if the model supports it
    try:
        proba       = model.predict_proba(vectorised)[0]
        confidence  = round(float(proba[prediction]) * 100, 1)
    except AttributeError:
        confidence  = None   # model doesn't expose probabilities

    label = "SPAM" if prediction == 1 else "NOT SPAM"

    return jsonify(
        success    = True,
        prediction = prediction,
        label      = label,
        confidence = confidence,
        message    = text,
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
