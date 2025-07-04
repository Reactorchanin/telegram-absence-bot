import json
import logging
from typing import Dict, Optional
from config import STATS_FILE

logger = logging.getLogger(__name__)

class StatsStorage:
    """Класс для работы с хранением статистики прогулов"""
    
    def __init__(self, filename: str = STATS_FILE):
        self.filename = filename
        self.stats = self._load_stats()
    
    def _load_stats(self) -> Dict[str, int]:
        """Загружает статистику из файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                stats = json.load(f)
                logger.info(f"Загружена статистика: {len(stats)} пользователей")
                return stats
        except FileNotFoundError:
            logger.info("Файл статистики не найден, создаём новый")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка при чтении файла статистики: {e}")
            return {}
    
    def _save_stats(self):
        """Сохраняет статистику в файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
            logger.info("Статистика сохранена")
        except Exception as e:
            logger.error(f"Ошибка при сохранении статистики: {e}")
    
    def add_absence(self, user_id: str, username: str = None) -> int:
        """Добавляет прогул пользователю и возвращает новое количество"""
        if user_id not in self.stats:
            self.stats[user_id] = 0
        
        self.stats[user_id] += 1
        self._save_stats()
        
        logger.info(f"Добавлен прогул для {username or user_id}: {self.stats[user_id]}")
        return self.stats[user_id]
    
    def get_absences(self, user_id: str) -> int:
        """Возвращает количество прогулов пользователя"""
        return self.stats.get(user_id, 0)
    
    def get_all_stats(self) -> Dict[str, int]:
        """Возвращает всю статистику"""
        return self.stats.copy()
    
    def reset_stats(self):
        """Сбрасывает всю статистику"""
        self.stats = {}
        self._save_stats()
        logger.info("Статистика сброшена")
    
    def get_user_info(self, user_id: str) -> Optional[Dict[str, int]]:
        """Возвращает информацию о пользователе"""
        if user_id in self.stats:
            return {user_id: self.stats[user_id]}
        return None 