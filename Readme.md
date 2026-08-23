```mermaid
graph TD
    A[User Input / CSV Data] --> B[Pandas Data Engine]
    B --> C[KPI Calculation & Spending Metrics]
    B --> D[Rule-Based Health Score Engine]

    C --> E[Streamlit Dashboard UI]
    D --> E

    B --> F[Google Gemini API Engine]
    F -->|gemini-2.5-flash| G[AI Financial Advisor & Action Plan]
    G --> E



```markdown
```text
  ___  _   _ ____  ____   ____ ____  ___ ____ _____ ___  _  _ 
 / _ \| | | |  _ \|  _ \ / ___|  _ \|_ _|  _ \_   _/ _ \| || |
| | | | | | | |_) | |_) | |   | |_) || || |_) || || | | | || |_
| |_| | |_| |  _ <|  _ <| |___|  _ < | ||  __/ | || |_| |__   _|
 \__\_\\___/|_| \_|_| \_\\____|_| \_\___|_|    |_| \___/   |_|

> **SYSTEM STATUS:** `[ONLINE]` — Financial Audit & Subscription Telemetry Dashboard  
> **ENGINE:** Python 3.x | Streamlit UI | Google Gemini API (`gemini-2.5-flash`)

---

## 🖥️ $ sys_info --overview

The **Subscription Auditor** is a terminal-inspired, dark-themed dashboard built with **Streamlit** to analyze, track, and optimize recurring digital expenses. It integrates rule-based heuristic scoring with real-time AI intelligence via the `google-genai` SDK.


```

[+] TELEMETRY Breakdown: Real-time Monthly & Annual KPI Tracking
[+] HEALTH DIAGNOSTICS: Automated leakage detection & budget threshold scoring
[+] DATA MATRIX EDITOR: In-app live manipulation of target subscription records
[+] I/O PIPELINE     : CSV state import / export workflow engine
[+] SAVINGS SIMULATOR: Real-time slider-driven discretionary spending modeling
[+] GEMINI AI ENGINE : Autonomous 30-day action plan & optimization advisor

```

---

## 📐 $ cat architecture.mmd

```mermaid
graph TD
    A[User Input / CSV Data] --> B[Pandas Data Engine]
    B --> C[KPI Calculation & Spending Metrics]
    B --> D[Rule-Based Health Score Engine]
    
    C --> E[Streamlit Dashboard UI]
    D --> E
    
    B --> F[Google Gemini API Engine]
    F -->|gemini-2.5-flash| G[AI Financial Advisor & Action Plan]
    G --> E

```

---

## 🖼️ $ display --gallery

---

## ⚡ $ ./quickstart.sh

### Step 1: Clone Repository

```bash
git clone https://github.com/your-username/subscription-auditor.git
cd subscription-auditor

```

### Step 2: Initialize Virtual Environment

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell / CMD)
python -m venv venv
.\venv\Scripts\activate

```

### Step 3: Install Required Dependencies

```bash
pip install streamlit pandas google-genai python-dotenv

```

### Step 4: Provision Environment Variables

Construct a `.env` file in the root environment directory:

```env
GEMINI_API_KEY="your_gemini_api_key_here"

```

*(Note: For Streamlit Community Cloud deployments, store `GEMINI_API_KEY` in `.streamlit/secrets.toml`)*

### Step 5: Execute Dashboard Entrypoint

```bash
streamlit run app.py

```

---

## 📊 $ cat csv_schema.json

When importing custom datasets, verify the payload structure adheres to the following layout:

| Field Name | Type | Description |
| --- | --- | --- |
| `Service` | `string` | Target service identifier (e.g., *Netflix*, *Spotify*) |
| `Monthly Cost` | `float` | Monthly billing rate in numeric format (e.g., `499.0`) |
| `Category` | `enum` | Classification: *Entertainment, Music, Productivity, AI, Cloud Storage, News, Gaming, Education, Shopping, Other* |
| `Essential` | `bool` | Spending tier: `TRUE` (Essential) | `FALSE` (Discretionary) |

---

## ⚙️ $ tech_stack --list

```
[FRAMEWORK]  :: Streamlit
[DATA LAB]   :: Pandas
[INTELLIGENCE]:: Google Gemini API (gemini-2.5-flash via google-genai)
[CONFIG]     :: python-dotenv

```

---

## 📄 $ cat LICENSE

Distributed under the **MIT License**. Free for personal modification, educational analysis, and distribution.

```

```
