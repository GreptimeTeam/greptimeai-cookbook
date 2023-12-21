# docker build -t greptime/greptimeai-openai-example:latest .
FROM python:3.11.6-slim
WORKDIR /app

COPY ./pyproject.toml ./src/ ./
RUN pip install .
EXPOSE 8001

CMD ["python", "openai_example/app.py"]
