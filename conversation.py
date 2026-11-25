
import re
from chatbot import get_response


def normalize(message):
    message = message.lower().strip()
    message = re.sub(r"[^\w\s']", " ", message)
    message = re.sub(r"\s+", " ", message)
    return message.strip()


def get_conversation_response(message):

    text = normalize(message)

    # Greetings
    if text in [
        "hi", "hello", "hey", "hii", "heyy",
        "hello there", "hi there", "hey there"
    ]:
        return "Hello! Welcome to CampusAI. How can I help you today?"

    # Time-based greetings
    if any(phrase in text for phrase in [
        "good morning", "good afternoon", "good evening"
    ]):
        if "morning" in text:
            greeting = "Good morning!"
        elif "afternoon" in text:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"

        return f"{greeting} How can I assist you today?"

    # Asking whether CampusAI is available
    if text in [
        "are you there", "are you online",
        "is anyone there", "can you hear me"
    ]:
        return "Yes! I'm here and ready to help you."

    # Identity
    if text in [
        "who are you", "what are you",
        "what is your name", "who am i talking to"
    ]:
        return (
            "I'm CampusAI, your college assistant. "
            "I can help you with admissions, courses, fees, "
            "placements, facilities and student life."
        )

    # What CampusAI can do
    if text in [
        "what can you do", "how can you help me",
        "help me", "what do you know"
    ]:
        return (
            "I can answer questions about X College, including "
            "admissions, courses, fees, scholarships, placements, "
            "hostel facilities, examinations and campus life."
        )

    # Appreciation and positive feedback
    positive_responses = [
        "that's sound good",
        "that sounds good",
        "sounds good",
        "sound good",
        "that's good",
        "that is good",
        "that's great",
        "that is great",
        "great",
        "good",
        "nice",
        "wonderful",
        "perfect",
        "awesome",
        "excellent",
        "cool",
        "interesting",
        "that's amazing",
        "looks good",
        "very good",
        "i like it",
        "i see",
        "got it",
        "understood",
        "makes sense"
    ]

    if text in positive_responses:
        return "Glad you think so! Is there anything else you'd like to know?"

    # Thanks
    if text in [
        "thanks", "thank you", "thank you so much",
        "thanks a lot", "many thanks"
    ]:
        return "You're very welcome! I'm happy to help."

    # Apologies
    if text in [
        "sorry", "i am sorry", "my mistake",
        "never mind", "nevermind"
    ]:
        return "No problem at all! How can I help you?"

    # Acknowledgements
    if text in [
        "ok", "okay", "alright", "all right",
        "fine", "okay then"
    ]:
        return "Alright! Let me know if you need anything else."

    # Yes and no
    if text in ["yes", "yeah", "yep", "sure"]:
        return "Great! What would you like to know?"

    if text in ["no", "nope", "not really"]:
        return "No problem. Let me know whenever you need help."

    # Follow-up confirmation
    if text in [
        "are you sure", "really",
        "is that true", "are you certain"
    ]:
        return (
            "I'm using the information available in the "
            "X College knowledge base. Which detail would "
            "you like me to clarify?"
        )

    # Farewell
    if text in [
        "bye", "goodbye", "see you",
        "see you later", "take care"
    ]:
        return "Goodbye! Have a wonderful day!"

    # Unrecognized conversational messages go to college retrieval.
    return get_response(message)
