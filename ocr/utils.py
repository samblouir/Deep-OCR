


def verify_response(message):
	# ```txt and ```csv should be present
	if "```txt" not in message or "```csv" not in message:
		return False
	return True
pass


def extract_codeblocks(message):
	# finds ```xxx 
	# uses xxx as the key
	output_dict = {}

	# split by ```xxx
	parts = message.split("```")
	for part_idx in range(1, len(parts), 2):
		splits = parts[part_idx].split("\n")
		if len(splits) == 2:
			key = splits[0].strip()
			value = splits[1].strip()
		else:
			key = parts[part_idx]
			value = parts[part_idx+1]
		output_dict[key] = value
	return output_dict


def get_thinking_system_prompt():
	return "You are a deep thinking AI, you may use extremely long chains of thought to deeply consider the problem and deliberate with yourself via systematic reasoning processes to help come to a correct solution prior to answering. You should enclose your thoughts and internal monologue inside <think> </think> tags, and then provide your solution or response to the problem."
pass

def safe_clean_think(content):
	content = content.rsplit("</think>", 1)[-1]
	content = content.replace("<think>", "").strip()
	return content

def clean_tags(history):
	for message_idx in range(len(history)):
		message = history[message_idx]
		content = message['content']
		content = content.rsplit("</think>", 1)[-1]
		content = content.replace("<think>", "").strip()
		history[message_idx]['content'] = content
	return history
	




if __name__ == "__main__":
	msg = '''
To clean up the formatting as requested:

**Title Codeblock:**
```txt
Table 2. Weibull parameters for Epoxy – Al₂O₃ composites.
```

**CSV Data Codeblock:**
```csv
Composition,Shape Parameter (β),Scale Parameter (α)
Unfilled,8.789,52.30
0.1% nano,19.57,36.01
0.5% nano,18.01,39.98
1% nano,15.60,37.83
5% nano,9.237,37.18
5% micron,13.94,32.61
```

**Explanation:**
- The table's title was extracted and placed in its own codeblock.
- All HTML tags were removed to convert the data into plain text rows.
- Each row of data was reformatted into a CSV format with headers and values separated by commas.
'''.strip()
	
	assert( verify_response(msg) )
	codeblocks = extract_codeblocks(msg)
	title = codeblocks['txt']
	csv = codeblocks['csv']
	print(title)
	print(csv)

	
