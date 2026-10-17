# FinSight AI - Production Google Cloud Run Dockerfile
# Minimal-Cost, Memory-Optimized, Non-Root Streamlit Container
FROM python:3.11-slim

# Set environment variables for Python & Streamlit
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080 \
    STREAMLIT_SERVER_PORT=8080 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Install minimal OS dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Create unprivileged non-root user for security compliance
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/bash -m appuser

# Copy dependency manifest first for Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application source code
COPY DashBoard /app/DashBoard
COPY lib /app/lib
COPY reports /app/reports

# Create writable data and models cache directories with proper permissions
RUN mkdir -p /app/data /app/models /app/DashBoard/exports && \
    chown -R appuser:appgroup /app

# Switch to non-root execution
USER appuser

# Healthcheck to verify Streamlit responsiveness
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl --fail http://localhost:${PORT}/_stcore/health || exit 1

# Expose default Cloud Run port
EXPOSE 8080

# Launch Streamlit with dynamic $PORT support and graceful SIGTERM handling
CMD ["sh", "-c", "exec streamlit run DashBoard/app.py --server.port=${PORT} --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false"]

