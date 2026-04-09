# ─────────────────────────────────────────────────────────────────────────────
# Gunicorn production configuration
# See: https://docs.gunicorn.org/en/stable/settings.html
# ─────────────────────────────────────────────────────────────────────────────
import os
import multiprocessing

# ── Binding ──────────────────────────────────────────────────────────────────
# HOST/PORT are read from environment; Docker exposes 8080 by default.
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"

# ── Workers ───────────────────────────────────────────────────────────────────
# Rule of thumb: (2 × CPU cores) + 1 — capped at 4 for a small classifier.
workers = int(os.environ.get('WORKERS', min((2 * multiprocessing.cpu_count()) + 1, 4)))

# Each worker runs multiple threads for I/O-bound work.
threads = int(os.environ.get('THREADS', 4))

# Worker class — sync is fine; model inference is CPU-bound and fast.
worker_class = "sync"

# ── Timeouts ─────────────────────────────────────────────────────────────────
timeout          = 30   # Kill workers that hang for > 30 s
keepalive        = 5    # Reuse HTTP connections for up to 5 s
graceful_timeout = 10   # Seconds to finish in-flight requests on SIGTERM

# ── Logging ──────────────────────────────────────────────────────────────────
# Log to stdout/stderr so Docker captures them with `docker logs`
accesslog  = "-"
errorlog   = "-"
loglevel   = os.environ.get('LOG_LEVEL', 'info')
access_log_format = '%(h)s "%(r)s" %(s)s %(b)s %(D)sµs'

# ── Process naming ────────────────────────────────────────────────────────────
proc_name = "spamshield"

# ── Security ─────────────────────────────────────────────────────────────────
# Disable the Server header — don't advertise Gunicorn version.
forwarded_allow_ips = "*"   # Trust X-Forwarded-For from any upstream proxy
