# AskRC

## Table of Contents
1. [Introduction](#1-introduction)
2. [Dataset Information](#2-dataset-information)
   - [Dataset Introduction](#21-dataset-introduction)
   - [Data Card](#22-data-card)
   - [Data Sources](#23-data-sources)
   - [Data Rights and Privacy](#24-data-rights-and-privacy)
3. [GitHub Repository](#3-github-repository)
   - [Folder Structure](#folder-structure)
4. [Project Scope](#4-project-scope)
   - [Problems](#41-problems)
   - [Current Solutions](#42-current-solutions)
   - [Proposed Solutions](#43-proposed-solutions)

## 1. Introduction
The Research Computing Department at Northeastern University offers numerous resources to researchers, yet these offerings are underutilized due to a lack of awareness. This project aims to develop a **Retrieval-Augmented Generation (RAG)** chatbot to address these issues by providing an interactive platform where users can ask questions and receive relevant, informative responses based on existing documentation.

By developing this chatbot, we will enhance awareness of the Research Computing Department's offerings and simplify the process of accessing resources, ultimately promoting more effective use of these valuable services.

**RAG-based chatbots** are ideal because they combine information retrieval with generation, ensuring responses are factually accurate and traceable to source documents. This solution is designed to promote resource discovery while maintaining the integrity and accuracy of the information being provided to users.

Our project includes developing an end-to-end **Machine Learning Operations (MLOps)** pipeline, including data ingestion, preprocessing, model training, and deployment. The chatbot will be deployed as a scalable serverless endpoint, enabling users to seamlessly interact and get the information they need.

## 2. Dataset Information

### 2.1 Dataset Introduction
The dataset will primarily come from the **Research Computing Department's website** at Northeastern University. This includes FAQs, documentation, and resource descriptions. Our chatbot will use this data to answer relevant queries accurately.

### 2.2 Data Card
- **Dataset Size:** Flexible; new documents can be added as the department updates its resources.
- **Data Format:** Textual data extracted from HTML pages and PDFs.
- **Data Types:** Text-based segments, categorized into FAQs, resource descriptions, and procedural documentation.
- **Data Processing:** Data will be segmented, encoded into embeddings, and stored for efficient retrieval by the RAG model.

### 2.3 Data Sources
- **Website:** Research Computing Department website at Northeastern University.
- **Documents:** HTML pages, PDF files, and other hosted resources.

### 2.4 Data Rights and Privacy
All public data on the Research Computing Department's website is eligible for educational use per Northeastern University's data policies. The project will ensure **FERPA compliance** and adhere to ethical web scraping practices, ensuring no personal or sensitive information is collected or processed.

## 3. GitHub Repository
The repository will contain a `README` file, which includes essential project information such as installation instructions, usage guidelines, and details of the folder structure.

### Folder Structure
The repository will follow this structure:

![Alt text](assets/folder_structure.png)


- **askRC (root directory):** Contains the main project components.
  - **airflow:** Configurations and DAGs for workflow automation.
  - **azure:** Infrastructure scripts and logic apps specific to Azure services.
  - **data:** Divided into `raw`, `processed`, and `embeddings` subfolders.
  - **dvc:** Data Version Control files, including `dvc.yaml`.
  - **docker:** `Dockerfile` and `docker-compose.yaml` for containerization.
  - **github_actions:** Workflow automation scripts.
  - **mlflow:** Directories for tracking model experiments.
  - **snoopy:** Monitoring scripts for the pipeline.
  - **src:** Divided into `data_ingestion`, `model_training`, `evaluation`, and `deployment` folders.
  - **README.md:** Project documentation.
  - **requirements.txt:** Lists all dependencies for the project.

## 4. Project Scope

### 4.1 Problems
- **Lack of Awareness:** Researchers are often unaware of the services offered by the Research Computing Department.
- **Access to Resources:** Navigating the information on the department's website is challenging for researchers, leading to difficulty in accessing resources.
- **Incident Overload:** Due to the challenges of finding information, many issues that could be resolved through self-service result in a large number of incident reports, increasing the workload for research assistants and employees.

### 4.2 Current Solutions
- **Manual Search:** Currently, researchers manually browse the website to find relevant information, which is inefficient and time-consuming.
- **Incident Tickets:** Every time an issue arises, a ticket is created, and the researcher must wait for the issue to be resolved by a research assistant, leading to delays in productivity.

### 4.3 Proposed Solutions
- **RAG-based Chatbot:** Develop a RAG chatbot that can efficiently answer common questions related to the department's resources and services.
- **Improved Resource Discovery:** Leverage existing information from the department's website to enhance the chatbot’s accuracy in responding to user queries, making resource discovery more efficient.

### 5. Data Pipeline
I.	Data Acquisition Summary
The Data Acquisition component is designed to dynamically fetch data from specific sections of a website based on the current week. This is achieved through the scraper.py and get_all_url.py modules, which handle URL scraping and link gathering, respectively.
1.	Section Management:
o	scraper.py defines the URLs for different sections of the website and manages the logic to scrape sections incrementally based on the current week.
o	The scrape_sections_up_to_current_week() function uses the get_current_week() function to determine which sections to scrape, ensuring it stays within the total number of sections available.
2.	Recursive Link Gathering:
o	The get_all_url.py module contains the get_all_links() function, which fetches all links from a given URL up to a specified depth. It recursively visits sub-links within the same domain, ensuring a thorough link gathering process without exceeding a defined depth limit to avoid overloading the crawler.
o	By converting relative URLs to absolute URLs and using a set to track visited URLs, this function avoids duplicating links, maintaining an efficient recursive crawl within each section.
3.	Data Fetching and Arrangement:
o	The fetch_and_print_links() function retrieves links for each section by calling get_all_links() on each URL provided. The number of links found is printed for each section to provide feedback on the volume of data captured.
o	After links are fetched, the arrange_scraped_data() function organizes the data into structured directories, ensuring ease of access and reusability.

II.	Data Preprocessing Summary
The Data Preprocessing component is responsible for preparing raw text data for further processing. This involves several key steps, outlined in modular functions that ensure code reusability and clarity:
1.	Text Cleaning:
o	The clean_text() function preprocesses text by converting it to lowercase, removing special characters and numbers, and excluding common English stopwords. This function enhances text quality by retaining only meaningful words.
2.	Content Splitting:
o	The split_content() function splits large chunks of text into smaller parts to meet the maximum term size constraint (MAX_TERM_SIZE) for Azure Search. This is crucial for efficiently managing large data within Azure's storage limits.
3.	Text File Processing:
o	The preprocess_text_file() function applies text cleaning and splitting to a single text file. It saves the cleaned and split text as separate JSON files, each with a unique ID, allowing easy identification and retrieval.
4.	Batch Processing:
o	The preprocess_data() function iterates through all text files in an input folder, applying cleaning and splitting functions to each file. The processed data is stored in an output folder, with organized JSON files that are easy to access and further process.


III.	Integration with Azure Blob Storage Summary
The Azure Blob Storage Integration component facilitates the storage of preprocessed data in Azure, ensuring accessibility and durability. This is handled through functions in the azure_uploader.py module:
Authentication Setup:
•	Azure credentials (client ID, client secret, tenant ID, and storage account URL) are loaded from environment variables. The ClientSecretCredential from azure.identity is used to authenticate securely.

credentials = ClientSecretCredential(
    client_id=client_id,
    client_secret=client_secret,
    tenant_id=tenant_id
)

Blob Service Client Setup: Establish a connection to the Blob service:

blob_service_client = BlobServiceClient(
    account_url=storage_account_url,
    credential=credentials
)
Container Client Access: Access the specific container:
container_client = blob_service_client.get_container_client('preprocessed-data')

File Upload to Blob Storage:
•	The upload_to_blob() function uploads preprocessed JSON files to a specified container in Azure Blob Storage. It opens the file, reads its content, and uploads it with overwrite protection enabled to ensure smooth updates without duplication issues.
with open(file_path, 'r') as file:
   container_client.upload_blob(name = file_name, data=file.read(), overwrite=True)
   print(file_path + " has been uploaded to blob storage")

IV.	Azure Search Indexing for Faster Search and Similarity Scoring
After data is uploaded to Azure Blob Storage, we implement a data indexing process in Azure Search to facilitate efficient similarity scoring and fast search capabilities for our RAG chatbot. Here’s a summary of the logic used:
1.	Azure Client Setup:
o	We initialize connections to Azure Blob Storage and Azure Search using environment variables for secure access (e.g., AZURE_BLOB_STORAGE_URL, AZURE_SEARCH_ENDPOINT).
o	BlobServiceClient is used to interact with blob storage, while SearchClient enables indexing and search operations on the Azure Search service.
2.	Data Retrieval from Blob Storage:
o	The script iterates over each blob in the designated container (preprocessed-data), downloading the content of each blob, which contains JSON-formatted documents.
o	Each document is checked for completeness; if the blob content is empty, it is skipped, and a warning is logged.
3.	Data Validation and Preprocessing:
o	The content field of each document is validated to ensure it does not exceed Azure’s maximum term size for indexing (32,766 bytes). If the content is too large, a warning is logged, and the document is excluded from indexing.
4.	Indexing in Azure Search:
o	Valid documents are indexed in the specified Azure Search index (askrcindex). This step enables similarity scoring, allowing the chatbot to perform fast and accurate searches over indexed data.
o	Response Logging: After each document is uploaded to the index, the indexing response is logged. If a document is successfully indexed, a success message is printed with the document ID. If there is an error, it logs the error message for troubleshooting.
5.	Error Handling:
o	The code includes error handling for JSON decoding issues and general exceptions, ensuring that errors do not halt the indexing process. This makes the process robust and minimizes interruptions.
By indexing the documents in Azure Search, we enable the RAG chatbot to perform efficient similarity searches and quickly retrieve relevant data for user queries, enhancing the chatbot's response accuracy and speed. This indexing step is a critical part of optimizing data access and searchability within the Azure ecosystem.
 
 
V.	Test Modules
To ensure the robustness of our data pipeline, we have implemented a suite of unit tests using pytest to cover key components of data retrieval, data formatting, and error handling. Additionally, we use GitHub Actions workflows to automate the testing process, providing continuous integration for our project.
1. Unit Tests for Pipeline Components
Our testing suite includes the following tests to validate data retrieval, processing, and error handling:
•	Data Retrieval Test (test_data_retrieval):
o	Verifies that data can be successfully retrieved from a randomly selected URL in the pipeline.
o	Checks that the data retrieved is not empty, confirming that the scraping process effectively captures information from the source.
•	Data Format Test (test_data_format):
o	Ensures that the data format returned from the scraping process matches the expected structure (e.g., dictionary format).
o	This test helps maintain consistency and accuracy in data processing, crucial for downstream tasks.
•	Error Handling Test (test_error_handling):
o	Uses unittest.mock.patch to simulate network failures and tests the pipeline’s error handling capabilities.
o	Confirms that appropriate exceptions are raised when network errors occur, which is vital for reliability, especially during real-time data retrieval.
2. GitHub Actions Workflow for Continuous Testing
To automate the testing process, we use GitHub Actions to run our tests on every push and pull request to the main branch. This CI setup provides consistent validation for new changes and includes the following steps:
•	Check out Code: Retrieves the latest version of the code.
•	Set up Python Environment: Configures the Python environment with the specified version.
•	Install Dependencies: Installs all required dependencies from requirements.txt.
•	Run Tests: Executes each test file (testcase_1.py, testcase_2.py, testcase_3.py) to ensure that all functions perform as expected.
     

VI.	Airflow Pipeline Orchestration Summary
The Pipeline Orchestration component uses Airflow to manage and automate the end-to-end data processing workflow, from scraping data to uploading and indexing it. Here’s a breakdown of the key steps and logic used in the Airflow DAG setup:
1.	DAG Configuration:
o	The DAG (Data_pipeline_dag) is scheduled to run daily, with retry logic and failure email alerts to handle errors. Default arguments include configurations such as the owner, start date, retry delay, and email notifications for errors, ensuring consistent and reliable workflow execution.
2.	Tasks and Logical Flow:
o	The DAG consists of four primary tasks, each handling a distinct stage in the data pipeline:
	Scraping Task (scrape_task): This task calls the scrape_sections_up_to_current_week() function to scrape content from specified sections of the website. This dynamically gathers content based on the current week.
	Data Preprocessing Task (preprocess_task): This task runs preprocess_data(), which processes raw data files by cleaning and organizing them into structured JSON files. Processed data is saved in a separate directory.
	Upload to Azure Blob Storage Task (blob_storage_task): This task uploads the preprocessed JSON files to Azure Blob Storage. It iterates over all JSON files in the PROCESSED_DATA_PATH and uses upload_to_blob() to securely store each file.
	Indexing Task (index_task): This task indexes the data in an Azure Search index by calling index_data_in_search(), making the data searchable and accessible for future use.
3.	Task Dependencies:
o	The DAG follows a sequential structure where each task depends on the successful completion of the previous one:
	scrape_task → preprocess_task → blob_storage_task → index_task.
o	This logical flow ensures that data scraping, preprocessing, uploading, and indexing occur in a streamlined and organized manner.
 

VII.	Data Version Control (DVC) and Tracking
Data Version Control (DVC) to track and manage data changes. Specifically, DVC is set up to track the following folders:

	•	data/raw - Contains raw, unprocessed data collected for the chatbot.
	•	data/processed - Contains preprocessed data, ready for embedding and indexing.

Tracking Data Changes
Data files are versioned and tracked with DVC, allowing for seamless collaboration and version history on data files. This ensures that changes to the data are tracked similarly to code, providing transparency and reproducibility.

GitHub Integration
DVC is integrated with GitHub for version control. The DVC tracking files are committed to GitHub, enabling collaborative work on data versions and ensuring that each team member can access consistent versions of the data.
To set up DVC and start tracking changes, you can use the following commands:

# Initialize DVC (if not already initialized)
dvc init

# Track raw and processed data folders
dvc add data/raw
dvc add data/processed

# Commit DVC tracking files to GitHub
git add data/raw.dvc data/processed.dvc .dvc/config
git commit -m "Track raw and processed data with DVC"
git push origin main

VIII.	Tracking and Logging Summary
For tracking and logging in our data pipeline, we utilize Airflow’s built-in logging system, which is integrated into our GitHub repository. This setup provides a streamlined approach to monitor task execution and manage logs directly within the version-controlled environment.
1.	Airflow’s Built-In Logging:
o	Each task in the Airflow DAG leverages Airflow’s native logging capabilities, which automatically records task progress, completion status, and errors. This logging setup allows us to monitor task states and view detailed logs for each execution, all accessible from within the Airflow UI.
o	Error detection and alerting are configured through Airflow’s settings, which trigger notifications upon task failures, enabling prompt resolution.
IX.	Anomaly Detection & Alerts Summary
In our Airflow pipeline, we have implemented an email alert system to notify the team of any failures or anomalies in real-time. This setup is crucial for quickly identifying and addressing issues, ensuring a smooth and reliable pipeline operation.
•	Automated Email Notifications:
o	Whenever a task in the Airflow pipeline fails, an automated email notification is sent to a predefined list of recipients. The email includes essential information, such as the task that failed, the type of exception encountered, and links to the relevant logs for further investigation.
o	The email example received here shows an error with the message "key must be a string," indicating an issue with the data processing task. The email provides a direct link to the task logs and an option to mark the task as successful if resolved.
•	Comprehensive Alerting Setup:
o	This alerting mechanism ensures that the team is notified immediately of any pipeline anomalies, allowing them to take prompt corrective actions.
o	The list of recipients includes all relevant stakeholders, ensuring visibility and collaboration across the team.
This approach enables effective anomaly detection and quick response to data pipeline issues, enhancing the overall stability and reliability of the project.
 

X.	Data Bias Detection Using Data Slicing
In the context of our RAG chatbot, which leverages information from a static source i.e. the Research Computing documentation site at Northeastern University, formal bias detection may not be strictly necessary. Since the chatbot draws from a standardized source of information rather than user-generated content, there is minimal risk of inherent bias in the information retrieved.
However, to ensure that the chatbot’s responses remain impartial and balanced, we have implemented several bias detection techniques as part of good data management practices. These include:
1.	Sentiment Analysis:
o	We perform sentiment analysis using the analyze_sentiment_distribution() function to check for any unexpected sentiment skew in the content extracted from the documentation. While we expect the documentation to be neutral, this analysis ensures that responses do not inadvertently favor overly positive or negative tones.
2.	Data Slicing by Sentiment:
o	Using the slice_data_by_sentiment() method, we divide the content based on sentiment polarity into positive, negative, and neutral slices. This allows us to observe any unintentional patterns in tone, which could affect how the chatbot’s responses are perceived by users.
3.	Topic Modeling and Keyword Frequency Analysis:
o	We apply topic modeling (perform_topic_analysis) and keyword frequency analysis (keyword_frequency_analysis) to ensure that no specific themes or terms dominate responses in a way that could skew the chatbot’s answers. This ensures that the chatbot’s replies are representative of the full breadth of information available on the documentation site.
Conclusion:
Although bias detection is not mandatory for this project due to the standardized nature of the source material, we implement these techniques as a proactive measure. This approach helps maintain the chatbot’s accuracy and neutrality, ensuring it delivers consistent and unbiased information. These steps also provide a framework for potential future applications where user-generated content may introduce bias risks, making our bias management practices robust and adaptable.


