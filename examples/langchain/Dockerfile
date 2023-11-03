FROM python:3.11.6-slim
WORKDIR /app

COPY ./requirements.lock .
RUN sed '/-e/d' requirements.lock > requirements.txt
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY ./src/langchain/ .

CMD ["python", "app.py"]