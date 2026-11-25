
const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const chatArea = document.getElementById("chatArea");
const sendButton = document.getElementById("sendButton");
const inputSection = document.getElementById("inputSection");
const pageTitle = document.getElementById("pageTitle");
const pageSubtitle = document.getElementById("pageSubtitle");

let isWaiting = false;
let currentTopic = null;

// Separate conversation histories for topics
const conversations = {
    Admissions: [],
    Courses: [],
    Placements: [],
    Fees: [],
    Hostel: [],
    Library: []
};

const topicPrompts = {
    Admissions: "Tell me about admissions",
    Courses: "What courses are offered?",
    Placements: "Tell me about placements",
    Fees: "What are the college fees?",
    Hostel: "Tell me about hostel facilities",
    Library: "What library facilities are available?"
};

const supportedLanguages = [
    { code: "te", name: "Telugu" },
    { code: "hi", name: "Hindi" },
    { code: "ta", name: "Tamil" },
    { code: "kn", name: "Kannada" },
    { code: "ml", name: "Malayalam" },
    { code: "bn", name: "Bengali" },
    { code: "mr", name: "Marathi" },
    { code: "gu", name: "Gujarati" },
    { code: "pa", name: "Punjabi" },
    { code: "ur", name: "Urdu" },
    { code: "es", name: "Spanish" },
    { code: "fr", name: "French" },
    { code: "de", name: "German" },
    { code: "ja", name: "Japanese" },
    { code: "ko", name: "Korean" },
    { code: "zh-cn", name: "Chinese" },
    { code: "ar", name: "Arabic" },
    { code: "ru", name: "Russian" },
    { code: "id", name: "Indonesian" },
    { code: "vi", name: "Vietnamese" }
];


// ----------------------------------------
// HOME / WELCOME PAGE
// ----------------------------------------

function goHome() {

    if (isWaiting) return;

    currentTopic = null;

    chatArea.innerHTML = `
        <div class="welcome-screen" id="welcomeScreen">

            <div class="welcome-icon">✦</div>

            <h1>Hey there! 👋</h1>

            <h2>How can I help you today?</h2>

            <p>
                Explore your college information.
                Select a topic to start a conversation.
            </p>

            <div class="suggestion-grid">

                <button class="topic-card" onclick="openTopic('Admissions')">
                    <span>🎓</span>
                    <strong>Admissions</strong>
                    <small>Learn about the admission process</small>
                </button>

                <button class="topic-card" onclick="openTopic('Courses')">
                    <span>📚</span>
                    <strong>Courses</strong>
                    <small>Explore available programmes</small>
                </button>

                <button class="topic-card" onclick="openTopic('Placements')">
                    <span>💼</span>
                    <strong>Placements</strong>
                    <small>Discover career opportunities</small>
                </button>

                <button class="topic-card" onclick="openTopic('Fees')">
                    <span>💳</span>
                    <strong>Fee Details</strong>
                    <small>Find fee-related information</small>
                </button>

            </div>

        </div>
    `;

    inputSection.style.display = "none";

    pageTitle.textContent = "College Assistant";
    pageSubtitle.textContent = "Your intelligent campus companion";

    chatArea.classList.remove("conversation-mode");
}


// ----------------------------------------
// OPEN A TOPIC
// ----------------------------------------

function openTopic(topic) {

    if (isWaiting) return;

    currentTopic = topic;

    pageTitle.textContent = topic;
    pageSubtitle.textContent = "Your " + topic.toLowerCase() + " assistant";

    inputSection.style.display = "block";

    chatArea.innerHTML = "";
    chatArea.classList.add("conversation-mode");

    // Restore this topic's conversation
    const history = conversations[topic];

    history.forEach(item => {
        addMessage(item.text, item.sender);
    });

    // Start a fresh topic conversation if empty
    if (history.length === 0) {

        sendMessage(topicPrompts[topic]);
    }

    userInput.focus();
}


// ----------------------------------------
// ADD MESSAGE
// ----------------------------------------

function addMessage(message, sender) {

    const wrapper = document.createElement("div");
    wrapper.className = `message ${sender}`;

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = sender === "bot" ? "C" : "U";

    const body = document.createElement("div");
    body.className = "message-body";

    const name = document.createElement("div");
    name.className = "message-name";
    name.textContent = sender === "bot" ? "CampusAI" : "You";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.textContent = message;

    body.appendChild(name);
    body.appendChild(bubble);

    wrapper.appendChild(avatar);
    wrapper.appendChild(body);

    if (sender === "bot") {

        const actions = document.createElement("div");
        actions.className = "message-actions";

        // COPY

        const copyButton = document.createElement("button");
        copyButton.className = "message-action";
        copyButton.type = "button";
        copyButton.textContent = "📋 Copy";

        copyButton.addEventListener("click", async () => {

            try {

                await navigator.clipboard.writeText(message);
                copyButton.textContent = "✓ Copied";

                setTimeout(() => {
                    copyButton.textContent = "📋 Copy";
                }, 1500);

            } catch (error) {

                copyButton.textContent = "Copy failed";
            }
        });

        // TRANSLATE

        const translateButton = document.createElement("button");
        translateButton.className = "message-action";
        translateButton.type = "button";
        translateButton.textContent = "🌐 Translate";

        const translationArea = document.createElement("div");
        translationArea.className = "translation-area";

        translateButton.addEventListener("click", () => {

            if (translationArea.querySelector("select")) {
                translationArea.innerHTML = "";
                return;
            }

            translationArea.innerHTML = "";

            const selector = document.createElement("select");
            selector.className = "language-select";

            const defaultOption = document.createElement("option");
            defaultOption.value = "";
            defaultOption.textContent = "Choose a language";

            selector.appendChild(defaultOption);

            supportedLanguages.forEach(language => {

                const option = document.createElement("option");
                option.value = language.code;
                option.textContent = language.name;

                selector.appendChild(option);
            });

            const translateNow = document.createElement("button");
            translateNow.className = "message-action";
            translateNow.type = "button";
            translateNow.textContent = "Translate";

            const translatedText = document.createElement("div");
            translatedText.className = "translated-text";

            translateNow.addEventListener("click", async () => {

                if (!selector.value) {

                    translatedText.textContent =
                        "Please select a language.";

                    return;
                }

                translateNow.disabled = true;
                translateNow.textContent = "Translating...";

                try {

                    const response = await fetch("/translate", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            text: message,
                            target_language: selector.value
                        })
                    });

                    const data = await response.json();

                    if (!response.ok) {
                        throw new Error(data.error || "Translation failed.");
                    }

                    translatedText.textContent =
                        data.language + ": " + data.translation;

                } catch (error) {

                    translatedText.textContent =
                        error.message || "Translation failed.";

                } finally {

                    translateNow.disabled = false;
                    translateNow.textContent = "Translate";
                }
            });

            translationArea.appendChild(selector);
            translationArea.appendChild(translateNow);
            translationArea.appendChild(translatedText);
        });

        actions.appendChild(copyButton);
        actions.appendChild(translateButton);

        body.appendChild(actions);
        body.appendChild(translationArea);
    }

    wrapper.appendChild(body);

    chatArea.appendChild(wrapper);

    chatArea.scrollTop = chatArea.scrollHeight;
}


// ----------------------------------------
// TYPING INDICATOR
// ----------------------------------------

function showTypingIndicator() {

    const typing = document.createElement("div");
    typing.className = "message bot typing-indicator";
    typing.id = "typingIndicator";

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = "C";

    const text = document.createElement("div");
    text.className = "typing-text";
    text.textContent = "CampusAI is thinking...";

    typing.appendChild(avatar);
    typing.appendChild(text);

    chatArea.appendChild(typing);

    chatArea.scrollTop = chatArea.scrollHeight;
}


function removeTypingIndicator() {

    const typing = document.getElementById("typingIndicator");

    if (typing) {
        typing.remove();
    }
}


// ----------------------------------------
// SEND MESSAGE
// ----------------------------------------

async function sendMessage(message) {

    if (!message || isWaiting || !currentTopic) return;

    isWaiting = true;
    sendButton.disabled = true;

    conversations[currentTopic].push({
        text: message,
        sender: "user"
    });

    addMessage(message, "user");

    userInput.value = "";

    showTypingIndicator();

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.response || "Unable to get a response.");
        }

        removeTypingIndicator();

        conversations[currentTopic].push({
            text: data.response,
            sender: "bot"
        });

        addMessage(data.response, "bot");

    } catch (error) {

        removeTypingIndicator();

        const errorMessage =
            error.message || "Something went wrong. Please try again.";

        conversations[currentTopic].push({
            text: errorMessage,
            sender: "bot"
        });

        addMessage(errorMessage, "bot");

        console.error(error);

    } finally {

        isWaiting = false;
        sendButton.disabled = false;
        userInput.focus();
    }
}


// ----------------------------------------
// FORM SUBMISSION
// ----------------------------------------

chatForm.addEventListener("submit", function(event) {

    event.preventDefault();

    const message = userInput.value.trim();

    if (message) {
        sendMessage(message);
    }
});


// ----------------------------------------
// NEW CHAT
// ----------------------------------------

window.goHome = goHome;
window.openTopic = openTopic;
