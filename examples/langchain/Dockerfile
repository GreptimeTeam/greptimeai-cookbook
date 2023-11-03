FROM python:3.11.6-slim
WORKDIR /app

COPY ./pyproject.toml .
RUN pip install . -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY ./src/langchain/ .
EXPOSE 8000

CMD ["python", "app.py"]