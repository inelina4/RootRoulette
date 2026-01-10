import requests
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
import random
import json
import os

API_URL = "https://en.wiktionary.org/w/api.php"
HEADERS = {
    "User-Agent": "RR_LU_Bot/0.1"
}

class Status(Enum):
    SUCCESS = "S"
    ERROR = "E"
    NOT_FOUND = "N"

@dataclass
class EtymologyData:
    word: str
    text: str
    origin_languages: List[str]

@dataclass
class EtymologyResponse:
    status: Status
    message: str
    data: Optional[EtymologyData] = None

def get_etymology_info(word: str) -> EtymologyResponse:
    try:
        params = {
            "action": "parse",
            "page": word,
            "prop": "text",
            "format": "json"
        }
        r = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
        r.raise_for_status()
        
        response_json = r.json()
        
        if "error" in response_json:
            return EtymologyResponse(
                status=Status.NOT_FOUND,
                message=f"Page '{word}' not found on Wiktionary",
                data=None
            )
        
        html = response_json["parse"]["text"]["*"]
        soup = BeautifulSoup(html, "html.parser")
        
        # Find English section
        english = soup.find("h2", id="English")
        if not english:
            return EtymologyResponse(
                status=Status.NOT_FOUND,
                message=f"No English entry found for '{word}'",
                data=EtymologyData(word=word, text="", origin_languages=[])
            )
        
        etymology_heading = None
        for h in english.find_all_next(["h3", "h4"]):
            if h.get_text(strip=True).startswith("Etymology"):
                etymology_heading = h
                break
            if h.name == "h2":
                break
        
        if not etymology_heading:
            return EtymologyResponse(
                status=Status.NOT_FOUND,
                message=f"No etymology section found for '{word}'",
                data=EtymologyData(word=word, text="", origin_languages=[])
            )
        
        heading_container = etymology_heading.parent
        etymology_paragraphs = []
        origin_languages = []
        
        for el in heading_container.next_siblings:
            if isinstance(el, Tag) and el.name in ("div", "h2", "h3", "h4"):
                if el.find(["h2", "h3", "h4"]):
                    break
            if isinstance(el, Tag) and el.name == "p":
                etymology_paragraphs.append(el.get_text(" ", strip=True))
                for span in el.select("span.etyl a"):
                    name = span.get_text(strip=True)
                    if name not in origin_languages:
                        origin_languages.append(name)
        
        etymology_text = "\n".join(etymology_paragraphs)
        
        if not etymology_text:
            return EtymologyResponse(
                status=Status.NOT_FOUND,
                message=f"Etymology section exists but contains no text for '{word}'",
                data=EtymologyData(word=word, text="", origin_languages=origin_languages)
            )
        
        return EtymologyResponse(
            status=Status.SUCCESS,
            message="Etymology retrieved successfully",
            data=EtymologyData(
                word=word,
                text=etymology_text,
                origin_languages=origin_languages
            )
        )
    
    except requests.RequestException as e:
        return EtymologyResponse(
            status=Status.ERROR,
            message=f"Network error: {str(e)}",
            data=None
        )
    except Exception as e:
        return EtymologyResponse(
            status=Status.ERROR,
            message=f"Unexpected error: {str(e)}",
            data=None
        )
#JSON file to store points
if __name__ == "__main__":
    if os.path.exists('points.json'):
        with open("points.json", "r", encoding="utf-8") as f:
            points_data = json.load(f)
    else:
        points_data = {"points": 0}
        with open('points.json', 'w', encoding="utf-8") as f:
            json.dump(points_data, f, indent=4)

    with open('points.json', 'w', encoding="utf-8") as f:
        json.dump(points_data, f, indent=4)

    def save_points():
        with open("points.json", "w", encoding="utf-8") as f:
            json.dump(points_data, f, indent=4)

    FILENAME = "word_dict.json"
    word_dict = {}

    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump(word_dict, f, indent=4)

    with open(FILENAME, "r", encoding="utf-8") as f:
        word_dict = json.load(f)

    new_game = input("Do you want to start a new game? Y/N   ").upper()
    if new_game == "Y":
        points_data["points"] = 0
        save_points()
    question_count = int(input("How many questions do you want to ask? The maximum is 64 questions.   "))
    if question_count > 0 and question_count <= 64:
        for i in range(int(question_count)):
            if __name__ == "__main__":
                word = random.choice(list(word_dict.keys()))
                correct_answer = word_dict[word]
                answer = input(f"\nQuestion {i+1}\nGuess the etymology of this word:  {word}\nOptions: \n   A) Greek\n   B) Latin\n   C) Old English\n   D) French\n   E) Norse \nYour answer:   ").upper()
                result = get_etymology_info(word)
                if answer == correct_answer:
                    print("Correct!\n")
                    points_data["points"] += 1
                    save_points()
                    print(f"Your total points: {points_data['points']}\n")
                else:
                    print(f"Wrong! The correct answer is {correct_answer}.\n")
                    print(f"Your total points: {points_data['points']}\n")
                if result.data:
                    print(f"Etymology of '{word}':\n{result.data.text}\n")
    elif question_count == 0:
        print("No questions asked.")
    elif question_count == 65:
        print("You can ask a maximum of 64 questions.")
    else:
        print("Invalid number of questions.")

