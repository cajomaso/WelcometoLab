import pygame
import os
import random
from time import localtime
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_CARD_BG, COLOR_TEXT, COLOR_ACCENT,
    COLOR_STRONG_ACCENT, FONT_FAMILY, MONTHS_LIST, DAYS_IN_MONTH, HOURS_LIST,
    MINUTES_LIST, WEATHER_OPTIONS, CHARACTERS_DATA, HITBOX_POSITIONS,
    BACKGROUND_LAYERS_PATHS, CHARACTER_POS_PATHS, CHARACTER_PORTRAITS_PATHS
)
from UI import UIDropdown, Hitbox


class State:
    """Base class for all discrete scene states in the game architecture."""

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.img = None
        self.hitboxes = []
        self.boot()

    def boot(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        any_hovered = False
        for hb in self.hitboxes:
            if hb.update_hover(mouse_pos):
                any_hovered = True
        if not any_hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self, screen):
        if self.img:
            screen.blit(self.img, (0, 0))

    def handle_event(self, event):
        pass


class StartScreen(State):
    """Main Start Screen State loading start background and option buttons."""

    def boot(self):
        try:
            self.bg_img = pygame.image.load("media/background/start_screen.jpeg").convert_alpha()
        except Exception:
            self.bg_img = None

        try:
            self.overlay_png = pygame.image.load("media/background/start_screen.png").convert_alpha()
        except Exception:
            self.overlay_png = None

        r1 = pygame.Rect(425, 397, 430, 130)

        r2 = pygame.Rect(425, 563, 430, 130)


        self.btn_start = Hitbox(r1, "[SPACE] START NEW GAME", lambda: self.game.change_state('PlayerDataScreen'))
        self.btn_load = Hitbox(r2, "[L] LOAD EXISTING GAME",
                               lambda: self.game.open_slot_selection(is_saving=False, return_state='StartScreen'))
        self.hitboxes = [self.btn_start, self.btn_load]

    def draw(self, screen):
        self.btn_start.draw(screen)
        self.btn_load.draw(screen)
        if self.bg_img:
            screen.blit(self.bg_img, (0, 0))
        if self.overlay_png:
            ov_rect = self.overlay_png.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            screen.blit(self.overlay_png, ov_rect)


    def handle_event(self, event):
        for hb in self.hitboxes:
            if hb.handle_event(event):
                return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.change_state('PlayerDataScreen')
            elif event.key == pygame.K_l:
                self.game.open_slot_selection(is_saving=False, return_state='StartScreen')


class SlotSelectionScreen(State):
    """Screen for selecting among 4 save slots to load, overwrite, or delete profiles."""

    def boot(self):
        try:
            self.bg_img = pygame.image.load("media/background/start_screen.jpeg").convert_alpha()
        except Exception:
            self.bg_img = None
        self.selected_slot_idx = 1

    def enter(self):
        self.selected_slot_idx = self.game.current_slot if self.game.current_slot is not None else 1
        self.refresh_slot_buttons()

    def refresh_slot_buttons(self):
        self.hitboxes = []
        card_x = SCREEN_WIDTH // 2 - 320
        card_y = 100
        self.slot_meta = self.game.get_all_slot_metadata()

        for slot_idx in range(1, 5):
            btn_rect = pygame.Rect(card_x + 30, card_y + 80 + (slot_idx - 1) * 85, 580, 70)
            meta = self.slot_meta.get(slot_idx, {})
            has_data = meta.get("exists", False)

            if self.game.is_slot_saving_mode:
                lbl = f"Slot {slot_idx}: {meta.get('name', 'Empty Slot')} ({meta.get('birthday', '')})" if has_data else f"Slot {slot_idx}: [Empty Slot - Save Here]"
            else:
                lbl = f"Slot {slot_idx}: {meta.get('name', 'Empty Slot')} ({meta.get('birthday', '')})" if has_data else f"Slot {slot_idx}: [Empty Slot]"

            cb = lambda s=slot_idx: self.select_slot(s)
            hb = Hitbox(btn_rect, lbl, cb)
            self.hitboxes.append(hb)

        if self.selected_slot_idx is not None:
            load_rect = pygame.Rect(card_x + 30, card_y + 420, 180, 45)
            over_rect = pygame.Rect(card_x + 230, card_y + 420, 180, 45)
            del_rect = pygame.Rect(card_x + 430, card_y + 420, 180, 45)

            meta = self.slot_meta.get(self.selected_slot_idx, {})
            if meta.get("exists", False) and not self.game.is_slot_saving_mode:
                self.btn_load_slot = Hitbox(load_rect, "LOAD", lambda: self.game.load_from_slot(self.selected_slot_idx))
                self.hitboxes.append(self.btn_load_slot)

            self.btn_overwrite = Hitbox(over_rect, "SAVE / OVERWRITE",
                                        lambda: self.game.save_to_slot(self.selected_slot_idx))
            self.hitboxes.append(self.btn_overwrite)

            if meta.get("exists", False):
                self.btn_delete = Hitbox(del_rect, "DELETE", lambda: self.delete_slot(self.selected_slot_idx))
                self.hitboxes.append(self.btn_delete)

        back_rect = pygame.Rect(card_x + 30, card_y + 480, 580, 45)
        back_cb = lambda: self.game.change_state(self.game.slot_return_state)
        self.btn_back = Hitbox(back_rect, "RETURN", back_cb)
        self.hitboxes.append(self.btn_back)

    def select_slot(self, slot_idx):
        self.selected_slot_idx = slot_idx
        self.refresh_slot_buttons()

    def delete_slot(self, slot_idx):
        path = self.game.get_slot_filepath(slot_idx)
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass
        self.selected_slot_idx = 1
        self.refresh_slot_buttons()

    def draw(self, screen):
        if self.bg_img:
            screen.blit(self.bg_img, (0, 0))

        card = pygame.Rect(SCREEN_WIDTH // 2 - 320, 90, 640, 550)
        pygame.draw.rect(screen, COLOR_CARD_BG, card, border_radius=14)
        pygame.draw.rect(screen, COLOR_ACCENT, card, 2, border_radius=14)

        font_title = pygame.font.SysFont(FONT_FAMILY, 26, bold=True)
        title_str = "SAVE GAME SLOT SELECTION" if self.game.is_slot_saving_mode else "LOAD GAME SLOT SELECTION"
        t_surf = font_title.render(title_str, True, COLOR_STRONG_ACCENT)
        screen.blit(t_surf, t_surf.get_rect(center=(SCREEN_WIDTH // 2, card.y + 35)))

        for idx in range(4):
            slot_idx = idx + 1
            hb = self.hitboxes[idx]
            if slot_idx == self.selected_slot_idx:
                hb.draw(screen, bg_color=COLOR_STRONG_ACCENT, text_color=COLOR_CARD_BG)
            else:
                hb.draw(screen, bg_color=COLOR_CARD_BG, text_color=COLOR_TEXT)

        for idx in range(4, len(self.hitboxes)):
            hb = self.hitboxes[idx]
            if hb == getattr(self, 'btn_overwrite', None):
                hb.draw(screen, bg_color=COLOR_STRONG_ACCENT, text_color=COLOR_CARD_BG)
            else:
                hb.draw(screen, bg_color=COLOR_CARD_BG, text_color=COLOR_TEXT)

    def handle_event(self, event):
        for hb in self.hitboxes:
            if hb.handle_event(event):
                return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state(self.game.slot_return_state)


class PlayerDataScreen(State):
    """Screen for creating player profile"""

    def boot(self):
        try:
            self.bg_img = pygame.image.load("media/background/start_screen.jpeg").convert_alpha()
        except Exception:
            self.bg_img = None

        self.name_text = ""
        self.input_active = True
        self.month_dd = UIDropdown((0, 0, 220, 42), MONTHS_LIST, default_idx=0, label="Birthday Month:")
        self.update_days_for_month()

        card_x = SCREEN_WIDTH // 2 - 320
        card_y = 120
        btn_rect = pygame.Rect(card_x + 50, card_y + 410, 540, 55)
        self.btn_confirm = Hitbox(btn_rect, "CONFIRM PROFILE & CONTINUE", self.save_and_continue)
        self.hitboxes = [self.btn_confirm]

    def update_days_for_month(self):
        m_name = self.month_dd.get_selected()
        max_days = DAYS_IN_MONTH.get(m_name, 31)
        day_options = [f"{d:02d}" for d in range(1, max_days + 1)]
        cur_idx = getattr(self, 'day_dd', None).selected_idx if hasattr(self, 'day_dd') else 0
        if cur_idx >= len(day_options):
            cur_idx = len(day_options) - 1
        self.day_dd = UIDropdown((0, 0, 140, 42), day_options, default_idx=cur_idx, label="Day:")

    def draw(self, screen):
        if self.bg_img:
            screen.blit(self.bg_img, (0, 0))

        card = pygame.Rect(SCREEN_WIDTH // 2 - 320, 120, 640, 520)
        pygame.draw.rect(screen, COLOR_CARD_BG, card, border_radius=14)
        pygame.draw.rect(screen, COLOR_ACCENT, card, 2, border_radius=14)

        font_title = pygame.font.SysFont(FONT_FAMILY, 30, bold=True)
        t_surf = font_title.render("STUDENT PROFILE", True, COLOR_STRONG_ACCENT)
        screen.blit(t_surf, t_surf.get_rect(center=(SCREEN_WIDTH // 2, card.y + 45)))

        font_lbl = pygame.font.SysFont(FONT_FAMILY, 18, bold=True)
        n_lbl = font_lbl.render("Student Name:", True, COLOR_TEXT)
        screen.blit(n_lbl, (card.x + 50, card.y + 95))

        n_box = pygame.Rect(card.x + 50, card.y + 125, 540, 45)
        pygame.draw.rect(screen, COLOR_CARD_BG, n_box, border_radius=6)
        pygame.draw.rect(screen, COLOR_STRONG_ACCENT if self.input_active else COLOR_ACCENT, n_box, 2, border_radius=6)

        font_txt = pygame.font.SysFont(FONT_FAMILY, 22)
        name_surf = font_txt.render(self.name_text + ("|" if self.input_active else ""), True, COLOR_TEXT)
        screen.blit(name_surf, (n_box.x + 15, n_box.y + 10))

        self.month_dd.rect.topleft = (card.x + 50, card.y + 230)
        self.day_dd.rect.topleft = (card.x + 300, card.y + 230)
        self.month_dd.draw(screen)
        self.day_dd.draw(screen)
        self.btn_confirm.draw(screen, bg_color=COLOR_STRONG_ACCENT, text_color=COLOR_CARD_BG)
        self.day_dd.draw_popup(screen)
        self.month_dd.draw_popup(screen)

    def handle_event(self, event):
        if self.btn_confirm.handle_event(event):
            return
        if self.month_dd.handle_event(event):
            self.update_days_for_month()
            return
        if self.day_dd.handle_event(event):
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            card_x = SCREEN_WIDTH // 2 - 320
            card_y = 120
            n_box = pygame.Rect(card_x + 50, card_y + 125, 540, 45)
            self.input_active = n_box.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_BACKSPACE:
                    self.name_text = self.name_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.save_and_continue()
                elif len(self.name_text) < 16 and event.unicode.isprintable():
                    self.name_text += event.unicode

    def save_and_continue(self):
        self.game.player_name = self.name_text.strip()
        self.game.player_birthday = f"{self.month_dd.get_selected()} {self.day_dd.get_selected()}"
        self.game.current_slot = 1
        self.game.save_current_slot()
        self.game.change_state('Menu')


class MenuScreen(State):
    """Main Menu Screen"""

    def boot(self):
        try:
            self.bg_img = pygame.image.load("media/background/start_screen.jpeg").convert_alpha()
        except Exception:
            self.bg_img = None

        self.month_dd = UIDropdown((0, 0, 160, 40), MONTHS_LIST, default_idx=0, label="Month:")
        self.update_days_for_month()

        self.hour_dd = UIDropdown((0, 0, 95, 40), HOURS_LIST, default_idx=8, label="Hour:")
        self.minute_dd = UIDropdown((0, 0, 95, 40), MINUTES_LIST, default_idx=0, label="Minute:")
        self.weather_dd = UIDropdown((0, 0, 210, 40), WEATHER_OPTIONS, default_idx=0, label="Weather:")

        card_x = SCREEN_WIDTH // 2 - 420
        card_y = 60
        btn_w = 340
        btn_h = 45
        right_x = card_x + 420

        self.btn_realtime = Hitbox(pygame.Rect(right_x, card_y + 110, btn_w, btn_h), "Use real life time",
                                   self.toggle_realtime)
        self.btn_reshuffle = Hitbox(pygame.Rect(right_x, card_y + 175, btn_w, btn_h), "RESHUFFLE SEATING",
                                    self.randomize_characters)
        self.btn_achievements = Hitbox(pygame.Rect(right_x, card_y + 240, btn_w, btn_h), "VIEW ACHIEVEMENTS",
                                       lambda: self.game.change_state('AchievementsScreen'))
        self.btn_save = Hitbox(pygame.Rect(right_x, card_y + 305, btn_w, btn_h), "SAVE OR LOAD GAME",
                               lambda: self.game.open_slot_selection(is_saving=True, return_state='Menu'))
        self.btn_title = Hitbox(pygame.Rect(right_x, card_y + 370, btn_w, btn_h), "RETURN TO TITLE SCREEN",
                                lambda: self.game.change_state('StartScreen'))
        self.btn_enter = Hitbox(pygame.Rect(card_x + 40, card_y + 465, 760, 55), "ENTER DIGI LAB",
                                self.confirm_and_enter)

        self.hitboxes = [self.btn_realtime, self.btn_reshuffle, self.btn_achievements, self.btn_save, self.btn_title,
                         self.btn_enter]

    def enter(self):
        if self.game.use_realtime:
            self.sync_realtime_values()

    def update_days_for_month(self):
        m_name = self.month_dd.get_selected()
        max_days = DAYS_IN_MONTH.get(m_name, 31)
        day_options = [f"{d:02d}" for d in range(1, max_days + 1)]
        cur_idx = getattr(self, 'day_dd', None).selected_idx if hasattr(self, 'day_dd') else 14
        if cur_idx >= len(day_options):
            cur_idx = len(day_options) - 1
        self.day_dd = UIDropdown((0, 0, 110, 40), day_options, default_idx=cur_idx, label="Day:")

    def sync_realtime_values(self):
        cur = localtime()
        self.game.sim_month_idx = cur.tm_mon - 1
        self.game.sim_day = cur.tm_mday
        self.game.sim_hour = cur.tm_hour
        self.game.sim_minute = cur.tm_min
        self.game.sim_second = cur.tm_sec
        self.game.is_day = 6 <= self.game.sim_hour < 20

        cur_month_name = MONTHS_LIST[self.game.sim_month_idx]
        if cur_month_name in self.month_dd.options:
            self.month_dd.selected_idx = self.month_dd.options.index(cur_month_name)
        self.update_days_for_month()

        day_str = f"{self.game.sim_day:02d}"
        if day_str in self.day_dd.options:
            self.day_dd.selected_idx = self.day_dd.options.index(day_str)

        hr_str = f"{self.game.sim_hour:02d}"
        if hr_str in self.hour_dd.options:
            self.hour_dd.selected_idx = self.hour_dd.options.index(hr_str)

        min_str = f"{self.game.sim_minute:02d}"
        if min_str in self.minute_dd.options:
            self.minute_dd.selected_idx = self.minute_dd.options.index(min_str)

    def toggle_realtime(self):
        self.game.use_realtime = not self.game.use_realtime
        if self.game.use_realtime:
            self.sync_realtime_values()

    def confirm_and_enter(self):
        if self.game.use_realtime:
            self.game.update_clock()
        else:
            selected_month = self.month_dd.get_selected()
            selected_day = self.day_dd.get_selected()
            if selected_month in MONTHS_LIST:
                self.game.sim_month_idx = MONTHS_LIST.index(selected_month)
            if selected_day is not None:
                self.game.sim_day = int(selected_day)

            selected_hour = self.hour_dd.get_selected()
            selected_minute = self.minute_dd.get_selected()
            if selected_hour is not None and selected_minute is not None:
                self.game.sim_hour = int(selected_hour)
                self.game.sim_minute = int(selected_minute)
                self.game.sim_second = 0
            self.game.last_clock_tick = pygame.time.get_ticks()
            self.game.is_day = 6 <= self.game.sim_hour < 20

        selected_weather = self.weather_dd.get_selected()
        if self.game.use_realtime or selected_weather == "Random":
            self.game.is_raining = random.choice([True, False])
        else:
            self.game.is_raining = (selected_weather == "Rainy")

        if not self.game.character_placements:
            self.randomize_characters()

        self.game.change_state('LocationScreen')

    def randomize_characters(self):
        spots = list(HITBOX_POSITIONS.keys())
        random.shuffle(spots)
        chars = list(CHARACTERS_DATA.keys())
        self.game.character_placements = {char: spots[i] for i, char in enumerate(chars)}

    def draw(self, screen):
        if self.bg_img:
            screen.blit(self.bg_img, (0, 0))

        card = pygame.Rect(SCREEN_WIDTH // 2 - 420, 50, 840, 580)
        pygame.draw.rect(screen, COLOR_CARD_BG, card, border_radius=16)
        pygame.draw.rect(screen, COLOR_ACCENT, card, 2, border_radius=16)

        font_title = pygame.font.SysFont(FONT_FAMILY, 28, bold=True)
        t_surf = font_title.render("DIGI LAB ENVIRONMENT & MENU", True, COLOR_STRONG_ACCENT)
        screen.blit(t_surf, t_surf.get_rect(center=(SCREEN_WIDTH // 2, card.y + 40)))

        pygame.draw.line(screen, COLOR_ACCENT, (card.x + 390, card.y + 90), (card.x + 390, card.y + 440), 2)

        font_section = pygame.font.SysFont(FONT_FAMILY, 18, bold=True)
        sec_lbl = font_section.render("Simulation Settings", True, COLOR_STRONG_ACCENT)
        screen.blit(sec_lbl, (card.x + 40, card.y + 85))

        self.month_dd.rect.topleft = (card.x + 40, card.y + 140)
        self.day_dd.rect.topleft = (card.x + 220, card.y + 140)
        self.hour_dd.rect.topleft = (card.x + 40, card.y + 240)
        self.minute_dd.rect.topleft = (card.x + 155, card.y + 240)
        self.weather_dd.rect.topleft = (card.x + 40, card.y + 340)

        self.month_dd.draw(screen)
        self.day_dd.draw(screen)
        self.hour_dd.draw(screen)
        self.minute_dd.draw(screen)
        self.weather_dd.draw(screen)

        act_lbl = font_section.render("Actions & Navigation", True, COLOR_STRONG_ACCENT)
        screen.blit(act_lbl, (card.x + 420, card.y + 85))

        rt_label = f"Realtime Sync: {'ENABLED' if self.game.use_realtime else 'DISABLED'}"
        self.btn_realtime.label = rt_label
        self.btn_realtime.draw(screen)
        self.btn_reshuffle.draw(screen)
        self.btn_achievements.draw(screen)
        self.btn_save.draw(screen, bg_color=COLOR_ACCENT, text_color=COLOR_CARD_BG)
        self.btn_title.draw(screen, bg_color=COLOR_CARD_BG, text_color=COLOR_STRONG_ACCENT)
        self.btn_enter.draw(screen, bg_color=COLOR_STRONG_ACCENT, text_color=COLOR_CARD_BG)

        self.weather_dd.draw_popup(screen)
        self.minute_dd.draw_popup(screen)
        self.hour_dd.draw_popup(screen)
        self.day_dd.draw_popup(screen)
        self.month_dd.draw_popup(screen)

    def handle_event(self, event):
        for hb in self.hitboxes:
            if hb.handle_event(event):
                return
        if self.month_dd.handle_event(event):
            self.game.use_realtime = False
            self.update_days_for_month()
            return
        if self.day_dd.handle_event(event):
            self.game.use_realtime = False
            return
        if self.hour_dd.handle_event(event):
            self.game.use_realtime = False
            return
        if self.minute_dd.handle_event(event):
            self.game.use_realtime = False
            return
        if self.weather_dd.handle_event(event):
            self.game.use_realtime = False
            return


class AchievementsScreen(State):
    """Screen displaying student achievements with checkboxes."""

    def boot(self):
        try:
            self.bg_img = pygame.image.load("media/background/start_screen.jpeg").convert_alpha()
        except Exception:
            self.bg_img = None
        card_x = SCREEN_WIDTH // 2 - 320
        card_y = 90
        btn_back_rect = pygame.Rect(card_x + 50, card_y + 480, 540, 50)
        self.btn_back = Hitbox(btn_back_rect, "BACK TO MENU", lambda: self.game.change_state('Menu'))
        self.hitboxes = [self.btn_back]

    def draw(self, screen):
        if self.bg_img:
            screen.blit(self.bg_img, (0, 0))

        card = pygame.Rect(SCREEN_WIDTH // 2 - 320, 80, 640, 570)
        pygame.draw.rect(screen, COLOR_CARD_BG, card, border_radius=14)
        pygame.draw.rect(screen, COLOR_ACCENT, card, 2, border_radius=14)

        font_title = pygame.font.SysFont(FONT_FAMILY, 28, bold=True)
        t_surf = font_title.render("STUDENT ACHIEVEMENTS", True, COLOR_STRONG_ACCENT)
        screen.blit(t_surf, t_surf.get_rect(center=(SCREEN_WIDTH // 2, card.y + 45)))

        achievements_list = [
            ("My first time at Digi Lab", self.game.ach_first_time),
            ("Meeting Arno", self.game.ach_meet_arno),
            ("Meeting Blob", self.game.ach_meet_blob),
            ("Meeting Brooke", self.game.ach_meet_brooke),
            ("My birthday at Digi Lab", self.game.ach_birthday_at_lab),
        ]

        font_item = pygame.font.SysFont(FONT_FAMILY, 20, bold=True)
        start_y = card.y + 110
        box_size = 30

        for idx, (label, unlocked) in enumerate(achievements_list):
            item_y = start_y + idx * 70
            box_rect = pygame.Rect(card.x + 50, item_y, box_size, box_size)

            if unlocked:
                pygame.draw.rect(screen, COLOR_STRONG_ACCENT, box_rect, border_radius=6)
                check_font = pygame.font.SysFont(FONT_FAMILY, 22, bold=True)
                chk_surf = check_font.render("X", True, COLOR_CARD_BG)
                screen.blit(chk_surf, chk_surf.get_rect(center=box_rect.center))
            else:
                pygame.draw.rect(screen, COLOR_CARD_BG, box_rect, border_radius=6)
                pygame.draw.rect(screen, COLOR_ACCENT, box_rect, 2, border_radius=6)

            lbl_color = COLOR_TEXT if unlocked else COLOR_ACCENT
            lbl_surf = font_item.render(label, True, lbl_color)
            screen.blit(lbl_surf, (box_rect.right + 20, box_rect.y + 3))

        self.btn_back.draw(screen, bg_color=COLOR_STRONG_ACCENT, text_color=COLOR_CARD_BG)

    def handle_event(self, event):
        for hb in self.hitboxes:
            if hb.handle_event(event):
                return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state('Menu')


class LocationScreen(State):
    """Main Lab (Sadly old Lab)"""

    def boot(self):
        self.layers = {}
        for key, path in BACKGROUND_LAYERS_PATHS.items():
            try:
                self.layers[key] = pygame.image.load(path).convert_alpha()
            except Exception:
                self.layers[key] = None

        self.char_pos_sprites = {}
        for char_key, pos_dict in CHARACTER_POS_PATHS.items():
            self.char_pos_sprites[char_key] = {}
            for spot, path in pos_dict.items():
                try:
                    self.char_pos_sprites[char_key][spot] = pygame.image.load(path).convert_alpha()
                except Exception:
                    self.char_pos_sprites[char_key][spot] = None

    def enter(self):
        self.game.ach_first_time = True
        self.game.save_current_slot()

        if len(self.game.character_placements) < 3 or self.is_birthday_today():
            spots = list(HITBOX_POSITIONS.keys())
            chars = list(CHARACTERS_DATA.keys())
            self.game.character_placements = {char: spots[i] for i, char in enumerate(chars)}

        self.refresh_hitboxes()
        self.check_entry_events()

    def is_birthday_today(self):
        if not self.game.player_birthday:
            return False
        cur_month = MONTHS_LIST[self.game.sim_month_idx]
        cur_day = self.game.sim_day
        parts = self.game.player_birthday.split()
        if len(parts) == 2:
            b_month, b_day = parts[0], int(parts[1])
            return cur_month == b_month and cur_day == b_day
        return False

    def check_entry_events(self):
        cur_date_str = f"{MONTHS_LIST[self.game.sim_month_idx]} {self.game.sim_day}"
        is_birthday = self.is_birthday_today() and (cur_date_str not in self.game.birthday_celebrated_dates)
        is_welcome = not self.game.has_triggered_welcome

        if not is_welcome and not is_birthday:
            return False

        queue = []
        if is_welcome:
            self.game.has_triggered_welcome = True
            self.game.ach_meet_arno = True
            self.game.save_current_slot()
            queue.extend([
                {
                    "char": "ARNO", "emotion": "shocked",
                    "name": "Arno", "role": "The Ecuadorian Student Watcher",
                    "text": [f"Oh! Whats your name? {self.game.player_name}!"," Welcome to the Digi Lab community space!"]
                },
                {
                    "char": "ARNO", "emotion": "neutral",
                    "name": "Arno", "role": "The Ecuadorian Student Watcher",
                    "text": ["Feel free to hang out, work on assignments,", "or chat with the other undergraduate students."]
                }
            ])

        if is_birthday:
            self.game.birthday_celebrated_dates.add(cur_date_str)
            self.game.ach_birthday_at_lab = True
            self.game.ach_meet_arno = True
            self.game.ach_meet_blob = True
            self.game.ach_meet_brooke = True
            self.game.save_current_slot()
            queue.extend([
                {
                    "char": "ARNO", "emotion": "moved",
                    "name": "Arno", "role": "The Ecuadorian Student Watcher",
                    "text": [fr"Happy Birthday, {self.game.player_name}!",
                             "We're thrilled to celebrate with you in the Digi Lab!"]

                },
                {
                    "char": "BLOB", "emotion": "happy",
                    "name": "Blob", "role": "The B is silent",
                    "text": f"Bloop bloop! Happy Birthday {self.game.player_name}!! Let's take a break from Spider-Man and celebrate!"
                },
                {
                    "char": "BROOKE", "emotion": "happy",
                    "name": "Brooke", "role": "The Ancient One (Digital Media Student)",
                    "text": f"Happy Birthday {self.game.player_name}! Wishing you a year full of wonderful romance stories."


                }
            ])

        spots = list(HITBOX_POSITIONS.keys())
        chars = list(CHARACTERS_DATA.keys())
        self.game.character_placements = {char: spots[i] for i, char in enumerate(chars)}
        self.refresh_hitboxes()

        self.game.event_dialogue_queue = queue
        self.game.change_state('DialogueScreen')
        return True

    def refresh_hitboxes(self):
        self.hitboxes = []
        spot_occupant = {spot: None for spot in HITBOX_POSITIONS.keys()}
        for char_key, spot in self.game.character_placements.items():
            spot_occupant[spot] = char_key

        for spot_name, rect in HITBOX_POSITIONS.items():
            char_key = spot_occupant.get(spot_name)
            if char_key:
                cb = lambda c=char_key: self.trigger_dialogue(c)
                hb = Hitbox(rect, callback=cb)
                self.hitboxes.append(hb)

    def trigger_dialogue(self, char_key):
        self.game.active_character = char_key
        if char_key == "ARNO":
            self.game.ach_meet_arno = True
        elif char_key == "BLOB":
            self.game.ach_meet_blob = True
        elif char_key == "BROOKE":
            self.game.ach_meet_brooke = True
        self.game.save_current_slot()
        self.game.change_state('DialogueScreen')
        return True

    def update(self):
        super().update()
        if self.game.current_state == self:
            self.check_entry_events()

    def draw(self, screen):
        t_key = 'day' if self.game.is_day else 'night'
        w_key = 'rain' if self.game.is_raining else ''
        bg_key = f"{t_key}{w_key}"

        base_bg = self.layers.get(bg_key) or self.layers.get('day')
        if base_bg:
            screen.blit(base_bg, (0, 0))

        for char_key, spot in self.game.character_placements.items():
            if spot == "couch":
                sprite = self.char_pos_sprites.get(char_key, {}).get("couch")
                if sprite:
                    screen.blit(sprite, (0, 0))

        second_layer = self.layers.get("secondlayer")
        if second_layer:
            screen.blit(second_layer, (0, 0))

        for char_key, spot in self.game.character_placements.items():
            if spot in ["tableleft", "tablemiddle", "tableright"]:
                sprite = self.char_pos_sprites.get(char_key, {}).get(spot)
                if sprite:
                    screen.blit(sprite, (0, 0))

        third_layer = self.layers.get("thirdlayer")
        if third_layer:
            screen.blit(third_layer, (0, 0))

        if not self.game.is_day:
            night_overlay = self.layers.get("nightoverlay")
            if night_overlay:
                screen.blit(night_overlay, (0, 0))

        for hb in self.hitboxes:
            if hb.is_hovered:
                hb.draw(screen, filled=False, hover_border_color=COLOR_STRONG_ACCENT)

        self.draw_hud(screen)

    def draw_hud(self, screen):
        font = pygame.font.SysFont(FONT_FAMILY, 18, bold=True)
        clock_font = pygame.font.SysFont(FONT_FAMILY, 32, bold=True)

        cur_month = MONTHS_LIST[self.game.sim_month_idx]
        date_time_str = f"{cur_month} {self.game.sim_day:02d} | {self.game.sim_hour:02d}:{self.game.sim_minute:02d}"

        clock_txt = clock_font.render(date_time_str, True, COLOR_STRONG_ACCENT)
        clock_rect = clock_txt.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        pygame.draw.rect(screen, COLOR_CARD_BG, clock_rect.inflate(26, 14), border_radius=10)
        pygame.draw.rect(screen, COLOR_STRONG_ACCENT, clock_rect.inflate(26, 14), 2, border_radius=10)
        screen.blit(clock_txt, clock_rect)

        info_txt = font.render(f"Student: {self.game.player_name}  |  [M] Menu", True, COLOR_TEXT)
        info_rect = info_txt.get_rect(topleft=(20, 20))
        pygame.draw.rect(screen, COLOR_CARD_BG, info_rect.inflate(20, 10), border_radius=8)
        pygame.draw.rect(screen, COLOR_ACCENT, info_rect.inflate(20, 10), 2, border_radius=8)
        screen.blit(info_txt, info_rect)

    def handle_event(self, event):
        for hb in self.hitboxes:
            if hb.handle_event(event):
                return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            self.game.change_state('Menu')


class DialogueScreen(State):
    """Visual Dialogue view displaying character emotion portraits and event sequences."""

    def boot(self):
        self.current_line_idx = 0
        self.emotion_portraits = {}
        for char_key, emotions in CHARACTER_PORTRAITS_PATHS.items():
            self.emotion_portraits[char_key] = {}
            for emotion, path in emotions.items():
                try:
                    self.emotion_portraits[char_key][emotion] = pygame.image.load(path).convert_alpha()
                except Exception:
                    self.emotion_portraits[char_key][emotion] = None

    def enter(self):
        self.current_line_idx = 0
        char_key = self.game.active_character
        if char_key == "ARNO":
            self.game.ach_meet_arno = True
        elif char_key == "BLOB":
            self.game.ach_meet_blob = True
        elif char_key == "BROOKE":
            self.game.ach_meet_brooke = True
        self.game.save_current_slot()

    def get_dialogues(self):
        char_key = self.game.active_character or "ARNO"
        info = CHARACTERS_DATA.get(char_key, CHARACTERS_DATA["ARNO"])
        t_key = 'day' if self.game.is_day else 'night'
        w_key = 'rain' if self.game.is_raining else 'clear'
        lines = info["dialogues"].get(f"{t_key}_{w_key}", ["Hey there!"])
        return char_key, info, lines

    def draw(self, screen):
        self.game.states['LocationScreen'].draw(screen)

        if self.game.event_dialogue_queue:
            if self.game.event_dialogue_queue:
                if self.current_line_idx < len(self.game.event_dialogue_queue):
                    item = self.game.event_dialogue_queue[self.current_line_idx]
                    char_key = item.get("char", "ARNO")
                    emotion = item.get("emotion", "neutral")
                    portrait_img = self.emotion_portraits.get(char_key, {}).get(emotion) or self.emotion_portraits.get(
                        char_key, {}).get('neutral')
                    if portrait_img:
                        screen.blit(portrait_img, (0, 0))

                    f_name = pygame.font.SysFont(FONT_FAMILY, 24, bold=True)
                    name_txt = f_name.render(f"{item['name']} — {item['role']}", True, COLOR_STRONG_ACCENT)
                    screen.blit(name_txt, (160, 520))

                    f_text = pygame.font.SysFont(FONT_FAMILY, 22)
                    text_lines = item["text"]
                    if isinstance(text_lines, str):
                        text_lines = [text_lines]

                    for l_idx, l_text in enumerate(text_lines[:2]):
                        body_surf = f_text.render(
                            f'"{l_text}"' if l_idx == 0 and len(text_lines) == 1 else f'"{l_text}' + (
                                '"' if l_idx == len(text_lines) - 1 else ''), True, COLOR_TEXT)
                        screen.blit(body_surf, (160, 570 + l_idx * 30))

                    f_hint = pygame.font.SysFont(FONT_FAMILY, 16, bold=True)
                    hint_surf = f_hint.render(
                        f"Event {self.current_line_idx + 1}/{len(self.game.event_dialogue_queue)}  |  [SPACE / CLICK] Next",
                        True, COLOR_ACCENT)
                    screen.blit(hint_surf, (160, 740))
                return

        char_key, info, lines = self.get_dialogues()
        portrait_img = self.emotion_portraits.get(char_key, {}).get('neutral')
        if portrait_img:
            screen.blit(portrait_img, (0, 0))

        f_name = pygame.font.SysFont(FONT_FAMILY, 24, bold=True)
        name_txt = f_name.render(f"{info['name']} — {info['role']}", True, COLOR_STRONG_ACCENT)
        screen.blit(name_txt, (160, 520))

        f_text = pygame.font.SysFont(FONT_FAMILY, 22)
        line_txt = lines[self.current_line_idx % len(lines)]
        body_surf = f_text.render(f'"{line_txt}"', True, COLOR_TEXT)
        screen.blit(body_surf, (160, 570))

        f_hint = pygame.font.SysFont(FONT_FAMILY, 16, bold=True)
        hint_surf = f_hint.render(
            f"Line {self.current_line_idx + 1}/{len(lines)}  |  [SPACE / CLICK] Next  |  [ESC] Exit Dialogue", True,
            COLOR_ACCENT)
        screen.blit(hint_surf, (160, 740))

    def handle_event(self, event):
        if self.game.event_dialogue_queue:
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.current_line_idx += 1
                if self.current_line_idx >= len(self.game.event_dialogue_queue):
                    self.game.event_dialogue_queue = []
                    self.game.change_state('LocationScreen')
            return

        _, _, lines = self.get_dialogues()
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or \
            (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            self.current_line_idx += 1
            if self.current_line_idx >= len(lines):
                self.game.change_state('LocationScreen')
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state('LocationScreen')