# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.cloud import bigquery


def execute_bigquery_sql(query: str) -> str:
    """Executes a BigQuery SQL query and returns the results as a string.

    Args:
        query: The BigQuery SQL query to execute.

    Returns:
        A string representation of the query results, or an error message.
    """
    if not query:
        return "Error: Received an empty query."

    try:
        project_id = "ccibt-hack25ww7-749"
        dataset_id = "realtor"
        client = bigquery.Client(project=project_id)
        job_config = bigquery.QueryJobConfig(
            default_dataset=f"{project_id}.{dataset_id}"
        )
        print(f"Executing query:\n---\n{query}\n---")
        query_job = client.query(query, job_config=job_config)  # Make an API request.
        records = [dict(row) for row in query_job]

        if not records:
            return "Query executed successfully, but returned no results."

        return str(records)
    except Exception as e:
        return f"Error executing query: {e}"