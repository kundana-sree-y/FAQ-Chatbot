
import json
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "dataset" / "college_data.json"


# --------------------------------------------------
# LOAD COLLEGE KNOWLEDGE
# --------------------------------------------------

with open(DATA_FILE, "r", encoding="utf-8") as file:
    college_data = json.load(file)


# --------------------------------------------------
# FIELD ALIASES
# Help CampusAI understand different question styles
# --------------------------------------------------

FIELD_ALIASES = {
    "application_start": "admission start date when admissions begin application opening date",
    "application_deadline": "last date admission closing date deadline",
    "eligibility": "admission qualification requirements who can apply",
    "minimum_percentage": "minimum marks percentage eligibility cutoff",
    "entrance_exams": "entrance test exam required admission examination",
    "process": "admission procedure steps how to apply application process",
    "documents": "documents certificates required for admission",
    "intake": "number of seats vacancies available seats capacity",
    "duration": "course duration how many years",
    "tuition_per_year": "tuition fee college fee annual fee per year",
    "admission_fee": "admission charges registration fee",
    "hostel_per_year": "hostel accommodation fee charges",
    "transport_per_year": "bus transport fee charges",
    "scholarships": "scholarship financial assistance fee concession",
    "recruiters": "companies employers recruiters hiring organizations",
    "activities": "training placement preparation interviews aptitude resume",
    "internships": "internship opportunities training",
    "attendance": "attendance percentage requirement rules",
    "results": "exam results marks grades",
    "revaluation": "rechecking recounting examination answer paper",
    "timings": "opening closing working hours schedule",
    "availability": "available offered facilities accommodation",
    "application": "how to apply registration process"
}


# --------------------------------------------------
# CONVERT JSON INTO SEARCHABLE KNOWLEDGE
# --------------------------------------------------

knowledge = []


def add_fact(path, value, context=""):

    if value is None:
        return

    field = path.split(".")[-1] if path else ""

    aliases = FIELD_ALIASES.get(field, "")

    path_text = path.replace(".", " ").replace("_", " ")

    search_text = (
        f"{context} {path_text} {aliases} {value}"
    )

    knowledge.append({
        "path": path,
        "value": value,
        "context": context,
        "search_text": search_text
    })


def build_knowledge(data, path="", context=""):

    if isinstance(data, dict):

        for key, value in data.items():

            new_path = f"{path}.{key}" if path else key

            if isinstance(value, (dict, list)):
                build_knowledge(value, new_path, context)
            else:
                add_fact(new_path, value, context)

    elif isinstance(data, list):

        if all(not isinstance(item, (dict, list)) for item in data):
            add_fact(path, ", ".join(str(item) for item in data), context)

        else:
            for index, item in enumerate(data):

                item_context = context

                if isinstance(item, dict):
                    name = item.get("name", "")
                    short_name = item.get("short_name", "")

                    item_context = (
                        f"{context} {name} {short_name}"
                    ).strip()

                build_knowledge(
                    item,
                    f"{path}.{index}",
                    item_context
                )


build_knowledge(college_data)


# --------------------------------------------------
# CREATE SEARCH ENGINE
# --------------------------------------------------

vectorizer = TfidfVectorizer(
    lowercase=True,
    analyzer="char_wb",
    ngram_range=(2, 5),
    sublinear_tf=True
)

knowledge_vectors = vectorizer.fit_transform(
    [item["search_text"] for item in knowledge]
)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def format_value(value):

    if isinstance(value, list):
        return ", ".join(str(item) for item in value)

    if isinstance(value, dict):
        return "; ".join(
            f"{key.replace('_', ' ').title()}: {format_value(val)}"
            for key, val in value.items()
        )

    return str(value)


def get_fact(field, context=None):

    matches = [
        item for item in knowledge
        if item["path"].split(".")[-1] == field
    ]

    if context:
        context = context.lower()

        relevant = [
            item for item in matches
            if context in item["context"].lower()
            or context in item["path"].lower()
        ]

        if relevant:
            matches = relevant

    return matches


def find_course(message):

    message = message.lower()

    for course in college_data.get("courses", []):

        names = [
            course.get("name", ""),
            course.get("short_name", "")
        ]

        for name in names:
            if name and name.lower() in message:
                return course

    aliases = {
        "computer science": "CSE",
        "computer science engineering": "CSE",
        "artificial intelligence": "AI & ML",
        "machine learning": "AI & ML",
        "electronics": "ECE",
        "electrical": "EEE",
        "mechanical": "ME",
        "civil": "CE"
    }

    for phrase, code in aliases.items():
        if phrase in message:
            for course in college_data.get("courses", []):
                if course.get("short_name") == code:
                    return course

    return None


# --------------------------------------------------
# TARGETED QUESTION ANSWERS
# --------------------------------------------------

def answer_question(message):

    q = message.lower().strip()

    course = find_course(q)

    # Questions about a particular course
    if course and any(word in q for word in [
        "seat", "vacancy", "vacancies", "intake",
        "available", "admission", "possible",
        "course", "branch", "duration"
    ]):

        if any(word in q for word in [
            "seat", "vacancy", "vacancies", "intake", "how many"
        ]):
            return (
                f"{course['name']} ({course['short_name']}) "
                f"has an intake of {course['intake']} seats. "
                f"The course duration is {course['duration']}."
            )

        return (
            f"Yes, {course['name']} ({course['short_name']}) "
            f"is offered at {college_data['college']['name']}. "
            f"It has {course['intake']} seats and a duration of "
            f"{course['duration']}. "
            f"Admission is subject to the eligibility and "
            f"admission process."
        )

    # Admission starting date
    if any(word in q for word in [
        "when", "from when", "starting", "start", "begin"
    ]) and any(word in q for word in ["admission", "apply", "application"]):

        value = college_data["admissions"]["application_start"]
        return f"Applications for the {college_data['admissions']['academic_year']} academic year start in {value}."

    # Admission deadline
    if any(word in q for word in [
        "last date", "deadline", "closing date", "end date"
    ]) and any(word in q for word in ["admission", "apply", "application"]):

        return (
            "The application deadline is "
            + college_data["admissions"]["application_deadline"] + "."
        )

    # Admission documents
    if any(word in q for word in [
        "document", "certificate", "papers"
    ]):
        docs = college_data["admissions"]["documents"]
        return "The required admission documents include:\n" + "\n".join(
            f"• {doc}" for doc in docs
        )

    # Admission process
    if any(word in q for word in [
        "how can i apply", "how to apply", "admission process",
        "procedure", "steps to apply", "how can i get admission"
    ]):
        steps = college_data["admissions"]["process"]
        return "The admission process is:\n" + "\n".join(
            f"{i + 1}. {step}" for i, step in enumerate(steps)
        )

    # Tuition fees
    if any(word in q for word in [
        "tuition", "college fee", "fees", "fee structure"
    ]) and "hostel" not in q and "transport" not in q:

        amount = college_data["fees"]["tuition_per_year"]
        return f"The annual tuition fee is ₹{amount:,}."

    # Hostel fees
    if "hostel" in q and any(word in q for word in ["fee", "fees", "cost", "charge"]):
        amount = college_data["fees"]["hostel_per_year"]
        return f"The annual hostel fee is ₹{amount:,}."

    # Scholarships
    if any(word in q for word in ["scholarship", "financial assistance"]):
        options = college_data["fees"]["scholarships"]
        return "Available scholarship options include:\n" + "\n".join(
            f"• {item}" for item in options
        )

    # General course list
    if any(word in q for word in [
        "what courses", "which courses", "branches",
        "departments", "engineering branches"
    ]):
        return "X College offers these engineering programmes:\n" + "\n".join(
            f"• {item['name']} ({item['short_name']})"
            for item in college_data["courses"]
        )

    # Placement recruiters
    if any(word in q for word in [
        "companies", "recruiters", "which company"
    ]):
        companies = college_data["placements"]["recruiters"]
        return "The sample recruiter list includes:\n" + "\n".join(
            f"• {company}" for company in companies
        )

    return None


# --------------------------------------------------
# MAIN CHATBOT RESPONSE
# --------------------------------------------------

def get_response(message):

    if not message or not message.strip():
        return "Please enter a question."

    message = message.strip()

    # Handle follow-up confirmation
    if message.lower() in ["are you sure", "really", "is that true"]:
        return (
            "I'm using the information available in the X College "
            "knowledge base. Please ask which detail you would like "
            "me to clarify."
        )

    # First try specific question handling
    direct_answer = answer_question(message)

    if direct_answer:
        return direct_answer

    # Search all available college information
    question_vector = vectorizer.transform([message])

    scores = cosine_similarity(
        question_vector,
        knowledge_vectors
    )[0]

    best_index = scores.argmax()
    best_score = scores[best_index]

    if best_score < 0.16:
        return (
            "I couldn't find reliable information about that in "
            "the X College knowledge base. Please try another "
            "college-related question."
        )

    best_fact = knowledge[best_index]

    return (
        f"According to the X College information, "
        f"{best_fact['path'].split('.')[-1].replace('_', ' ').title()}: "
        f"{format_value(best_fact['value'])}."
    )


# --------------------------------------------------
# TERMINAL TEST
# --------------------------------------------------

if __name__ == "__main__":

    print("\n================================")
    print("       CampusAI Chatbot")
    print("================================")
    print(f"Knowledge facts loaded: {len(knowledge)}")
    print("Type 'exit' to stop.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower().strip() == "exit":
            break

        print("CampusAI:", get_response(user_input))
        print()
