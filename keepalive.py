# -*- coding: utf-8 -*-
"""
Simple web server to keep the Discord bot alive with UptimeRobot.
Only needed when running on Replit, not on Render.com.
"""
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    """Home route that UptimeRobot will ping."""
    return "Discord bot is alive!"

def run():
    """Run the Flask app on port 8080."""
    # Use PORT environment variable if available (for Render compatibility)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    """
    Start the server in a separate thread.
    Skip if running on Render.com (RENDER environment variable exists)
    """
    # Don't start the web server if we're on Render
    if os.environ.get('RENDER') == 'true':
        print("Running on Render.com - web server not started")
        return
        
    print("Keep alive server started!")
    t = Thread(target=run)
    t.daemon = True
    t.start()