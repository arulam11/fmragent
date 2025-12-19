# FMR Agent: Real Estate Data Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

An AI agent that provides insights into a real estate portfolio by answering natural language questions about Fair Market Rent (FMR) and property data.

## Description

The FMR (Fair Market Rent) Agent is an intelligent system designed to streamline the analysis of real estate data. It is built using the Google Agent Development Kit (ADK) and leverages Google Cloud's Vertex AI and BigQuery.

This project exposes the agent through a simple Flask API, allowing users to ask complex questions about property data—such as "what is the average 2-bedroom fair market rent in Los Angeles?" or "which 5 zip codes in California have the highest 1-bedroom rent?"—and receive direct, data-driven answers.

## Table of Contents

- [Architecture](#architecture)
- [Data Model & Prompting](#data-model--prompting)
- [Technologies Used](#technologies-used)
- [API Endpoint](#api-endpoint)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Architecture

The system is composed of a few key components:

1.  **Flask API Server** (`main.py`): A lightweight web server that provides an HTTP endpoint to interact with the agent.
2.  **FMR Agent** (`fmr_agent/agent.py`): The core logic, built with the Google ADK. It interprets the user's question, formulates queries, and retrieves data.
3.  **Google Cloud Vertex AI**: The platform for hosting and running the AI agent's reasoning engine.
4.  **Google Cloud BigQuery**: The data warehouse that stores the real estate and FMR data, which the agent queries for answers.

## Data Model & Prompting

The agent's effectiveness comes from its understanding of the underlying data structure. The instructions for the `SqlGeneratorAgent` include the schema of the BigQuery table it is expected to query. This allows the LLM to translate a natural language question into a valid and accurate SQL query.

### BigQuery Table Schema

The agent is configured to work with a table from the `realtorzip` dataset with the following schema:

| Column Name              | Data Type | Description                                                                 |
| ------------------------ | --------- | --------------------------------------------------------------------------- |
| `zip_code`               | STRING    | The 5-digit postal zip code.                                                |
| `city`                   | STRING    | The city corresponding to the zip code.                                     |
| `state`                  | STRING    | The 2-letter state abbreviation (e.g., "CA", "NY").                         |
| `county_name`            | STRING    | The name of the county.                                                     |
| `fmr_0_br`               | INTEGER   | The Fair Market Rent for a 0-bedroom (studio) unit.                         |
| `fmr_1_br`               | INTEGER   | The Fair Market Rent for a 1-bedroom unit.                                  |
| `fmr_2_br`               | INTEGER   | The Fair Market Rent for a 2-bedroom unit.                                  |
| `fmr_3_br`               | INTEGER   | The Fair Market Rent for a 3-bedroom unit.                                  |
| `fmr_4_br`               | INTEGER   | The Fair Market Rent for a 4-bedroom unit.                                  |

### Agent Output

As defined in `fmr_agent/agent.py`, the final output is structured in a user-friendly markdown format. It presents the generated SQL query for transparency, followed by a natural language interpretation of the results returned from BigQuery.

## Technologies Used

- **Backend**: Python, Flask
- **AI/ML**: Google Cloud AI Platform (Vertex AI), Google Agent Development Kit (ADK)
- **Data**: Google Cloud BigQuery
- **Dependencies**: See `requirements.txt`

## API Endpoint

### Invoke the Agent

- **URL**: `/invoke_agent`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "question": "Your natural language question about the loan data"
  }
  ```
- **Success Response (200 OK)**:
  ```json
  {
    "response": "The agent's answer to your question."
  }
  ```
- **Error Response (400/500)**:
  ```json
  {
    "error": "Description of the error."
  }
  ```

## Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/fmr-agent.git
    cd fmr-agent
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Google Cloud authentication**
    This agent requires access to Google Cloud services. Ensure your environment is authenticated. The simplest method for local development is to use the gcloud CLI:
    ```bash
    gcloud auth application-default login
    ```

5.  **Run the Flask application**
    ```bash
    python fmr-agent/main.py
    ```
    The server will start on `http://0.0.0.0:8080` by default.

## Usage

Once the server is running, you can send requests to the `/invoke_agent` endpoint using a tool like `curl` or any API client.

```bash
curl -X POST http://127.0.0.1:8080/invoke_agent \
-H "Content-Type: application/json" \
-d '{
  "question": "What is the average 2 bedroom FMR in the state of Florida?"
}'
