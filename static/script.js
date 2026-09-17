console.log("script.js loaded successfully");

let thinkingInterval;
let thinkingMessageInterval;

async function askQuestion() {

    console.log("Send button clicked");

    const questionInput = document.getElementById("question");
    const answerElement = document.getElementById("answer");
    const sendButton = document.getElementById("send-button");

    const question = questionInput.value.trim();

    if (question === "") {
        alert("Please enter a question.");
        return;
    }

    sendButton.disabled = true;

    const thinkingMessages = [
        "Reading your notes",
        "Understanding your question",
        "Searching the uploaded PDF",
        "Preparing your answer"
    ];

    let messageIndex = 0;
    let dotCount = 0;

    answerElement.innerHTML = `
        <div class="ai-thinking">

            <div class="thinking-top">

                <div class="animated-robot">
                    🤖
                </div>

                <div>
                    <div class="thinking-title">
                        AI is thinking<span id="title-dots">...</span>
                    </div>

                    <div id="thinking-message" class="thinking-message">
                        Reading your notes
                    </div>
                </div>

            </div>

            <div class="thinking-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>

            <div class="thinking-shimmer"></div>

        </div>
    `;

    const thinkingMessage =
        document.getElementById("thinking-message");

    const titleDots =
        document.getElementById("title-dots");

    thinkingInterval = setInterval(() => {

        dotCount = (dotCount + 1) % 4;

        titleDots.textContent = ".".repeat(dotCount);

    }, 400);

    thinkingMessageInterval = setInterval(() => {

        messageIndex =
            (messageIndex + 1) % thinkingMessages.length;

        thinkingMessage.textContent =
            thinkingMessages[messageIndex];

    }, 1800);

    try {

        console.log("Sending question to Flask...");

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        console.log("Response received:", response.status);

        if (!response.ok) {
            throw new Error("Flask error: " + response.status);
        }

        const data = await response.json();

        console.log("Answer received:", data);

        answerElement.textContent = data.answer;

    } catch (error) {

        console.error("Error:", error);

        answerElement.textContent =
            "Something went wrong. Please check the Flask terminal.";

    } finally {

        clearInterval(thinkingInterval);
        clearInterval(thinkingMessageInterval);

        sendButton.disabled = false;

    }
}