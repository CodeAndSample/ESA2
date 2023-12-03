import pygame
import random
from peewee import *

# Initialize database
# Create database
db = SqliteDatabase("game_high_scores.db")


# Create model
class HighScore(Model):
    player_name = CharField()
    stability = IntegerField()
    popularity = IntegerField()
    turns_taken = IntegerField()

    class Meta:
        database = db


# Connect to database and create table
db.connect()
db.create_tables([HighScore])


# Database functions
def get_high_scores():
    return (
        HighScore.select()
        .order_by(
            HighScore.popularity.desc(),
            HighScore.turns_taken.asc(),
            HighScore.stability.desc(),
        )
        .execute()
    )


def insert_high_score(player_name, popularity, stability, turns_taken):
    HighScore.create(
        player_name=player_name,
        popularity=popularity,
        stability=stability,
        turns_taken=turns_taken,
    )


# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
OFFICE_COLOR = (210, 180, 140)
BUTTON_COLOR = (100, 100, 200)
TEXT_BOX_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
TEXT_COLOR_SCORE = (255, 255, 255)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chancellor Simulator")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)


# Button class
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, BUTTON_COLOR, self.rect)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        screen.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Event class
class Event:
    def __init__(self, description, impact):
        self.description = description
        self.impact = impact

    def handle_event(self, action):
        if action == "delay":
            return random.choice([-1, 1, 3])
        elif action == "address":
            return self.impact


# Start Screen elements
start_screen = True
start_button = Button(540, 360, 200, 40, "Spiel starten")

# Start Screen Loop
while start_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_screen = False
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.is_clicked(event.pos):
                start_screen = False

    screen.fill(OFFICE_COLOR)
    # Display welcome message
    welcome_text = font.render("Der Kanzler-Simulator", True, TEXT_COLOR)
    info_text_1 = font.render(
        "Treffe keine Entscheidungen, um Deine Beliebtheit zu vergrößern und die Stabilität im Land zu gewährleisten.",
        True,
        TEXT_COLOR,
    )
    info_text_2 = font.render(
        "Das Spiel endet, wenn Du einen Beliebtheitswert von über 15 erreicht hast.",
        True,
        TEXT_COLOR,
    )
    screen.blit(welcome_text, (300, 200))
    screen.blit(info_text_1, (300, 240))
    screen.blit(info_text_2, (300, 260))

    # Draw the start button
    start_button.draw()

    pygame.display.flip()
    clock.tick(60)

# Game elements
popularity = 10
stability = 10
buttons = [
    Button(50, 550, 200, 40, "Entscheidung vertagen"),
    Button(300, 550, 200, 40, "Problem angehen"),
]
current_event = None
event_timer = 0
turns = 0

# Main game loop
running = True


def main_game_loop():
    global running, popularity, stability, turns, current_event, event_timer
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button in buttons:
                    if button.is_clicked(mouse_pos) and current_event:
                        # Handle event based on button clicked
                        if button.text == "Entscheidung vertagen":
                            change_popularity = current_event.handle_event("delay")
                            change_stability = random.choice([-1, 1, 3])
                        elif button.text == "Problem angehen":
                            change = current_event.handle_event("address")
                        # Update metrics
                        popularity += change_popularity
                        stability += change_stability
                        turns += 1
                        current_event = None

        # Generate a random event periodically
        event_timer += 1
        if event_timer > 150:
            event_timer = 0
            event_descriptions = [
                "Diplomatische Krise",
                "Wirtschaftskrise",
                "Naturkatastrophe",
                "Korruptionsskandal",
                "Terroranschlag",
                "Pandemie",
                "Krieg",
                "Wahlkampf",
                "Streik",
                "Klimawandel",
                "Inflation",
                "Finanzkrise",
                "Flüchtlingskrise",
                "Krise in der Regierung",
                "Krise in der Opposition",
            ]

            impacts = [-3, -5, -9]  # More significant impact
            current_event = Event(
                random.choice(event_descriptions), random.choice(impacts)
            )

        # Clear screen
        screen.fill(OFFICE_COLOR)

        # Use image as background instead of color
        background = pygame.image.load("images/office.jpg", "office")

        # fill the screen with the background image
        screen.blit(
            background, (0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), special_flags=0
        )

        # Draw buttons, metrics, and event
        for button in buttons:
            button.draw()
        popularity_text = font.render(
            f"Beliebtheit: {popularity}", True, TEXT_COLOR_SCORE
        )
        stability_text = font.render(f"Stabilität: {stability}", True, TEXT_COLOR_SCORE)
        screen.blit(popularity_text, (600, 20))
        screen.blit(stability_text, (600, 50))
        if current_event:
            event_text = font.render(
                f"Ereignis: {current_event.description}", True, TEXT_COLOR
            )
            # Draw a box around the event text and fill it with white
            pygame.draw.rect(screen, TEXT_BOX_COLOR, (50, 500, 500, 40))

            screen.blit(event_text, (55, 505))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

        if popularity > 15:
            # End pygame loop
            running = False


main_game_loop()


# Get player name using Tkinter
class InputBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = TEXT_BOX_COLOR
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = TEXT_COLOR if self.active else TEXT_BOX_COLOR
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text  # Return text when Enter is pressed
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = font.render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


input_box = InputBox(100, 100, 140, 32)
# Add text next to the input box to save their score and enter their name with enter


player_name = ""
play_again_button = Button(540, 560, 200, 40, "Noch einmal spielen")
end_screen = True

end_screen = True
score_recorded = False
while end_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_screen = False
        player_name = input_box.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_again_button.is_clicked(event.pos):
                running = True  # Restart the game
                event_timer = 0
                popularity = 10
                stability = 10
                turns = 0
                score_recorded = False
                player_name = ""
                main_game_loop()

    # Only record and show the score once
    if player_name and not score_recorded:
        insert_high_score(player_name, popularity, stability, turns)
        score_recorded = True

    screen.fill(OFFICE_COLOR)
    if not score_recorded:
        input_box.draw(screen)
        screen.blit(
            font.render(
                "Namen eingeben und mit <ENTER> den Highscore speichern",
                True,
                TEXT_COLOR,
            ),
            (50, 135),
        )

    if score_recorded:
        # Remove the input box
        pygame.draw.rect(screen, OFFICE_COLOR, input_box.rect)
        high_scores = get_high_scores()
        for i, score in enumerate(high_scores):
            score_text = font.render(
                f"{i+1}. {score.player_name} - Popularität: {score.popularity} - Anzahl der Runden: {score.turns_taken} - Stabilität: {score.stability}",
                True,
                TEXT_COLOR,
            )
            screen.blit(score_text, (100, 150 + 30 * i))
        play_again_button.draw()

    pygame.display.flip()
    clock.tick(30)


# close database connection peewee
db.close()
pygame.quit()
