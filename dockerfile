# Pull base image
FROM python:3.13.1

# Set environment variables
#ENV PIP_DISABLE_PIP_VERSION_CHECK=1
#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /crm

# Install dependencies

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .




EXPOSE 8000


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "inquiry_dashboard.wsgi:application", "--workers", "3"]