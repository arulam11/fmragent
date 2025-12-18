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

import os

from jinja2 import Environment, FileSystemLoader


def load_table_structure_prompt() -> str:
    """Loads and renders the BigQuery table structure and rules template.

    Returns:
        str: The rendered template content.
    """
    try:
        # Set up Jinja environment
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(current_dir, "prompt-template")
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("CAM_table_structure.j2")

        # Render the template
        return template.render()

    except Exception as e:
        print(f"Error loading table structure template: {str(e)}")
        raise


def load_agent_instructions():
    """Dynamically loads agent instructions."""
    try:
        full_instruction = load_table_structure_prompt()
        print("Successfully loaded agent instructions.")
        return full_instruction
    except Exception as e:
        print(f"FATAL: Could not load agent instructions: {e}")
        # Fallback to a basic instruction if dynamic loading fails
        return "You are an agent that can query real estate and FMR data from BigQuery."