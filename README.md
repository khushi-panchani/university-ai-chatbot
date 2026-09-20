# 🎓 University AI Chatbot

An AI-powered chatbot that allows students to upload university PDF notes and ask questions about their content.

The project uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from the uploaded PDF and uses **Google Gemini** to generate a clear and structured answer.

## 🚀 Live Demo

🌐 **Try the University AI Chatbot:**

https://university-ai-chatbot.onrender.com

> Upload a university PDF, ask a question, and get an AI-generated answer based on the uploaded notes.

---

## 📌 Project Overview

Students often have to search through large university PDFs to find specific information.

This project solves that problem by allowing users to:

- 📄 Upload a university PDF
- 🔍 Search information from the uploaded notes
- 🤖 Ask questions in natural language
- 🧠 Retrieve relevant content using semantic search
- ✨ Generate structured answers using Google Gemini

The chatbot is designed to answer questions using the information retrieved from the uploaded PDF.

---

## 🧠 How It Works

The project follows a **Retrieval-Augmented Generation (RAG)** pipeline.


                University PDF
                      ↓
               Extract Text
                      ↓
                 Chunk Text
                      ↓
              Generate Embeddings
                      ↓
              Store in FAISS Index
                      ↓
                User Question
                      ↓
           Generate Query Embedding
                      ↓
             FAISS Similarity Search
                      ↓
             Retrieve Relevant Chunks
                      ↓
              Create Gemini Prompt
                      ↓
                Google Gemini
                      ↓
              Generate Final Answer
                      ↓
                Display on Website
