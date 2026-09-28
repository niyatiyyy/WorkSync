# WorkSync

> **Monitor. Detect. Recover. Work Better.**

WorkSync is an adaptive workplace wellness assistant that monitors aggregated computer interaction patterns, compares them with a user's personal activity baseline, detects sustained deviations, and recommends recovery breaks.

## Overview

### Problem Statement

Computer-based work frequently involves long, uninterrupted stretches of keyboard and mouse activity. Changes in activity levels and work intensity build up gradually and can often go unnoticed by the individual.

Traditional break reminder applications rely almost exclusively on fixed timers (e.g., prompting a break every 60 minutes) regardless of actual activity patterns. They do not adapt to an individual's unique workflow or natural baseline.

**Core Framing:**

> *Don't ask only: "Has the user worked for an hour?"*  
> *Ask: "Has this user's recent activity meaningfully changed from their normal pattern?"*

WorkSync is designed for office workers, students, researchers, and professionals who spend extended hours working at a computer.

*Disclaimer: WorkSync does NOT medically detect fatigue, stress, burnout, or any clinical medical condition.*

### The WorkSync Loop

[ MONITOR ] ──> [ DETECT ] ──> [ INTERVENE ] ──> [ RECOVER ]

1. Monitor: Observes aggregated local interaction metrics such as keyboard activity, mouse activity, and session duration without storing actual typed text.


2. Detect: Creates a personal activity baseline from initial activity samples and checks recent activity for sustained deviations from that baseline.


3. Intervene: Recommends a short recovery break when the prototype fatigue-risk indicator reaches the intervention threshold.


4. Recover: Guides the user through a 60-second recovery routine and compares pre- and post-break activity against the user's baseline.



Key Features

Personal Activity Baseline: Creates a baseline from the user's initial activity samples, including typical WPM, correction rate, and mouse movement.

Aggregated Interaction Tracking: Tracks local metrics including keyboard activity, estimated WPM, correction rate (backspace frequency), mouse clicks, mouse movement, and continuous session duration.

Sustained Deviation Detection: Evaluates recent activity patterns rather than triggering alerts from a single slow sample or momentary pause.

Prototype Fatigue-Risk Indicator: Computes an activity-based indicator ranging from 0 to 100, mapped to four qualitative levels:

0–29: Normal

30–59: Mild

60–79: Elevated

80–100: High


Guided 60-Second Recovery Break: Offers an interactive break screen with step-by-step recovery prompts including eye rest, shoulder relaxation, breathing, and stretching.

Before/After Recovery Comparison: Compares activity before and after the break and checks whether post-break activity moves closer to the user's baseline.

Browser-Based Local Dashboard: Provides a browser interface for monitoring live metrics, baseline status, fatigue-risk level, recommendations, and recent activity.

Privacy-Focused Local Architecture: Data capture, processing, and storage remain on the user's local machine. Actual typed text is not stored.


Note: The fatigue-risk indicator is a prototype software metric and is NOT a medical assessment.

Architecture & Technical Implementation

WorkSync is built as a lightweight, locally executed desktop application paired with a local Flask web server and a browser-based interface.

System Architecture

### System Architecture

```text
+---------------------------------------------------------------+
|                        Local Environment                      |
|                                                               |
|   Keyboard / Mouse Activity                                   |
|            |                                                  |
|            v                                                  |
|   pynput Tracker (tracker.py)                                 |
|            |                                                  |
|            v                                                  |
|   Activity Metrics (WPM, Corrections, Clicks, Movement)       |
|            |                                                  |
|            v                                                  |
|   Personal Baseline & SQLite Database (database.py)           |
|            |                                                  |
|            v                                                  |
|   Rule-Based Detector (detector.py)                            |
|            |                                                  |
|            v                                                  |
|   Fatigue-Risk Indicator & Intervention Thresholds            |
|            |                                                  |
|            v                                                  |
|   Flask Web Server (app.py)                                   |
|            |                                                  |
|            v                                                  |
|   Local Dashboard (Browser)                                   |
|            |                                                  |
|            v                                                  |
|   Guided Recovery → Recovery Comparison                       |
+---------------------------------------------------------------+
```

Technology Stack

### Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic, metric aggregation, and risk scoring |
| Flask | Local web application server, UI routes, and API endpoints |
| pynput | Keyboard and mouse event monitoring |
| SQLite | Local storage for activity samples and baseline data |
| HTML / CSS | Dashboard structure and styling |
| JavaScript | Periodic metric polling, timers, and client-side page updates |


Because pynput monitors local operating-system input events, the application is designed to run on the local machine where the user's keyboard and mouse are being used.

Fatigue-Risk Detection Model

WorkSync uses a transparent, rule-based scoring system to generate its prototype fatigue-risk indicator from 0 to 100. It does not use machine learning models or black-box algorithms.

The score is based on four behavioral factors relative to the user's baseline:

1. Sustained WPM Decline: Compares recent typing speed against the baseline. Multiple recent samples showing a significant drop below the baseline can increase the score.


2. Increased Correction Rate: Evaluates backspace frequency relative to overall keystrokes. A higher correction rate can contribute to the score.


3. Reduced Mouse Activity: Compares recent mouse movement activity with the baseline and contributes to the score when activity decreases significantly.


4. Continuous Session Duration: Adds to the score as the current work session becomes longer without a sufficient break.



Indicator Thresholds

### Indicator Thresholds

| Score Range | Risk Level | System Action |
|---|---|---|
| 0–29 | Normal | Normal activity monitoring |
| 30–59 | Mild | Activity changes are indicated |
| 60–79 | Elevated | Break recommendation is shown |
| 80–100 | High | Break recommendation is shown |

> These thresholds are experimental prototype parameters and are not medical or clinical standards.

Project Structure

### Project Structure

```text
WorkSync/
├── app.py
├── tracker.py
├── detector.py
├── database.py
├── requirements.txt
├── LICENSE
├── README.md
├── templates/
│   ├── dashboard.html
│   ├── break.html
│   ├── recovery.html
│   └── history.html
└── static/
    ├── style.css
    └── script.js
```

Module Responsibilities

app.py: Runs the local Flask web service, serves the application pages, and provides API endpoints used by the dashboard.

tracker.py: Uses pynput listeners to monitor keyboard and mouse events and calculate aggregated metrics such as WPM, correction rate, mouse clicks, and mouse movement without storing typed text.

detector.py: Compares current activity and recent samples with the user's baseline and calculates the prototype 0–100 fatigue-risk score.

database.py: Manages the SQLite database, initializes the required tables, stores periodic activity samples, and creates and retrieves the user's activity baseline.


Setup & Installation

Prerequisites

Python 3.8+ installed on your system

Git for repository cloning


Step-by-Step Setup

1. Clone the Repository

git clone https://github.com/niyatiyyy/WorkSync
cd WorkSync


2. Install Dependencies

python -m pip install -r requirements.txt

requirements.txt includes flask and pynput. SQLite is included in the Python standard library.


3. Run the Application

python app.py


4. Access the Local Dashboard

Open a browser and navigate to:

http://127.0.0.1:5000/



Upon execution, the application automatically initializes a local SQLite database named worksync.db in the project directory.

Usage Flow

1. Launch: Run python app.py and open the local dashboard in a web browser.


2. Calibration: Work normally on the computer. WorkSync collects activity samples locally and uses them to create a personal activity baseline.


3. Continuous Monitoring: The dashboard periodically updates with current interaction metrics and the fatigue-risk score.


4. Detection & Intervention: If recent activity shows sustained deviations from the user's baseline, the risk score can increase. When the score reaches 60 or above, the dashboard displays a recovery break recommendation.


5. Guided Recovery: Start the recommended break to enter a 60-second recovery session with prompts for looking away from the screen, breathing, and stretching.


6. Evaluation: After the break, the Recovery Page shows activity before and after the break and compares the post-break WPM with the user's baseline.


7. History: Navigate to the History page to view previously recorded activity samples and summary statistics.



Database & Data Persistence

WorkSync stores activity metrics locally in an SQLite database file named worksync.db.

The database is automatically generated when app.py is run.

Activity samples and baseline information are stored locally.

worksync.db is excluded from source control through .gitignore.

Each user running the project generates their own local database and personal baseline.


Privacy & Data Security

Privacy is a core design consideration of WorkSync.

No Text Storage: Keypresses are counted for activity metrics such as WPM and backspace frequency, but actual key identities, characters, words, and sentences are not stored.

No Content Storage: The application does not store the actual text, passwords, search queries, or document contents typed by the user.

No Media Capture: WorkSync does not use a webcam, microphone, facial recognition, screenshots, or video/audio recording.

Local Processing: Activity calculations and database storage are performed locally on the user's machine. The prototype does not send activity data to external cloud servers or third-party analytics services.


Known Limitations

Rule-Based Detection: The current prototype uses fixed mathematical heuristics rather than machine learning or adaptive AI models.

Metric Scope: Recovery analysis focuses primarily on short-term WPM and interaction activity comparison.

Content Agnostic: The system measures interaction patterns without understanding the meaning or type of work being performed. Different activities can therefore produce similar raw metrics.

Local Instance Only: WorkSync runs as a local application and does not synchronize activity data across multiple devices.

Sample Storage: The History page currently displays raw periodic activity samples rather than synthesized daily or weekly wellness trends.

Prototype Indicator: The fatigue-risk score is an experimental software metric and should not be interpreted as a medical or clinical measurement.


Future Scope

Planned enhancements for future iterations include:

Advanced statistical and machine learning models for more personalized anomaly detection.

Broader cross-platform packaging, such as a standalone desktop or system-tray application.

Improved handling of multi-monitor mouse activity.

Long-term wellness trends and session summary visualizations.

Customizable recovery duration and user-configurable threshold sensitivity.

More detailed recovery analytics using additional activity metrics.


Development & Disclosure

Hackathon: ASYNC'26
Track: Wellness & Lifestyle
Team: KINETIX
Project: WorkSync

Development Disclosure

WorkSync was developed by Team KINETIX during the pre-hackathon preparation and mentoring period for ASYNC'26. The repository reflects the team's development work and iterations leading into the hackathon.

Any further changes made during the official hackathon period will be reflected in the project repository.

External Libraries

WorkSync uses the following open-source libraries:

Flask — local web application framework

pynput — keyboard and mouse input monitoring


External APIs & Datasets

The project uses:

No external datasets

No pretrained AI or machine learning models

No cloud-based APIs

No third-party analytics services


The core application logic and rule-based detection system run locally on the user's machine.

License

This project is licensed under the MIT License. See the LICENSE file for complete license terms.

Team Information

Team Name: KINETIX
Project: WorkSync
Hackathon: ASYNC'26
Track: Wellness & Lifestyle

Team Members:

1MS25CS080

1MS25CS092

1MS25CS123

1MS25CS124


