import pygame
from settings import COLOR_CARD_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_STRONG_ACCENT, FONT_FAMILY

class UIDropdown:
    """Reusable Dropdown selection component with scroll support."""
    def __init__(self, rect, options, default_idx=0, label=""):
        self.rect = pygame.Rect(rect)
        self.options = options
        self.selected_idx = default_idx
        self.is_open = False
        self.label = label
        self.scroll_offset = 0
        self.font = pygame.font.SysFont(FONT_FAMILY, 16, bold=True)

    def draw(self, screen):
        if self.label:
            lbl_surf = self.font.render(self.label, True, COLOR_TEXT)
            screen.blit(lbl_surf, (self.rect.x, self.rect.y - 22))

        pygame.draw.rect(screen, COLOR_CARD_BG, self.rect, border_radius=6)
        pygame.draw.rect(screen, COLOR_STRONG_ACCENT if self.is_open else COLOR_ACCENT, self.rect, 2, border_radius=6)

        selected_text = str(self.options[self.selected_idx]) if self.options else ""
        txt_surf = self.font.render(selected_text, True, COLOR_TEXT)
        screen.blit(txt_surf, (self.rect.x + 12, self.rect.y + (self.rect.height - txt_surf.get_height()) // 2))

        arrow_str = "^" if self.is_open else "v"
        arrow_surf = self.font.render(arrow_str, True, COLOR_STRONG_ACCENT)
        screen.blit(arrow_surf, (self.rect.right - 24, self.rect.y + (self.rect.height - arrow_surf.get_height()) // 2))

    def draw_popup(self, screen):
        if not self.is_open or not self.options:
            return

        item_height = 30
        pop_height = min(len(self.options) * item_height, 120)
        pop_rect = pygame.Rect(self.rect.x, self.rect.bottom + 4, self.rect.width, pop_height)

        pygame.draw.rect(screen, COLOR_CARD_BG, pop_rect, border_radius=6)
        pygame.draw.rect(screen, COLOR_STRONG_ACCENT, pop_rect, 2, border_radius=6)

        mouse_pos = pygame.mouse.get_pos()
        visible_count = pop_height // item_height
        max_scroll = max(0, len(self.options) - visible_count)
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))

        for idx in range(visible_count):
            opt_idx = self.scroll_offset + idx
            if opt_idx >= len(self.options):
                break

            opt_rect = pygame.Rect(self.rect.x, pop_rect.y + idx * item_height, self.rect.width, item_height)
            hover = opt_rect.collidepoint(mouse_pos)

            if hover:
                pygame.draw.rect(screen, COLOR_STRONG_ACCENT, opt_rect, border_radius=4)
                opt_txt = self.font.render(str(self.options[opt_idx]), True, COLOR_CARD_BG)
            elif opt_idx == self.selected_idx:
                pygame.draw.rect(screen, COLOR_ACCENT, opt_rect, border_radius=4)
                opt_txt = self.font.render(str(self.options[opt_idx]), True, COLOR_CARD_BG)
            else:
                opt_txt = self.font.render(str(self.options[opt_idx]), True, COLOR_TEXT)

            screen.blit(opt_txt, (opt_rect.x + 12, opt_rect.y + (item_height - opt_txt.get_height()) // 2))

    def handle_event(self, event):
        item_height = 30
        pop_height = min(len(self.options) * item_height, 120) if self.options else 0
        visible_count = pop_height // item_height if item_height else 1
        max_scroll = max(0, len(self.options) - visible_count)

        if event.type == pygame.MOUSEWHEEL and self.is_open:
            self.scroll_offset = max(0, min(self.scroll_offset - event.y, max_scroll))
            return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.is_open = not self.is_open
                    if self.is_open:
                        self.scroll_offset = max(0, min(self.selected_idx - visible_count // 2, max_scroll))
                    return True

                if self.is_open and self.options:
                    pop_rect = pygame.Rect(self.rect.x, self.rect.bottom + 4, self.rect.width, pop_height)
                    if pop_rect.collidepoint(event.pos):
                        click_y = event.pos[1] - pop_rect.y
                        idx = click_y // item_height
                        opt_idx = self.scroll_offset + idx
                        if 0 <= opt_idx < len(self.options):
                            self.selected_idx = opt_idx
                            self.is_open = False
                            return True

                self.is_open = False

            elif self.is_open and event.button == 4:
                self.scroll_offset = max(0, self.scroll_offset - 1)
                return True
            elif self.is_open and event.button == 5:
                self.scroll_offset = min(max_scroll, self.scroll_offset + 1)
                return True

        return False

    def get_selected(self):
        return self.options[self.selected_idx] if self.options else None


class Hitbox:
    """Interactive Hitbox and Button component handling callbacks and hover cursors."""
    def __init__(self, rect, label="", callback=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.callback = callback
        self.is_hovered = False

    def update_hover(self, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos)
        self.is_hovered = hovered
        if hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        return hovered

    def draw(self, screen, bg_color=COLOR_CARD_BG, border_color=COLOR_ACCENT,
             hover_border_color=COLOR_STRONG_ACCENT, text_color=COLOR_TEXT,
             border_radius=8, font_size=18, filled=True):
        cur_border = hover_border_color if self.is_hovered else border_color
        if filled:
            pygame.draw.rect(screen, bg_color, self.rect, border_radius=border_radius)
        pygame.draw.rect(screen, cur_border, self.rect, 2, border_radius=border_radius)

        if self.label:
            font = pygame.font.SysFont(FONT_FAMILY, font_size, bold=True)
            if filled and bg_color == COLOR_STRONG_ACCENT:
                cur_text_color = COLOR_CARD_BG if self.is_hovered else text_color
            else:
                cur_text_color = hover_border_color if self.is_hovered else text_color

            txt_surf = font.render(self.label, True, cur_text_color)
            screen.blit(txt_surf, txt_surf.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        return False