# docker build -t greptime/greptimeai-langchain-example:latest .
FROM python:3.11.6-slim
WORKDIR /app

COPY ./pyproject.toml ./src/ ./
RUN pip install .
EXPOSE 8000

CMD ["python", "langchain_example/app.py"]
