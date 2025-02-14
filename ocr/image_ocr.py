import ollama
import utils
import openai_api
import cache


def ocr_image(
		image_path="./image.png",
		msg=None,
		stream=True,
		model_temperature=0.0,
		use_cached=True,
		**kwargs,
	):

	cache_key = cache.quick_key(dict(image_path=image_path, msg=msg, model_temperature=model_temperature,))
	if use_cached:
		try:
			return cache.quick_load(cache_key)
		except:
			pass

	if msg is None:
		msg = "Please carefully transcribe and format this table. Be gentle."

	# Default model call options
	options = dict(
		top_k=40,
		top_p=0.95,
		min_p=0.04,
		temperature=model_temperature,
		num_predict=8192,
	)
	options.update(kwargs)

	messages = [
		{
			'role': 'user',
			'content': msg,
			'images': [image_path]
		},
	]

	res = ollama.chat(
		model="minicpm-v",
		messages=messages,
		stream=stream,
		options=options,
	)

	if stream:
		ts = []
		for chunk in res:
			content_chunk = chunk['message']['content']
			ts.append(content_chunk)
			print(content_chunk, end='', flush=True)
		print()
		ret_str = "".join(ts)
	else:
		ret_str = res['message']['content']
	
	cache.quick_save(cache_key, ret_str)
	return ret_str






def ocr(image_path, user_message=None):
	ret_dict = {}

	# Encode the image
	ret_dict['ocr_result'] = ocr_image(image_path, )

	
	if user_message is None:
		user_message = f'''Please help clean up this formatting. Place the CSV and title in their own codeblocks, like so:\n\n```txt\nTable x.  Title\n```\n\n```csv\n\n```\n\nMake sure that you include the number of elements per row exactly matches the number of headers.\n\nDouble-check to make sure you are using the user's preferred format at the end."'''
	else:
		user_message += "\n\nIf applicable, please place independent components (like the title and content) in seperate codeblocks. Making a CSV? Make sure that you include the number of elements per row exactly matches the number of headers.\n\nDouble-check to make sure you are using the user's preferred format at the end."

	user_message += f"""\n\nHere is the table to clean up:\n```\n{ret_dict['ocr_result']}\n```"""

	messages = [
		{
			'role': 'system',
			'content': utils.get_thinking_system_prompt(),
		},
		{
			'role': 'user',
			'content': user_message,
		},
	]

	output = openai_api.get_completion(messages, stream=True,)
	output = utils.safe_clean_think(output)
	messages.append({"role": "assistant", "content": output})
	messages = utils.clean_tags(messages)


	messages.append({"role": "user", "content": "Which specific format did I ask for? Please carefully double-check each step to make sure that the formatting is correct and the instructions were followed. Double-check that this outut has the exact formatting style desired - it is probably the structure is different. Create a checklist. Finally, re-make the table in the specific format I asked for exactly."})
	second_output = openai_api.get_completion(messages, stream=True,)
	second_output = utils.safe_clean_think(second_output)


	joined_output = output + "\n\n" + second_output
	final_output = utils.extract_codeblocks(joined_output)

	for output_idx, (key, value) in enumerate(final_output.items()):
		print(f"*" * 20,)
		print(f"  final_output[{key}]: {value}")
		print(f"*" * 20,)
		
	ret_dict.update(final_output)

	return ret_dict




