# 🛡️ Spam Shield — AI-Powered SMS & Email Spam Classifier

> A sleek Flask web application that classifies SMS and email messages as **Spam** or **Not Spam** using a Multinomial Naïve Bayes model trained on the UCI SMS Spam Collection dataset.

---

## 📸 Features

- 🔍 **Instant classification** — results in milliseconds
- 📊 **Confidence score** with animated progress bar
- 💡 **Example messages** pre-loaded for quick testing
- 🧹 **Character counter** and clear button
- ⌨️ **Keyboard shortcut** — `Ctrl/Cmd + Enter` to analyse
- 🌑 **Premium dark UI** — glassmorphism, animated orbs, smooth micro-animations
- 📱 **Fully responsive** — works on mobile, tablet, and desktop
- ⚡ **AJAX-powered** — no full-page reload on analysis

---

## 🧠 How It Works

```
Raw text
   │
   ▼
Lowercase → Tokenise (NLTK punkt) → Remove stopwords & punctuation → Porter Stemmer
   │
   ▼
TF-IDF Vectorizer  →  Multinomial Naïve Bayes  →  SPAM / NOT SPAM
```

| Component | Detail |
|---|---|
| Dataset | UCI SMS Spam Collection (5 572 messages → 5 169 after deduplication) |
| Vectorizer | `TfidfVectorizer` (saved as `vectorizer.pkl`) |
| Classifier | `MultinomialNB` (saved as `model.pkl`) |
| Pre-processing | lowercase, tokenise, alphanumeric filter, stopword removal, PorterStemmer |
| Class encoding | `0 = ham (not spam)`, `1 = spam` |

---

## 📂 Project Structure

```
Flask Email Spam/
├── app.py                  # Flask backend + prediction logic
├── requirements.txt        # Python dependencies
├── model.pkl               # Pre-trained Naïve Bayes classifier
├── vectorizer.pkl          # Pre-trained TF-IDF vectorizer
├── spam_data.csv           # Raw dataset (UCI SMS Spam Collection)
├── sms_spam_detection.ipynb  # Jupyter notebook (EDA + model training)
├── Spam_Messages.txt       # Sample spam messages for manual testing
├── templates/
│   └── index.html          # Jinja2 HTML template
└── static/
    └── style.css           # Custom CSS (dark glassmorphic design)
```

---

## 🚀 Quick Start

### 1 — Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/Flask-Email-Spam.git
cd "Flask Email Spam"
```

### 2 — Create & activate a virtual environment

```bash
python3 -m venv demo
source demo/bin/activate        # macOS / Linux
# demo\Scripts\activate         # Windows
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** The very first run automatically downloads NLTK's `punkt` tokenizer and `stopwords` corpus. This is a one-time operation (~3 MB).

### 4 — Run the app

```bash
python app.py
```

Open your browser and navigate to **[http://localhost:8080](http://localhost:8080)**.

---

## 🔌 API Reference

The app exposes a JSON endpoint you can call from any HTTP client:

### `POST /predict`

**Request**

```http
POST /predict
Content-Type: application/json

{
  "message": "Congratulations! You've won a FREE gift card!"
}
```

**Response (success)**

```json
{
  "success": true,
  "prediction": 1,
  "label": "SPAM",
  "confidence": 99.7,
  "message": "Congratulations! You've won a FREE gift card!"
}
```

**Response (error)**

```json
{
  "success": false,
  "error": "Please enter a message before analysing."
}
```

| Field | Type | Description |
|---|---|---|
| `prediction` | `int` | `1` = spam, `0` = not spam |
| `label` | `string` | `"SPAM"` or `"NOT SPAM"` |
| `confidence` | `float \| null` | Model's probability score (0–100 %) |
| `message` | `string` | The original input text |

---

## 🧪 Testing with Sample Messages

A set of real-world test messages (including edge cases the model struggles with) is available in [`Spam_Messages.txt`](Spam_Messages.txt).

**Spam examples the model correctly catches:**
- *"Congratulations! You've won a FREE ₹10,000 Amazon Gift Card! Click here…"*
- *"Your credit card has been temporarily blocked. Click to verify immediately"*

**Edge cases (borderline spam):**
- *"Upgrade your mobile plan & get unlimited data."*
- *"Get instant loan up to ₹10,00,000 without documents."*

---

## ⚙️ Configuration

| Env variable | Default | Description |
|---|---|---|
| `PORT` | `8080` | Port the Flask server listens on |

```bash
PORT=3000 python app.py
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| Flask | 3.0.0 | Web framework |
| scikit-learn | 1.6.1 | TF-IDF vectorizer & Naïve Bayes model |
| NLTK | 3.8.1 | Tokenisation, stopwords, stemming |
| NumPy | 1.26.2 | Numeric operations |
| pandas | 2.1.3 | Data manipulation (notebook only) |

---

## 🛠️ Re-training the Model

Open and run all cells in [`sms_spam_detection.ipynb`](sms_spam_detection.ipynb). The notebook will:

1. Load and clean `spam_data.csv`
2. Perform EDA (pie charts, word-length distributions, word clouds)
3. Pre-process text using `transform_text()`
4. Vectorise with TF-IDF
5. Evaluate multiple classifiers (Naïve Bayes, SVM, Random Forest, …)
6. Export the best model as `model.pkl` + `vectorizer.pkl`

---

## 📝 License

This project is released under the **MIT License** — free to use, modify, and distribute.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

<p align="center">Built with ❤️ using Flask · NLTK · Scikit-Learn</p>
