# Youtube Research Project

## Running the frontend

- Cd into the front-end folder, run npm i to install all the dependencies.
- Run npm run dev to run a dev server.

## Running the backend

- Cd into the backend folder and run the run.py script with python run.py.
- Ensure you have the pip dependecies installed.

## Running the survey

- The frontend should now pull and update comments properly.

## Code for graph and comment generation

I have 4 README's in the README folder for each of my 4 code files already. They have the instructions to run each code, and also the video I recorded shows how to run the 3 new code files. As for the description of each py file, I have the description written as comments at the top of each code file

Can check this for visualizing the output. https://youtu.be/SDw8uGt5lQY

A zip file of collected comments is stored at https://osf.io/r7gae/

## Code for filtering and classification

Within the code folder, general scripts outside an inner folder, featuring gemini llm classification, with quantative filtering.

---


# Project Pipeline

This project explores disinformation trends in public discourse by collecting and filtering YouTube comments on controversial topics using a two-stage classification pipeline. The focus is on identifying meaningful, claim-based content that may contain misinformation, with a specific emphasis on the following categories:

- China Data Security  
- COVID-19  
- Election Interference  
- Russia-Ukraine Conflict  

---

## 🚀 Overview

We built a pipeline that automates the collection, filtering, and classification of YouTube comments, combining metadata processing, rule-based filtering, and LLM-assisted evaluation using Google Gemini 2.0.

---

## 🧪 Pipeline Description

### 1. **Comment Collection via YouTube Data API**
- Search for videos using topic-related keywords.
- For each video:
  - Download all top-level comments and replies.
  - Exclude videos with comments disabled.
  - Store each video's comments and metadata (author, likes, timestamp) in a topic-specific folder as `.txt` files.

### 2. **Raw Comment Aggregation**
- Merge individual text files into a single **unfiltered CSV** for each topic.
- Includes metadata: `comment text`, `likes`, `author`, `timestamp`, and `video_id`.

### 3. **Stage 1 Filtering (Rule-Based)**
- Filter out comments that:
  - Are not in English.
  - Have fewer than 150 likes.
  - Are shorter than 20 characters or longer than 300 characters.
- Clean comments by removing irrelevant characters (e.g., `@mentions`, emojis, excessive symbols).

### 4. **Stage 2 Filtering (LLM Evaluation)**
- Input the filtered comments into a **Google Gemini 2.0** model using the following prompt:

  ```text
  You are a content classifier. Your task is to determine whether a comment contains meaningful information or makes a claim that could be controversial.

  A meaningful comment must have a clear opinion, claim, or verifiable statement. Respond with 'Yes' if the comment is meaningful and 'No' otherwise.

  **Input Format**:
  Comment 1: <comment text>
  Comment 2: <comment text>
  ...

  **Output Format**:
  Comment 1: Yes
  Comment 2: No
  ...

  NOTE: when outputting, only return the output format, do not give me anything else.
  ```

- Only comments marked **"Yes"** are retained in the **final filtered dataset**.

---

## 🗂 Folder Structure

```
project_root/
│
├── data/
│   ├── raw/               # Individual topic folders with .txt files
│   ├── unfiltered_csv/    # Aggregated CSVs before filtering
│   └── filtered_csv/      # Final output after LLM filtering
│
├── scripts/
│   ├── collect_comments.py
│   ├── filter_comments.py
│   └── classify_with_gemini.py
│
├── prompts/
│   └── gemini_prompt.txt
│
└── README.md
```

---

## 🔧 Requirements

- Python 3.8+
- Google API Client (for YouTube Data API)
- OpenAI or Google Gemini access
- Pandas, Langdetect, etc. (see `requirements.txt`)

---

## 📌 Future Improvements

- Add **pronoun-based claim detection**
- Integrate misinformation verification modules
- Visualize misinformation trends per topic

---

## 📜 License

This repository is released under the MIT License. See `LICENSE` for details.
