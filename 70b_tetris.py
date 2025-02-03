import pygame                                                                                                     
import random                                                                                                     
                                                                                                                
pygame.init()                                                                                                     
                                                                                                                
# Define colors                                                                                                   
BLACK = (0, 0, 0)                                                                                                 
WHITE = (255, 255, 255)                                                                                           
GRAY = (128, 128, 128)                                                                                            
                                                                                                                
# Board dimensions                                                                                                
BOARD_WIDTH = 10                                                                                                  
BOARD_HEIGHT = 20                                                                                                 
BLOCK_SIZE = 30                                                                                                   
                                                                                                                
# Shapes                                                                                                          
SHAPES = {                                                                                                        
    'I': [[1, 1, 1, 1]],                                                                                          
    'O': [[1, 1], [1, 1]],                                                                                        
    'T': [[0, 1, 0], [1, 1, 1]],                                                                                  
    'S': [[0, 1, 1], [1, 1, 0]],                                                                                  
    'Z': [[1, 1, 0], [0, 1, 1]],                                                                                  
    'J': [[1, 0, 0], [1, 1, 1]],                                                                                  
    'L': [[0, 0, 1], [1, 1, 1]]                                                                                   
}                                                                                                                 
                                                                                                                
# Colors for each shape                                                                                           
COLORS = {                                                                                                        
    'I': (0, 255, 255),                                                                                           
    'O': (255, 255, 0),                                                                                           
    'T': (0, 255, 255),                                                                                           
    'S': (0, 255, 0),                                                                                             
    'Z': (255, 0, 0),                                                                                             
    'J': (0, 0, 255),                                                                                             
    'L': (255, 165, 0)                                                                                            
}                                                                                                                 
                                                                                                                
class Tetris:                                                                                                     
    def __init__(self):                                                                                           
        self.width = BOARD_WIDTH * BLOCK_SIZE                                                                     
        self.height = BOARD_HEIGHT * BLOCK_SIZE                                                                   
        self.screen = pygame.display.set_mode((self.width + 300, self.height))                                    
        self.clock = pygame.time.Clock()                                                                          
        self.font = pygame.font.Font(None, 36)                                                                    
                                                                                                                
        self.board = self.create_board()                                                                          
        self.score = 0                                                                                            
                                                                                                                
        self.current_piece = None                                                                                 
        self.game_over = False                                                                                    
                                                                                                                
    def create_board(self):                                                                                       
        return [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]                                     
                                                                                                                
    def get_new_piece(self):                                                                                      
        shape = random.choice(list(SHAPES.keys()))                                                                
        matrix = SHAPES[shape]                                                                                    
        color = COLORS[shape]                                                                                     
                                                                                                                
        x = (BOARD_WIDTH - len(matrix[0])) // 2                                                                   
        y = 0                                                                                                     
                                                                                                                
        return {'shape': shape, 'matrix': matrix, 'color': color, 'x': x, 'y': y}                                 
                                                                                                                
    def draw_text(self, text, x, y):                                                                              
        text_surface = self.font.render(text, True, WHITE)                                                        
        self.screen.blit(text_surface, (x + 50, y))                                                               
                                                                                                                
    def draw(self):                                                                                               
        self.screen.fill(BLACK)                                                                                   
                                                                                                                
        # Draw board                                                                                              
        for i in range(BOARD_HEIGHT):                                                                             
            for j in range(BOARD_WIDTH):                                                                          
                if self.board[i][j] != 0:                                                                         
                    pygame.draw.rect(                                                                             
                        self.screen,                                                                              
                        (self.board[i][j]),                                                                       
                        [j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE]                                  
                    )                                                                                             
                                                                                                                
        # Draw current piece                                                                                      
        if self.current_piece is not None:                                                                        
            matrix = self.current_piece['matrix']                                                                 
            x = self.current_piece['x']                                                                           
            y = self.current_piece['y']                                                                           
                                                                                                                
            for i in range(len(matrix)):                                                                          
                for j in range(len(matrix[i])):                                                                   
                    if matrix[i][j] == 1:                                                                         
                        color = self.current_piece['color']                                                       
                        pygame.draw.rect(                                                                         
                            self.screen,                                                                          
                            color,                                                                                
                            [(j + x) * BLOCK_SIZE, (i + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE]                  
                        )                                                                                         
                                                                                                                
        # Draw score                                                                                              
        self.draw_text(f'Score: {self.score}', self.width, 100)                                                   
                                                                                                                
        if self.game_over:                                                                                        
            self.draw_text('Game Over!', self.width, 200)                                                         
            self.draw_text('Press Q to quit or R to restart', self.width, 250)                                    
                                                                                                                
        pygame.display.update()                                                                                   
                                                                                                                
    def rotate(self, matrix):                                                                                     
        rotated = list(zip(*matrix[::-1]))                                                                        
        return [list(row) for row in rotated]                                                                     
                                                                                                                
    def move_down(self):                                                                                          
        if self.current_piece['y'] + len(self.current_piece['matrix']) == BOARD_HEIGHT:                           
            return False                                                                                          
        self.current_piece['y'] += 1                                                                              
        return True                                                                                               
                                                                                                                
    def move_side(self, dx):                                                                                      
        new_x = self.current_piece['x'] + dx                                                                      
        if new_x < 0 or (new_x + len(self.current_piece['matrix'][0])) > BOARD_WIDTH:                             
            return False                                                                                          
        self.current_piece['x'] = new_x                                                                           
        return True                                                                                               
                                                                                                                
    def rotate_piece(self):                                                                                       
        matrix = self.rotate(self.current_piece['matrix'])                                                        
        original_matrix = self.current_piece['matrix']                                                            
                                                                                                                
        self.current_piece['matrix'] = matrix                                                                     
                                                                                                                
        if not self.is_valid_position():                                                                          
            self.current_piece['matrix'] = original_matrix                                                        
                                                                                                                
    def is_valid_position(self):                                                                                  
        matrix = self.current_piece['matrix']                                                                     
        x = self.current_piece['x']                                                                               
        y = self.current_piece['y']                                                                               
                                                                                                                
        for i in range(len(matrix)):                                                                              
            for j in range(len(matrix[i])):                                                                       
                if matrix[i][j] == 1:                                                                             
                    board_x = j + x                                                                               
                    board_y = i + y                                                                               
                                                                                                                
                    if board_x < 0 or board_x >= BOARD_WIDTH or board_y >= BOARD_HEIGHT:                          
                        return False                                                                              
                    if self.board[board_y][board_x] != 0:                                                         
                        return False                                                                              
                                                                                                                
        return True                                                                                               
                                                                                                                
    def lock_piece(self):                                                                                         
        matrix = self.current_piece['matrix']                                                                     
        x = self.current_piece['x']                                                                               
        y = self.current_piece['y']                                                                               
                                                                                                                
        for i in range(len(matrix)):                                                                              
            for j in range(len(matrix[i])):                                                                       
                if matrix[i][j] == 1:                                                                             
                    board_x = j + x                                                                               
                    board_y = i + y                                                                               
                    self.board[board_y][board_x] = self.current_piece['color']                                    
                                                                                                                
        lines_cleared = self.clear_lines()                                                                        
        self.score += lines_cleared * 100                                                                         
                                                                                                                
    def clear_lines(self):                                                                                        
        lines = 0                                                                                                 
        for row in range(BOARD_HEIGHT-1, -1, -1):                                                                 
            if all(cell != 0 for cell in self.board[row]):                                                        
                del self.board[row]                                                                               
                self.board.insert(0, [0]*BOARD_WIDTH)                                                             
                lines += 1                                                                                        
        return lines                                                                                              
                                                                                                                
    def start_game(self):                                                                                         
        running = True                                                                                            
                                                                                                                
        self.current_piece = self.get_new_piece()                                                                 
                                                                                                                
        while running:                                                                                            
            if not self.game_over:                                                                                
                self.move_down()                                                                                  
                                                                                                                
                if not self.is_valid_position():                                                                  
                    self.lock_piece()                                                                             
                    self.current_piece = self.get_new_piece()                                                     
                                                                                                                
                    if not self.is_valid_position():                                                              
                        self.game_over = True                                                                     
                                                                                                                
            for event in pygame.event.get():                                                                      
                if event.type == pygame.QUIT:                                                                     
                    running = False                                                                               
                elif event.type == pygame.KEYDOWN:                                                                
                    if event.key == pygame.K_LEFT:                                                                
                        self.move_side(-1)                                                                        
                    elif event.key == pygame.K_RIGHT:                                                             
                        self.move_side(1)                                                                         
                    elif event.key == pygame.K_DOWN:                                                              
                        self.move_down()                                                                          
                    elif event.key == pygame.K_UP:                                                                
                        self.rotate_piece()                                                                       
                    elif event.key == pygame.K_q and self.game_over:                                              
                        running = False                                                                           
                    elif event.key == pygame.K_r and self.game_over:                                              
                        # Reset game                                                                              
                        self.board = self.create_board()                                                          
                        self.score = 0                                                                            
                        self.current_piece = self.get_new_piece()                                                 
                        self.game_over = False                                                                    
                                                                                                                
            self.draw()                                                                                           
            self.clock.tick(60)                                                                                   
                                                                                                                
        pygame.quit()                                                                                             
                                                                                                                
if __name__ == "__main__":                                                                                        
    game = Tetris()                                                                                               
    game.start_game()   