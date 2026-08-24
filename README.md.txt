# 🤖 Voice-First AI Personal Assistant Cloud Suite

A live, multi-user, and private AI Personal Assistant that operates over standard global web ports. It schedules activities across Health, Business, and Personal categories, logs daily mood patterns, tracks time-bound phone call schedules, and fetches real-time web data using advanced cloud infrastructures.

## ✨ Core Features
- **Secure Cloud Authentication:** Independent Signup/Login screens mapping individual account workspace session states.
- **Data Isolation:** User-separated timeline structures grouping private Health, Business, Personal calendars, and Call lists.
- **High-Speed Cloud Reasoning:** Zero-latency text synthesis utilizing specialized remote compute processing nodes.
- **Proactive Voice Engine:** Offline text-to-speech loops tracking chronological alerts exactly 24h, 10h, and 1h before events.
- **Scheduled Call Reminders:** Chronological phone book trackers executing voice prompts the exact minute a call is due, cleanly wiping data entries upon execution.
- **Media Asset Loader:** Audio file-vault interface allowing custom morning `.mp3` track uploads.

## 🛠️ The Technology Stack
- **Cloud AI Inference Platform:** Groq Cloud Core (Running `openai/gpt-oss-120b`)
- **Serverless Cloud Relational Database:** Supabase / Render PostgreSQL Engines
- **Visual Interface Control Panel:** Streamlit Application Web Nodes
- **Web Search Connectivity Bridge:** DuckDuckGo Web Scraping Core
- **Hardware Audio Output Core:** Python pyttsx3 Native Speech Layer

## 🚀 Local Installation & Execution
1. Clone the repository and navigate into the project workspace:
   ```bash
   git clone <your-repository-url-here>
   cd ai_personal_assistant
   ```
2. Create and activate a isolated Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install the required cloud network drivers, audio capture nodes, and utility libraries:
   ```bash
   pip install streamlit psycopg2-binary groq duckduckgo-search apscheduler playsound==1.2.2 pyttsx3 speechrecognition pyaudio
   ```
4. Define your active global credentials on Line 4 inside your configurations (`database_manager.py` & `cloud_brain.py`).
5. Launch the synchronized background checker engine in a separate terminal:
   ```bash
   python -c "from background_scheduler import check_and_send_reminders, trigger_scheduled_contact_voice_calls; import time; from apscheduler.schedulers.background import BackgroundScheduler; s=BackgroundScheduler(); s.add_job(check_and_send_reminders, 'interval', seconds=10); s.add_job(trigger_scheduled_contact_voice_calls, 'interval', seconds=10); s.start(); print('Cloud Background Tracker Core Active...'); [time.sleep(1) for _ in iter(int, 1)]"
   ```
6. Launch your visual control center dashboard page inside your web browser:
   ```bash
   streamlit run web_app.py
   ```
