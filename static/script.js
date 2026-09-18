console.log("script.js loaded successfully");

let thinkingInterval;
let thinkingMessageInterval;

async function askQuestion() {

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

    // Show thinking animation
    answerElement.innerHTML = `
        <div class="ai-thinking">

            <div class="thinking-top">

                <div class="animated-robot">
                    🤖
                </div>

                <div>
                    <div class="thinking-title">
                        AI is thinking<span class="title-dots"></span>
                    </div>

                    <div class="thinking-message">
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
        document.querySelector(".thinking-message");

    const titleDots =
        document.querySelector(".title-dots");

    // Animate title dots
    thinkingInterval = setInterval(() => {

        dotCount = (dotCount + 1) % 4;

        if (titleDots) {
            titleDots.textContent = ".".repeat(dotCount);
        }

    }, 400);

    // Change thinking messages
    thinkingMessageInterval = setInterval(() => {

        messageIndex =
            (messageIndex + 1) % thinkingMessages.length;

        if (thinkingMessage) {
            thinkingMessage.textContent =
                thinkingMessages[messageIndex];
        }

    }, 1800);

    try {

        const response = await fetch("/ask", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        // Stop animation before displaying the answer
        clearInterval(thinkingInterval);
        clearInterval(thinkingMessageInterval);

        // Display successful answer
        if (response.ok && data.answer) {

            answerElement.innerHTML = marked.parse(data.answer);

        } else if (data.error) {

            answerElement.textContent = data.error;

        } else {

            answerElement.textContent =
                "No answer received from the server.";

        }

    } catch (error) {

        console.error("Error:", error);

        answerElement.textContent =
            "Unable to connect to the Flask server.";

    } finally {

        clearInterval(thinkingInterval);
        clearInterval(thinkingMessageInterval);

        sendButton.disabled = false;

    }

}