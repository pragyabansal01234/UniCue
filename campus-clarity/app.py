from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, Message
from ai_processor import process_messages, detect_duplicates_and_conflicts

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()   # pehli baar chalane pe database.db aur table ban jayegi


# ---------- CREATE ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        raw_text = request.form.get("messages", "")

        if raw_text.strip():
            # Step 1: AI se process karwao
            processed = process_messages(raw_text)

            # Step 2: duplicates/conflicts detect karo
            final_items = detect_duplicates_and_conflicts(processed)

            # Step 3: database mein save karo
            for item in final_items:
                msg = Message(
                    raw_text=item.get("raw_text", ""),
                    title=item.get("title", "Untitled"),
                    category=item.get("category", "general"),
                    event_date=item.get("event_date"),
                    urgency=item.get("urgency", "soon"),
                    seats_limited=item.get("seats_limited", False),
                    is_cancelled=item.get("is_cancelled", False),
                    missing_info=item.get("missing_info", False),
                    duplicate_count=item.get("duplicate_count", 1),
                    has_conflict=item.get("has_conflict", False),
                    conflict_note=item.get("conflict_note", ""),
                )
                db.session.add(msg)
            db.session.commit()

            return redirect(url_for("dashboard"))

    return render_template("index.html")


# ---------- READ ----------
@app.route("/dashboard")
def dashboard():
    all_messages = Message.query.filter(Message.status != "ignored").all()

    now_list = [m for m in all_messages if m.urgency == "now" and not m.is_cancelled]
    soon_list = [m for m in all_messages if m.urgency == "soon" and not m.is_cancelled]
    later_list = [m for m in all_messages if m.urgency == "later" and not m.is_cancelled]
    uncertain_list = [m for m in all_messages if m.missing_info or m.is_cancelled]

    stats = {
        "total": len(all_messages),
        "duplicates_merged": sum(m.duplicate_count - 1 for m in all_messages if m.duplicate_count > 1),
        "priorities": len(now_list) + len(soon_list),
    }

    return render_template(
        "dashboard.html",
        now_list=now_list,
        soon_list=soon_list,
        later_list=later_list,
        uncertain_list=uncertain_list,
        stats=stats,
    )


# ---------- UPDATE ----------
@app.route("/edit/<int:message_id>", methods=["GET", "POST"])
def edit(message_id):
    msg = Message.query.get_or_404(message_id)

    if request.method == "POST":
        msg.title = request.form.get("title", msg.title)
        msg.status = request.form.get("status", msg.status)
        msg.urgency = request.form.get("urgency", msg.urgency)
        msg.event_date = request.form.get("event_date", msg.event_date)
        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("edit.html", msg=msg)


# ---------- DELETE ----------
@app.route("/delete/<int:message_id>", methods=["POST"])
def delete(message_id):
    msg = Message.query.get_or_404(message_id)
    db.session.delete(msg)
    db.session.commit()
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
