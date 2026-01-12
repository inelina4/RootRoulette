#savāc vārdus un pareizās atbildes (valodas A, B, C, D, E)
#pārbauda kešatmiņu un iegūst etimoloģiju no API, ja nepieciešams, saglabā datus kešatmiņā
#randomizē valodu opcijas un nodrošina ērtu piekļuvi vārdu sarakstam un kešatmiņas informācijai

import json
import os
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from src.data.scrape2 import get_etymology_info, EtymologyResponse, Status
from src.data.etymology_cache import EtymologyCache, CachedEtymology

#datu klase, kas satur pilnu vārda informāciju
@dataclass 
class WordData:
    word: str
    correct_language: str
    etymology_text: str
    origin_languages: List[str]

#grupē pareižo atbilžu burtus ar pilniem valodu nosaukumiem
class EtymologyService:
    LANGUAGE_CODE_MAP = {
        'A': 'Greek',
        'B': 'Latin', 
        'C': 'Old English',
        'D': 'French',
        'E': 'Norse'
    }
    
    #paplašināts valodu saraksts nejaušai izvēlei
    ALL_LANGUAGES = [
        'Greek', 'Latin', 'Old English', 'French', 'Norse',
        'German', 'Spanish', 'Italian', 'Dutch', 'Sanskrit',
        'Arabic', 'Hebrew', 'Celtic', 'Slavic'
    ]
    
    #sāk ar vārdu vārdnīcu un kešatmiņu
    def __init__(self, word_dict_file: str = "src/data/data/word_dict.json", cache_file: str = "etymology_cache.json"):
        self.word_dict_file = word_dict_file
        self.cache = EtymologyCache(cache_file)
        self.word_dict = self._load_word_dict()
    
    #nolasa un ielādē sākotnējo vārdu vārdnīcu
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
    
    #randomizēta vārda iegūšana no vārdnīcas
    def get_random_word(self) -> Optional[str]:
        """Iegūst nejaušu vārdu no vārdnīcas."""
        if not self.word_dict:
            return None
        return random.choice(list(self.word_dict.keys()))
    
    #iegūst pareizo valodu, pamatojoties uz burtu kodu
    def get_correct_language(self, word: str) -> Optional[str]:
        """Iegūst pareizo valodu vārdam, izmantojot burtu kodu."""
        if word not in self.word_dict:
            return None
        
        letter_code = self.word_dict[word]
        return self.LANGUAGE_CODE_MAP.get(letter_code)
    
    #iegūst 4 nejaušas valodu opcijas, ieskaitot pareizo
    def get_language_options(self, correct_language: str) -> List[str]:
        """Iegūst 4 nejaušas valodu opcijas, ieskaitot pareizo."""

        #sāk ar pareizo valodu
        options = [correct_language]

        #iegūst 3 randomizētas papildu valodas (neskaitot pareizo)
        available_languages = [lang for lang in self.ALL_LANGUAGES if lang != correct_language]
        additional_options = random.sample(available_languages, min(3, len(available_languages)))
        options.extend(additional_options)
        
        #sajauc atbilžu kārtību
        random.shuffle(options)
        return options
    
    #iegūst pilnu vārda informāciju, tai skaitā etimoloģiju no kešatmiņas vai API
    async def get_word_data(self, word: str) -> Optional[WordData]:
        """Iegūst pilnu vārda informāciju, tai skaitā etimoloģiju no kešatmiņas vai API."""
        correct_language = self.get_correct_language(word)
        if not correct_language:
            return None
        
        #sākumā mēģina iegūt no kešatmiņas
        cached_etymology = self.cache.get(word)
        if cached_etymology:
            return WordData(
                word=word,
                correct_language=correct_language,
                etymology_text=cached_etymology.text,
                origin_languages=cached_etymology.origin_languages
            )
        
        #ja nav kešatmiņā, iegūst no API
        etymology_response = get_etymology_info(word)
        
        #ja viss norit veiksmīgi, saglabā kešatmiņā un atgriež datus
        if etymology_response.status == Status.SUCCESS and etymology_response.data:
            self.cache.put(
                word=word,
                text=etymology_response.data.text,
                origin_languages=etymology_response.data.origin_languages,
                correct_answer=self.word_dict[word]
            )
            
            #izpildās, kad dati ir veiksmīgi iegūti
            return WordData(
                word=word,
                correct_language=correct_language,
                etymology_text=etymology_response.data.text,
                origin_languages=etymology_response.data.origin_languages
            )
        else:
            #saglabā tukšu rezultātu, lai izvairītos no atkārtotiem API pieprasījumiem problemātiskiem vārdiem
            self.cache.put(
                word=word,
                text=f"Etymology information not available for '{word}'.",
                origin_languages=[],
                correct_answer=self.word_dict[word]
            )
            
            #izpildās, kad dati nav pieejami
            return WordData(
                word=word,
                correct_language=correct_language,
                etymology_text=f"Etymology information not available for '{word}'.",
                origin_languages=[]
            )
    
    #sinhroni atgriež vārda datus ērtākai integrācijai
    def get_word_data_sync(self, word: str) -> Optional[WordData]:
        """Sinhroni atgriež vārda datus ērtākai integrācijai."""

        #pārbauda, vai ir pareizā valoda (A, B, C, D, E) vārdnīcā
        correct_language = self.get_correct_language(word)
        if not correct_language:
            return None
        
        #vispirms pārbauda kešatmiņu
        cached_etymology = self.cache.get(word)
        if cached_etymology:
            return WordData(
                word=word,
                correct_language=correct_language,
                etymology_text=cached_etymology.text,
                origin_languages=cached_etymology.origin_languages
            )
        
        #ja nav kešatmiņā, iegūst no API
        etymology_response = get_etymology_info(word)
        
        #ja viss norit veiksmīgi, saglabā kešatmiņā un atgriež datus
        if etymology_response.status == Status.SUCCESS and etymology_response.data:
            self.cache.put(
                word=word,
                text=etymology_response.data.text,
                origin_languages=etymology_response.data.origin_languages,
                correct_answer=self.word_dict[word]
            )
            
            #izpildās, kad dati ir veiksmīgi iegūti
            return WordData(
                word=word,
                correct_language=correct_language,
                etymology_text=etymology_response.data.text,
                origin_languages=etymology_response.data.origin_languages
            )
        
        #saglabā tukšu rezultātu, lai izvairītos no atkārtotiem API pieprasījumiem problemātiskiem vārdiem
        else:
            self.cache.put(
                word=word,
                text=f"Etymology information not available for '{word}'.",
                origin_languages=[],
                correct_answer=self.word_dict[word]
            )
            
            #izpildās, kad dati nav pieejami
            return WordData(
                word=word,
                correct_language=correct_language,
                etymology_text=f"Etymology information not available for '{word}'.",
                origin_languages=[]
            )
    
    #iegūst visu pieejamo vārdu sarakstu
    def get_available_words(self) -> List[str]:
        """Iegūst visu pieejamo vārdu sarakstu."""
        return list(self.word_dict.keys())
    
    #iegūst kešatmiņas statistiku
    def get_cache_info(self) -> Tuple[int, int]:
        """Iegūst kešatmiņas statistiku: (kešotie_vārdi, kopējie_vārdi)."""
        return (self.cache.size(), len(self.word_dict))