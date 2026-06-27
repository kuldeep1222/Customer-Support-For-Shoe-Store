# Customer Support For Shoe Store

## Overview

The Customer Support For Shoe Store is an Agentic AI application that uses a Large Language Model (LLM) as a planning agent to understand user requests, decide which tool(s) should be executed, validate the generated execution plan, execute Python tools on a local JSON database, and return a user-friendly response.

Unlike a traditional chatbot, the LLM does not directly answer customer questions or access the database. Instead, it generates an execution plan which is validated before any tool is executed. This architecture improves reliability, transparency, and modularity.

---

# Features

* LLM-based planning
* Tool selection
* Multi-tool execution
* Tool chaining
* Plan validation
* Error handling
* Product search
* Product comparison
* Product recommendation
* Order tracking
* Alternative product suggestion
* Streamlit user interface


---

# Project Structure

```
AI-Shoe-Store-Agent/

│
├── app.py
├── agent.py
├── tools.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── products.json
│   └── orders.json
│

```

---

# Architecture

```
                 User
                   │
                   ▼
          Streamlit Interface
                   │
                   ▼
            LLM Planning Agent
                   │
                   ▼
            Plan Validator
                   │
        ┌──────────┴──────────┐
        │                     │
     Invalid               Valid
        │                     │
 Return Friendly Error        ▼
                        Execute Tools
                               │
                               ▼
                        JSON Database
                               │
                               ▼
                       Response Formatter
                               │
                               ▼
                        Streamlit Output
```

---

# Workflow

## Step 1 — User Query

The user enters a natural language question.

Example:

```
Show Nike running shoes under ₹5000
```

---

## Step 2 — Planning

The query is sent to Gemini 2.5 Flash.

The LLM only generates an execution plan.

Example:

```json
{
  "intent":"search_products",
  "tools":[
    {
      "tool":"search_products",
      "arguments":{
        "brand":"Nike",
        "category":"running shoes",
        "max_price":5000
      }
    }
  ]
}
```

The LLM never accesses the database.

---

## Step 3 — Validation

The generated plan is validated.

Checks include:

* Valid JSON
* Valid intent
* Valid tool names
* Required arguments
* Missing arguments
* Empty values

Invalid plans are rejected before execution.

---

## Step 4 — Tool Execution

Python executes the validated tools.

Example:

```
search_products()
```

Tools read data from

* products.json
* orders.json

---

## Step 5 — Response Formatting

Tool outputs are converted into a clean, customer-friendly response.

Example:

```
  Nike Revolution 7

Brand: Nike
Price: ₹4,799
Sizes: 7,8,9
Stock: 12 pairs
```

---

# Available Tools

## get_order()

Returns order details using Order ID.

Example:

```
Track my order ORD-1002
```

---

## get_product()

Returns product information.

Example:

```
Tell me about P001
```

---

## search_products()

Search using

* brand
* category
* price
* size
* stock

Example:

```
Nike shoes under ₹5000
```

---

## compare_products()

Compares two products.

Example:

```
Compare P001 and P005
```

---

## recommend_products()

Returns products matching user preferences.

Example:

```
Recommend Adidas running shoes
```

---

## find_alternatives()

Suggests cheaper or similar products.

Example:

```
Find a cheaper alternative to P001
```


# Error Handling

The system handles:

* Invalid JSON
* Invalid tool
* Invalid intent
* Missing arguments
* Unknown Order ID
* Unknown Product ID
* Empty search results
* Runtime exceptions

---

# Sample Inputs and Outputs

## Example 1

Input

```
Track my order ORD-1003
```

Output

```
Order ID: ORD-1003
Status: Delivered
Expected Delivery: 2026-06-15
```

---

## Example 2

Input

```
Nike shoes under ₹5000
```

Output

```
Nike Revolution 7

Price: ₹4,799

Sizes: 7,8,9
```

---

## Example 3

Input

```
Recommend Adidas running shoes
```

Output

```
Adidas Run Falcon 3
₹4,499
```

---

## Example 4

Input

```
Compare P001 and P005
```

Output

```
Price Difference: ₹1700

Cheaper Product:
P005
```

---

## Example 5

Input

```
Find a cheaper alternative to P001
```

Output

```
Adidas Duramo SL

₹4,799
```

---

# Technologies Used

* Python
* Streamlit
* python-dotenv
* JSON
* openai

# Model used

* gemini flash-2.5
---

# Approach

The project follows an Agentic AI architecture.

Instead of allowing the LLM to directly answer questions, the LLM is only responsible for planning.

Python performs

* validation
* execution
* formatting

This separation improves reliability and prevents hallucinated database responses.

---

# Current Limitations

* Multi-brand queries depend on LLM planning.
* Planner performance depends on prompt quality.
* Database is static (JSON).
* No authentication.
* No real-time inventory updates.

---

# Future Improvements

* SQL or MongoDB backend
* Customer login
* Shopping cart
* Order placement
* Inventory management
* Payment integration
* Vector search
* Retrieval-Augmented Generation (RAG)
* Better multi-tool planning
* Support for multiple simultaneous brands
* Docker deployment
* REST API
* Cloud deployment

---

# Installation

Install dependencies

```
pip install -r requirements.txt
```

Run Streamlit

```
streamlit run app.py
```

---

# Conclusion

The AI Shoe Store Assistant demonstrates an Agentic AI workflow where a Large Language Model acts as a planning agent while Python performs validation, tool execution, and response formatting. This modular architecture provides reliable execution, improved transparency, and easy extensibility compared to directly relying on LLM-generated responses.
