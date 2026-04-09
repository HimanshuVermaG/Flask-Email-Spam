# ─────────────────────────────────────────────────────────────────────────────
# Stage 1 – dependency builder
#   Uses a full Python image to compile any native extensions, then copies
#   only the installed site-packages into the final slim image.
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# System deps needed to compile scientific packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps into an isolated prefix so we can copy them cleanly
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --prefix=/install --no-cache-dir -r requirements.txt

# Pre-download NLTK corpora into the builder layer so the final image doesn't
# need outbound internet access at runtime.
RUN PYTHONPATH=/install/lib/python3.11/site-packages python -c "\
import nltk; \
nltk.download('punkt',     download_dir='/nltk_data', quiet=True); \
nltk.download('punkt_tab', download_dir='/nltk_data', quiet=True); \
nltk.download('stopwords', download_dir='/nltk_data', quiet=True)"


# ─────────────────────────────────────────────────────────────────────────────
# Stage 2 – final runtime image
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

LABEL maintainer="SpamShield"
LABEL description="SMS / Email spam classifier — Flask + Gunicorn"
LABEL version="1.0"

# Non-root user for security
RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy NLTK data from builder
COPY --from=builder /nltk_data /home/app/nltk_data

# Copy application source
COPY app.py            ./
COPY gunicorn.conf.py  ./
COPY model.pkl         ./
COPY vectorizer.pkl    ./
COPY templates/        ./templates/
COPY static/           ./static/

# Tell NLTK where its data lives
ENV NLTK_DATA=/home/app/nltk_data

# Runtime knobs — override with -e at `docker run`
ENV PORT=8080
ENV WORKERS=2
ENV THREADS=4

# Drop privileges
RUN chown -R app:app /app /home/app/nltk_data
USER app

EXPOSE 8080

# Gunicorn is the production WSGI server; never run Flask's dev server in Docker
CMD ["sh", "-c", \
     "gunicorn --config gunicorn.conf.py \
               --bind 0.0.0.0:${PORT} \
               app:app"]
