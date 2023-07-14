# First stage: Build
FROM python:3.11.4 as builder

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Second stage: Runtime
FROM python:3.11.4

# Set the working directory in the container to /app
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

# Copy application files
COPY . .

# Create a new directory for data persistence
RUN mkdir -p /app/articles

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    wget unzip tzdata \
    && rm -rf /var/lib/apt/lists/*

# Set timezone
RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/ \
    && unzip ~/chromedriver_linux64.zip -d ~/ \
    && rm ~/chromedriver_linux64.zip \
    && mv -f ~/chromedriver /usr/local/bin/chromedriver \
    && chown root:root /usr/local/bin/chromedriver \
    && chmod 0755 /usr/local/bin/chromedriver

# Define environment variable
ENV NAME GPT-SentimentTrader
ENV IN_DOCKER_CONTAINER=True
ENV PYTHONPATH /app

# Download NLTK datasets
RUN python -c "import nltk; nltk.download('punkt')"
RUN python -c "import nltk; nltk.download('stopwords')"
RUN python -c "import nltk; nltk.download('averaged_perceptron_tagger')"
RUN python -c "import nltk; nltk.download('wordnet')"

# Run main.py when the container launches - unbuffered
#CMD ["python", "-u", "main.py"]

# Run app.py when the container launches - unbuffered
CMD ["python", "-u", "/app/app.py"]
