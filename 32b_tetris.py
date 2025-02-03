                                                                                                                
import pygame                                                                                                     
from random import randint                                                                                        
                                                                                                                
pygame.init()                                                                                                     
                                                                                                                
# Colors                                                                                                          
BLACK = (0, 0, 0)                                                                                                 
WHITE = (255, 255, 255)                                                                                           
RED = (255, 0, 0)                                                                                                 
GREEN = (0, 255, 0)                                                                                               
BLUE = (0, 0, 255)                                                                                                
CYAN = (0, 255, 255)                                                                                              
MAGENTA = (255, 0, 255)                                                                                           
YELLOW = (255, 255, 0)                                                                                            
                                                                                                                
# Tetromino shapes                                                                                                
SHAPES = [                                                                                                        
    [[(0, 0), (1, 0), (2, 0), (3, 0)], RED],          # I                                                         
    [[(0, 0), (1, 0), (1, -1), (1, 1)], GREEN],       # T                                                         
    [[(0, 0), (1, 0), (2, 0), (2, 1)], BLUE],         # L                                                         
    [[(0, 0), (1, 0), (2, 0), (0, -1)], CYAN],        # J                                                         
    [[(0, 0), (1, 0), (1, -1), (2, -1)], MAGENTA],    # Z                                                         
    [[(0, 0), (1, 0), (1, 1), (2, 0)], YELLOW],       # S                                                         
    [[(0, 0), (1, 0), (0, -1), (1, -1)], WHITE]       # O                                                         
]                                                                                                                 
                                                                                                                
# Game constants                                                                                                  
BLOCK_SIZE = 30                                                                                                   
WIDTH = 10                                                                                                        
HEIGHT = 20                                                                                                       
SCREEN_WIDTH = WIDTH * BLOCK_SIZE + 200  # Extra space for next piece display                                     
SCREEN_HEIGHT = HEIGHT * BLOCK_SIZE                                                                               
                                                                                                                
# Initialize the screen                                                                                           
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))                                                   
pygame.display.set_caption("Tetris")                                                                              
                                                                                                                
class Tetromino:                                                                                                  
    def __init__(self):                                                                                           
        self.shape, self.color = SHAPES[randint(0, len(SHAPES)-1)]                                                
        self.x = WIDTH // 2                                                                                       
        self.y = 0                                                                                                
                                                                                                                
    def rotate(self, direction=1):                                                                                
        new_shape = []                                                                                            
        for (x, y) in self.shape:                                                                                 
            if direction == 1:  # Clockwise                                                                       
                new_x = -y                                                                                        
                new_y = x                                                                                         
            else:  # Counter-clockwise                                                                            
                new_x = y                                                                                         
                new_y = -x                                                                                        
            new_shape.append((new_x + self.x, new_y + self.y))                                                    
        return new_shape                                                                                          
                                                                                                                
class Board:                                                                                                      
    def __init__(self):                                                                                           
        self.grid = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]                                         
        self.score = 0                                                                                            
                                                                                                                
    def draw(self):                                                                                               
        for y in range(HEIGHT):                                                                                   
            for x in range(WIDTH):                                                                                
                if self.grid[y][x]:                                                                               
                    pygame.draw.rect(screen, self.grid[y][x],                                                     
                                (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE-1, BLOCK_SIZE-1))                      
                                                                                                                
def draw_next_piece(tetromino):                                                                                   
    font = pygame.font.Font(None, 36)                                                                             
    text = font.render("Next Piece:", True, WHITE)                                                                
    screen.blit(text, (SCREEN_WIDTH // 2 - 60, 20))                                                               
    for x, y in tetromino.shape:                                                                                  
        pygame.draw.rect(screen, tetromino.color,                                                                 
                        ((x + 4) * BLOCK_SIZE, (y + 5) * BLOCK_SIZE,                                             
                        BLOCK_SIZE-1, BLOCK_SIZE-1))                                                            
                                                                                                                
def draw_score(score):                                                                                            
    font = pygame.font.Font(None, 36)                                                                             
    text = font.render(f"Score: {score}", True, WHITE)                                                            
    screen.blit(text, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT - 50))                                               
                                                                                                                
def game_over():                                                                                                  
    font = pygame.font.Font(None, 74)                                                                             
    text = font.render("Game Over!", True, RED)                                                                   
    screen.blit(text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2))                                                  
    pygame.display.flip()                                                                                         
    pygame.time.wait(2000)                                                                                        
    return False                                                                                                  
                                                                                                                
def main():                                                                                                       
    clock = pygame.time.Clock()                                                                                   
    board = Board()                                                                                               
    current_tetromino = Tetromino()                                                                               
    next_tetromino = Tetromino()                                                                                  
    game_speed = 1                                                                                                
    last_drop = 0                                                                                                 
    running = True                                                                                                
                                                                                                                
    while running:                                                                                                
        for event in pygame.event.get():                                                                          
            if event.type == pygame.QUIT:                                                                         
                running = False                                                                                   
            if event.type == pygame.KEYDOWN:                                                                      
                if event.key == pygame.K_LEFT:                                                                    
                    current_tetromino.x -= 1                                                                      
                    rotated = current_tetromino.rotate()                                                          
                elif event.key == pygame.K_RIGHT:                                                                 
                    current_tetromino.x += 1                                                                      
                    rotated = current_tetromino.rotate()                                                          
                elif event.key == pygame.K_UP:                                                                    
                    rotated = current_tetromino.rotate(-1)                                                        
                elif event.key == pygame.K_DOWN:                                                                  
                    current_tetromino.y += 1                                                                      
                                                                                                                
        screen.fill(BLACK)                                                                                        
                                                                                                                
        # Move piece down at intervals                                                                            
        if pygame.time.get_ticks() - last_drop > 1000 / game_speed:                                               
            current_tetromino.y += 1                                                                              
            last_drop = pygame.time.get_ticks()                                                                   
                                                                                                                
        # Check for collisions and rotate                                                                         
        temp_shape = [ (x + current_tetromino.x, y + current_tetromino.y)                                         
                    for x, y in current_tetromino.shape ]                                                       
        collision = False                                                                                         
        for (x, y) in temp_shape:                                                                                 
            if not (0 <= x < WIDTH and 0 <= y < HEIGHT):                                                          
                collision = True                                                                                  
            elif board.grid[y][x] is not None:                                                                    
                collision = True                                                                                  
        if collision:                                                                                             
            current_tetromino.y -= 1                                                                              
            for (x, y) in temp_shape:                                                                             
                board.grid[y][x - (current_tetromino.x)] = current_tetromino.color                                
                                                                                                                
            # Check for completed lines                                                                           
            lines_cleared = 0                                                                                     
            for y in range(HEIGHT-1, -1, -1):                                                                     
                if all(board.grid[y][x] is not None for x in range(WIDTH)):                                       
                    board.grid.pop(y)                                                                             
                    board.grid.insert(0, [None]*WIDTH)                                                            
                    lines_cleared += 1                                                                            
                    board.score += (lines_cleared**2)*100                                                         
                                                                                                                
            # Start new piece                                                                                     
            current_tetromino = next_tetromino                                                                    
            next_tetromino = Tetromino()                                                                          
            if any(x < 0 or x >= WIDTH for x, y in temp_shape):                                                   
                running = game_over()                                                                             
                                                                                                                
        # Draw                                                                                                    
        board.draw()                                                                                              
        draw_next_piece(next_tetromino)                                                                           
        draw_score(board.score)                                                                                   
                                                                                                                
        # Update screen                                                                                           
        pygame.display.flip()                                                                                     
        clock.tick(60)                                                                                            
                                                                                                                
    pygame.quit()                                                                                                 
                                                                                                                
if __name__ == "__main__":                                                                                        
    main()  