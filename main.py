from abilities import key_value_storage, llm_prompt
from flask import request
import logging
from flask import Flask, render_template, jsonify
from gunicorn.app.base import BaseApplication
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')

@app.route("/", methods=["GET"])
def home_route():
    return render_template("home.html")

@app.route("/generate_event_idea", methods=["GET"])
def generate_event_idea_route():
    return render_template("generate_event_idea.html")

@app.route("/events", methods=["GET"])
def get_events():
    events = key_value_storage("retrieve", "events", "", "")
    if events["upstream_service_result_code"] == 200:
        return jsonify(events["kv_pairs"])
    return jsonify([])

@app.route("/add_event", methods=["GET", "POST"])
def add_event_route():
    if request.method == "POST":
        event_name = request.form["event_name"]
        event_date = request.form["event_date"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        # Save event details to storage
        event_details = {
            "event_name": event_name,
            "event_date": event_date,
            "start_time": start_time,
            "end_time": end_time
        }
        key_value_storage("store", "events", event_name, str(event_details))
        return f"Event '{event_name}' on {event_date} from {start_time} to {end_time} added successfully!"
    return render_template("add_event.html")

@app.route("/delete_event", methods=["POST"])
def delete_event():
    event_name = request.json["event_name"]
    key_value_storage("delete", "events", event_name, "")
    return f"Event '{event_name}' deleted successfully!"

@app.route("/generate_event_idea", methods=["GET"])
def generate_event_idea():
    prompt = "Generate a unique and interesting event idea."
    idea = llm_prompt(prompt, model="gpt-4-1106-preview", temperature=0.7)
    return idea

class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        # Apply configuration to Gunicorn
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == "__main__":
    options = {
        "bind": "0.0.0.0:8080",
        "workers": 4,
        "loglevel": "info",
        "accesslog": "-"
    }
    StandaloneApplication(app, options).run()
    StandaloneApplication(app, options).run()