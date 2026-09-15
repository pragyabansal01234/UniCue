import json
import google.generativeai as genai
from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

SYSTEM_PROMPT = """Tum ek campus announcement assistant ho. Tumhe raw messages diye jayenge
(WhatsApp groups, emails, notices se). Tumhara kaam hai in messages ko samajh kar
structured JSON format mein nikalna.

Har message ke liye yeh fields nikalo:
- title: chhota sa title (max 8 words)
- category: "deadline" ya "event" ya "cancellation" ya "opportunity" ya "general"
- event_date: date agar mention hai (jaise "16 Sept"), warna null
- urgency: "now" (aaj/kal ka kaam), "soon" (is hafte), "later" (aage ka)
- seats_limited: true agar limited seats ka zikr hai, warna false
- is_cancelled: true agar yeh event/activity cancel ho gaya hai
- missing_info: true agar message mein zaroori info (jaise date) missing hai

IMPORTANT RULES:
- Kabhi bhi missing information ko khud se mat banao (invent mat karo)
- Agar date clear nahi hai, event_date ko null rakho aur missing_info ko true karo
- Sirf jo message mein likha hai wahi use karo

Sirf valid JSON array return karo, kuch aur text nahi (no markdown fences). Format:
[
  {"title": "...", "category": "...", "event_date": "...", "urgency": "...", "seats_limited": false, "is_cancelled": false, "missing_info": false}
]
"""

model = genai.GenerativeModel(
    model_name="gemini-3.6-flash",
    system_instruction=SYSTEM_PROMPT,
)


def process_messages(raw_text):
    """
    raw_text: ek bada text block jisme multiple messages newline se separated hain
    Return: list of dicts, har dict ek processed message hai
    """
    lines = [line.strip() for line in raw_text.split("\n") if len(line.strip()) > 5]

    if not lines:
        return []

    numbered_messages = "\n".join(f"{i+1}. {line}" for i, line in enumerate(lines))

    user_prompt = f"""Yeh raha messages ki list, har ek ko process karo:

{numbered_messages}

Har message ke liye ek JSON object banao, order same rakhna jo upar diya hai."""

    response = model.generate_content(
        user_prompt,
        generation_config={"response_mime_type": "application/json"},
    )

    raw_response = response.text.strip()

    if raw_response.startswith("```"):
        raw_response = raw_response.split("```")[1]
        if raw_response.startswith("json"):
            raw_response = raw_response[4:]

    try:
        parsed_results = json.loads(raw_response)
    except json.JSONDecodeError:
        parsed_results = []

    final_results = []
    for i, item in enumerate(parsed_results):
        if i < len(lines):
            item["raw_text"] = lines[i]
        else:
            item["raw_text"] = ""
        final_results.append(item)

    return final_results


def detect_duplicates_and_conflicts(processed_items):
    """
    Simple rule-based dedupe aur conflict detection
    (AI se alag - yeh Python logic hai, taaki predictable rahe)
    """
    groups = []

    for item in processed_items:
        title_words = set(item.get("title", "").lower().split())
        matched_group = None

        for group in groups:
            existing_words = set(group["title"].lower().split())
            overlap = len(title_words & existing_words)
            if overlap >= 2:
                matched_group = group
                break

        if matched_group:
            matched_group["duplicate_count"] += 1
            if item.get("is_cancelled"):
                matched_group["is_cancelled"] = True
            if item.get("event_date"):
                matched_group["event_date"] = item["event_date"]
        else:
            item["duplicate_count"] = 1
            groups.append(item)

    date_buckets = {}
    for group in groups:
        date = group.get("event_date")
        if date and not group.get("is_cancelled"):
            date_buckets.setdefault(date, []).append(group)

    for date, items in date_buckets.items():
        if len(items) > 1:
            for item in items:
                others = [x["title"] for x in items if x is not item]
                item["has_conflict"] = True
                item["conflict_note"] = "Clashes with: " + ", ".join(others)

    return groups
