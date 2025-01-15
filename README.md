# **Mini GPT**  
An AI-Powered Web Application for Seamless Real-Time Communication and Advanced Language Model Integrations.

---

## **Project Summary**  
This project is a modern web application built on **FastAPI**, designed for dynamic, real-time communication powered by AI. It provides robust tools for project management, chat functionalities, and AI-driven tasks like summarization, translation, and sentiment analysis. With Redis-backed guest sessions, rate-limiting features, and custom helper libraries, it offers a scalable and secure platform for diverse use cases.

---

## **Key Tools & Technologies**  

### **Backend**  
1. **FastAPI**: High-performance web framework for building APIs and WebSocket-based communication.  
2. **Tortoise ORM**: Database ORM for schema management and seamless database interaction.  
3. **PostgreSQL**: Primary database for storing application data.  

### **Real-Time Communication**  
4. **WebSockets**: Live communication for real-time user and AI interactions.  

### **AI Model Integration**  
5. **Hugging Face API**: Interaction with state-of-the-art language models like `Qwen/Qwen2.5-72B-Instruct`.  
6. **Custom Prompt Management**: Dynamically contextualize prompts using project names.  

### **Guest Access with Redis**  
7. **Redis**: Fast, in-memory key-value store to manage guest sessions without user authentication.  

### **Rate Limiting**  
8. **Custom Rate Limiter**: Protects against misuse and ensures fair resource allocation for both guests and authenticated users.  

### **Authentication & Authorization**  
9. **OAuth2 with JWT**: Secures authenticated endpoints. Guests operate without authentication while adhering to rate limits.  

### **Custom Libraries**  
10. **Helper Utilities**: Includes a suite of utilities for pagination, filtering, and error handling.  

---

## **Features**  

### **1. AI-Driven Real-Time Chat**  
- WebSocket-based chat integrates AI models for instantaneous and context-aware responses.  
- Dynamically includes project-specific context in AI prompts.  

### **2. Guest User Support**  
- Guests can access the application without authentication.  
- Sessions are managed using Redis for lightweight and efficient storage.  

### **3. Rate Limiting**  
- Ensures fair usage for both authenticated users and guests.  
- Protects APIs from overuse or abuse.  

### **4. User Authentication**  
- Secure JWT-based authentication for registered users.  
- Granular control over API access for guests vs. authenticated users.  

### **5. Extensible AI Tasks**  
- Includes predefined tasks like summarization, translation, and sentiment analysis.  
- Flexible for user-defined tasks based on project context.  

### **6. Database-Powered Design**  
- Tracks all prompts, AI responses, and WebSocket sessions.  
- Ensures data integrity and transparency.  

### **7. Modular Design with Custom Libraries**  
- **Pagination**: Simplifies API responses for large datasets.  
- **Filters**: Enhances querying capabilities with dynamic filters.  
- **Error Handling**: Custom exception classes for consistent and descriptive error reporting.  

---

![Screenshot (113)](https://github.com/user-attachments/assets/74296b40-7e23-4ecf-a905-070ce90b5f9f)
![Screenshot (112)](https://github.com/user-attachments/assets/2cf808a0-3dcb-426c-a1f0-e0723ee2a43b)
![Screenshot (111)](https://github.com/user-attachments/assets/acba1bb0-ca08-43c0-8541-363eabe67294)
![Screenshot (109)](https://github.com/user-attachments/assets/80480d16-c3b7-40b9-b8ad-963c516ccc5f)
![Screenshot (108)](https://github.com/user-attachments/assets/5d87be38-e69c-4f5d-ae9e-d73720279b71)
![Screenshot (107)](https://github.com/user-attachments/assets/04e18277-dcd5-4e42-90c5-fa0f38681049)
![Screenshot (114)](https://github.com/user-attachments/assets/fb0e19eb-38bd-4b6f-965b-2495cdb39c13)
