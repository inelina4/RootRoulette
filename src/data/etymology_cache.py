#saglabā un ielādē etimoloģijas kešatmiņu JSON formātā, lai nebūtu jāveic atkārtoti tīmekļa pieprasījumi

import json
import os
from typing import Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class CachedEtymology:
    word: str
    text: str
    origin_languages: list[str]
    correct_answer: str  # pareizās atbildes (A, B, C, D, E) no word_dict.json
    cached_at: str  # ISO timestamp

#pārvalda visu etimoloģijas kešatmiņu - ielādē, saglabā, piekļūst un atjaunina kešatmiņu
class EtymologyCache:

    #izveido kešatmiņu, ielādējot no JSON faila, ja tā pastāv
    def __init__(self, cache_file: str = "etymology_cache.json"):
        self.cache_file = cache_file
        self.cache: Dict[str, CachedEtymology] = {}
        self._load_cache()

    #ielādē kešatmiņu no JSON faila, ja tā pastāv   
    def _load_cache(self) -> None:
        """Ielādē kešatmiņu no JSON faila, ja tā pastāv."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)
                    self.cache = {
                        word: CachedEtymology(**data) 
                        for word, data in cache_data.items()
                    }
            except (json.JSONDecodeError, TypeError, KeyError) as e:
                print(f"Warning: Could not load etymology cache: {e}")
                self.cache = {}
    
    #saglabā pašreizējo kešatmiņu JSON failā
    def _save_cache(self) -> None:
        """Saglabā pašreizējo kešatmiņu JSON failā."""
        try:
            cache_data = {
                word: asdict(etymology) 
                for word, etymology in self.cache.items()
            }
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save etymology cache: {e}")
    
    #ja vārds ir kešatmiņā, atgriež kešatmiņā saglabāto etimoloģiju
    def get(self, word: str) -> Optional[CachedEtymology]:
        """Iegūst vārda etimoloģiju no kešatmiņas, ja tā pastāv."""
        return self.cache.get(word.lower())
    
    #saglabā jaunus vārdus kešatmiņā ar pašreizējo laika zīmogu
    def put(self, word: str, text: str, origin_languages: list[str], correct_answer: str) -> None:
        """Saglabā etimoloģiju kešatmiņā ar pašreizējo laika zīmogu."""
        cached_etymology = CachedEtymology(
            word=word.lower(),
            text=text,
            origin_languages=origin_languages,
            correct_answer=correct_answer,
            cached_at=datetime.now().isoformat()
        )
        self.cache[word.lower()] = cached_etymology
        self._save_cache()
    
    #pārbauda, vai vārds jau ir kešatmiņā
    def contains(self, word: str) -> bool:
        """Pārbauda, vai vārds jau ir kešatmiņā."""
        return word.lower() in self.cache
    
    #notīra visu kešatmiņu
    def clear(self) -> None:
        """Notīra visu kešatmiņu."""
        self.cache.clear()
        self._save_cache()
    
    #iegūst kešatmiņā saglabāto ierakstu skaitu
    def size(self) -> int:
        """Iegūst kešatmiņā saglabāto ierakstu skaitu."""
        return len(self.cache)