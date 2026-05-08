import json
from system_prompt import AUTOMATION_SYSTEM_PROMPT

def parse_with_llm(user_input: str) -> dict:
    """
    Calls Claude to parse a plain English automation request.
    Swap the stub below for a real API call when the key arrives.
    """

    # ── STUB — replace this block with the real API call ──────────────
    # import anthropic
    # client = anthropic.Anthropic(api_key="your-key-here")
    # message = client.messages.create(
    #     model="claude-sonnet-4-20250514",
    #     max_tokens=1024,
    #     system=AUTOMATION_SYSTEM_PROMPT,
    #     messages=[{"role": "user", "content": user_input}]
    # )
    # raw = message.content[0].text
    # return json.loads(raw)
    # ──────────────────────────────────────────────────────────────────

    # Stub response simulating what Claude would return
    if "won" in user_input.lower() or "closed" in user_input.lower():
        return {
            "trigger": {"object": "deal", "event": "won"},
            "conditions": [],
            "actions": [{"type": "send_slack_message", "parameters": {}}]
        }
    elif "big" in user_input.lower() or "top" in user_input.lower():
        return {
            "trigger": {"object": "deal", "event": "won"},
            "conditions": [],
            "actions": [{"type": "send_slack_message", "parameters": {"channel": "#sales"}}],
            "warnings": ["'big' implies a deal value condition but no threshold was specified — add a value like 'over $10,000' to complete this condition"]
        }
    else:
        return {
            "trigger": {"object": "deal", "event": "updated"},
            "conditions": [],
            "actions": [{"type": "add_note", "parameters": {}}],
            "warnings": [f"Could not confidently map '{user_input}' to a known automation pattern"]
        }

if __name__ == "__main__":
    test_inputs = [
        "when a deal moves to closed won, send me a Slack message",
        "ping the sales team whenever we close a big one",
        "do something when stuff happens"
    ]

    for input_text in test_inputs:
        print(f"\nInput:  {input_text}")
        result = parse_with_llm(input_text)
        print(f"Output: {json.dumps(result, indent=2)}")
