import pygame
import sys
import os
import json
from time import localtime
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_ACCENT, MONTHS_LIST, DAYS_IN_MONTH
from states import (
    StartScreen, SlotSelectionScreen, PlayerDataScreen,
    MenuScreen, AchievementsScreen, LocationScreen, DialogueScreen
)


class Game:
    """Master controller managing global application loop, save files, clock, and state transitions."""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Digi Lab Canvas")
        self.clock = pygame.time.Clock()
        self.running = True

        self.player_name = ""
        self.player_birthday = "January 1"
        self.is_day = True
        self.is_raining = False
        self.use_realtime = False
        self.current_slot = None
        self.is_slot_saving_mode = False
        self.slot_return_state = 'StartScreen'

        self.ach_first_time = False
        self.ach_meet_arno = False
        self.ach_meet_blob = False
        self.ach_meet_brooke = False
        self.ach_birthday_at_lab = False

        self.sim_month_idx = 1
        self.sim_day = 1
        self.sim_hour = 8
        self.sim_minute = 0
        self.sim_second = 0
        self.last_clock_tick = pygame.time.get_ticks()

        self.character_placements = {}
        self.active_character = "ARNO"

        self.has_triggered_welcome = False
        self.birthday_celebrated_dates = set()
        self.event_dialogue_queue = []

        self.states = {
            'StartScreen': StartScreen(self),
            'SlotSelectionScreen': SlotSelectionScreen(self),
            'PlayerDataScreen': PlayerDataScreen(self),
            'Menu': MenuScreen(self),
            'AchievementsScreen': AchievementsScreen(self),
            'LocationScreen': LocationScreen(self),
            'DialogueScreen': DialogueScreen(self)
        }

        self.current_state = None
        self.change_state('StartScreen')

    def get_slot_filepath(self, slot_idx):
        if not os.path.exists("Tests/savefiles"):
            os.makedirs("Tests/savefiles", exist_ok=True)
        return f"savefiles/slot{slot_idx}.json"

    def get_all_slot_metadata(self):
        metadata = {}
        for idx in range(1, 5):
            path = self.get_slot_filepath(idx)
            if os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        data = json.load(f)
                    metadata[idx] = {
                        "exists": True,
                        "name": data.get("player_name", "Unknown"),
                        "birthday": data.get("player_birthday", "")
                    }
                except Exception:
                    metadata[idx] = {"exists": False}
            else:
                metadata[idx] = {"exists": False}
        return metadata

    def save_current_slot(self):
        if self.current_slot is None:
            self.current_slot = 1
        data = {
            "player_name": self.player_name,
            "player_birthday": self.player_birthday,
            "ach_first_time": self.ach_first_time,
            "ach_meet_arno": self.ach_meet_arno,
            "ach_meet_blob": self.ach_meet_blob,
            "ach_meet_brooke": self.ach_meet_brooke,
            "ach_birthday_at_lab": self.ach_birthday_at_lab,
            "has_triggered_welcome": self.has_triggered_welcome,
            "birthday_celebrated_dates": list(self.birthday_celebrated_dates)
        }
        path = self.get_slot_filepath(self.current_slot)
        try:
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception:
            pass

    def save_to_slot(self, slot_idx):
        self.current_slot = slot_idx
        self.save_current_slot()
        self.change_state('Menu')

    def load_from_slot(self, slot_idx):
        path = self.get_slot_filepath(slot_idx)
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                self.current_slot = slot_idx
                self.player_name = data.get("player_name", self.player_name)
                self.player_birthday = data.get("player_birthday", self.player_birthday)
                self.ach_first_time = data.get("ach_first_time", self.ach_first_time)
                self.ach_meet_arno = data.get("ach_meet_arno", self.ach_meet_arno)
                self.ach_meet_blob = data.get("ach_meet_blob", self.ach_meet_blob)
                self.ach_meet_brooke = data.get("ach_meet_brooke", self.ach_meet_brooke)
                self.ach_birthday_at_lab = data.get("ach_birthday_at_lab", self.ach_birthday_at_lab)
                self.has_triggered_welcome = data.get("has_triggered_welcome", self.has_triggered_welcome)
                self.birthday_celebrated_dates = set(data.get("birthday_celebrated_dates", []))

                self.use_realtime = True
                self.change_state('LocationScreen')
            except Exception:
                pass

    def open_slot_selection(self, is_saving, return_state='StartScreen'):
        self.is_slot_saving_mode = is_saving
        self.slot_return_state = return_state
        self.change_state('SlotSelectionScreen')

    def advance_days(self, days):
        for _ in range(days):
            current_month_name = MONTHS_LIST[self.sim_month_idx]
            max_days = DAYS_IN_MONTH.get(current_month_name, 31)
            self.sim_day += 1
            if self.sim_day > max_days:
                self.sim_day = 1
                self.sim_month_idx = (self.sim_month_idx + 1) % 12

    def update_clock(self):
        if self.use_realtime:
            cur = localtime()
            self.sim_month_idx = cur.tm_mon - 1
            self.sim_day = cur.tm_mday
            self.sim_hour = cur.tm_hour
            self.sim_minute = cur.tm_min
            self.sim_second = cur.tm_sec
            self.is_day = 6 <= self.sim_hour < 20
        else:
            now = pygame.time.get_ticks()
            dt = (now - self.last_clock_tick) / 100.0
            if dt >= 1.0:
                add_secs = int(dt)
                self.last_clock_tick += add_secs * 100
                self.sim_second += add_secs
                if self.sim_second >= 60:
                    add_mins = self.sim_second // 60
                    self.sim_second %= 60
                    self.sim_minute += add_mins
                    if self.sim_minute >= 60:
                        add_hours = self.sim_minute // 60
                        self.sim_minute %= 60
                        total_hours = self.sim_hour + add_hours
                        days_passed = total_hours // 24
                        self.sim_hour = total_hours % 24
                        if days_passed > 0:
                            self.advance_days(days_passed)
                self.is_day = 6 <= self.sim_hour < 20

    def change_state(self, new_state_name):
        if new_state_name in self.states:
            if self.current_state:
                self.current_state.exit()
            self.current_state = self.states[new_state_name]
            self.current_state.enter()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_state.handle_event(event)

            self.update_clock()
            self.current_state.update()

            self.screen.fill(COLOR_ACCENT)
            self.current_state.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game_app = Game()
    game_app.run()