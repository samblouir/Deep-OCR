import sys
sys.path.append('..')
import cache
import time
import traceback
import pickle

from openai import OpenAI
client = OpenAI(base_url="http://localhost:1234/v1/", api_key='lm-studio')

def get_model():
	models = client.models.list()
	for model in models:
		return model.id
	

def get_completion(messages, use_cache=True, **kwargs):

	sleep_time = 5
	stream = kwargs.get("stream", True)

	settings = dict(
		model=get_model(),
		store=False,
		max_completion_tokens=32768,
		messages=messages,
		reasoning_effort="high",
		stream=True,
	)
	settings.update(kwargs)
	settings = dict(sorted(settings.items()))

	settings['stream'] = True
	cache_key = cache.quick_key(settings)

	try:
		if not use_cache:
			raise Exception("Force cache miss")
		output = cache.quick_load(cache_key)
		if len(output) == 0:
			raise Exception("Empty output, forcing cache miss...")
		return output
	except:

		for settings_idx, (key, value) in enumerate(settings.items()):
			print(f"  settings[{key}]: {value}")
			


		while True:
			try:
				completion = client.chat.completions.create(**settings)
				break
			except Exception as e:
				# raise e
				print(f'  openai_api.py  Exception when creating the completion!  e: {e}, retrying')
				time.sleep(sleep_time)
				sleep_time += 5
				sleep_time = min(sleep_time, 30)
				print(f"  e: {e}")

		built = []

		show_border = 2
		try:
			for chunk in completion:

				if isinstance(chunk.choices, tuple):
					continue

				try:
					chunk.choices[0].delta.content
				except Exception as e:
					print(f"*" * 60,)
					traceback.print_exc()
					print(f"*" * 60,)
					print(chunk)
					print(f"*" * 60,)
					print(f"*" * 60,)
					continue

				if chunk.choices[0].delta.content is not None:
					if stream and (show_border == 2):
						show_border -= 1
						print(f"\n" * 3, end='',)
						print(f"*" * 60,)


					text = chunk.choices[0].delta.content
					built.append(text)
					if stream:
						print(text, end="", flush=True)


		except Exception as e:
			print(f" *** "*4)
			print(f"  real_api.py  Broke on: {e}")
			traceback.print_exc()
			print(f" *** "*4)


		if stream and (show_border == 1):
			show_border = 0
			print(f"*" * 60,)
			print(f"\n" * 3, end='',)

		text = "".join(built)
		text = text.strip()

				
		cache.quick_save(cache_key, text)

		return text
	