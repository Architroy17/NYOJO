#Created By Archit Roy

#importing libraries and modules
import pyaudio #audio input output
import wave #reading, writing .wav files
import time #time related operations
import threading #for multithreading like tinker window simultaneously
import whisper # audio to text transcription
from pynput import keyboard #interacting with keyboard, listed to Enter etc
import google.generativeai as palm #generate content
from gtts import gTTS #text to speach
from pydub import AudioSegment #for audio processing such as increaing speed to make it more humane
import os #interact with os such as delete file after creation
import pygame # audio playback
import requests
from bs4 import BeautifulSoup #web scraping
from newsapi import NewsApiClient #getting latest news
from word2number import w2n # converting transcribed wrd to numbe







# to record the audio
class VoiceRecorder:
    """
    The VoiceRecorder class handles audio recording, saving, and transcription.
    """
    def __init__(self):
        #Initializes a VoiceRecorder object with default values.
        self.recording = False
        self.audio_file = "voice_recording.wav"
        self.recording_thread = None
        print()
        print("**************************************************************")
        print()
        #print("press enter to start recording")
        print()

    def start_recording(self):
        #start recording
        self.recording = True
        self.frames = [] #store audio frames
        self.start_time = time.time()
        self.recording_thread = threading.Thread(target=self.record)
        self.recording_thread.start()
        print("Recording started, Press Enter to stop recording.")
        print()

    def stop_recording(self):
        #stop recording
        self.recording = False

    def record(self):

        #Records audio using PyAudio and saves it to a WAV file. Also transcribes the audio using the Whisper library.
        #Returns:- The transcribed text.

        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, #indicates that each audio sample is represented as a 16-bit integer. This is a common format for audio recording and playback.
                            channels=1,
                            rate=48000,
                            input=True,
                            frames_per_buffer=1024) #The size of the buffer can affect the latency and performance of audio processing.
        
        while self.recording:
            data = stream.read(1024)
            self.frames.append(data)
            # self.update_timer()
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        #to save audio to transcribe it
        self.save_audio()
        return self.transcribe_audio()


    def save_audio(self):
        #save audio as .wav file
        sound_file = wave.open(self.audio_file, "wb")
        sound_file.setnchannels(1) #set autio to monaural(single channel) and not stereo(2 channel)
        sound_file.setsampwidth(2) #num of bytes to represent each audio sample, more means more amplitude but larger file size
        sound_file.setframerate(48000) #frame rate is crucial for determining the duration of the audio and the pitch of the sound. 
        #normal=44100 but using more here for more clarity
        sound_file.writeframes(b"".join(self.frames))
        sound_file.close()
        print()
        print("**************************************************************")
        print()
        

    def transcribe_audio(self):
        #using locally installed openai's opensource whisper to transcribe audio
        model = whisper.load_model("base.en")# base model to keep it fast but accurate
        result = model.transcribe(self.audio_file, language="en", fp16=False)
        user_response = result["text"]
        # print("Transcription:", user_response)
        return user_response.lower()




# Function to handle voice recording and transcription
#has error handeling as most error prone area of code like not preoperly recorded

def record_and_transcribe():
    print()
    #print("Type Your Input Below or press Enter to speak :")
    user_input = input("Type Your Input Below or press Enter to speak : ")
    print()

    if user_input.strip() == "":
        # Initialize VoiceRecorder object
        voice_recorder = VoiceRecorder()

        # Callback function for the release of the Enter key
        def on_key_release(key):
            if key == keyboard.Key.enter:
                if not voice_recorder.recording:
                    try:
                        # Start recording if not already recording
                        voice_recorder.start_recording()
                    except Exception as e:
                        # Handle and log any errors during recording start
                        print("Error starting recording:", str(e))

                        text_to_audio("Sorry, I couldn't start recording. Please try again.")
                else:
                    try:
                        # Stop recording if currently recording
                        voice_recorder.stop_recording()
                        return False
                    except Exception as e:
                        # Handle and log any errors during recording stop
                        print("Error stopping recording:", str(e))

                        text_to_audio("Sorry, I couldn't stop recording. Please try again.")

        try:
            # Set up keyboard listener with the defined callback function
            with keyboard.Listener(on_release=on_key_release) as listener:
                listener.join()
        except Exception as e:
            # Handle and log any errors with the keyboard listener
            print("Error with keyboard listener:", str(e))

            text_to_audio("Sorry, there was an issue with the keyboard listener. Please try again.")

        try:
            # Transcribe the recorded audio
            return voice_recorder.transcribe_audio()
        except Exception as e:
            # Handle and log any errors during transcription
            print("Error during transcription:", str(e))

            text_to_audio("Sorry, there was an issue with transcription. Please try again.")
   

    return user_input















#TTS
#Converts text to audio and plays the generated speech with adjusted speed.
def text_to_audio(text, speed=1.0):
    # Initialize the gTTS object with the text
    tts = gTTS(text)
    # Check if the output file already exists and remove it
    if os.path.exists("output.mp3"):
        os.remove("output.mp3")

    # Save the generated speech to a file
    tts.save("output.mp3")

    # Use pydub to adjust the speech speed
    audio = AudioSegment.from_mp3("output.mp3")
    # Speed up the speech by the specified factor
    audio = audio.speedup(playback_speed=1.5)
    audio.export("output_fast.mp3", format="mp3")

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load and play the generated speech with adjusted speed
    pygame.mixer.music.load("output_fast.mp3")
    pygame.mixer.music.play()

    # Wait for the speech to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up by removing temp files
    pygame.mixer.quit()
    os.remove("output.mp3")
    os.remove("output_fast.mp3")



# func to get the latest top 10 news vai news api
def getnews():
    
    # get news, store in lists for further use as per need
    titles = []
    descriptions = []
    urls = []
    content=[]
    #parameters for customising
    countries_iso_mapping = {
    'Afghanistan': 'af',
    'Albania': 'al',
    'Algeria': 'dz',
    'Andorra': 'ad',
    'Angola': 'ao',
    'Antigua and Barbuda': 'ag',
    'Argentina': 'ar',
    'Armenia': 'am',
    'Australia': 'au',
    'Austria': 'at',
    'Azerbaijan': 'az',
    'Bahamas': 'bs',
    'Bahrain': 'bh',
    'Bangladesh': 'bd',
    'Barbados': 'bb',
    'Belarus': 'by',
    'Belgium': 'be',
    'Belize': 'bz',
    'Benin': 'bj',
    'Bhutan': 'bt',
    'Bolivia': 'bo',
    'Bosnia and Herzegovina': 'ba',
    'Botswana': 'bw',
    'Brazil': 'br',
    'Brunei': 'bn',
    'Bulgaria': 'bg',
    'Burkina Faso': 'bf',
    'Burundi': 'bi',
    'Cabo Verde': 'cv',
    'Cambodia': 'kh',
    'Cameroon': 'cm',
    'Canada': 'ca',
    'Central African Republic': 'cf',
    'Chad': 'td',
    'Chile': 'cl',
    'China': 'cn',
    'Colombia': 'co',
    'Comoros': 'km',
    'Congo (Congo-Brazzaville)': 'cg',
    'Costa Rica': 'cr',
    'Croatia': 'hr',
    'Cuba': 'cu',
    'Cyprus': 'cy',
    'Czechia (Czech Republic)': 'cz',
    'Denmark': 'dk',
    'Djibouti': 'dj',
    'Dominica': 'dm',
    'Dominican Republic': 'do',
    'Ecuador': 'ec',
    'Egypt': 'eg',
    'El Salvador': 'sv',
    'Equatorial Guinea': 'gq',
    'Eritrea': 'er',
    'Estonia': 'ee',
    'Eswatini (fmr. "Swaziland")': 'sz',
    'Ethiopia': 'et',
    'Fiji': 'fj',
    'Finland': 'fi',
    'France': 'fr',
    'Gabon': 'ga',
    'Gambia': 'gm',
    'Georgia': 'ge',
    'Germany': 'de',
    'Ghana': 'gh',
    'Greece': 'gr',
    'Grenada': 'gd',
    'Guatemala': 'gt',
    'Guinea': 'gn',
    'Guinea-Bissau': 'gw',
    'Guyana': 'gy',
    'Haiti': 'ht',
    'Holy See': 'va',
    'Honduras': 'hn',
    'Hungary': 'hu',
    'Iceland': 'is',
    'India': 'in',
    'Indonesia': 'id',
    'Iran': 'ir',
    'Iraq': 'iq',
    'Ireland': 'ie',
    'Israel': 'il',
    'Italy': 'it',
    'Jamaica': 'jm',
    'Japan': 'jp',
    'Jordan': 'jo',
    'Kazakhstan': 'kz',
    'Kenya': 'ke',
    'Kiribati': 'ki',
    'Kuwait': 'kw',
    'Kyrgyzstan': 'kg',
    'Laos': 'la',
    'Latvia': 'lv',
    'Lebanon': 'lb',
    'Lesotho': 'ls',
    'Liberia': 'lr',
    'Libya': 'ly',
    'Liechtenstein': 'li',
    'Lithuania': 'lt',
    'Luxembourg': 'lu',
    'Madagascar': 'mg',
    'Malawi': 'mw',
    'Malaysia': 'my',
    'Maldives': 'mv',
    'Mali': 'ml',
    'Malta': 'mt',
    'Marshall Islands': 'mh',
    'Mauritania': 'mr',
    'Mauritius': 'mu',
    'Mexico': 'mx',
    'Micronesia': 'fm',
    'Moldova': 'md',
    'Monaco': 'mc',
    'Mongolia': 'mn',
    'Montenegro': 'me',
    'Morocco': 'ma',
    'Mozambique': 'mz',
    'Myanmar (formerly Burma)': 'mm',
    'Namibia': 'na',
    'Nauru': 'nr',
    'Nepal': 'np',
    'Netherlands': 'nl',
    'New Zealand': 'nz',
    'Nicaragua': 'ni',
    'Niger': 'ne',
    'Nigeria': 'ng',
    'North Korea': 'kp',
    'North Macedonia': 'mk',
    'Norway': 'no',
    'Oman': 'om',
    'Pakistan': 'pk',
    'Palau': 'pw',
    'Palestine State': 'ps',
    'Panama': 'pa',
    'Papua New Guinea': 'pg',
    'Paraguay': 'py',
    'Peru': 'pe',
    'Philippines': 'ph',
    'Poland': 'pl',
    'Portugal': 'pt',
    'Qatar': 'qa',
    'Romania': 'ro',
    'Russia': 'ru',
    'Rwanda': 'rw',
    'Saint Kitts and Nevis': 'kn',
    'Saint Lucia': 'lc',
    'Saint Vincent and the Grenadines': 'vc',
    'Samoa': 'ws',
    'San Marino': 'sm',
    'Sao Tome and Principe': 'st',
    'Saudi Arabia': 'sa',
    'Senegal': 'sn',
    'Serbia': 'rs',
    'Seychelles': 'sc',
    'Sierra Leone': 'sl',
    'Singapore': 'sg',
    'Slovakia': 'sk',
    'Slovenia': 'si',
    'Solomon Islands': 'sb',
    'Somalia': 'so',
    'South Africa': 'za',
    'South Korea': 'kr',
    'South Sudan': 'ss',
    'Spain': 'es',
    'Sri Lanka': 'lk',
    'Sudan': 'sd',
    'Suriname': 'sr',
    'Sweden': 'se',
    'Switzerland': 'ch',
    'Syria': 'sy',
    'Tajikistan': 'tj',
    'Tanzania': 'tz',
    'Thailand': 'th',
    'Timor-Leste': 'tl',
    'Togo': 'tg',
    'Tonga': 'to',
    'Trinidad and Tobago': 'tt',
    'Tunisia': 'tn',
    'Turkey': 'tr',
    'Turkmenistan': 'tm',
    'Tuvalu': 'tv',
    'Uganda': 'ug',
    'Ukraine': 'ua',
    'United Arab Emirates': 'ae',
    'United Kingdom': 'gb',
    'United States': 'us',
    'Uruguay': 'uy',
    'Uzbekistan': 'uz',
    'Vanuatu': 'vu',
    'Venezuela': 've',
    'Vietnam': 'vn',
    'Yemen': 'ye',
    'Zambia': 'zm',
    'Zimbabwe': 'zw',
    }
    
    print()
    print()
    print()
    #basic flow is print options, get input from user via voice, transcribe, convert to req format and use in api call
    
    #getting user input
    
    print("Please say the name of the country you want to hear news from else you can also hear from all around the globe: ")
    print("For Example you can say India, United States, South Korea or World Wide")
    text_to_audio("Please say the name of the country you want to hear news from else you can also hear from all around the globe For Example you can say India, United States, South Korea or World Wide")
    print()
    country=record_and_transcribe()
    print("You said: ",country)
    print()
    print()
    if country in countries_iso_mapping:
        country = countries_iso_mapping[country]
    else:
        country = None
    
    print("Is there any specific topic you want news on or you want the general? ")
    print("For Example you can say Bitcoin, war, vaccine or NOTHING")
    text_to_audio("Is there any specific topic you want news on or you want the general? For Example you can say Bitcoin, war, vaccnie or NOTHING")
    print()
    topic = record_and_transcribe()
    print("You said: ",topic)
    print()
    print()
    if topic=="none" or topic=="nothing":
        topic=None
        
    print("Is there any specific category you want news on or you want the general? ")
    print("You can Choose from:")
    print("- Business")
    print("- Entertainment")
    print("- General")
    print("- Health")
    print("- Science")
    print("- Sports")
    print("- Technology")
    print("OR NONE")
    text_to_audio("Is there any specific category you want news on or you want the general? You can choose from: Business, Entertainment, General, Health, Science, Sports, Technology, or NONE.")
    print()
    
    category_list=['buisness','entertainment','general',' health','science','sports','technology']
    category = record_and_transcribe()
    print("You said: ",category)
    print()
    print()
    if category not in category_list:
        category=None
    # categories business entertainment general health science sports technology
    
    
    print()
    print("Please Enter How Many news articles you want(for trial recommend 1-3): ")
    text_to_audio("Please Enter How Many news articles you want for trial recommend 1-3: ")
    print()
    number=record_and_transcribe()
    print("You said: ",number)
    converted_number = w2n.word_to_num(number.lstrip().strip('.'))
    print()
    print()
    
    #getting latest news

    # Init
    newsapi = NewsApiClient(api_key='Enter Your Key or use env var')

    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(q=topic,
                                            sources=None,
                                            category=category,
                                            language='en',
                                            country=country)
    print()
    # print("api")
    # print(top_headlines)
    # print()

    # Extract and print headlines
    #extract and format data
    news_counter = 0
    if 'articles' in top_headlines:
        articles = top_headlines['articles']
        for article in articles:
            if 'title' in article and article['title']!= None :
                titles.append(article['title'].lstrip().rstrip())
            else:
                titles.append(" ")
            if 'description' in article and article['description']!= None:
                descriptions.append(article['description'].lstrip().rstrip())
            else:
                descriptions.append(" ")
            if 'url' in article and article['url']!= None:
                urls.append(article['url'].lstrip().rstrip())
            else:
                urls.append(" ")
            if 'content' in article and article['content']!= None:
                content.append(article['content'])
            else:
                content.append(" ")
            news_counter += 1
            # Check if 10 news articles have been added
            if news_counter >= converted_number:
                break



    # Return the lists
    return titles, descriptions, urls,content


def get_news_details(title, url, max_length=12000):
    # web scraping
    try:
        # Google search URL
        google_search_url = f'https://www.google.com/search?q={title}'
        response_google = requests.get(google_search_url)
        html_content_google = response_google.content
        soup_google = BeautifulSoup(html_content_google, 'html.parser')

        # Get text from the Google search soup
        text_google = soup_google.get_text(strip=True, separator='\n')
        text_google_lines = text_google.split('\n')

        # Generic URL
        #getting more text from the news article directly
        response_generic = requests.get(url)
        html_content_generic = response_generic.content
        soup_generic = BeautifulSoup(html_content_generic, 'html.parser')

        # Get text from the generic URL soup
        text_generic = soup_generic.get_text(strip=True, separator='\n')
        #text_generic_lines = text_generic.split('\n')

        # Truncate generic_url_text to a maximum length
        truncated_generic_url_text = truncate_string(text_generic, max_length)

        return {
            'google_search_text': text_google_lines,
            'generic_url_text': truncated_generic_url_text
        }

    except Exception as e:
        # Handle any errors that might occur during the process
        print(f"Error fetching content: {str(e)}")
        return {
            'generic_url_text': [],
            'google_search_text': []
        }









def truncate_string(input_string, max_length):
    if len(input_string) <= max_length:
        return input_string
    else:
        return input_string[:max_length]













################main function###############################


def main():
    # ... (existing code)

    # Set up AI configuration
    key='Your palm api key'
    palm.configure(api_key=key)
    #model_id = 'models/chat-bison-001'
    
    examples=[]
    #    examples=[('next', 'Moving on'),
    # ('System: Russia Announces Successful Test of Hypersonic Missile\nRussia declared a successful test of a new hypersonic missile, claiming it can travel at Mach 7 and evade enemy defenses. The test was conducted in a remote area, and details are emerging about its capabilities.\nhttps://www.example.com/russia-hypersonic-test\nThe Russian Ministry of Defense announced the successful test, highlighting its potential impact on global military capabilities.\nArticle Content: Detailed information about the hypersonic missile\'s specifications, capabilities, and potential geopolitical implications.',
    #  'TITLE: Russia\'s Successful Test of Hypersonic Missile\nDESC: Russia declared a successful test of a new hypersonic missile, claiming it can travel at Mach 7 and evade enemy defenses. The test was conducted in a remote area, and details are emerging about its capabilities.'),
    # ('User: What are the potential implications of Russia\'s new hypersonic missile on global military dynamics?',
    #  'User: What are the potential implications of Russia\'s new hypersonic missile on global military dynamics?\nAI: The new hypersonic missile could shift the balance of power, offering Russia a strategic advantage. It raises concerns about the arms race and the need for other nations to enhance their defense capabilities.'),
    # ('System: Tech Giant XYZ Unveils Breakthrough in Quantum Computing\nTech giant XYZ has revealed a major breakthrough in quantum computing, claiming a significant increase in processing power. The company aims to revolutionize various industries with this advancement.\nhttps://www.example.com/xyz-quantum-breakthrough\nThe breakthrough centers around a new quantum processor architecture, promising faster and more efficient computations.\nArticle Content: Detailed information on the quantum computing breakthrough, its potential applications, and reactions from experts in the field.',
    #  'TITLE: Tech Giant XYZ Unveils Breakthrough in Quantum Computing\nDESC: Tech giant XYZ has revealed a major breakthrough in quantum computing, claiming a significant increase in processing power. The company aims to revolutionize various industries with this advancement.'),
    # ('User: How could this quantum computing breakthrough impact industries, and what are the key features of the new quantum processor architecture?',
    #  'User: How could this quantum computing breakthrough impact industries, and what are the key features of the new quantum processor architecture?\nAI: The breakthrough could revolutionize industries by enabling faster and more efficient computations, impacting fields like finance, healthcare, and logistics. The new quantum processor architecture emphasizes increased processing power and efficiency, ushering in a new era of computing.'),
    # ('System: Global Leaders Gather for Climate Summit in Paris\nWorld leaders convene in Paris for a crucial climate summit to address escalating environmental challenges. The summit focuses on collaborative efforts to reduce carbon emissions, foster sustainable practices, and mitigate the impacts of climate change.\nhttps://www.example.com/climate-summit-paris\nCoverage includes key speeches, proposed initiatives, and expectations for global cooperation.\nArticle Content: Detailed coverage of the climate summit, discussions on climate action, and potential outcomes.',
    #  'TITLE: Global Leaders Gather for Climate Summit in Paris\nDESC: World leaders convene in Paris for a crucial climate summit to address escalating environmental challenges. The summit focuses on collaborative efforts to reduce carbon emissions, foster sustainable practices, and mitigate the impacts of climate change.'),
    # ('User: What specific initiatives are being proposed at the climate summit, and how do they plan to reduce carbon emissions?',
    #  'User: What specific initiatives are being proposed at the climate summit, and how do they plan to reduce carbon emissions?\nAI: The summit proposes a range of initiatives, including stricter emission targets, investments in renewable energy, and international cooperation on climate-friendly technologies. The goal is to collectively reduce carbon emissions and promote sustainable practices globally.'),
    # ('System: Breakthrough in Medical Research Offers Potential Cure for Rare Disease\nA breakthrough in medical research brings hope for a potential cure for a rare genetic disease. Scientists have discovered a novel treatment approach that targets the root cause of the disease, showing promising results in preclinical trials.\nhttps://www.example.com/medical-research-breakthrough\nThe breakthrough has significant implications for patients affected by this rare genetic disorder.\nArticle Content: In-depth coverage of the medical breakthrough, details on the treatment approach, and insights from researchers.',
    #  'TITLE: Breakthrough in Medical Research Offers Potential Cure for Rare Disease\nDESC: A breakthrough in medical research brings hope for a potential cure for a rare genetic disease. Scientists have discovered a novel treatment approach that targets the root cause of the disease, showing promising results in preclinical trials.'),
    # ('User: Can you provide more details about the treatment approach and its potential impact on patients with the rare genetic disease?',
    #  'User: Can you provide more details about the treatment approach and its potential impact on patients with the rare genetic disease?\nAI: The treatment approach involves targeting the root cause of the genetic disease, showing promising results in preclinical trials. If successful, it could offer a potential cure and significantly improve the quality of life for patients affected by this rare genetic disorder.'),
    # ('System: Space Exploration Milestone: Human Crew Successfully Orbits Mars\nIn a historic space exploration achievement, a human crew successfully completes an orbit around Mars. The mission, conducted by a collaboration of international space agencies, marks a significant milestone in human space exploration.\nhttps://www.example.com/space-exploration-mars-orbit\nDetails include mission objectives, crew profiles, and the broader implications for future space exploration.\nArticle Content: Comprehensive coverage of the space exploration milestone, insights from astronauts, and the global significance of human Mars orbit.',
    #  'TITLE: Space Exploration Milestone: Human Crew Successfully Orbits Mars\nDESC: In a historic space exploration achievement, a human crew successfully completes an orbit around Mars. The mission, conducted by a collaboration of international space agencies, marks a significant milestone in human space exploration.'),
    # ('User: What were the mission objectives, and how does this human Mars orbit impact future space exploration?',
    #  'User: What were the mission objectives, and how does this human Mars orbit impact future space exploration?\nAI: The mission aimed to achieve a human orbit around Mars, providing valuable data for future manned missions. The success of this milestone opens possibilities for extended space exploration missions, setting the stage for potential human missions to Mars in the future.'),
    # ('System: Breakthrough in Renewable Energy: Solar Panel Efficiency Surpasses 30%\nResearchers announce a groundbreaking achievement in renewable energy as solar panel efficiency surpasses 30%. The breakthrough is expected to significantly improve the viability of solar energy as a mainstream power source.\nhttps://www.example.com/renewable-energy-solar-breakthrough\nCoverage includes the technical aspects of the breakthrough, potential applications, and industry reactions.\nArticle Content: Detailed information on the solar panel efficiency breakthrough, its implications for renewable energy, and expert opinions.',
    #  'TITLE: Breakthrough in Renewable Energy: Solar Panel Efficiency Surpasses 30%\nDESC: Researchers announce a groundbreaking achievement in renewable energy as solar panel efficiency surpasses 30%. The breakthrough is expected to significantly improve the viability of solar energy as a mainstream power source.'),
    # ('User: How does this breakthrough in solar panel efficiency impact the broader adoption of solar energy, and what are the technical aspects of the achievement?',
    #  'User: How does this breakthrough in solar panel efficiency impact the broader adoption of solar energy, and what are the technical aspects of the achievement?\nAI: The breakthrough enhances the viability of solar energy by surpassing 30% efficiency, making it more competitive with traditional energy sources. Technical aspects include improvements in photovoltaic cell design, allowing for increased energy conversion rates and broader applications in various industries.'),
    # ('System: International Collaboration on Vaccine Research Targets Emerging Infectious Diseases\nCountries worldwide join forces in an international collaboration to accelerate vaccine research and development for emerging infectious diseases. The initiative aims to enhance global preparedness and response to potential pandemics.\nhttps://www.example.com/international-vaccine-collaboration\nDetails cover participating countries, research focus areas, and the significance of this collaborative effort.\nArticle Content: In-depth coverage of the international collaboration on vaccine research, its potential impact on global health, and insights from leading researchers.',
    #  'TITLE: International Collaboration on Vaccine Research Targets Emerging Infectious Diseases\nDESC: Countries worldwide join forces in an international collaboration to accelerate vaccine research and development for emerging infectious diseases. The initiative aims to enhance global preparedness and response to potential pandemics.'),
    # ('User: Which countries are participating in the international collaboration on vaccine research, and what are the research focus areas?',
    #  'User: Which countries are participating in the international collaboration on vaccine research, and what are the research focus areas?\nAI: Multiple countries are participating in the collaboration, pooling resources for vaccine research. Research focus areas include developing vaccines for emerging infectious diseases to enhance global preparedness and response to potential pandemics.'),
    # ('System: Advancements in Artificial Intelligence Lead to Breakthroughs in Medical Diagnostics\nSignificant advancements in artificial intelligence (AI) contribute to breakthroughs in medical diagnostics. AI algorithms demonstrate high accuracy in detecting various medical conditions, revolutionizing the field of diagnostic medicine.\nhttps://www.example.com/ai-medical-diagnostics\nCoverage includes specific applications, benefits, and potential challenges associated with integrating AI into medical diagnostics.\nArticle Content: Detailed information on AI advancements in medical diagnostics, specific applications, and expert opinions on the transformative impact.',
    #  'TITLE: Advancements in Artificial Intelligence Lead to Breakthroughs in Medical Diagnostics\nDESC: Significant advancements in artificial intelligence (AI) contribute to breakthroughs in medical diagnostics. AI algorithms demonstrate high accuracy in detecting various medical conditions, revolutionizing the field of diagnostic medicine.'),
    # ('User: What specific medical conditions can AI algorithms detect, and what are the potential benefits and challenges of integrating AI into medical diagnostics?',
    #  'User: What specific medical conditions can AI algorithms detect, and what are the potential benefits and challenges of integrating AI into medical diagnostics?\nAI: AI algorithms can detect a range of medical conditions with high accuracy. The potential benefits include improved diagnostic accuracy, early disease detection, and personalized treatment plans. Challenges include ethical considerations, data privacy concerns, and the need for rigorous validation of AI algorithms in clinical settings.'),
    # ('System: Major Tech Companies Unveil Collaborative Initiative for Ethical AI Development\nLeading tech companies announce a collaborative initiative to prioritize ethical artificial intelligence (AI) development. The initiative aims to establish guidelines, share best practices, and promote transparency in AI technologies.\nhttps://www.example.com/tech-companies-ethical-ai\nDetails include the participating companies, key focus areas, and the significance of fostering ethical AI.\nArticle Content: Comprehensive coverage of the collaborative initiative for ethical AI development, insights from industry leaders, and potential impacts on the tech landscape.',
    #  'TITLE: Major Tech Companies Unveil Collaborative Initiative for Ethical AI Development\nDESC: Leading tech companies announce a collaborative initiative to prioritize ethical artificial intelligence (AI) development. The initiative aims to establish guidelines, share best practices, and promote transparency in AI technologies.'),
    # ('User: Which tech companies are participating in the collaborative initiative for ethical AI development, and what are the key focus areas of this initiative?',
    #  'User: Which tech companies are participating in the collaborative initiative for ethical AI development, and what are the key focus areas of this initiative?\nAI: Several major tech companies are participating, working together to establish guidelines, share best practices, and promote transparency in AI technologies. The key focus areas include ethical considerations in AI algorithms, responsible data usage, and addressing potential biases in AI systems.'),
    # ('System: Breakthrough in Clean Energy: Advanced Fusion Reactor Achieves Sustainable Power Generation\nScientists achieve a breakthrough in clean energy with an advanced fusion reactor that demonstrates sustainable power generation. The innovative technology holds the potential to revolutionize the global energy landscape.\nhttps://www.example.com/clean-energy-fusion-reactor\nDetails cover the technical aspects of the fusion reactor, potential applications, and expert perspectives on its significance.\nArticle Content: In-depth coverage of the breakthrough in clean energy, insights from scientists, and the transformative impact of advanced fusion reactor technology.',
    #  'TITLE: Breakthrough in Clean Energy: Advanced Fusion Reactor Achieves Sustainable Power Generation\nDESC: Scientists achieve a breakthrough in clean energy with an advanced fusion reactor that demonstrates sustainable power generation. The innovative technology holds the potential to revolutionize the global energy landscape.'),
    # ('User: Can you provide more details about the technical aspects of the advanced fusion reactor and its potential applications in the global energy landscape?',
    #  'User: Can you provide more details about the technical aspects of the advanced fusion reactor and its potential applications in the global energy landscape?\nAI: The advanced fusion reactor involves innovative technology for sustainable power generation. Technical aspects include controlled nuclear fusion, which has the potential to provide clean and abundant energy. Potential applications range from meeting global energy demands to reducing reliance on traditional fossil fuels.'),
    # ('System: Global Health Organizations Collaborate to Combat Emerging Infectious Disease Threat\nInternational health organizations join forces in a collaborative effort to combat the threat of emerging infectious diseases. The initiative focuses on early detection, rapid response, and global coordination to prevent potential pandemics.\nhttps://www.example.com/global-health-collaboration-infectious-disease\nDetails include the participating organizations, key strategies, and the importance of global cooperation in public health.\nArticle Content: Comprehensive coverage of the global health organizations collaborative effort, insights from health experts, and potential impacts on global public health.',
    #  'TITLE: Global Health Organizations Collaborate to Combat Emerging Infectious Disease Threat\nDESC: International health organizations join forces in a collaborative effort to combat the threat of emerging infectious diseases. The initiative focuses on early detection, rapid response, and global coordination to prevent potential pandemics.'),
    # ('User: Which health organizations are participating in the collaborative effort to combat emerging infectious diseases, and what are the key strategies employed?',
    #  'User: Which health organizations are participating in the collaborative effort to combat emerging infectious diseases, and what are the key strategies employed?\nAI: Several international health organizations are collaborating to combat emerging infectious diseases. Key strategies include early detection, rapid response, and global coordination to prevent potential pandemics. The collaborative effort aims to enhance global preparedness and response in the face of health threats.'),
    # ('System: Innovative Breakthrough in Space Exploration: Solar Sail Propulsion Successfully Tested\nIn a groundbreaking achievement, scientists successfully test solar sail propulsion for space exploration. The innovative technology harnesses the power of sunlight for propulsion, opening new possibilities for long-duration space missions.\nhttps://www.example.com/space-exploration-solar-sail\nDetails include the mechanics of solar sail propulsion, potential applications, and expert opinions on the future of space exploration.\nArticle Content: Detailed coverage of the innovative breakthrough in space exploration, insights from scientists, and the transformative impact of solar sail propulsion technology.',
    #  'TITLE: Innovative Breakthrough in Space Exploration: Solar Sail Propulsion Successfully Tested\nDESC: In a groundbreaking achievement, scientists successfully test solar sail propulsion for space exploration. The innovative technology harnesses the power of sunlight for propulsion, opening new possibilities for long-duration space missions.'),
    # ('User: Can you explain how solar sail propulsion works and its potential applications in space exploration?',
    #  'User: Can you explain how solar sail propulsion works and its potential applications in space exploration?\nAI: Solar sail propulsion harnesses the power of sunlight for propulsion, utilizing the pressure of sunlight on large reflective sails. Potential applications include long-duration space missions, as this technology offers a continuous and sustainable method of propulsion without the need for traditional fuel sources.'),
    # ('System: Global Effort to Address Plastic Pollution: New Biodegradable Plastic Technology Unveiled\nA global initiative is underway to address plastic pollution as scientists unveil a new biodegradable plastic technology. The innovative technology promises to reduce the environmental impact of plastic waste and revolutionize the plastic industry.\nhttps://www.example.com/plastic-pollution-biodegradable-technology\nDetails cover the science behind the biodegradable plastic, potential applications, and environmental benefits.\nArticle Content: In-depth coverage of the global effort to address plastic pollution, insights from scientists, and the potential impact of new biodegradable plastic technology.',
    #  'TITLE: Global Effort to Address Plastic Pollution: New Biodegradable Plastic Technology Unveiled\nDESC: A global initiative is underway to address plastic pollution as scientists unveil a new biodegradable plastic technology. The innovative technology promises to reduce the environmental impact of plastic waste and revolutionize the plastic industry.'),
    # ('User: How does the new biodegradable plastic technology work, and what are the potential applications and environmental benefits?',
    #  'User: How does the new biodegradable plastic technology work, and what are the potential applications and environmental benefits?\nAI: The new biodegradable plastic technology breaks down more easily in the environment, reducing the impact of plastic pollution. It has various potential applications, from packaging to disposable items. The environmental benefits include a significant decrease in plastic waste and a positive impact on ecosystems.')]

    


    
    conversation = []

    # Introductory prompt for the News Presenter
    intro_prompt = '''
    YOU ARE A NEWS PRESENTER ON LIVE TELEVISIOIN
    reply under 100 words
    get into the role of a news presenter from right now, no need to acknowlege to this propt as sure etc, just begin presenting
    You are the News Presenter in the NewsChat project. Your role is to present news articles to the "user",
    providing a concise summary of each article. Here's how the process works:
        
        1. The system will ask the user for their preferences, such as a specific topic, category, or general news.
        2. Using the NewsAPI, the system will fetch a list of top headlines, along with brief descriptions and URLs to the articles.
        3. The system will then perform web scraping to gather more details about each article.
        4. All gathered information, including the headline, brief description, article URL, and additional details from web scraping,
            will be provided to you as input starting with 'System:', there might be some useless info there due to web scraping, ignore it.
        5. When the input begins with 'System:', it means it's all the information about a particular news article.
            Your task is to start presenting the entire news to the user. Provide a summary of what happened, why it
            happened, and any other relevant information. Keep it concise and engaging.
        6. If the input begins with 'User:', it indicates a follow-up question from the user.
            Your role is to answer these questions as accurately and informatively as possible.
            
    Remember to keep your responses clear, concise, and engaging. Aim to provide valuable
        information to the user while maintaining a conversational tone. If you have any questions
        or need clarification during the conversation, feel free to ask. Do your best, and thank you
        for being the News Presenter in this project!
        
    Reply now with an intro to the user as a news presenter no "Sure, here is a summary of the article" etc, 
    JUST begin with the presentation of title and then details
    
    BE Breif in about 100 words only, dont exceed unless necessary
    
    present in this format:
        title: use original or create own
        details: give breif summary of what happened
        
        
        here is an example
        ('System: Russia Announces Successful Test of Hypersonic Missile\nRussia declared a successful test of a new hypersonic missile, claiming it can travel at Mach 7 and evade enemy defenses. The test was conducted in a remote area, and details are emerging about its capabilities.\nhttps://www.example.com/russia-hypersonic-test\nThe Russian Ministry of Defense announced the successful test, highlighting its potential impact on global military capabilities.\nArticle Content: Detailed information about the hypersonic missile\'s specifications, capabilities, and potential geopolitical implications.',
            'TITLE: Russia\'s Successful Test of Hypersonic Missile\nDESC: Breaking news as Russia announces a successful test of a groundbreaking hypersonic missile, capable of reaching Mach 7 and evading enemy defenses. The test, conducted in a remote area, is shrouded in secrecy, with emerging details about the missile's specifications, capabilities, and potential geopolitical impact. The Russian Ministry of Defense underscores the significance of this achievement, hinting at a potential shift in global military capabilities. Stay tuned as we delve into the specifics of this game-changing development that could reshape the balance of power in the international arena.'),
            ('User: What are the potential implications of Russia\'s new hypersonic missile on global military dynamics?',
            'User: What are the potential implications of Russia\'s new hypersonic missile on global military dynamics?\nAI: The new hypersonic missile could shift the balance of power, offering Russia a strategic advantage. It raises concerns about the arms race and the need for other nations to enhance their defense capabilities.'),
        # 
    '''
    # conversation.append({'author': 'user', 'content': intro_prompt})

    # Get AI's response for the News Presenter's introduction
    # response = palm.chat(messages=conversation, temperature=0.8, context=intro_prompt, examples=examples)
    # ai_reply = response.messages[-1]['content']
    # print(ai_reply)
    # conversation.append({'author': 'AI', 'content': ai_reply})

    # Get the latest news
    titles, descriptions, urls, content = getnews()


    # Iterate through each news article
    for i in range(len(titles)):
        # Get additional details through web scraping
        conversation=[]
        news_details = get_news_details(titles[i], urls[i])
        #truncated_news_details = truncate_string(news_details.get('generic_url_text', ''), 15000)
        #print(news_details)
        print()
        print()
        

        # Configure AI with system prompt and context
        
        prompt = f'''System: {titles[i]}\n{descriptions[i]}\n{urls[i]}\n{content[i]}\nGoogle Search: {news_details.get('google_search_text', 'N/A')}\nArticle Content: {news_details.get('generic_url_text', 'N/A')}'''
        #prompt = f'''System: {titles[i]}\n{descriptions[i]}\n{urls[i]}\n{content[i]}\nArticle Content: {truncated_news_details}'''
        #prompt = f'''System: {titles[i]}\n{descriptions[i]}\n{urls[i]}\n{content[i]}\nArticle Content: {news_details.get('generic_url_text', 'N/A')}'''

        print()
        print()
        # Send the API request with the truncated prompt
        #prompt = f'''System: {titles[i]}\n{descriptions[i]}\n{urls[i]}\n{content[i]}\nGoogle Search: {news_details['google_search_text']}\nArticle Content: {news_details['generic_url_text']}'''
        conversation.append({'author': 'user', 'content': prompt})

        # Get AI's response for news presentation
        response = palm.chat(messages=conversation, 
                                temperature=0.3, \
                                context=intro_prompt , 
                                examples=examples)
        
        # ai_reply = response.messages[-1]['content']
        # conversation.append({'author': 'AI', 'content': ai_reply})

        # # Present news to the user
        # # print("System:", titles[i])
        # # print("Description:", descriptions[i])
        # # print("URL:", urls[i])
        # print("AI Presentation:")
        # print()
        # print(ai_reply)
        # #text_to_audio(ai_reply)
        # print()
        if response and response.messages:
            ai_reply = response.messages[-1]['content']
            if(ai_reply==None):
                break
            conversation.append({'author': 'AI', 'content': ai_reply})
    # Present news to the user
            print("NYOJO Presentation:")
            print()
            print(ai_reply)
            text_to_audio(ai_reply)
            print()
        else:
            print("Error: Unable to get a valid response from the AI model.")

        # User interaction loop
        while True:
            print("You can ask follow up questions or say next to move on to the next news")
            user_input = record_and_transcribe()  # For simplicity, replace this with your voice input code
            print(user_input)
            print()
            if user_input.lower() == 'next' or user_input.lower() == 'next.':
                # Move on to the next news article
                print()
                print()
                conversation=[]
                break
            elif user_input.lower() == 'goodbye':
                # End the program if the user says goodbye
                text_to_audio("Goodbye ")
                print("NYOJO: Goodbye ")
                return
            else:
                conversation.append({'author': 'user', 'content': user_input})
                # User asked a question, get AI's response
                response = palm.chat(messages=conversation, temperature=0.3, context=intro_prompt)
                ai_reply = response.messages[-1]['content']
                conversation.append({'author': 'AI', 'content': ai_reply})
                print("AI Reply:")
                print()
                print(ai_reply)
                text_to_audio(ai_reply)
                print()

    print("NYOJO: No more news articles. Goodbye!")
    return


main()

