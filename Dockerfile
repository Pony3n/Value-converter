FROM python:3.10

RUN apt-get update && apt-get install -y nano vim lsof\
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/

RUN echo "Installing Python dependencies" && \
    pip install --no-cache-dir -r requirements.txt && \
    echo "Python dependencies installed successfully"

RUN echo "Copying source code"

COPY . /app/

RUN echo "Source code copied successfully"

EXPOSE 8000

RUN echo "Source code copied successfully! Starting app"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]