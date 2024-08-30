FROM python:3.12

WORKDIR /chatbot-llamaindex

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6333

CMD ["python", "main.py"]