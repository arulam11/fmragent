# CRE Agent: Commercial Real Estate Loan Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

An AI agent that assists with commercial real estate loan analysis by providing data-driven insights on market value, rental income potential, and flood risk.

## Description

The CRE (Commercial Real Estate) Agent is an intelligent system designed to streamline due diligence for loan analysis. It is built using the Google Agent Development Kit (ADK) and leverages Google Cloud's Vertex AI and BigQuery.

This project exposes the agent through a simple Flask API. It allows users to ask complex questions—such as "What is the median listing price for properties in zip code 08807?" or "Generate a loan analysis memo for a property in Los Angeles, CA"—and receive direct, data-driven answers synthesized from multiple datasets.

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

The agent's effectiveness comes from its understanding of the underlying data structures it can query. The prompt template (`CAM_table_structure.j2`) provides the LLM with the schemas and purposes of three distinct BigQuery tables, enabling it to translate a natural language question into a valid SQL query.

### BigQuery Table Schema

The agent is configured to work with the following tables within the `realtorzip` dataset:

#### 1. Realtor Zip Data (`realtorzip`)
Contains individual real estate property listings. Used for questions about listing prices, property attributes (beds, baths, size), and market trends.

| Column Name              | Data Type | Description                                                                 |
| ------------------------ | --------- | --------------------------------------------------------------------------- |
| `status`                 | STRING    | Listing status (e.g., 'for_sale'). Must be filtered for current market data. |
| `price`                  | BIGNUMERIC| The listing price of the property.                                          |
| `bed`                    | INTEGER   | Number of bedrooms.                                                         |
| `bath`                   | INTEGER   | Number of bathrooms.                                                        |
| `house_size`             | FLOAT     | Size in square feet.                                                        |
| `zip_code`               | STRING    | The 5-digit postal zip code.                                                |
| `city`                   | STRING    | The city corresponding to the zip code.                                     |
| `state`                  | STRING    | The 2-letter state abbreviation (e.g., "CA", "NY").                         |

#### 2. FY2026 Small Area Fair Market Rent (`FY2026`)
Contains Fiscal Year 2026 SAFMR data. Critical for assessing a property's rental income potential.

| Column Name              | Data Type | Description                                                                 |
| ------------------------ | --------- | --------------------------------------------------------------------------- |
| `zip_code`               | STRING    | 5-digit zip code.                                                           |
| `safmr_0br`              | INTEGER   | Fair Market Rent for a 0-bedroom/studio unit.                               |
| `safmr_1br`              | INTEGER   | Fair Market Rent for a 1-bedroom unit.                                      |
| `safmr_2br`              | INTEGER   | Fair Market Rent for a 2-bedroom unit.                                      |
| `safmr_3br`              | INTEGER   | Fair Market Rent for a 3-bedroom unit.                                      |
| `safmr_4br`              | INTEGER   | Fair Market Rent for a 4-bedroom unit.                                      |

#### 3. Flood Risk Data (`floodlossbystate`)
Contains flood risk statistics aggregated at the **state level**. Used for questions related to flood risk and potential financial loss.

| Column Name                   | Data Type | Description                                                                 |
| ----------------------------- | --------- | --------------------------------------------------------------------------- |
| `state`                       | STRING    | 2-letter state abbreviation.                                                |
| `fema_risk_rating`            | STRING    | Categorical risk rating (e.g., 'Low', 'Medium', 'High').                    |
| `percent_properties_at_risk`  | FLOAT     | The percentage of properties in the state with significant flood risk.      |
| `average_annual_loss_usd`     | FLOAT     | The estimated average financial loss per property per year due to flooding. |

### Agent Output

The agent provides a natural language answer based on the query results. For more complex requests (e.g., asking for a "memo" or "report"), it can generate a structured Markdown document that synthesizes findings from all three data sources into an analysis memo covering market value, rental income potential, and flood risk.

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
  "question": "Generate a commercial real estate loan analysis memo for a property in zip code 90210."
}'
