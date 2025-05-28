import os
import json
from mcp.server.fastmcp import FastMCP

md_mcp = FastMCP("Modus Migration Markdown Server")


def load_md_prompt(tool_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(script_dir, "md_prompts", f"{tool_name}.md")
    with open(md_path, "r", encoding="utf-8") as f:
        return f.read()


def call_ai(prompt, user_input):
    # Placeholder for LLM call
    return (
        f"AI output for prompt: {prompt[:100]}... and user input: {user_input[:100]}..."
    )


@md_mcp.tool()
def analyze_code_for_migration_md(file_content: str) -> str:
    prompt = load_md_prompt("analyze")
    ai_response = call_ai(prompt, file_content)
    return ai_response


@md_mcp.tool()
def generate_migrated_code_md(file_content: str) -> str:
    prompt = load_md_prompt("migrate")
    ai_response = call_ai(prompt, file_content)
    return ai_response


@md_mcp.tool()
def verify_migration_with_gold_standard_md(migrated_content: str) -> str:
    prompt = load_md_prompt("verify")
    ai_response = call_ai(prompt, migrated_content)
    return ai_response


@md_mcp.tool()
def log_migration_summary_md(summary_input: str) -> str:
    prompt = load_md_prompt("log")
    ai_response = call_ai(prompt, summary_input)
    return ai_response


@md_mcp.tool()
def run_migration_workflow_md(user_input: str, previous_state: str = None) -> str:
    prompt = load_md_prompt("workflow")
    ai_response = call_ai(prompt, user_input + (previous_state or ""))
    return ai_response


if __name__ == "__main__":
    md_mcp.run(transport="stdio")
