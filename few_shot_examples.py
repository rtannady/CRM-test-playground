# Few-shot examples for the Pipedrive automation parser
# These are example input/output pairs that teach the LLM
# how to handle edge cases consistently

examples = [
    {
        "input": "when a deal moves to closed won, send me a Slack message",
        "output": {
            "trigger": {"object": "deal", "event": "won"},
            "conditions": [],
            "actions": [{"type": "send_slack_message"}]
        }
    },
    {
        "input": "when a new contact is added, create a follow-up call",
        "output": {
            "trigger": {"object": "person", "event": "created"},
            "conditions": [],
            "actions": [{"type": "create_activity", "activity_type": "call"}]
        }
    },
    {
        "input": "ping the sales team whenever we close a big one",
        "output": {
            "trigger": {"object": "deal", "event": "won"},
            "conditions": [],
            "actions": [{"type": "send_slack_message", "channel": "#sales"}],
            "warnings": ["'big' implies a deal value condition but no threshold was specified"]
        }
    }
]

if __name__ == "__main__":
    for i, example in enumerate(examples, 1):
        print(f"Example {i}:")
        print(f"  Input:  {example['input']}")
        print(f"  Output: {example['output']}\n")