#!/usr/bin/env python3
"""
Simple Flask application for monitoring workshop
Demonstrates metrics collection, logging, and error simulation
"""

import os
import time
import random
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Number of active connections')
ERROR_RATE = Gauge('error_rate', 'Current error rate percentage')

# Application state
active_connections = 0
error_count = 0
total_requests = 0

@app.before_request
def before_request():
    global active_connections
    active_connections += 1
    ACTIVE_CONNECTIONS.set(active_connections)

@app.after_request
def after_request(response):
    global active_connections, error_count, total_requests
    active_connections -= 1
    ACTIVE_CONNECTIONS.set(active_connections)
    
    # Update metrics
    total_requests += 1
    if response.status_code >= 400:
        error_count += 1
    
    error_rate = (error_count / total_requests) * 100 if total_requests > 0 else 0
    ERROR_RATE.set(error_rate)
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown',
        status=response.status_code
    ).inc()
    
    return response

@app.route('/')
def home():
    """Home endpoint"""
    logger.info("Home endpoint accessed")
    return jsonify({
        'message': 'Flask Monitoring Workshop App',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/may-fail')
def may_fail():
    """Endpoint that may fail based on configuration"""
    failure_rate = float(os.getenv('FAILURE_RATE', '0.1'))
    
    # Simulate processing time
    time.sleep(random.uniform(0.1, 0.5))
    
    if random.random() < failure_rate:
        logger.error("Simulated error in may-fail endpoint")
        return jsonify({
            'error': 'Simulated failure',
            'timestamp': datetime.now().isoformat()
        }), 500
    
    logger.info("may-fail endpoint succeeded")
    return jsonify({
        'message': 'Success!',
        'timestamp': datetime.now().isoformat(),
        'failure_rate': failure_rate
    })

@app.route('/slow')
def slow():
    """Endpoint that simulates slow responses"""
    delay = float(os.getenv('SLOW_DELAY', '2.0'))
    time.sleep(delay)
    
    logger.info(f"Slow endpoint completed after {delay}s")
    return jsonify({
        'message': f'Slow response after {delay}s',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/status')
def status():
    """Application status endpoint"""
    return jsonify({
        'active_connections': active_connections,
        'total_requests': total_requests,
        'error_count': error_count,
        'error_rate': (error_count / total_requests) * 100 if total_requests > 0 else 0,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/generate-logs')
def generate_logs():
    """Generate various log levels for testing"""
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    return jsonify({
        'message': 'Generated logs at various levels',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

