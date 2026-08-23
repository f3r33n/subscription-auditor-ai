
# 💳 Subscription Auditor

A modern, dark-themed financial dashboard built with **Streamlit** for tracking, analyzing, and optimizing recurring digital subscriptions. Features an integrated AI Financial Advisor powered by the **Google Gemini API** (`gemini-2.5-flash`).

---

## 🌟 Key Features

- **📊 KPI Financial Overview**: Real-time breakdown of monthly and annual spending, average subscription costs, and discretionary vs. essential splits.
- **🏥 Subscription Health Score**: Transparent rule-based health status (Healthy, Review, Critical) detecting spending leaks and over-budget thresholds.
- **✏️ Interactive Editor**: Add, edit, or remove subscriptions directly within an in-app data table.
- **📁 Data Import/Export**: Upload custom CSV subscription lists or export your current setup instantly.
- **📈 Savings Simulator**: Interactive slider to model potential annual savings by cutting non-essential subscriptions.
- **🤖 Gemini AI Advisor**: Dynamic financial advice generated via the `google-genai` SDK for audit reports, alternative recommendations, and a 30-day action plan.

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/subscription-auditor.git](https://github.com/your-username/subscription-auditor.git)
cd subscription-auditor

```

### 2. Create & Activate a Virtual Environment

```bash
# On Linux / macOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install streamlit pandas google-genai python-dotenv

```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add your Google Gemini API key:

```env
GEMINI_API_KEY="your_gemini_api_key_here"

```

*(Alternatively, configure `GEMINI_API_KEY` inside `.streamlit/secrets.toml` if deploying to Streamlit Community Cloud).*

### 5. Run the Application

```bash
streamlit run app.py

```

---

## 📂 CSV File Schema

If you choose to upload a custom CSV file, ensure it contains the following mandatory columns:

| Column Name | Type | Description |
| --- | --- | --- |
| `Service` | Text | Name of the platform (e.g., Netflix, Spotify) |
| `Monthly Cost` | Numeric | Price per month (e.g., 499.0) |
| `Category` | Text | One of: *Entertainment, Music, Productivity, AI, Cloud Storage, News, Gaming, Education, Shopping, Other* |
| `Essential` | Boolean | `TRUE` if essential, `FALSE` if discretionary |

---

## 🛠️ Tech Stack

* **Frontend / UI**: [Streamlit](https://streamlit.io/)
* **Data Handling**: [Pandas](https://pandas.pydata.org/)
* **AI Model**: Google Gemini API (`gemini-2.5-flash` via `google-genai`)
* **Environment Management**: `python-dotenv`

---

## 📜 License

This project is licensed under the MIT License — feel free to modify and use it for personal or academic projects.

```

```
