import pygame
import sys
import math
import random

# Inicialização do Pygame
pygame.init()

# Configurações para mobile
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Math Quest Mobile")

# Otimizações para mobile
pygame.key.set_repeat(200, 50)  # Para manter pressionado

# Cores (mantidas as mesmas)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)
GREEN = (100, 200, 100)
RED = (255, 100, 100)
YELLOW = (255, 255, 100)
PURPLE = (200, 100, 255)
ORANGE = (255, 150, 50)
BROWN = (150, 100, 50)
GRAY = (150, 150, 150)
LIGHT_BLUE = (200, 230, 255)
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (255, 200, 200)

# Estados do jogo
class GameState:
    MENU = 0
    PLAYING = 1
    MATH_CHALLENGE = 2
    GAME_OVER = 3
    PAUSED = 4

# Controles virtuais para mobile
class VirtualJoystick:
    def __init__(self):
        self.base_radius = 60
        self.stick_radius = 25
        self.base_pos = (100, SCREEN_HEIGHT - 100)
        self.stick_pos = self.base_pos
        self.active = False
        self.direction = [0, 0]
    
    def draw(self, screen):
        # Base do joystick
        pygame.draw.circle(screen, (100, 100, 100, 150), self.base_pos, self.base_radius)
        # Stick do joystick
        pygame.draw.circle(screen, (50, 50, 50, 200), self.stick_pos, self.stick_radius)
    
    def handle_touch(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            distance = math.sqrt((pos[0] - self.base_pos[0])**2 + (pos[1] - self.base_pos[1])**2)
            if distance <= self.base_radius:
                self.active = True
                self.stick_pos = pos
                self.calculate_direction()
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.active = False
            self.stick_pos = self.base_pos
            self.direction = [0, 0]
        
        elif event.type == pygame.MOUSEMOTION and self.active:
            pos = pygame.mouse.get_pos()
            distance = math.sqrt((pos[0] - self.base_pos[0])**2 + (pos[1] - self.base_pos[1])**2)
            if distance <= self.base_radius:
                self.stick_pos = pos
            else:
                # Limita ao raio máximo
                angle = math.atan2(pos[1] - self.base_pos[1], pos[0] - self.base_pos[0])
                self.stick_pos = (
                    self.base_pos[0] + self.base_radius * math.cos(angle),
                    self.base_pos[1] + self.base_radius * math.sin(angle)
                )
            self.calculate_direction()
    
    def calculate_direction(self):
        dx = self.stick_pos[0] - self.base_pos[0]
        dy = self.stick_pos[1] - self.base_pos[1]
        self.direction = [dx / self.base_radius, dy / self.base_radius]

# Botão virtual para ações
class VirtualButton:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.pressed = False
        self.font = pygame.font.SysFont(None, 30)
    
    def draw(self, screen):
        color = self.color if not self.pressed else (self.color[0]//2, self.color[1]//2, self.color[2]//2)
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=15)
        
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_pressed(self, pos):
        return self.rect.collidepoint(pos)

# Classe do jogador (adaptada para mobile)
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.width = 40
        self.height = 40
        self.speed = 4
        self.color = BLUE
        self.current_mentor = None
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), border_radius=8)
        # Olhos do jogador
        pygame.draw.circle(screen, WHITE, (self.x + 28, self.y + 12), 6)
        pygame.draw.circle(screen, WHITE, (self.x + 12, self.y + 12), 6)
    
    def move(self, direction):
        self.x += direction[0] * self.speed
        self.y += direction[1] * self.speed
        
        # Limites da tela
        self.x = max(50, min(SCREEN_WIDTH - 50 - self.width, self.x))
        self.y = max(50, min(SCREEN_HEIGHT - 50 - self.height, self.y))
    
    def check_collision(self, mentor):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        mentor_rect = pygame.Rect(mentor.x, mentor.y, mentor.width, mentor.height)
        return player_rect.colliderect(mentor_rect)

# Classes dos mentores (mantidas as mesmas, com visual melhorado para mobile)
class Mentor:
    def __init__(self, x, y, color, name, subject):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.color = color
        self.name = name
        self.subject = subject
        self.active = True
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), border_radius=10)
        # Símbolo de interação
        pygame.draw.circle(screen, WHITE, (self.x + 25, self.y + 25), 15)
        pygame.draw.circle(screen, self.color, (self.x + 25, self.y + 25), 10)

# Classes específicas dos mentores (mantidas)
class Kayo(Mentor):
    def __init__(self, x, y):
        super().__init__(x, y, BLACK, "Kayo", "Lógica")
        self.problems = [
            {"question": "2X + 5 = 15. Qual é X?", "answer": "5", "options": ["3", "5", "10", "7"]},
            {"question": "A = {1,2,3}, B = {3,4,5}. A ∩ B = ?", "answer": "{3}", "options": ["{1,2,3,4,5}", "{3}", "{1,2}", "{}"]},
            {"question": "(Verdadeiro E Falso) = Verdadeiro?", "answer": "Falso", "options": ["Verdadeiro", "Falso"]}
        ]

class Leo(Mentor):
    def __init__(self, x, y):
        super().__init__(x, y, GREEN, "Leo", "Álgebra")
        self.problems = [
            {"question": "X² - 5X + 6 = 0", "answer": "2 e 3", "options": ["1 e 6", "2 e 3", "-2 e -3", "0 e 5"]},
            {"question": "f(X) = 2X - 8. Raiz?", "answer": "4", "options": ["2", "4", "8", "-4"]},
            {"question": "f(X) = X + 3. f(5) = ?", "answer": "8", "options": ["5", "8", "3", "15"]}
        ]

class Clara(Mentor):
    def __init__(self, x, y):
        super().__init__(x, y, YELLOW, "Clara", "Geometria")
        self.problems = [
            {"question": "Triângulo: base=6, altura=4. Área?", "answer": "12", "options": ["10", "12", "24", "18"]},
            {"question": "Círculo: raio=5. Área? (π=3.14)", "answer": "78.5", "options": ["15.7", "31.4", "78.5", "157"]},
            {"question": "Catetos: 3 e 4. Hipotenusa?", "answer": "5", "options": ["7", "5", "6", "12"]}
        ]

class Imani(Mentor):
    def __init__(self, x, y):
        super().__init__(x, y, PURPLE, "Imani", "Trigonometria")
        self.problems = [
            {"question": "Sen(30°) = ?", "answer": "0.5", "options": ["0.87", "0.5", "1", "0"]},
            {"question": "Cateto oposto=3, hipotenusa=5. Sen(θ)=?", "answer": "0.6", "options": ["0.6", "0.8", "0.75", "1.67"]},
            {"question": "Cos(60°) = ?", "answer": "0.5", "options": ["0.87", "0.5", "1", "0"]}
        ]

class Chef(Mentor):
    def __init__(self, x, y):
        super().__init__(x, y, RED, "Chef", "Mat. Financeira")
        self.problems = [
            {"question": "Produto: R$80 com 25% desconto. Preço original?", "answer": "106.67", "options": ["100", "106.67", "95", "105"]},
            {"question": "2 xícaras para 4 pessoas. Para 10 pessoas?", "answer": "5", "options": ["5", "6", "8", "4"]},
            {"question": "R$100 a 2% ao mês (3 meses, juros simples)", "answer": "106", "options": ["106", "102", "110", "112"]}
        ]

class Scientist(Mentor):
    def __init__(self, x, y):
        super().__init__(x, y, ORANGE, "Cientista", "Estatística")
        self.problems = [
            {"question": "Dados: 2,4,6,8,10. Média?", "answer": "6", "options": ["5", "6", "7", "8"]},
            {"question": "Dados: 1,3,3,7. Moda?", "answer": "3", "options": ["3", "3.5", "1", "7"]},
            {"question": "Dados: 5,2,9,1,7. Mediana?", "answer": "5", "options": ["5", "4.8", "2", "7"]}
        ]

# Sistema de desafios matemáticos (adaptado para mobile)
class MathChallenge:
    def __init__(self, mentor):
        self.mentor = mentor
        self.current_problem = None
        self.selected_answer = None
        self.correct_answers = 0
        self.questions_answered = 0
        self.answer_buttons = []
        self.load_new_problem()
    
    def load_new_problem(self):
        if self.mentor.problems:
            self.current_problem = random.choice(self.mentor.problems)
            self.selected_answer = None
            self.create_answer_buttons()
    
    def create_answer_buttons(self):
        self.answer_buttons = []
        option_y = 300
        for option in self.current_problem["options"]:
            button = VirtualButton(150, option_y, 500, 50, LIGHT_GREEN, option)
            self.answer_buttons.append(button)
            option_y += 70
    
    def check_answer(self):
        if self.selected_answer == self.current_problem["answer"]:
            self.correct_answers += 1
            self.questions_answered += 1
            return True
        else:
            self.questions_answered += 1
            return False
    
    def draw(self, screen):
        # Fundo do desafio
        pygame.draw.rect(screen, LIGHT_BLUE, (50, 50, SCREEN_WIDTH-100, SCREEN_HEIGHT-100), border_radius=20)
        pygame.draw.rect(screen, BLACK, (50, 50, SCREEN_WIDTH-100, SCREEN_HEIGHT-100), 3, border_radius=20)
        
        # Título
        font_title = pygame.font.SysFont(None, 40)
        title_text = f"{self.mentor.name} - {self.mentor.subject}"
        title_surface = font_title.render(title_text, True, BLACK)
        screen.blit(title_surface, (SCREEN_WIDTH//2 - title_surface.get_width()//2, 80))
        
        # Pergunta
        font_question = pygame.font.SysFont(None, 32)
        # Quebra de linha para perguntas longas
        question = self.current_problem["question"]
        if len(question) > 40:
            words = question.split(' ')
            lines = []
            current_line = ""
            for word in words:
                if len(current_line + word) < 40:
                    current_line += word + " "
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)
            
            for i, line in enumerate(lines):
                question_surface = font_question.render(line, True, BLACK)
                screen.blit(question_surface, (SCREEN_WIDTH//2 - question_surface.get_width()//2, 150 + i*35))
        else:
            question_surface = font_question.render(question, True, BLACK)
            screen.blit(question_surface, (SCREEN_WIDTH//2 - question_surface.get_width()//2, 150))
        
        # Opções de resposta como botões
        for button in self.answer_buttons:
            if button.text == self.selected_answer:
                button.color = LIGHT_BLUE  # Destacar seleção
            else:
                button.color = LIGHT_GREEN
            button.draw(screen)
        
        # Progresso
        font_progress = pygame.font.SysFont(None, 30)
        progress_text = f"Pergunta {self.questions_answered + 1}/3 - Acertos: {self.correct_answers}"
        progress_surface = font_progress.render(progress_text, True, BLACK)
        screen.blit(progress_surface, (SCREEN_WIDTH//2 - progress_surface.get_width()//2, 520))
        
        # Botão de confirmar
        if self.selected_answer:
            confirm_button = VirtualButton(SCREEN_WIDTH//2 - 100, 560, 200, 40, GREEN, "CONFIRMAR")
            confirm_button.draw(screen)

# Classe principal do jogo (adaptada para mobile)
class MathGame:
    def __init__(self):
        self.state = GameState.MENU
        self.player = Player()
        self.joystick = VirtualJoystick()
        
        # Posicionar mentores de forma mais espaçada para mobile
        self.mentors = [
            Kayo(650, 100),
            Leo(650, 200),
            Clara(650, 300),
            Imani(100, 100),
            Chef(100, 200),
            Scientist(100, 300)
        ]
        
        self.current_challenge = None
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 28)
        
        # Progresso do jogo
        self.completed_challenges = 0
        self.total_challenges = len(self.mentors) * 3
        
        # Botões para mobile
        self.menu_button = VirtualButton(SCREEN_WIDTH - 120, 20, 100, 40, LIGHT_RED, "MENU")
        self.pause_button = VirtualButton(SCREEN_WIDTH - 120, 20, 100, 40, LIGHT_RED, "PAUSAR")
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Controles touch para mobile
            self.joystick.handle_touch(event)
            
            if self.state == GameState.MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    start_button = VirtualButton(SCREEN_WIDTH//2 - 100, 400, 200, 60, GREEN, "INICIAR JOGO")
                    if start_button.is_pressed(pos):
                        self.state = GameState.PLAYING
            
            elif self.state == GameState.PLAYING:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.pause_button.is_pressed(pos):
                        self.state = GameState.PAUSED
                    
                    # Verificar colisão com mentores via touch
                    for mentor in self.mentors:
                        mentor_rect = pygame.Rect(mentor.x, mentor.y, mentor.width, mentor.height)
                        if mentor_rect.collidepoint(pos):
                            self.player.current_mentor = mentor
                            self.current_challenge = MathChallenge(mentor)
                            self.state = GameState.MATH_CHALLENGE
                            break
            
            elif self.state == GameState.MATH_CHALLENGE:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    # Botão voltar
                    back_button = VirtualButton(50, 50, 100, 40, LIGHT_RED, "VOLTAR")
                    if back_button.is_pressed(pos):
                        self.state = GameState.PLAYING
                        self.current_challenge = None
                        return True
                    
                    # Selecionar resposta
                    for button in self.current_challenge.answer_buttons:
                        if button.is_pressed(pos):
                            self.current_challenge.selected_answer = button.text
                    
                    # Botão confirmar
                    if self.current_challenge.selected_answer:
                        confirm_button = VirtualButton(SCREEN_WIDTH//2 - 100, 560, 200, 40, GREEN, "CONFIRMAR")
                        if confirm_button.is_pressed(pos):
                            if self.current_challenge.check_answer():
                                if self.current_challenge.questions_answered >= 3:
                                    self.completed_challenges += 3
                                    self.mentors.remove(self.current_challenge.mentor)
                                    self.state = GameState.PLAYING
                                    self.current_challenge = None
                                else:
                                    self.current_challenge.load_new_problem()
                            else:
                                self.current_challenge.load_new_problem()
            
            elif self.state == GameState.PAUSED:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    resume_button = VirtualButton(SCREEN_WIDTH//2 - 100, 300, 200, 60, GREEN, "CONTINUAR")
                    menu_button = VirtualButton(SCREEN_WIDTH//2 - 100, 400, 200, 60, LIGHT_RED, "MENU")
                    
                    if resume_button.is_pressed(pos):
                        self.state = GameState.PLAYING
                    elif menu_button.is_pressed(pos):
                        self.state = GameState.MENU
        
        return True
    
    def update(self):
        if self.state == GameState.PLAYING:
            self.player.move(self.joystick.direction)
    
    def draw(self):
        screen.fill(WHITE)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.MATH_CHALLENGE:
            self.draw_game()
            self.current_challenge.draw(screen)
        elif self.state == GameState.PAUSED:
            self.draw_pause_menu()
        
        pygame.display.flip()
    
    def draw_menu(self):
        # Título
        title_font = pygame.font.SysFont(None, 64)
        title = title_font.render("MATH QUEST", True, BLUE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        
        subtitle_font = pygame.font.SysFont(None, 36)
        subtitle = subtitle_font.render("Versão Mobile", True, BLACK)
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 220))
        
        # Botão iniciar
        start_button = VirtualButton(SCREEN_WIDTH//2 - 100, 400, 200, 60, GREEN, "INICIAR JOGO")
        start_button.draw(screen)
        
        # Instruções
        instructions = [
            "• Use o joystick para se mover",
            "• Toque nos mentores para desafios",
            "• Resolva problemas matemáticos",
            "• Complete todos os desafios!"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, BLACK)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 300 + i*30))
    
    def draw_game(self):
        # Área de jogo
        pygame.draw.rect(screen, LIGHT_BLUE, (50, 50, SCREEN_WIDTH-100, SCREEN_HEIGHT-100), border_radius=20)
        pygame.draw.rect(screen, BLACK, (50, 50, SCREEN_WIDTH-100, SCREEN_HEIGHT-100), 2, border_radius=20)
        
        # Jogador
        self.player.draw(screen)
        
        # Mentores
        for mentor in self.mentors:
            mentor.draw(screen)
            # Nome do mentor
            name_surface = self.small_font.render(mentor.name, True, BLACK)
            screen.blit(name_surface, (mentor.x - 10, mentor.y - 25))
        
        # Joystick virtual
        self.joystick.draw(screen)
        
        # Botão de pausa
        self.pause_button.draw(screen)
        
        # Progresso
        progress_text = f"Completos: {self.completed_challenges}/{self.total_challenges}"
        progress_surface = self.small_font.render(progress_text, True, BLACK)
        screen.blit(progress_surface, (20, 20))
        
           # Dica de interação
        if any(self.player.check_collision(mentor) for mentor in self.mentors):
            hint_text = "Toque no mentor para desafio!"
            hint_surface = self.small_font.render(hint_text, True, GREEN)
            screen.blit(hint_surface, (SCREEN_WIDTH//2 - hint_surface.get_width()//2, SCREEN_HEIGHT - 40))
    def draw_pause_menu(self):
        # Fundo semitransparente
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        screen.blit(s, (0, 0))
        
        # Menu de pausa
        pygame.draw.rect(screen, WHITE, (150, 150, 500, 300), border_radius=20)
        pygame.draw.rect(screen, BLACK, (150, 150, 500, 300), 3, border_radius=20)
        
        title = self.font.render("JOGO PAUSADO", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 180))
        
        resume_button = VirtualButton(SCREEN_WIDTH//2 - 100, 300, 200, 60, GREEN, "CONTINUAR")
        menu_button = VirtualButton(SCREEN_WIDTH//2 - 100, 400, 200, 60, LIGHT_RED, "MENU PRINCIPAL")
        
        resume_button.draw(screen)
        menu_button.draw(screen)
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Executar o jogo
if __name__ == "__main__":
    game = MathGame()
    game.run()
