import os
from pathlib import Path

def load_prompt(prompt_name: str) -> str:
    """Load a system prompt from the prompts/ directory.
    
    Args:
        prompt_name: The filename of the prompt (e.g., 'market_eval.txt').
    
    Returns:
        The content of the prompt file.
    
    Raises:
        FileNotFoundError: If the prompt file does not exist.
    """
    # Assuming this file is in <project_root>/core/prompts.py
    # We want <project_root>/prompts/
    
    # Get the directory of this file (core/)
    current_dir = Path(__file__).parent.absolute()
    
    # Go up one level to project root, then into prompts/
    project_root = current_dir.parent
    prompt_path = project_root / "prompts" / prompt_name
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        
    return prompt_path.read_text(encoding="utf-8")
