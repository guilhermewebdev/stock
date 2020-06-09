FROM python
ENV PYTHONUNBUFFERED 1
WORKDIR /code
ADD requirements.txt /code
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
