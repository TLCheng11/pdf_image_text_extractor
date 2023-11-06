FROM python:3.11-slim

# create group and user
RUN adduser --system --group worker

# set ownership and permissions
# RUN chown -R worker:worker .

# Make sure we use the virtualenv:
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Add current working directory to python path
ENV PYTHONPATH="/home/worker/app"

WORKDIR /home/worker/app

RUN pip install --upgrade pip

COPY --chown=worker:worker requirements.txt .
RUN pip install -r requirements.txt

# Install dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=worker:worker . .

# # Expose port 8601
# EXPOSE 8601

# # Specify the command to run your Streamlit app on port 8601
# ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8601"]

USER worker