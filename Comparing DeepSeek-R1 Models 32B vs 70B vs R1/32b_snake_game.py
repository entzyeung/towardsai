import pygame                                                                                                     
import sys                                                                                                        
import random                                                                                                     
from pygame.locals import *                                                                                       
                                                                                                                
# Set up window dimensions                                                                                        
WINDOW_WIDTH = 800                                                                                                
WINDOW_HEIGHT = 600                                                                                               
BLOCK_SIZE = 20                                                                                                   
FPS = 15                                                                                                          
                                                                                                                
# Colors                                                                                                          
BLACK = (0, 0, 0)                                                                                                 
RED = (255, 0, 0)                                                                                                 
WHITE = (255, 255, 255)                                                                                           
                                                                                                                
pygame.init()                                                                                                     
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))                                           
pygame.display.set_caption('Snake Game')                                                                          
clock = pygame.time.Clock()                                                                                       
                                                                                                                
def main():                                                                                                       
    # Initial snake position and direction                                                                        
    start_x = WINDOW_WIDTH // 4                                                                                   
    start_y = WINDOW_HEIGHT // 4                                                                                  
    snake = [{'x': start_x, 'y': start_y}]                                                                        
    direction = 'RIGHT'                                                                                           
    food = {'x': random.randint(0, (WINDOW_WIDTH//BLOCK_SIZE)-1)*BLOCK_SIZE,                                      
            'y': random.randint(0, (WINDOW_HEIGHT//BLOCK_SIZE)-1)*BLOCK_SIZE}                                     
                                                                                                                
    while True:                                                                                                   
        for event in pygame.event.get():                                                                          
            if event.type == QUIT:                                                                                
                pygame.quit()                                                                                     
                sys.exit()                                                                                        
            elif event.type == KEYDOWN:                                                                           
                if (event.key == K_UP or event.key == K_w) and direction != 'DOWN':                               
                    direction = 'UP'                                                                              
                elif (event.key == K_DOWN or event.key == K_s) and direction != 'UP':                             
                    direction = 'DOWN'                                                                            
                elif (event.key == K_LEFT or event.key == K_a) and direction != 'RIGHT':                          
                    direction = 'LEFT'                                                                            
                elif (event.key == K_RIGHT or event.key == K_d) and direction != 'LEFT':                          
                    direction = 'RIGHT'                                                                           
                                                                                                                
        # Move snake                                                                                              
        head = {'x': snake[0]['x'], 'y': snake[0]['y']}                                                           
                                                                                                                
        if direction == 'UP':                                                                                     
            head['y'] -= BLOCK_SIZE                                                                               
        elif direction == 'DOWN':                                                                                 
            head['y'] += BLOCK_SIZE                                                                               
        elif direction == 'LEFT':                                                                                 
            head['x'] -= BLOCK_SIZE                                                                               
        elif direction == 'RIGHT':                                                                                
            head['x'] += BLOCK_SIZE                                                                               
                                                                                                                
        # Check for collisions with walls or self                                                                 
        if (head['x'] < 0 or head['x'] >= WINDOW_WIDTH or                                                         
            head['y'] < 0 or head['y'] >= WINDOW_HEIGHT or                                                        
            head in snake[1:]):                                                                                   
            game_over()                                                                                           
                                                                                                                
        snake.insert(0, head)                                                                                     
                                                                                                                
        # Check for food collision                                                                                
        if head['x'] == food['x'] and head['y'] == food['y']:                                                     
            food = {'x': random.randint(0, (WINDOW_WIDTH//BLOCK_SIZE)-1)*BLOCK_SIZE,                              
                    'y': random.randint(0, (WINDOW_HEIGHT//BLOCK_SIZE)-1)*BLOCK_SIZE}                             
        else:                                                                                                     
            snake.pop()                                                                                           
                                                                                                                
        # Draw window                                                                                             
        window_surface.fill(WHITE)                                                                                
                                                                                                                
        for segment in snake:                                                                                     
            pygame.draw.rect(window_surface, BLACK, (segment['x'], segment['y'], BLOCK_SIZE, BLOCK_SIZE))         
                                                                                                                
        pygame.draw.rect(window_surface, RED, (food['x'], food['y'], BLOCK_SIZE, BLOCK_SIZE))                     
                                                                                                                
        # Update window                                                                                           
        pygame.display.update()                                                                                   
        clock.tick(FPS)                                                                                           
                                                                                                                
def game_over():                                                                                                  
    font = pygame.font.Font('freesansbold.ttf', 32)                                                               
    text = font.render('Game Over!', True, BLACK)                                                                 
    text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))                                           
                                                                                                                
    window_surface.fill(WHITE)                                                                                    
    window_surface.blit(text, text_rect)                                                                          
    pygame.display.update()                                                                                       
                                                                                                                
    # Wait for a second then exit                                                                                 
    time.sleep(1)                                                                                                 
    pygame.quit()                                                                                                 
    sys.exit()                                                                                                    
                                                                                                                
if __name__ == '__main__':                                                                                        
    main()              