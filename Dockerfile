FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

EXPOSE 5001

# Set the default command to run the Flask app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:create_app()"]