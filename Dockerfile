FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -e .
CMD ["uv", "run", "services"] 