import pygame
from .player import Player
from .obstacle import Obstacle

WHITE = (255, 255, 255)
BROWN = (120, 80, 40)
DARK_GREEN = (30, 100, 30)


class GameEngine:
    def __init__(self, width, height, difficulty="medium"):
        self.width = width
        self.height = height
        self.ground_y = height - 40
        self.player = Player(80, self.ground_y)

        self.max_speed = 12
        self.speed_increase_per_frame = 0.003

        self.set_difficulty(difficulty)

        self._spawn_timer = 0
        self.obstacles = []
        self.distance = 0
        self.score = 0

        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 60, bold=True)

        self.jump_sound = pygame.mixer.Sound("sounds/jump.wav")
        self.score_sound = pygame.mixer.Sound("sounds/score.wav")
        self.game_over_sound = pygame.mixer.Sound("sounds/game_over.wav")

        self.game_over = False

    def set_difficulty(self, difficulty):
        if difficulty == "easy":
            self.speed = 4
            self.spawn_interval = 90
        elif difficulty == "hard":
            self.speed = 8
            self.spawn_interval = 55
        else:
            self.speed = 6
            self.spawn_interval = 70
            difficulty = "medium"

        self.difficulty = difficulty

    def restart(self, difficulty):
        self.set_difficulty(difficulty)

        self.player = Player(80, self.ground_y)
        self._spawn_timer = 0
        self.obstacles = []
        self.distance = 0
        self.score = 0
        self.game_over = False

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return False

        if self.game_over:
            if event.key == pygame.K_1:
                self.restart("easy")
            elif event.key == pygame.K_2:
                self.restart("medium")
            elif event.key == pygame.K_3:
                self.restart("hard")
            elif event.key == pygame.K_ESCAPE:
                return True

            return False

        if event.key in (
            pygame.K_SPACE,
            pygame.K_UP,
            pygame.K_w
        ):
            if self.player.on_ground:
                self.player.jump()
                self.jump_sound.play()

        return False

    def handle_input(self):
        pass

    def update(self):
        if self.game_over:
            return

        self.speed = min(
            self.speed + self.speed_increase_per_frame,
            self.max_speed
        )

        self.player.update()

        self._spawn_timer += 1

        if self._spawn_timer >= self.spawn_interval:
            self._spawn_timer = 0
            self.obstacles.append(
                Obstacle(
                    self.width,
                    self.ground_y,
                    self.speed
                )
            )

        for obstacle in self.obstacles:
            obstacle.move()
            obstacle.speed = self.speed

        for obstacle in self.obstacles:
            if obstacle.rect().colliderect(self.player.rect()):
                self.game_over = True
                self.game_over_sound.play()
                return

        for obstacle in self.obstacles:
            if (
                not obstacle.scored
                and obstacle.x + obstacle.width < self.player.x
            ):
                obstacle.scored = True
                self.score += 1
                self.score_sound.play()

        self.obstacles = [
            obstacle
            for obstacle in self.obstacles
            if not obstacle.off_screen()
        ]

        self.distance += self.speed

    def render(self, screen):
        pygame.draw.line(
            screen,
            BROWN,
            (0, self.ground_y),
            (self.width, self.ground_y),
            4
        )

        pygame.draw.rect(
            screen,
            WHITE,
            self.player.rect()
        )

        for obstacle in self.obstacles:
            pygame.draw.rect(
                screen,
                DARK_GREEN,
                obstacle.rect()
            )

        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            (0, 0, 0)
        )

        screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = self.game_over_font.render(
                "GAME OVER",
                True,
                (0, 0, 0)
            )

            final_score_text = self.font.render(
                f"Final Score: {self.score}",
                True,
                (0, 0, 0)
            )

            difficulty_text = self.font.render(
                "1 - EASY    2 - MEDIUM    3 - HARD",
                True,
                (0, 0, 0)
            )

            exit_text = self.font.render(
                "ESC - EXIT",
                True,
                (0, 0, 0)
            )

            game_over_rect = game_over_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 - 90
                )
            )

            score_rect = final_score_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 - 30
                )
            )

            difficulty_rect = difficulty_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 + 30
                )
            )

            exit_rect = exit_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 + 75
                )
            )

            screen.blit(game_over_text, game_over_rect)
            screen.blit(final_score_text, score_rect)
            screen.blit(difficulty_text, difficulty_rect)
            screen.blit(exit_text, exit_rect)