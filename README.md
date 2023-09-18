# Quickly_Extract_Science_Papers
Too many science papers to read. For papers in your experienced field, you might not need to read from front to back to understand and extract useful information. However, for unfamiliar fields, it's often inaccessible and hard to read, even with decent scientific reading training.

This script automatically classifies the research paper and asks appropriate questions to help you quickly extract information, or decide to give it a detailed read.

I hope this can help reduce information overload and encourage interdisciplinary reading and understanding.

## Background 
This project is inspired by and built upon David Shapiro's "Quickly_Extract_Science_Papers" (https://github.com/daveshap/Quickly_Extract_Science_Papers). Many thanks to him.

In David's original version, the GPT API is prompted with a fixed set of questions, which is probably good enough for David's use case, since he mainly uses it to read AI-related papers.

However, different types of papers (empirical vs. theoretical, for example) may not be easily extracted with the same prompt. Therefore, I built a two-tier process. First, the LLM reads the paper and classifies it into 12 types of common research papers (see Prompts.yaml for details). For each type of paper, I prepared 3 questions to quickly extract the key takeaways from the paper.

I also changed the model from GPT-4 to GPT-3.5-turbo-16k to improve the token window and affordability (about 1/10 of the GPT-4 price).

## Repo Contents

- `chat.py` - this file is a simple chatbot that will chat with you about the contents of `input.txt` (you can copy/paste anything into this text file). Very useful to quickly discuss papers. 
- `Smart_generate_multiple_reports.py` - this will consume all PDFs in the `input/` folder and generate summaries in the `output/` folder. This is helpful for bulk processing such as for literature reviews. 
- `render_report.py` - this will render all the reports in `output/` to a an *easier* to read file in `report.html`.

## EXECUTIVE SUMMARY

This repository contains Python scripts that automate the process of generating reports from PDF files using OpenAI's GPT-3.5 model. The scripts extract text from PDF files, send the text to the GPT-3.5 model for processing, and save the generated reports as text files. The scripts also include functionality to render the generated reports as an HTML document for easy viewing.

## SETUP

1. Clone the repository to your local machine.
2. Install the required Python packages by running `pip install -r requirements.txt` in your terminal.
3. Obtain an API key from OpenAI and save it in a file named `key_openai.txt` in the root directory of the repository.
4. Place the PDF files you want to generate reports from in the `input/` directory.

## USAGE

1. Run the `generate_multiple_reports.py` script to generate reports from the PDF files in the `input/` directory. The
generated reports will be saved as text files in the `output/` directory.
2. Run the `render_report.py` script to render the generated reports as an HTML document. The HTML document will be
saved as `report.html` in the root directory of the repository.
3. You can modify the `prompts.yaml` to change the clisification and focus on any questions you would like to ask. In other words you can automatically ask any set of questions in bulk against any set of papers. This can help you greatly accelerate your literature reviews and surveys.

## NOTE

The scripts are designed to handle errors and retries when communicating with the OpenAI API. If the API returns an
error due to the maximum context length being exceeded, the scripts will automatically trim the oldest message and retry
the API call. If the API returns any other type of error, the scripts will retry the API call after a delay, with the
delay increasing exponentially for each consecutive error. If the API returns errors for seven consecutive attempts, the
scripts will stop and exit.

GPT-3.5-turbo-16k limits token size to 16 thousand, so the script is set up such that it will only read the first 50k characters (approximately 15 pages). In my testing, it provided good results (even for 20+ page papers), but if your paper is significantly longer, it might result in an incomplete summary since a large chunk of the original paper is not fed into the API.