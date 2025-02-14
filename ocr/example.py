import image_ocr
import os

if __name__ == "__main__":
	msg = "Please transcribe this csv"

	base_dir = os.path.dirname(__file__)
	image_path = os.path.join(base_dir, "sample_table.png")

	result = image_ocr.ocr(
		image_path=image_path,
	)
	
	for result_idx, (key, value) in enumerate(result.items()):
		print(f"  result[{key}]: {value}")
		
	

