# Cybersecurity Dataset and Research Domain Analysis Repository

##  Overview
This repository focuses on analyzing cybersecurity dataset and research domain trends extracted from top-tier conferences. The analysis includes dataset categorization, availability, and research trends over time.

##  Repository Structure

### **1. Codes and Script Files**
- all_codes_in_one_first_script.PY – Python script containing consolidated functions for dataset extraction and processing. This is are very first script, we started with Zero Shot Technique here.
- all_codes_in_one_uss.ipynb – Jupyter Notebook version of the main script for easier debugging and visualization.
- prompts_final.txt – Contains structured prompts used for LLM-based dataset extraction.

### **2. Datasets and Results**
- datasets_summary.csv – Summary of datasets analyzed.
- research_domain_trends.csv / .json – Trends in cybersecurity research domains across years.
- results_final_2.0.csv / .jsonl – Final processed results extracted from research papers.
- subcategory_domain_correlation.csv – Correlation between dataset subcategories and research domains.
- subcategory_trends_over_time.csv – Trends in dataset subcategories over time.
- top_10_subcategories_per_year.csv / .png – Top dataset subcategories used each year (CSV + visual).
- unique_datasets_2.0.csv / .json – List of unique datasets extracted from cybersecurity papers.
- `cybersecurity_research_dataset.csv / .jsonl` – Complete dataset containing **1,194 research papers**, including **titles, conference names, years, and research domains**.

##  Features
- Extracts cybersecurity dataset usage from **top-tier conferences**.
- Analyzes dataset trends from **2015-2023**.
- Identifies **dataset subcategories, availability, and gaps**.
- Generates **visual trends, datasets and research domain insights**.

##  Data Insights & Trends
The repository includes:
- **Trend analysis** of cybersecurity dataset usage.
- **Research domain categorization** (NIDS, MAD, PPC, AML etc.).
- **Public dataset identification** for reproducibility.
- **Benchmarking and standardization** issues in dataset studies.

## Installation & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/Anonymoususs25/cybersecurity-dataset-analysis.git
cd cybersecurity-dataset-analysis



### **2. Install Dependencies**

pip install pandas matplotlib seaborn json csv


### **3. Run the Jupyter Notebook**
jupyter notebook all_codes_in_one_uss.ipynb

### **4. Run the Python Script**
python
!python all_codes_in_one_first_script.PY


## Requirements
- **Python 3.8+**
- **Jupyter Notebook (if running .ipynb)**
- **Pandas, Matplotlib, Seaborn, JSON, CSV modules**

##  License
This repository is licensed under the **MIT License**. Feel free to contribute and use it for research purposes.

## Contributing
Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to modify.

---

 **Maintainer:** [Anonymoususs25](https://github.com/Anonymoususs25)  
 **GitHub Repository:** [Cybersecurity Dataset Analysis](https://github.com/Anonymoususs25/cybersecurity_dataset_research_domain_2025)
