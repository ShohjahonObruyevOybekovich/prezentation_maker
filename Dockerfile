FROM python:3.10
WORKDIR app/
COPY . .
RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip install -r req.txt

RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
RUN apt-get update && apt-get install -y libgl1-mesa-glx
ENTRYPOINT ["/app/entrypoint.sh"]