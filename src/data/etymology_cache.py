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
    correct_answer: str  # The letter code (A, B, C, D, E) from word_dict.json
    cached_at: str  # ISO timestamp

class EtymologyCache:
    def __init__(self, cache_file: str = "etymology_cache.json"):
        self.cache_file = cache_file
        self.cache: Dict[str, CachedEtymology] = {}
        self._load_cache()
    
    def _load_cache(self) -> None:
        """Load cache from JSON file if it exists."""
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
    
    def _save_cache(self) -> None:
        """Save current cache to JSON file."""
        try:
            cache_data = {
                word: asdict(etymology) 
                for word, etymology in self.cache.items()
            }
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save etymology cache: {e}")
    
    def get(self, word: str) -> Optional[CachedEtymology]:
        """Retrieve cached etymology for a word."""
        return self.cache.get(word.lower())
    
    def put(self, word: str, text: str, origin_languages: list[str], correct_answer: str) -> None:
        """Store etymology in cache with current timestamp."""
        cached_etymology = CachedEtymology(
            word=word.lower(),
            text=text,
            origin_languages=origin_languages,
            correct_answer=correct_answer,
            cached_at=datetime.now().isoformat()
        )
        self.cache[word.lower()] = cached_etymology
        self._save_cache()
    
    def contains(self, word: str) -> bool:
        """Check if word exists in cache."""
        return word.lower() in self.cache
    
    def clear(self) -> None:
        """Clear all cached data."""
        self.cache.clear()
        self._save_cache()
    
    def size(self) -> int:
        """Get number of cached entries."""
        return len(self.cache)