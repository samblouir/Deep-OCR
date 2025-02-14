# Deep-OCR

## Description
This code takes in a local image (png or jpg) and returns the text in a format you desire.
By default, the prompt assumes you are turning a screenshot of a table into an CSV.
It also caches the results.


## Example

```python
import deep_ocr

result = deep_ocr.load_image(
 "sample_table.png",
 "Please return this as a CSV. Also, return the title.",
)
```

## Input table:
![Sample Table](https://raw.githubusercontent.com/samblouir/Deep-OCR/refs/heads/main/sample_table.png)

### Output

The model outputs text like this:

```python

print(result)

{
 "title": "Table 1: Salt Concentration and Light Transmittance Data",
 "csv": "Salt Concentration (%),Trial 1 Transmittance (%),Trial 2 Transmittance (%),Trial 3 Transmittance (%),Trial 4 Transmittance (%),Trial 5 Transmittance (%)
0,77.23,74.50,64.88,75.27,54.66
3,85.23,92.82,78.91,60.71,57.96
6,88.39,100.05,73.66,66.51,64.54
9,80.71,100.05,68.29,64.91,52.96
12,82.66,117.18,71.01,56.91,46.95
15,72.55,115.40,65.72,66.03,55.38",
}
```





## Usage

```python
import deep_ocr

result = deep_ocr.load_image(
 "path/to/image.png",
 "Please convert this into a csv. I want the title and content separately.",
)

print(result["title"])
print(result["content"])
```



## Underneath

- deephermes-3-llama-3-8B for formatting the table and recognizing what elements you want.
- mini-cpm for raw OCR

## Installation

```bash
pip install -r requirements.txt
pip install deep-ocr
```