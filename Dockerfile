FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget libnss3 libgtk-3-0 libxss1 libasound2 libatk1.0-0 \
    libgbm1 libxrandr2 libatk-bridge2.0-0 libxkbcommon0 libpangocairo-1.0-0 \
    libpango-1.0-0 libcairo2 libatspi2.0-0 libdrm2 libxcomposite1 libxdamage1 \
    libxfixes3 libxext6 libxcursor1 libxrender1 libxi6 libxtst6 fonts-liberation \
    libappindicator3-1 libdbusmenu-glib4 libdbusmenu-gtk3-4 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright itself
RUN pip install playwright

# Install Playwright browser dependencies + Chromium
RUN playwright install --with-deps chromium

# Expose port
EXPOSE 8000

# Run server
CMD ["sh", "-c", "uvicorn server.main:app --host 0.0.0.0 --port ${PORT}"]
