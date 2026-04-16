FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir pandas pymongo
COPY . .
CMD ["python", "migration.py"]
