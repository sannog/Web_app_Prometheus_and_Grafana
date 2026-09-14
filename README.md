# Web_app_Prometheus_and_Grafana
Monitor Web Application using Prometheus, Grafana, ELK stack, and more

# This Project:
This project creates a complete monitoring system for a Flask web application. It includes:

Flask App: A simple web application that we will monitor
Prometheus: Collects and stores metrics (numbers about your app)
Grafana: Creates beautiful charts and dashboards
ELK Stack: Collects and analyzes logs (text messages from your app)
Alertmanager: Sends alerts when something goes wrong

# Learn:
How to collect metrics from a web application
How to create beautiful dashboards
How to analyze logs
How to set up alerts
How to monitor application performance
How to troubleshoot issues

# Works like:
Flask App → Prometheus → Grafana (Charts)
    ↓
Filebeat → Logstash → Elasticsearch → Kibana (Logs)
    ↓
Alertmanager → Slack/PagerDuty (Alerts)

# Requirments:
Docker - Download from https://docker.com
Docker Compose - Usually comes with Docker
At least 8GB RAM on your computer
These ports should be free: 3000, 5000, 5601, 9090, 9093, 9200

# Implementation guid:

Step 1: Download and Setup
1. Download this project
git clone https://github.com/auspicious27/metrics.git
cd metrics

2. Run the setup script:
./setup.sh

Expected output:
🚀 Setting up Monitoring Stack for Windows/Mac/Linux...
================================
Universal Monitoring Stack Setup
================================
This script works on Windows, Mac, and Linux

[INFO] Detected OS: mac
[INFO] Docker is installed
Docker version 28.3.0, build 38b7060a21
[INFO] Docker Compose is installed
docker-compose version 1.29.2
[INFO] Docker is running
[INFO] Directories created successfully
[INFO] Port 3000 is available
[INFO] Port 5000 is available
[INFO] Port 5601 is available
[INFO] Port 9090 is available
[INFO] Port 9093 is available
[INFO] Port 9200 is available

