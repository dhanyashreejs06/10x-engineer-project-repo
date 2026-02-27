# Step 1: Base image - official Python 3.11 lightweight version
FROM python:3.11-slim

# Step 2: Set working directory inside the container
WORKDIR /app

# Step 3: Copy requirements first (Docker caching trick - only reinstalls if requirements change)
COPY requirements.txt .

# Step 4: Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the application code
COPY . .

# Step 6: Expose port 8000 (the port our app runs on)
EXPOSE 8000

# Step 7: Command to start the app when container launches
# 0.0.0.0 = accept connections from outside the container
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]