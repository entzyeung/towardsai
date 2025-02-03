import pygame                                                                                                     
import random                                                                                                     
pygame.init()                                                                                                     
                                                                                                                
# Game Window Dimensions                                                                                          
window_width = 800                                                                                                
window_height = 600                                                                                               
                                                                                                                
# Colors                                                                                                          
BLACK = (0, 0, 0)                                                                                                 
WHITE = (255, 255, 255)                                                                                           
RED = (255, 0, 0)                                                                                                 
GREEN = (0, 255, 0)                                                                                               
                                                                                                                
# Initialize Display                                                                                              
display = pygame.display.set_mode((window_width, window_height))                                                  
pygame.display.set_caption("Snake Game")                                                                          
                                                                                                                
# Snake and Food Setup                                                                                            
snake_block = 20                                                                                                  
snake_speed = 15                                                                                                  
                                                                                                                
# Initial Positions                                                                                               
x1 = window_width / 4                                                                                             
y1 = window_height / 2                                                                                            
x1_int = int(x1)                                                                                                  
y1_int = int(y1)                                                                                                  
                                                                                                                
# Direction Variables                                                                                             
dx = snake_block                                                                                                  
dy = 0                                                                                                            
                                                                                                                
foodx = round(random.randrange(0, window_width - snake_block) / 20.0) * 20.0                                      
foody = round(random.randrange(0, window_height - snake_block) / 20.0) * 20.0                                     
                                                                                                                
score = 0                                                                                                         
                                                                                                                
snake_List = []                                                                                                   
snake_Length = 1                                                                                                  
                                                                                                                
game_over = False                                                                                                 
running = True                                                                                                    
clock = pygame.time.Clock()                                                                                       
                                                                                                                
while running:                                                                                                    
    while game_over:                                                                                              
        display.fill(BLACK)                                                                                       
        font_style = pygame.font.SysFont(None, 50)                                                                
        mesg = font_style.render("You Lost! Press Q-Quit or C-Play Again", True, RED)                             
        mesg_rect = mesg.get_rect(center=(window_width / 2, window_height / 2))                                   
        display.blit(mesg, mesg_rect)                                                                             
                                                                                                                
        pygame.display.update()                                                                                   
        for event in pygame.event.get():                                                                          
            if event.type == pygame.KEYDOWN:                                                                      
                if event.key == pygame.K_q:                                                                       
                    running = False                                                                               
                    game_over = False                                                                             
                if event.key == pygame.K_c:                                                                       
                    # Reset Game State                                                                            
                    x1 = window_width / 4                                                                         
                    y1 = window_height / 2                                                                        
                    dx = snake_block                                                                              
                    dy = 0                                                                                        
                    score = 0                                                                                     
                    snake_List = []                                                                               
                    snake_Length = 1                                                                              
                    foodx = round(random.randrange(0, window_width - snake_block) / 20.0) * 20.0                  
                    foody = round(random.randrange(0, window_height - snake_block) / 20.0) * 20.0                 
                    game_over = False                                                                             
                                                                                                                
    for event in pygame.event.get():                                                                              
        if event.type == pygame.QUIT:                                                                             
            running = False                                                                                       
        if event.type == pygame.KEYDOWN:                                                                          
            if event.key == pygame.K_LEFT and dx == 0:  # Prevent moving left when going right                    
                dx = -snake_block                                                                                 
                dy = 0                                                                                            
            elif event.key == pygame.K_RIGHT and dx == 0:  # Prevent moving right when going left                 
                dx = snake_block                                                                                  
                dy = 0                                                                                            
            elif event.key == pygame.K_UP and dy == 0:    # Prevent moving up when going down                     
                dx = 0                                                                                            
                dy = -snake_block                                                                                 
            elif event.key == pygame.K_DOWN and dy == 0:  # Prevent moving down when going up                     
                dx = 0                                                                                            
                dy = snake_block                                                                                  
                                                                                                                
    if not game_over:                                                                                             
        x1 += dx                                                                                                  
        y1 += dy                                                                                                  
                                                                                                                
        # Check if Snake has eaten Food                                                                           
        if x1 == foodx and y1 == foody:                                                                           
            score += 10                                                                                           
            foodx = round(random.randrange(0, window_width - snake_block) / 20.0) * 20.0                          
            foody = round(random.randrange(0, window_height - snake_block) / 20.0) * 20.0                         
            snake_Length += 1                                                                                     
                                                                                                                
        # Update Snake Body                                                                                       
        snake_Head = []                                                                                           
        snake_Head.append(x1)                                                                                     
        snake_Head.append(y1)                                                                                     
        snake_List.append(snake_Head)                                                                             
                                                                                                                
        if len(snake_List) > snake_Length:                                                                        
            del snake_List[0]                                                                                     
                                                                                                                
        # Check for Collision with Walls or Self                                                                  
        for x in range(len(snake_List)):                                                                          
            if x == 0 and (snake_List[x][0] < 0 or snake_List[x][0] >= window_width or                            
                        snake_List[x][1] < 0 or snake_List[x][1] >= window_height):                            
                game_over = True                                                                                  
            for other in range(len(snake_List)):                                                                  
                if x != other and snake_List[x][0] == snake_List[other][0] and snake_List[x][1] == snake_List[other][1]:                                                      
                    game_over = True                                                                              
                                                                                                                
        # Drawing                                                                                                 
        display.fill(BLACK)                                                                                       
        font_style = pygame.font.SysFont(None, 25)                                                                
        score_mesg = font_style.render(f"Score: {score}", True, WHITE)                                            
        display.blit(score_mesg, [0, 0])                                                                          
                                                                                                                
        for x in snake_List:                                                                                      
            pygame.draw.rect(display, GREEN, [x[0], x[1], snake_block, snake_block])                              
                                                                                                                
        pygame.draw.rect(display, RED, [foodx, foody, snake_block, snake_block])                                  
        pygame.display.update()                                                                                   
                                                                                                                
    clock.tick(snake_speed)                                                                                       
                                                                                                                
pygame.quit() 