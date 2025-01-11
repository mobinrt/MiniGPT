# **Mini GPT**  
An AI-Powered Web Application for Seamless Real-Time Communication and Advanced Language Model Integrations.

## **Project Summary**  
This project is a modern FastAPI-based web application that integrates AI language models for real-time user interaction, project management, and chat functionalities. It uses WebSockets for live communication and incorporates Hugging Face's inference API for generating intelligent responses based on user input. The application is flexible, supports various AI-based tasks, and maintains robust database-backed session and prompt-response management.

---

## **Key Tools & Technologies**  
### **Backend**  
1. **FastAPI**: For building the web API and managing asynchronous routes.  
2. **Tortoise ORM**: Database ORM for schema design and query management.  
3. **PostgreSQL**: Database for storing user data, prompts, and responses.
4. **AIOClock**: Using for handling tasks with time interval
5. Using custome library for pagination, filters, order_by, and etc


### **AI Integration**  
4. **Hugging Face API**: For interacting with models like `Qwen/Qwen2.5-72B-Instruct`.  
5. **Custom Prompt Management**: Includes project-specific context in the AI prompts.  

### **Real-Time Communication**  
6. **WebSockets**: For live communication between users and the AI model.  

### **Authentication & Authorization**  
7. **OAuth2 with JWT**: For securing API endpoints.  

---

## **Features**  
1. **Real-Time AI Chat**:  
   - WebSocket-based chat for instant responses from AI models.
   - Context-sensitive responses based on project names.  

2. **AI Model Integration**:  
   - Supports dynamic prompts with Hugging Face's inference API.
   - Handles tasks like summarization, translation, sentiment analysis, or user-defined tasks.  

3. **User & Session Management**:  
   - User authentication with JWT.  
   - WebSocket session tracking for analytics and debugging.  

4. **CRUD Operations**:  
   - Fully functional API endpoints for creating, reading, updating, and deleting projects, chats, prompts, and responses.  

5. **Database-Backed Design**:  
   - Tracks all prompts and AI responses.  
   - WebSocket sessions are logged for auditing and debugging.  

6. **Extensible Design**:  
   - Modular codebase for easy integration of new AI models or features.  

![Screenshot (113)](https://github.com/user-attachments/assets/74296b40-7e23-4ecf-a905-070ce90b5f9f)
![Screenshot (112)](https://github.com/user-attachments/assets/2cf808a0-3dcb-426c-a1f0-e0723ee2a43b)
![Screenshot (111)](https://github.com/user-attachments/assets/acba1bb0-ca08-43c0-8541-363eabe67294)
![Screenshot (109)](https://github.com/user-attachments/assets/80480d16-c3b7-40b9-b8ad-963c516ccc5f)
![Screenshot (108)](https://github.com/user-attachments/assets/5d87be38-e69c-4f5d-ae9e-d73720279b71)
![Screenshot (107)](https://github.com/user-attachments/assets/04e18277-dcd5-4e42-90c5-fa0f38681049)
![Screenshot (114)](https://github.com/user-attachments/assets/fb0e19eb-38bd-4b6f-965b-2495cdb39c13)
