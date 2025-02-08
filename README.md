# Gemini Nutrition Tracking App

## Overview
The **Gemini Nutrition Tracking App** is a web application built using Streamlit and Google's Gemini API. The app allows users to upload or select an image of food and receive detailed nutritional information, including a calorie breakdown for each food item detected.

## Features
- Upload an image of food or select one from the sidebar.
- Uses **Google Gemini API** to analyze the image and extract nutritional details.
- Displays a structured breakdown of food items along with their respective calorie counts.
- User-friendly UI with a visually appealing background and layout.

## Technologies Used
- **Python** (Backend Logic)
- **Streamlit** (Web Framework)
- **Google Gemini API** (AI Model for Image Analysis)
- **PIL (Pillow)** (Image Processing)
- **Requests** (Fetching Images from URLs)
- **Dotenv** (Environment Variable Management)

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.7+
- Pip package manager

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repository.git
   cd Gemini-Nutrition-App
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up the environment variable for the **Google API Key**:
   - Create a `.env` file in the root directory.
   - Add your API key:
     ```sh
     GOOGLE_API_KEY=your_google_api_key_here
     ```

4. Run the application:
   ```sh
   streamlit run app.py
   ```

## Usage
1. Open the app in your browser.
2. Upload a food image or select one from the sidebar.
3. Click the **"Tell me about the total calories"** button.
4. The app will display a breakdown of food items and their calorie counts.

## File Structure
```
📂 Gemini-Nutrition-App
│── .env                   # Environment variables
│── app.py                 # Main application file
│── requirements.txt       # Required dependencies
│── README.md              # Documentation
```

## Future Improvements
- Improve accuracy of food item recognition.
- Add support for multiple AI models.
- Enhance UI with more interactive elements.
- Provide dietary recommendations based on calorie intake.

## License
This project is licensed under the MIT License.

## Acknowledgments
- [Streamlit](https://streamlit.io/) for the UI framework.
- [Google Gemini API](https://ai.google.dev/) for AI-powered image analysis.

---
Developed by **[Your Name]**

