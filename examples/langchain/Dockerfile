FROM python:3.11
WORKDIR /app

COPY ./pyproject.toml ./src/ ./
RUN pip install .
EXPOSE 8000

CMD ["python", "langchain_example/app.py"]
