from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import PyPDF2  # install: pip install PyPDF2

# load environmental variables
load_dotenv('../.env')

# establish client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #actual api key

# Pre-existing list of datasets
existing_datasets = [
    {"unique_id": 1, "dataset_name": "KITSUNE", "authors": "Yisroel Mirsky, Tomer Doitshman, Yuval Elovici, Asaf Shabtai", 
     "doi": "https://www.ndss-symposium.org/wp-content/uploads/2018/02/ndss2018_03A-3_Mirsky_paper.pdf"},
    
    {"unique_id": 2, "dataset_name": "NSL-KDD", "authors": "GhulamMohi-ud-din", 
     "doi": "https://dx.doi.org/10.21227/425a-3e55"},
    
    {"unique_id": 3, "dataset_name": "UNSW-NB15", "authors": "Moustafa, Nour, and Jill Slay", 
     "doi": "https://research.unsw.edu.au/projects/unsw-nb15-dataset"},
    
    {"unique_id": 4, "dataset_name": "CICIDS2017", "authors": "Iman Sharafaldin, Arash Habibi Lashkari, and Ali A. Ghorbani", 
     "doi": "https://www.unb.ca/cic/datasets/ids-2017.html"},
    
    {"unique_id": 5, "dataset_name": "BoT-IoT dataset", "authors": "Nickolaos Koroniotis, Nour Moustafa, Elena Sitnikova, Benjamin Turnbull",  
     "doi": "https://research.unsw.edu.au/projects/bot-iot-dataset"}
]

# Path to the folder containing PDF files
pdf_folder = r"C:\Users\Roohana Karim\Desktop\Papers\PDFs"

# Function to read PDFs from the specified folder
def extract_pdfs_from_folder(pdf_folder):
    pdf_files = []
    for file_name in os.listdir(pdf_folder):
        if file_name.endswith('.pdf'):  # Check if the file is a PDF
            pdf_files.append(os.path.join(pdf_folder, file_name))
    return pdf_files

# Function to extract text from PDF files
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    pdf_text = ""
    for page_num in range(len(pdf_reader.pages)):
        pdf_text += pdf_reader.pages[page_num].extract_text()
    return pdf_text

# Load PDF files and extract content
papers = []
pdf_files = extract_pdfs_from_folder(pdf_folder)
for pdf_file in pdf_files:
    try:
        text = extract_text_from_pdf(pdf_file)
        papers.append(text)  # Add extracted text to the papers list
        print(f"Extracted text from: {pdf_file}")
    except Exception as e:
        print(f"Error extracting text from {pdf_file}: {e}")

# Function to check if dataset exists
def find_matching_dataset(new_dataset, existing_datasets):
    for dataset in existing_datasets:
        if (new_dataset['dataset_name'].lower() == dataset['dataset_name'].lower()) and \
           (new_dataset['authors'].lower() == dataset['authors'].lower() or \
            new_dataset['doi'].lower() == dataset['doi'].lower()):
            return dataset['unique_id']
    return None

# Function to generate system prompts for various tasks
def generate_system_prompt(task):
    if task == "domain":
        return """
        You are tasked with identifying the research domain of a cybersecurity paper. 
        Please extract the research domain (e.g., IoT, network traffic, malware, APT , network intrusion etc) for each paper provided.
        """
    elif task == "dataset_name":
        return f"""
        You are tasked with extracting datasets used in cybersecurity research papers and comparing them to an existing list.
        For each dataset mentioned, extract and list:
        {"dataset_name": "DATASET_NAME", "authors": "AUTHOR_STRING", "doi": "DOI_LINK"}.
        Compare the extracted dataset with the following existing list of datasets:
        {json.dumps(existing_datasets, indent=4)}
        If the dataset matches an existing entry by name, author, or DOI/link, return the unique_id. 
        If no match is found, assign a new unique_id.
        """
    elif task == "sub_domain":
        return """
        For the extracted dataset, identify the sub-domains or specific attacks/vulnerabilities it covers.
        """
    elif task == "dataset_usage":
        return """
        For the extracted dataset, indicate what percentage of the dataset was used by the research (e.g., full dataset, or a specific sampled portion).
        """
    elif task == "dataset_type":
        return """
        For the extracted dataset, identify whether the dataset is realistic, synthetic, or hybrid.
        """
    elif task == "labeling_type":
        return """
        For the extracted dataset, identify whether the dataset is labeled, unlabeled, or a hybrid of both.
        """
    elif task == "availability":
        return """
        For the extracted dataset, identify its availability:
        Is it public, proprietary, restricted, or a custom dataset (created just for this research and never shared)?
        """
    else:
        raise ValueError("Invalid task")

# Function to process papers for multiple tasks
def process_papers_for_tasks(papers, tasks):
    task_results = {}
    next_unique_id = len(existing_datasets) + 1  # For adding new datasets
    
    for task in tasks:
        print(f"Processing task: {task}")
        # Generate system prompt for the task
        system_prompt = generate_system_prompt(task)
        
        # Combine all papers into a single user prompt (could limit based on token size)
        user_prompt = ""
        for paper in papers:
            user_prompt += f"Process this cybersecurity paper for {task}: {paper}\n"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # Call OpenAI API for the task
        try:
            response = client.chat.completions.create(
                model='gpt-4o-2024-08-06',  # Adjust model if necessary
                messages=messages,
                temperature=0.2,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": f"{task}_extraction",
                        "schema": {
                            "type": "object",
                            "properties": {
                                task: {
                                    "type": "array",
                                    "description": f"List of {task} for the paper",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "dataset_name": {"type": "string"},
                                            "value": {"type": "string"}  # This will vary depending on the task
                                        },
                                        "required": ["dataset_name", "value"]
                                    }
                                }
                            },
                            "required": [task],
                            "additionalProperties": False
                        },
                        "strict": True
                    }
                }
            )
            
            # Parse the response and aggregate results
            json_object = json.loads(response.choices[0].message.content)
            task_results[task] = json_object[task]

            # Handle dataset name comparison
            if task == "dataset_name":
                for dataset in json_object['dataset_name']:
                    match = find_matching_dataset(dataset, existing_datasets)
                    if match:
                        print(f"Match found for dataset '{dataset['dataset_name']}' with unique ID: {match}")
                        dataset['unique_id'] = match
                    else:
                        print(f"Adding new dataset: {dataset['dataset_name']} with unique ID: {next_unique_id}")
                        dataset['unique_id'] = next_unique_id
                        existing_datasets.append({"unique_id": next_unique_id, **dataset})
                        next_unique_id += 1

        except Exception as e:
            print(f"Error processing {task}: {e}")

    return task_results

# List of tasks to perform
tasks = ["domain", "dataset_name", "sub_domain", "dataset_usage", "dataset_type", "labeling_type", "availability"]

# Process all papers for all tasks
all_results = process_papers_for_tasks(papers, tasks)

# Print the final results for each task
for task, results in all_results.items():
    print(f"Results for {task}:")
    for result in results:
        print(result)

# Optionally, save the updated list to a file
with open('datasets_updated.json', 'w') as f:
    json.dump(existing_datasets, f, indent=4)
