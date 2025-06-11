# Garden Designer Bot

Garden Designer Bot is a smart Streamlit application that helps you create a personalized garden blueprint based on your backyard photo and gardening preferences. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, this bot analyzes your garden image, identifies the landscape type, and generates a detailed markdown report with planting suggestions, layout ideas, and web-sourced inspiration links.

## Folder Structure

```
Garden-Designer-Bot/
├── garden-designer-bot.py
├── README.md
└── requirements.txt
```

* **garden-designer-bot.py**: The main Streamlit application.
* **requirements.txt**: Required Python packages.
* **README.md**: This documentation file.

## Features

* **Garden Preferences Form**
  Upload a clear photo of your garden or backyard and select key details like climate, lighting, watering needs, and garden usage.

* **AI-Powered Visual Analysis**
  A computer vision agent evaluates your photo to identify the landscape type, surface layout, vegetation density, sun exposure, and more.

* **Smart Garden Research**
  A second AI agent uses SerpAPI to find curated links to suitable plant types, garden layout inspirations, and hardscaping strategies based on your inputs.

* **Personalized Garden Design Report**
  A markdown-style report is generated that includes:

  * Visual insights from your garden photo
  * Layout and climate considerations
  * Garden usage strategy (relaxation, edible beds, play area, etc.)
  * Planting recommendations
  * Curated inspiration links from across the web

* **Clean Streamlit UI**
  Intuitive 3-column layout with sidebar API configuration ensures a smooth user experience.

* **Download Option**
  Save your garden design plan as a `.md` file to keep recommendations and resources accessible.

## Prerequisites

* Python 3.11 or higher
* An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))
* A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/akash301191/Garden-Designer-Bot.git
   cd Garden-Designer-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:

   ```bash
   streamlit run garden-designer-bot.py
   ```

2. **In your browser**:

   * Enter your OpenAI and SerpAPI keys in the sidebar.
   * Upload a photo of your backyard or garden.
   * Select lighting, climate, garden use, and watering preferences.
   * Click **🌿 Generate Garden Design Report**.
   * View and download a tailored garden report with layout and planting insights.

3. **Download Option**
   Use the **📥 Download Garden Report** button to save your personalized garden blueprint.

## Code Overview

* **`render_sidebar()`**
  Collects OpenAI and SerpAPI keys through the sidebar.

* **`render_garden_preferences()`**
  Gathers user inputs such as garden photo, climate zone, lighting, garden use, and watering comfort.

* **`generate_garden_report()`**

  * Uses a `Landscape Visual Analyzer` agent to evaluate garden image.
  * Uses a `Garden Research Assistant` to find inspiration links via SerpAPI.
  * Uses a `Garden Report Generator` to compile a markdown-formatted garden report.

* **`main()`**
  Sets up the layout, coordinates form rendering, runs agents, and displays/downloads the final report.

## Contributions

Contributions are welcome! If you'd like to improve features, fix bugs, or suggest enhancements, feel free to fork the repo, raise an issue, or submit a pull request. Please make sure your changes are clear, tested, and align with the purpose of the project.
