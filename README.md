# AI WhatsApp Support Agent

This project was developed to explore the construction of an automated WhatsApp support agent using a containerized, distributed architecture and integration with large language models.

## Overview

The application receives messages via WhatsApp, processes them, and generates contextual responses using an AI agent when necessary.

The system is designed with a focus on:

* separation of concerns
* asynchronous processing
* response optimization through semantic caching

---

## Architecture

The solution is composed of the following components:

* **FastAPI (Webhook)**
  Entry layer responsible for receiving messages and orchestrating the application flow.

* **AI Agent (Agno + Groq)**
  Responsible for generating responses based on predefined context.

* **RedisVL (Semantic Cache)**
  Stores previous question/answer pairs to reduce latency and inference costs.

* **Celery + RabbitMQ**
  Handle asynchronous message delivery, decoupling response generation from the request cycle.

* **WAHA (WhatsApp API)**
  Gateway responsible for communication with WhatsApp.

* **Docker + Docker Compose**
  Manage service orchestration and environment standardization.

---

## Application Flow

1. A user sends a message via WhatsApp
2. The message is received through the FastAPI webhook
3. The system checks the semantic cache (RedisVL)

   * Cache hit → return stored response
   * Cache miss → invoke the AI agent
4. The response is sent asynchronously via Celery
5. The user receives the response on WhatsApp

---

## Technologies

* Python
* FastAPI
* Celery
* RabbitMQ
* Redis / RedisVL
* Agno
* Groq (LLM)
* WAHA
* Docker / Docker Compose

---

## Purpose

This project was built for learning purposes, focusing on:

* distributed system architecture
* integration with large language models (LLMs)
* performance optimization using semantic caching
* asynchronous processing patterns

---

## Limitations

* Uses a non-official WhatsApp API (WAHA)
* Strong reliance on LLM behavior for response control
* Semantic cache may return incorrect responses in cases of ambiguous similarity
* Architecture may be over-engineered for the problem scope (intentional for learning purposes)

---

## Next Steps

* Introduce request control and validation layer
* Improve response consistency and reduce hallucinations
* Add observability and metrics
* Evaluate architectural simplifications

---

## Status

Project under development with a focus on learning and experimentation.
