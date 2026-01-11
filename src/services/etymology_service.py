import json
import os
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from src.data.scrape2 import get_etymology_info, EtymologyResponse, Status
from src.data.etymology_cache import EtymologyCache, CachedEtymology

@dataclass 
class WordData:
    word: str
    correct_language: str
    etymology_text: str
    origin_languages: List[str]

class EtymologyService:
    # Map letter codes from word_dict.json to full language names
    LANGUAGE_CODE_MAP = {
        'A': 'Greek',
        'B': 'Latin', 
        'C': 'Old English',
        'D': 'French',
        'E': 'Norse'
    }
    
    # Extended language pool for random selection
    ALL_LANGUAGES = [
        'Greek', 'Latin', 'Old English', 'French', 'Norse',
        'German', 'Spanish', 'Italian', 'Dutch', 'Sanskrit',
        'Arabic', 'Hebrew', 'Celtic', 'Slavic'
    ]
    
    def __init__(self, word_dict_file: str = "word_dict.json", cache_file: str = "etymology_cache.json"):
        self.word_dict_file = word_dict_file
        self.cache = EtymologyCache(cache_file)
        self.word_dict = self._load_word_dict()
    
    def _load_word_dict(self) -> Dict[str, str]:
        """Load the seed word dictionary."""
        if not os.path.exists(self.word_dict_file):
            return {}
        
        try:
            with open(self.word_dict_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Warning: Could not load word dictionary: {e}")
            return {}
    
    def get_random_word(self) -> Optional[str]:
        """Get a random word from the word dictionary."""
        if not self.word_dict:
            return None
        return random.choice(list(self.word_dict.keys()))
    
    def get_correct_language(self, word: str) -> Optional[str]:
        """Get the correct language for a word using the letter code mapping."""
        if word not in self.word_dict:
            return None
        
        letter_code = self.word_dict[word]
        return self.LANGUAGE_CODE_MAP.get(letter_code)
    
    def get_language_options(self, correct_language: str) -> List[str]:
        """Get 4 random language options including the correct one."""
        # Start with the correct language
        options = [correct_language]
        
        # Get 3 additional random languages (excluding the correct one)
        available_languages = [lang for lang in self.ALL_LANGUAGES if lang != correct_language]
        additional_options = random.sample(available_languages, min(3, len(available_languages)))
        options.extend(additional_options)
        
        # Shuffle so correct answer isn't always in the same position
        random.shuffle(options)
        return options
    
    async def get_word_data(self, word: str) -> Optional[WordData]:
        """Get complete word data including etymology from cache or API."""
        # Check if we have the correct language mapping
        correct_language = self.get_correct_language(word)
        if not correct_language:
            return None
        
        # Try to get from cache first
        cached_etymology = self.cache.get(word)
        if cached_etymology:
            return WordData(
                word=word,
                correct_language=correct_language,
                etymology_text=cached_etymology.text,
                origin_languages=cached_etymology.origin_languages
            )
        
        # If not in cache, fetch from API
        etymology_response = get_etymology_info(word)
        
        if etymology_response.status == Status.SUCCESS and etymology_response.data:
            # Cache the successful response
            self.cache.put(
                word=word,
                text=etymology_response.data.text,
                origin_languages=etymology_response.data.origin_languages,
                correct_answer=self.word_dict[word]
            )
            
            return WordData(
                word=word,
                correct_language=correct_language,
                etymology_text=etymology_response.data.text,
                origin_languages=etymology_response.data.origin_languages
            )
        else:
            # Cache empty result to avoid repeated API calls for problematic words
            self.cache.put(
                word=word,
                text=f"Etymology information not available for '{word}'.",
                origin_languages=[],
                correct_answer=self.word_dict[word]
            )
            
            return WordData(
                word=word,
                correct_language=correct_language,
                etymology_text=f"Etymology information not available for '{word}'.",
                origin_languages=[]
            )
    
    def get_word_data_sync(self, word: str) -> Optional[WordData]:
        """Synchronous version of get_word_data for easier integration."""
        # Check if we have the correct language mapping
        correct_language = self.get_correct_language(word)
        if not correct_language:
            return None
        
        # Try to get from cache first
        cached_etymology = self.cache.get(word)
        if cached_etymology:
            return WordData(
                word=word,
                correct_language=correct_language,
                etymology_text=cached_etymology.text,
                origin_languages=cached_etymology.origin_languages
            )
        
        # If not in cache, fetch from API
        etymology_response = get_etymology_info(word)
        
        if etymology_response.status == Status.SUCCESS and etymology_response.data:
            # Cache the successful response
            self.cache.put(
                word=word,
                text=etymology_response.data.text,
                origin_languages=etymology_response.data.origin_languages,
                correct_answer=self.word_dict[word]
            )
            
            return WordData(
                word=word,
                correct_language=correct_language,
                etymology_text=etymology_response.data.text,
                origin_languages=etymology_response.data.origin_languages
            )
        else:
            # Cache empty result to avoid repeated API calls for problematic words
            self.cache.put(
                word=word,
                text=f"Etymology information not available for '{word}'.",
                origin_languages=[],
                correct_answer=self.word_dict[word]
            )
            
            return WordData(
                word=word,
                correct_language=correct_language,
                etymology_text=f"Etymology information not available for '{word}'.",
                origin_languages=[]
            )
    
    def get_available_words(self) -> List[str]:
        """Get list of all available words."""
        return list(self.word_dict.keys())
    
    def get_cache_info(self) -> Tuple[int, int]:
        """Get cache statistics: (cached_words, total_words)."""
        return (self.cache.size(), len(self.word_dict))