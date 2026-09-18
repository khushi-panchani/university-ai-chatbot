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


    thinkingInterval = setInterval(() => {

        dotCount = (dotCount + 1) % 4;

        if (titleDots) {
            titleDots.textContent = ".".repeat(dotCount);
        }

    }, 400);


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

        if (!response.ok) {

            answerElement.textContent =
                data.answer || "Something went wrong.";

            return;
        }

        // Convert Markdown response into properly formatted HTML
        answerElement.innerHTML = marked.parse(data.answer);


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