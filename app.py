import pygame
import random
import os
import sys
import cmath  # For complex number operations

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cat Runner Game")

# Game constants
GROUND_LEVEL = SCREEN_HEIGHT - 100  # Define a consistent ground level
PLAYER_X = 100  # Fixed x position for the player

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Game states
PLAYING = "playing"
GAME_OVER = "game_over"

# Complex number constants for movement
JUMP_COMPLEX = complex(0, -15)  # Complex number for jump
GRAVITY_COMPLEX = complex(0, 0.5)  # Complex number for gravity
MOVEMENT_COMPLEX = complex(5, 0)  # Complex number for horizontal movement

# Load assets
cat_image = pygame.image.load("cat.png")
mouse_image = pygame.image.load("mouse.png")
tree_image = pygame.image.load("tree.png")
dog_image = pygame.image.load("dog.png")
background_image = pygame.image.load("background.png")

# Scale images
cat_image = pygame.transform.scale(cat_image, (70, 70))
mouse_image = pygame.transform.scale(mouse_image, (40, 40))
tree_image = pygame.transform.scale(tree_image, (60, 80))
dog_image = pygame.transform.scale(dog_image, (60, 60))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Create cat animation frames
cat_frames = []
frame_width = cat_image.get_width()
frame_height = cat_image.get_height()
cat_frames.append(cat_image)  # Original frame
# Create slightly different frames for animation
for i in range(3):
    frame = cat_image.copy()
    if i == 1:  # Second frame - cat slightly up
        frame = pygame.transform.scale(cat_image, (70, 65))
    elif i == 2:  # Third frame - cat slightly down
        frame = pygame.transform.scale(cat_image, (70, 75))
    cat_frames.append(frame)

# Load sounds
jump_sound = pygame.mixer.Sound("jump.wav")
collision_sound = pygame.mixer.Sound("collision.wav")
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1, 0.0)

# Load fonts
title_font = pygame.font.Font(None, 74)
font = pygame.font.Font(None, 36)

# Button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (50, 200, 50)
BUTTON_HOVER_COLOR = (70, 220, 70)

class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = cat_frames
        self.current_frame = 0
        self.animation_speed = 100
        self.last_update = pygame.time.get_ticks()
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, GROUND_LEVEL)
        self.velocity = complex(0, 0)  # Using complex number for velocity
        self.is_jumping = False
        self.gravity = GRAVITY_COMPLEX
        self.jump_power = JUMP_COMPLEX

    def update(self):
        # Update animation
        now = pygame.time.get_ticks()
        if not self.is_jumping and now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            bottom = self.rect.bottom
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.midbottom = (SCREEN_WIDTH // 2, bottom)

        # Update physics using complex numbers
        self.velocity += self.gravity
        if self.velocity.imag > 15:
            self.velocity = complex(self.velocity.real, 15)
            
        # Apply velocity to position
        self.rect.x += int(self.velocity.real)
        self.rect.y += int(self.velocity.imag)
        
        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL
            self.velocity = complex(self.velocity.real, 0)
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = self.jump_power
            self.current_frame = 0
            self.image = self.frames[self.current_frame]
            jump_sound.play()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        
        # Use complex number for position
        self.position = complex(SCREEN_WIDTH + 50, GROUND_LEVEL)
        
        # Adjust height based on obstacle type
        if image == mouse_image:
            self.type = "mouse"
            self.speed = complex(-speed, 0)
            # Position mouse slightly above ground
            self.rect.bottom = GROUND_LEVEL - 5
        else:  # tree
            self.type = "tree"
            # Randomly choose tree type
            self.tree_type = random.choice(["normal", "fast", "bouncing"])
            if self.tree_type == "fast":
                self.speed = complex(-speed * 1.5, 0)  # 50% faster
                self.image = pygame.transform.scale(tree_image, (50, 70))  # Smaller but faster
            elif self.tree_type == "bouncing":
                self.speed = complex(-speed, 0)
                self.bounce_height = 0
                self.bounce_speed = 0.2
                self.bounce_direction = 1
            else:  # normal
                self.speed = complex(-speed, 0)
            # Position tree on ground
            self.rect.bottom = GROUND_LEVEL
            
        self.rect.left = int(self.position.real)
        self.passed = False
        self.caught = False

    def update(self):
        # Update position using complex numbers
        self.position += self.speed
        
        # Special behavior for bouncing trees
        if self.type == "tree" and self.tree_type == "bouncing":
            self.bounce_height += self.bounce_speed * self.bounce_direction
            if self.bounce_height > 20 or self.bounce_height < 0:
                self.bounce_direction *= -1
            # Keep the tree's bottom at ground level while bouncing
            self.rect.bottom = GROUND_LEVEL - self.bounce_height
        else:
            # For non-bouncing obstacles, keep them at their proper height
            if self.type == "mouse":
                self.rect.bottom = GROUND_LEVEL - 5
            else:  # tree
                self.rect.bottom = GROUND_LEVEL
        
        self.rect.x = int(self.position.real)
        
        if self.rect.right < 0:
            self.kill()


def draw_button(text, x, y, width, height, color):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect

def reset_game(cat, all_sprites, obstacles):
    # Reset cat position and state
    cat.rect.midbottom = (SCREEN_WIDTH // 2, GROUND_LEVEL)
    cat.velocity = complex(0, 0)
    cat.is_jumping = False
    
    # Clear all obstacles
    for sprite in all_sprites:
        if sprite != cat:
            sprite.kill()
    obstacles.empty()
    
    return 0  # Reset score

def draw_score_popup(x, y, score):
    score_text = font.render(f"+{score}", True, GREEN)
    screen.blit(score_text, (x, y))

def draw_warning(x, y):
    warning_text = font.render("!", True, YELLOW)
    screen.blit(warning_text, (x, y))

def main():
    cat = Cat()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(cat)

    obstacles = pygame.sprite.Group()
    score = 0
    high_score = 0
    clock = pygame.time.Clock()
    game_state = PLAYING
    
    # Background scrolling using complex numbers
    bg_position = complex(0, 0)
    bg_scroll_speed = complex(-5, 0)
    bg_width = background_image.get_width()
    
    # Add time tracking for score
    time_since_last_point = 0
    point_interval = 1000  # Increased interval for slower point gain
    
    # Obstacle spawning control
    spawn_timer = 0
    spawn_delay = 2000  # Increased delay between spawns
    last_obstacle_x = SCREEN_WIDTH
    min_obstacle_spacing = 300

    # Score popup tracking
    score_popups = []  # List to store active score popups
    
    # Warning system
    warnings = []  # List to store active warnings
    
    # Mouse spawn tracking
    mouse_spawn_timer = 0
    mouse_spawn_delay = 8000  # Mice appear every 8 seconds
    
    running = True
    while running:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state == PLAYING:
                    cat.jump()
            if event.type == pygame.MOUSEBUTTONDOWN and game_state == GAME_OVER:
                mouse_pos = pygame.mouse.get_pos()
                button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2,
                                        SCREEN_HEIGHT * 2 // 3,
                                        BUTTON_WIDTH, BUTTON_HEIGHT)
                if button_rect.collidepoint(mouse_pos):
                    game_state = PLAYING
                    score = reset_game(cat, all_sprites, obstacles)
                    pygame.mixer.music.play(-1)

        if game_state == PLAYING:
            time_since_last_point += dt
            spawn_timer += dt
            mouse_spawn_timer += dt
            
            if time_since_last_point >= point_interval:
                score += 1
                time_since_last_point = 0
            
            # Scroll background using complex numbers
            bg_position += bg_scroll_speed
            if bg_position.real <= -bg_width:
                bg_position = complex(0, 0)
                
            # Draw scrolling background
            screen.fill(WHITE)
            screen.blit(background_image, (int(bg_position.real), 0))
            screen.blit(background_image, (int(bg_position.real + bg_width), 0))

            # Update and draw all sprites
            all_sprites.update()
            all_sprites.draw(screen)

            # Check if we can spawn a new obstacle
            can_spawn = True
            for obstacle in obstacles:
                if obstacle.rect.right > last_obstacle_x:
                    last_obstacle_x = obstacle.rect.right
                if SCREEN_WIDTH - obstacle.rect.left < min_obstacle_spacing:
                    can_spawn = False

            # Spawn trees based on timer and spacing
            if spawn_timer >= spawn_delay and can_spawn:
                spawn_timer = 0
                obstacle = Obstacle(tree_image, 5)  # Always spawn trees
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
                last_obstacle_x = obstacle.rect.right

            # Spawn mice separately with their own timer
            if mouse_spawn_timer >= mouse_spawn_delay and can_spawn:
                mouse_spawn_timer = 0
                # Only spawn mice if there are less than 2 mice on screen
                mouse_count = sum(1 for obs in obstacles if obs.type == "mouse")
                if mouse_count < 2:
                    obstacle = Obstacle(mouse_image, 5)
                    all_sprites.add(obstacle)
                    obstacles.add(obstacle)
                    last_obstacle_x = obstacle.rect.right

            # Check for collisions and update score
            for obstacle in obstacles:
                if pygame.sprite.collide_rect(cat, obstacle):
                    if obstacle.type == "tree":
                        collision_sound.play()
                        pygame.mixer.music.stop()
                        high_score = max(score, high_score)
                        game_state = GAME_OVER
                    elif obstacle.type == "mouse" and not obstacle.caught:
                        obstacle.caught = True
                        score += 5  # Reduced points for catching mice
                        score_popups.append({
                            'x': obstacle.rect.centerx,
                            'y': obstacle.rect.top,
                            'timer': 30,
                            'score': 5
                        })
                        obstacle.kill()

            # Update and draw score popups
            for popup in score_popups[:]:
                popup['timer'] -= 1
                popup['y'] -= 1  # Move popup upward
                if popup['timer'] <= 0:
                    score_popups.remove(popup)
                else:
                    draw_score_popup(popup['x'], popup['y'], popup['score'])

            # Draw score
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))
            
            # Draw high score
            high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
            screen.blit(high_score_text, (SCREEN_WIDTH - 200, 10))

        elif game_state == GAME_OVER:
            # Draw game over screen
            screen.fill(WHITE)
            game_over_text = title_font.render("Game Over!", True, RED)
            score_text = font.render(f"Score: {score}", True, BLACK)
            high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
            
            screen.blit(game_over_text, 
                       (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                        SCREEN_HEIGHT // 3))
            screen.blit(score_text,
                       (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                        SCREEN_HEIGHT // 2))
            screen.blit(high_score_text,
                       (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2,
                        SCREEN_HEIGHT // 2 + 40))
            
            # Draw play again button
            mouse_pos = pygame.mouse.get_pos()
            button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2,
                                    SCREEN_HEIGHT * 2 // 3,
                                    BUTTON_WIDTH, BUTTON_HEIGHT)
            button_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
            draw_button("Play Again", button_rect.x, button_rect.y,
                       BUTTON_WIDTH, BUTTON_HEIGHT, button_color)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()