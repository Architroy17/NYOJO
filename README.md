# NYOJO | Your Personal News Presenter

NYOJO is an innovative news presenter powered by Google's PaLM language model. It delivers personalized and up-to-date news while also allowing you to ask questions to get more detailed explanations and insights on the latest happenings. No more being left with unanswered questions—NYOJO is here to help!

NYOJO is a basic RAG created from scratch without using any already exiting frameworks/ libraries.

## Images

-user giving details for personalisation verbaly
![nyojo_1](https://github.com/user-attachments/assets/147ce550-a15e-40d1-8e1f-44aee6302c3e)
-nyojo presenting the article while communicating with the user
![nyojo_2](https://github.com/user-attachments/assets/66f69555-ff22-4c4c-ac74-00c838064925)
-user asking question 
![nyojo_3](https://github.com/user-attachments/assets/5a201bdc-9b10-4b96-858f-d8cffbde15f7)
-nyojo replying to question
![nyojo_4](https://github.com/user-attachments/assets/d8208ea0-3257-4ae9-9a5f-38a9716f702e)


## Features
- **Personalized News Delivery:** Get news tailored to your interests and preferences.
- **Interactive Q&A:** Ask questions about the news and get detailed responses to understand the context, impacts, and reasons behind the headlines.
- **Advanced AI Integration:** Powered by Google's PaLM, OpenAI Whisper for speech-to-text, and Google Text-to-Speech (gTTS).
- **Comprehensive News Sources:** Leverages NewsAPI and web scraping to fetch the most recent and relevant news from a variety of sources.
- **Iris Model Foundation:** Built upon the Iris model for enhanced performance and accuracy.





## Why NYOJO?
Many of us start our day with the news, but traditional news presentations often leave us with unanswered questions. NYOJO was created to solve this problem. With NYOJO, you can not only stay updated with the latest news but also dive deeper into the stories that matter to you, all without having to manually search for answers. It's a simple yet powerful example of how AI can enhance our daily lives, making information more accessible and our mornings a bit less hectic.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/nyojo.git
   ```
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your API keys for Google PaLM, NewsAPI, and other services in a `.env` file:
   ```bash
   GOOGLE_PALM_API_KEY=your_google_palm_api_key
   NEWS_API_KEY=your_news_api_key
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Start the application, and NYOJO will begin delivering news based on your preferences.
2. Use the voice input or text input feature to ask questions about the current news topic.
3. NYOJO will provide detailed explanations or additional context in response to your queries.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
