#123
import json
import logging
import os
from typing import Dict, Optional
from config import STATS_FILE

logger = logging.getLogger(__name__)

class StatsStorage:
    """Класс для работы с хранением статистики прогулов"""
    
    def __init__(self, filename: str = STATS_FILE):
        # Создаем папку для файла, если её нет
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
        self.filename = filename
        logger.info(f"Загружаем статистику из файла: {self.filename}")
        self.stats = self._load_stats()
        logger.info(f"Загружено пользователей: {len(self.stats)}")
    
    def _load_stats(self) -> Dict[str, int]:
        """Загружает статистику из файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                stats = json.load(f)
                logger.info(f"Загружена статистика: {len(stats)} пользователей, данные: {stats}")
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
            logger.info(f"Сохраняем статистику в файл: {self.filename}")
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
            logger.info(f"Статистика сохранена успешно. Пользователей: {len(self.stats)}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении статистики в {self.filename}: {e}")
    
    def add_absence(self, user_id: str, username: str = None) -> int:
        """Добавляет прогул пользователю и возвращает новое количество"""
        if user_id not in self.stats:
            self.stats[user_id] = 0
        
        self.stats[user_id] += 1
        self._save_stats()
        
        logger.info(f"Добавлен прогул для {username or user_id}: {self.stats[user_id]}")
        return self.stats[user_id]
    
    def remove_absence(self, user_id: str) -> bool:
        """Снимает прогул пользователю и возвращает True если успешно"""
        if user_id not in self.stats or self.stats[user_id] <= 0:
            return False
        
        self.stats[user_id] -= 1
        
        # Если прогулов стало 0, удаляем пользователя из статистики
        if self.stats[user_id] == 0:
            del self.stats[user_id]
        
        self._save_stats()
        logger.info(f"Снят прогул для {user_id}: {self.stats.get(user_id, 0)}")
        return True
    
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
        #удалить
    
    def save_stats_to_file(self):
        """Явно сохраняет текущую статистику в файл"""
        self._save_stats()

    def load_stats_from_file(self):
        """Явно загружает статистику из файла в память"""
        self.stats = self._load_stats() 
        