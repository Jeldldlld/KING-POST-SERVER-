# Helpers
# ------------------------
def create_task(post_id, hater_name, token, messages, delay):
    task_id = str(uuid.uuid4())
    stop_event = threading.Event()
    task = {
        "thread": None,
        "stop_event": stop_event,
        "owner_token": token,
        "post_id": post_id,
        "hater_name": hater_name,
        "messages": messages,
        "delay": delay,
        "logs": [],
        "status": "running",
        "created": time.time(),
        "last_run": None,
    }
    # start thread
    t = threading.Thread(target=comment_worker, args=(task_id,), daemon=True)
    task["thread"] = t
    tasks[task_id] = task
    t.start()
    return task_id

# ------------------------
# Routes
# ------------------------
@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/send", methods=["POST"])
def send_message():
    try:
        post_id = request.form.get("postId", "").strip()
        hater_name = request.form.get("haterName", "").strip()
        token = request.form.get("token", "").strip()
        messages_text = request.form.get("messages", "").strip()
        delay = int(request.form.get("delay", 20))

        if not post_id or not token or not messages_text:
            return jsonify({"success": False, "error": "postId, token and messages are required."})

        if delay < 20:
            return jsonify({"success": False, "error": "Delay must be at least 20 seconds."})

        messages = [m.strip() for m in messages_text.splitlines() if m.strip()]
        if not messages:
            return jsonify({"success": False, "error": "No valid messages found."})

        # create and start task
        task_id = create_task(post_id, hater_name, token, messages, delay)
        return jsonify({"success": True, "task_id": task_id})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/stop", methods=["POST"])
def stop_task():
    try:
        task_id = request.form.get("task_id", "").strip()
        token = request.form.get("token", "").strip()

        if not task_id or not token:
            return jsonify({"success": False, "error": "task_id and token are required."})

        task = tasks.get(task_id)
        if not task:
            return jsonify({"success": False, "error": "Task not found."})

        # verify owner
        if task["owner_token"] != token:
            return jsonify({"success": False, "error": "You are not the owner of this task."})

        # signal stop
        task["stop_event"].set()
        task["logs"].append(f"[{time.strftime('%Y-%m-%d %I:%M:%S %p')}] Stop requested by owner.")
        task["status"] = "stopping"
        return jsonify({"success": True, "message": "Stop signal sent."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/my_tasks")
def my_tasks():
    token = request.args.get("token", "").strip()
    if not token:
        return jsonify({"success": False, "error": "token required", "tasks": []})
    res = []
    for tid, t in tasks.items():
        if t["owner_token"] == token:
            res.append({
                "task_id": tid,
                "post_id": t["post_id"],
                "msg_count": len(t["messages"]),
                "delay": t["delay"],
                "status": t.get("status", "unknown"),
                "created": t.get("created")
            })
    return jsonify({"success": True, "tasks": res})

@app.route("/status/<task_id>")
def task_status(task_id):
    token = request.args.get("token", "").strip()
    if not token:
        return jsonify({"success": False, "error": "token required"})
    t = tasks.get(task_id)
    if not t:
        return jsonify({"success": False, "error": "task not found"})
    if t["owner_token"] != token:
        return jsonify({"success": False, "error": "Not owner of task"})
    return jsonify({"success": True, "logs": t["logs"], "status": t.get("status", "unknown")})
