# Official Python runtime as a parent image
FROM python:3.11.4

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Create a new directory for data persistence
RUN mkdir -p /app/articles

# Install needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    wget unzip \
    && rm -rf /var/lib/apt/lists/*

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

# Run main.py when the container launches
CMD ["python", "main.py"]

# Health check to check if container is running as expected
HEALTHCHECK --interval=5m --timeout=3s CMD python -c 'print("alive")' || exit 1
