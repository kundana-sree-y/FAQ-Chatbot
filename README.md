



# 🎓 CampusAI — Intelligent College Assistant



CampusAI is an intelligent, web-based college assistant designed to help students access college-related information and interact through a conversational interface. It combines Natural Language Processing (NLP), a college-specific knowledge base, and multilingual capabilities to make information more accessible.



## ✨ Features



- 💬 Conversational Interaction — Supports greetings, basic conversations, and student queries.

- 🎓 College Information — Provides college-related information from its knowledge base.

- 🧠 NLP-Based Intent Recognition — Uses machine learning and text processing to identify user query patterns and intents.

- 🌐 Multilingual Support — Enables interaction across different languages using the translation engine.

- 🔄 Translation Support — Translates queries and responses to improve accessibility.

- 📚 Knowledge Base — Uses structured college information and FAQ datasets.

- 🖥️ Web Interface — Interactive chatbot interface built using HTML, CSS, JavaScript, and Flask.

- ❓ Fallback Responses — Handles queries for which reliable information is unavailable.



## 🛠️ Tech Stack



| Technology | Purpose |

|---|---|

| Python | Backend development and NLP logic |

| Flask | Web application framework |

| Scikit-learn | NLP model training and intent classification |

| TF-IDF | Text feature extraction |

| HTML | Web page structure |

| CSS | Interface styling |

| JavaScript | Frontend interactions |

| JSON | Dataset and knowledge-base storage |



## 📂 Project Structure



```text

FAQ-Chatbot/

├── app.py

├── chatbot.py

├── conversation.py

├── translation_engine.py

├── train_model.py

├── requirements.txt

├── dataset/

│   ├── college_data.json

│   ├── faqs.json

│   └── intents.json

├── templates/

│   └── index.html

├── static/

│   ├── css/

│   │   └── style.css

│   └── js/

│       └── script.js

├── .gitignore

└── README.md

```



## ⚙️ Installation and Setup



### 1. Clone the repository



```bash

git clone https://github.com/kundana-sree-y/FAQ-Chatbot.git

```



### 2. Navigate to the project directory



```bash

cd FAQ-Chatbot

```



### 3. Create a virtual environment



```bash

python -m venv .venv

```



### 4. Activate the virtual environment



**Windows — Git Bash:**



```bash

source .venv/Scripts/activate

```



**Windows — PowerShell:**



```bash

.venv\\Scripts\\Activate.ps1

```



### 5. Install dependencies



```bash

pip install -r requirements.txt

```



### 6. Train the NLP model



```bash

python train_model.py

```



### 7. Start the application



```bash

python app.py

```



### 8. Open in your browser



Visit:



http://127.0.0.1:5000



## 🧠 How CampusAI Works



1\. The user submits a query through the web interface.

2\. The application processes the query.

3\. NLP and conversational components help interpret the user's input.

4\. College-related information is retrieved or an appropriate conversational response is generated.

5\. The translation component supports multilingual interaction.

6\. The response is displayed through the chatbot interface.



## 🎯 Project Objective



The objective of CampusAI is to create an accessible and interactive college information assistant that reduces the difficulty of finding college-related information while exploring conversational NLP and multilingual interaction in a web-based application.



## 🚀 Future Enhancements



- Expand the college knowledge base.

- Improve query understanding and response accuracy.

- Enhance multilingual conversational capabilities.

- Integrate additional student-focused features.

- Improve the chatbot interface and accessibility.



## 👩‍💻 Developer



Developed as a Python-based AI and NLP project.



---



⭐ If you find this project interesting, feel free to explore the repository!



