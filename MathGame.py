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
pygame.display.set_caption("Math Quest RPG")

# Otimizações
pygame.key.set_repeat(200, 50)

# Cores
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
DARK_GREEN = (0, 100, 0)
DARK_BROWN = (101, 67, 33)

# Estados do jogo
class GameState:
    MENU = 0
    PLAYING = 1
    MATH_CHALLENGE = 2
    GAME_OVER = 3
    PAUSED = 4
    DIALOGUE = 5
    INTRO = 6

# Controles virtuais para mobile
class VirtualJoystick:
    def __init__(self):
        self.base_radius = 60
        self.stick_radius = 25
        self.base_pos = (100, SCREEN_HEIGHT - 100)
        self.stick_pos = self.base_pos
        self.active = False
        self.direction = [0, 0]
        self.touch_id = None  # Para multi-toque
    
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
    def __init__(self, x, y, width, height, color, text, font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.pressed = False
        self.font = pygame.font.SysFont("Arial", font_size)
    
    def draw(self, screen):
        color = self.color if not self.pressed else (self.color[0]//2, self.color[1]//2, self.color[2]//2)
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=15)
        
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_pressed(self, pos):
        return self.rect.collidepoint(pos)

# Sprite simples em pixel art
class Sprite:
    def __init__(self, x, y, width, height, color, sprite_type="player"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.sprite_type = sprite_type
        self.direction = "down"  # Para animação simples
    
    def draw(self, screen):
        # Desenha sprite baseado no tipo
        if self.sprite_type == "player":
            # Corpo
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            # Detalhes do rosto baseado na direção
            if self.direction == "down":
                pygame.draw.rect(screen, WHITE, (self.x + 10, self.y + 12, 6, 6))
                pygame.draw.rect(screen, WHITE, (self.x + 24, self.y + 12, 6, 6))
            elif self.direction == "up":
                pygame.draw.rect(screen, WHITE, (self.x + 10, self.y + 22, 6, 6))
                pygame.draw.rect(screen, WHITE, (self.x + 24, self.y + 22, 6, 6))
            elif self.direction == "left":
                pygame.draw.rect(screen, WHITE, (self.x + 24, self.y + 12, 6, 6))
                pygame.draw.rect(screen, WHITE, (self.x + 24, self.y + 22, 6, 6))
            elif self.direction == "right":
                pygame.draw.rect(screen, WHITE, (self.x + 10, self.y + 12, 6, 6))
                pygame.draw.rect(screen, WHITE, (self.x + 10, self.y + 22, 6, 6))
        
        elif self.sprite_type == "mentor":
            # Corpo do mentor
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            # Símbolo de matemática
            pygame.draw.circle(screen, WHITE, (self.x + 20, self.y + 15), 8)
            pygame.draw.rect(screen, WHITE, (self.x + 15, self.y + 25, 10, 3))
        
        elif self.sprite_type == "npc":
            # NPC simples
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            # Rosto
            pygame.draw.rect(screen, WHITE, (self.x + 12, self.y + 12, 5, 5))
            pygame.draw.rect(screen, WHITE, (self.x + 23, self.y + 12, 5, 5))
            pygame.draw.rect(screen, WHITE, (self.x + 15, self.y + 25, 10, 3))
        
        elif self.sprite_type == "tree":
            # Tronco
            pygame.draw.rect(screen, DARK_BROWN, (self.x + 15, self.y + 20, 10, 20))
            # Copa
            pygame.draw.circle(screen, DARK_GREEN, (self.x + 20, self.y + 15), 15)
        
        elif self.sprite_type == "house":
            # Casa
            pygame.draw.rect(screen, RED, (self.x + 5, self.y + 15, 30, 25))
            # Telhado
            pygame.draw.polygon(screen, BROWN, [(self.x + 5, self.y + 15), (self.x + 20, self.y + 5), (self.x + 35, self.y + 15)])
            # Porta
            pygame.draw.rect(screen, DARK_BROWN, (self.x + 15, self.y + 25, 10, 15))
        
        elif self.sprite_type == "rock":
            # Pedra
            pygame.draw.circle(screen, GRAY, (self.x + 15, self.y + 10), 12)

# Classe do jogador
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.width = 40
        self.height = 40
        self.speed = 5
        self.color = BLUE
        self.current_mentor = None
        self.sprite = Sprite(self.x, self.y, self.width, self.height, self.color, "player")
        self.interaction_cooldown = 0
    
    def draw(self, screen):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.draw(screen)
    
    def move(self, direction):
        if direction[0] != 0 or direction[1] != 0:
            self.x += direction[0] * self.speed
            self.y += direction[1] * self.speed
            
            # Atualizar direção para animação
            if abs(direction[0]) > abs(direction[1]):
                if direction[0] > 0:
                    self.sprite.direction = "right"
                else:
                    self.sprite.direction = "left"
            else:
                if direction[1] > 0:
                    self.sprite.direction = "down"
                else:
                    self.sprite.direction = "up"
            
            # Limites da tela
            self.x = max(50, min(SCREEN_WIDTH - 50 - self.width, self.x))
            self.y = max(50, min(SCREEN_HEIGHT - 50 - self.height, self.y))
    
    def update(self):
        if self.interaction_cooldown > 0:
            self.interaction_cooldown -= 1
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def can_interact(self):
        return self.interaction_cooldown == 0
    
    def start_interaction_cooldown(self):
        self.interaction_cooldown = 30  # 0.5 segundos a 60 FPS

# Sistema de controle para computador
class KeyboardControls:
    def __init__(self):
        self.direction = [0, 0]
        self.keys = {
            pygame.K_w: False,
            pygame.K_s: False,
            pygame.K_a: False,
            pygame.K_d: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False
        }
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys:
                self.keys[event.key] = True
                self.update_direction()
        elif event.type == pygame.KEYUP:
            if event.key in self.keys:
                self.keys[event.key] = False
                self.update_direction()
    
    def update_direction(self):
        dx, dy = 0, 0
        
        # Teclas WASD
        if self.keys[pygame.K_w] or self.keys[pygame.K_UP]:
            dy -= 1
        if self.keys[pygame.K_s] or self.keys[pygame.K_DOWN]:
            dy += 1
        if self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
            dx -= 1
        if self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
            dx += 1
        
        # Normalizar direção diagonal
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/√2
            dy *= 0.7071
        
        self.direction = [dx, dy]
    
    def get_direction(self):
        return self.direction

# Classes dos mentores
class Mentor:
    def __init__(self, x, y, color, name, subject, dialogue):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.color = color
        self.name = name
        self.subject = subject
        self.dialogue = dialogue
        self.active = True
        self.sprite = Sprite(x, y, self.width, self.height, color, "mentor")
    
    def draw(self, screen):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.draw(screen)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Classes específicas dos mentores (mantidas as mesmas)
class Kayo(Mentor):
    def __init__(self, x, y):
        dialogue = [
            "Olá, aventureiro! Sou Kayo, mestre da Lógica.",
            "Para recuperar o primeiro fragmento do Cristal,",
            "resolva meus desafios lógicos!",
            "Vamos começar?"
        ]
        super().__init__(x, y, (50, 50, 150), "Kayo", "Lógica", dialogue)
        self.problems = [
            {"question": "2X + 5 = 15. Qual é X?", "answer": "5", "options": ["3", "5", "10", "7"]},
            {"question": "A = {1,2,3}, B = {3,4,5}. A ∩ B = ?", "answer": "{3}", "options": ["{1,2,3,4,5}", "{3}", "{1,2}", "{}"]},
            {"question": "(Verdadeiro E Falso) = Verdadeiro?", "answer": "Falso", "options": ["Verdadeiro", "Falso"]}
        ]

class Leo(Mentor):
    def __init__(self, x, y):
        dialogue = [
            "Saudações! Eu sou Leo, o Sábio da Álgebra.",
            "O segundo fragmento está guardado por equações.",
            "Resolva meus problemas para obtê-lo!",
            "Você está preparado?"
        ]
        super().__init__(x, y, (50, 150, 50), "Leo", "Álgebra", dialogue)
        self.problems = [
            {"question": "X² - 5X + 6 = 0", "answer": "2 e 3", "options": ["1 e 6", "2 e 3", "-2 e -3", "0 e 5"]},
            {"question": "f(X) = 2X - 8. Raiz?", "answer": "4", "options": ["2", "4", "8", "-4"]},
            {"question": "f(X) = X + 3. f(5) = ?", "answer": "8", "options": ["5", "8", "3", "15"]}
        ]

class Clara(Mentor):
    def __init__(self, x, y):
        dialogue = [
            "Olá! Eu sou Clara, a Guardiã das Formas.",
            "O terceiro fragmento está em formas geométricas.",
            "Calcule áreas para revelá-lo!",
            "Vamos explorar a geometria?"
        ]
        super().__init__(x, y, (200, 200, 50), "Clara", "Geometria", dialogue)
        self.problems = [
            {"question": "Triângulo: base=6, altura=4. Área?", "answer": "12", "options": ["10", "12", "24", "18"]},
            {"question": "Círculo: raio=5. Área? (π=3.14)", "answer": "78.5", "options": ["15.7", "31.4", "78.5", "157"]},
            {"question": "Catetos: 3 e 4. Hipotenusa?", "answer": "5", "options": ["7", "5", "6", "12"]}
        ]

class Imani(Mentor):
    def __init__(self, x, y):
        dialogue = [
            "Salve! Sou Imani, Mestra dos Triângulos.",
            "O quarto fragmento requer trigonometria.",
            "Senos e cossenos te guiarão!",
            "Pronto para este desafio?"
        ]
        super().__init__(x, y, (150, 50, 150), "Imani", "Trigonometria", dialogue)
        self.problems = [
            {"question": "Sen(30°) = ?", "answer": "0.5", "options": ["0.87", "0.5", "1", "0"]},
            {"question": "Cateto oposto=3, hipotenusa=5. Sen(θ)=?", "answer": "0.6", "options": ["0.6", "0.8", "0.75", "1.67"]},
            {"question": "Cos(60°) = ?", "answer": "0.5", "options": ["0.87", "0.5", "1", "0"]}
        ]

class Chef(Mentor):
    def __init__(self, x, y):
        dialogue = [
            "Olá! Sou o Chef Matemático.",
            "O quinto fragmento envolve cálculos.",
            "Porcentagens e proporções te esperam!",
            "Vamos cozinhar alguns números?"
        ]
        super().__init__(x, y, (200, 50, 50), "Chef", "Mat. Financeira", dialogue)
        self.problems = [
            {"question": "Produto: R$80 com 25% desconto. Preço original?", "answer": "106.67", "options": ["100", "106.67", "95", "105"]},
            {"question": "2 xícaras para 4 pessoas. Para 10 pessoas?", "answer": "5", "options": ["5", "6", "8", "4"]},
            {"question": "R$100 a 2% ao mês (3 meses, juros simples)", "answer": "106", "options": ["106", "102", "110", "112"]}
        ]

class Scientist(Mentor):
    def __init__(self, x, y):
        dialogue = [
            "Saudações! Sou o Cientista de Dados.",
            "O último fragmento exige análise.",
            "Médias e medianas revelarão o caminho!",
            "Preparado para coletar dados?"
        ]
        super().__init__(x, y, (200, 100, 50), "Cientista", "Estatística", dialogue)
        self.problems = [
            {"question": "Dados: 2,4,6,8,10. Média?", "answer": "6", "options": ["5", "6", "7", "8"]},
            {"question": "Dados: 1,3,3,7. Moda?", "answer": "3", "options": ["3", "3.5", "1", "7"]},
            {"question": "Dados: 5,2,9,1,7. Mediana?", "answer": "5", "options": ["5", "4.8", "2", "7"]}
        ]

# NPCs para a história
class NPC:
    def __init__(self, x, y, color, name, dialogue):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.color = color
        self.name = name
        self.dialogue = dialogue
        self.sprite = Sprite(x, y, self.width, self.height, color, "npc")
    
    def draw(self, screen):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.draw(screen)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Sistema de diálogo
class DialogueSystem:
    def __init__(self):
        self.current_dialogue = []
        self.current_line = 0
        self.active = False
        self.speaker = None
    
    def start_dialogue(self, dialogue, speaker):
        self.current_dialogue = dialogue
        self.current_line = 0
        self.active = True
        self.speaker = speaker
    
    def next_line(self):
        self.current_line += 1
        if self.current_line >= len(self.current_dialogue):
            self.active = False
            return True  # Diálogo terminou
        return False
    
    def draw(self, screen):
        if not self.active:
            return
        
        # Caixa de diálogo
        pygame.draw.rect(screen, WHITE, (50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100), border_radius=10)
        pygame.draw.rect(screen, BLACK, (50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 100), 2, border_radius=10)
        
        # Nome do falante
        font_name = pygame.font.SysFont("Arial", 24, bold=True)
        name_surface = font_name.render(self.speaker, True, BLACK)
        screen.blit(name_surface, (70, SCREEN_HEIGHT - 140))
        
        # Texto do diálogo
        font_text = pygame.font.SysFont("Arial", 22)
        text_surface = font_text.render(self.current_dialogue[self.current_line], True, BLACK)
        screen.blit(text_surface, (70, SCREEN_HEIGHT - 110))
        
        # Indicador para continuar
        font_continue = pygame.font.SysFont("Arial", 18)
        continue_surface = font_continue.render("Toque/Espaço para continuar...", True, GRAY)
        screen.blit(continue_surface, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 60))

# Sistema de desafios matemáticos
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
        font_title = pygame.font.SysFont("Arial", 40, bold=True)
        title_text = f"{self.mentor.name} - {self.mentor.subject}"
        title_surface = font_title.render(title_text, True, BLACK)
        screen.blit(title_surface, (SCREEN_WIDTH//2 - title_surface.get_width()//2, 80))
        
        # Pergunta
        font_question = pygame.font.SysFont("Arial", 32)
        question = self.current_problem["question"]
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
        font_progress = pygame.font.SysFont("Arial", 30)
        progress_text = f"Pergunta {self.questions_answered + 1}/3 - Acertos: {self.correct_answers}"
        progress_surface = font_progress.render(progress_text, True, BLACK)
        screen.blit(progress_surface, (SCREEN_WIDTH//2 - progress_surface.get_width()//2, 520))
        
        # Botão de confirmar
        if self.selected_answer:
            confirm_button = VirtualButton(SCREEN_WIDTH//2 - 100, 560, 200, 40, GREEN, "CONFIRMAR (Espaço)")
            confirm_button.draw(screen)

# Mapa do jogo com elementos de cenário
class GameMap:
    def __init__(self):
        self.tile_size = 40
        self.obstacles = []
        self.decorations = []
        self.generate_map()
    
    def generate_map(self):
        # Gerar obstáculos (árvores, pedras, etc.)
        positions = [
            (200, 150), (600, 120), (300, 400), (500, 350),
            (150, 300), (650, 250), (250, 200), (550, 450),
            (350, 100), (450, 500), (100, 200), (700, 400)
        ]
        
        for i, (x, y) in enumerate(positions):
            if i % 3 == 0:
                self.obstacles.append(Sprite(x, y, 40, 40, DARK_GREEN, "tree"))
            elif i % 3 == 1:
                self.obstacles.append(Sprite(x, y, 30, 20, GRAY, "rock"))
            else:
                self.obstacles.append(Sprite(x, y, 40, 40, RED, "house"))
    
    def draw(self, screen):
        # Desenhar grama como fundo
        for x in range(0, SCREEN_WIDTH, self.tile_size):
            for y in range(0, SCREEN_HEIGHT, self.tile_size):
                color = (100, 200, 100) if (x//self.tile_size + y//self.tile_size) % 2 == 0 else (120, 220, 120)
                pygame.draw.rect(screen, color, (x, y, self.tile_size, self.tile_size))
        
        # Desenhar obstáculos
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    def check_collision(self, player_rect):
        for obstacle in self.obstacles:
            obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
            if player_rect.colliderect(obstacle_rect):
                return True
        return False

# Classe principal do jogo
class MathGame:
    def __init__(self):
        self.state = GameState.MENU
        self.player = Player()
        self.joystick = VirtualJoystick()
        self.keyboard = KeyboardControls()
        self.dialogue_system = DialogueSystem()
        self.game_map = GameMap()
        self.use_touch_controls = False  # Detectar automaticamente
        
        # Introdução da história
        self.intro_dialogue = [
            "Era uma vez o Reino da Matemágica,",
            "onde o conhecimento era a fonte de poder.",
            "O Cristal da Sabedoria foi quebrado",
            "em seis fragmentos espalhados pelo reino.",
            "Sem o cristal, o reino começou a definhar...",
            "Você foi escolhido para reunir os fragmentos",
            "resolvendo desafios matemáticos!",
            "Sua jornada começa agora!"
        ]
        
        # Posicionar mentores em locais acessíveis (evitando spawn no player)
        self.mentors = [
            Kayo(700, 100),    # Canto superior direito
            Leo(700, 500),     # Canto inferior direito  
            Clara(100, 100),   # Canto superior esquerdo
            Imani(100, 500),   # Canto inferior esquerdo
            Chef(400, 100),    # Centro superior
            Scientist(400, 500) # Centro inferior
        ]
        
        # NPCs para a história (posicionados longe do spawn)
        self.npcs = [
            NPC(200, 300, BROWN, "Velho Sábio", [
                "Bem-vindo, herói!",
                "Encontre os seis mentores pelo reino.",
                "Cada um guarda um fragmento do Cristal.",
                "Resolva seus desafios para restaurá-lo!",
                "A Matemágica depende de você!"
            ])
        ]
        
        self.current_challenge = None
        self.font = pygame.font.SysFont("Arial", 36)
        self.small_font = pygame.font.SysFont("Arial", 24)
        
        # Progresso do jogo
        self.completed_challenges = 0
        self.total_challenges = len(self.mentors) * 3
        self.fragments_collected = 0
        
        # Botões para mobile
        self.pause_button = VirtualButton(SCREEN_WIDTH - 120, 20, 100, 40, LIGHT_RED, "PAUSAR")
        self.interact_button = VirtualButton(SCREEN_WIDTH - 120, 70, 100, 40, GREEN, "INTERAGIR")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Detectar tipo de controle
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                self.use_touch_controls = True
            elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                self.use_touch_controls = False
            
            # Controles para mobile
            if self.use_touch_controls:
                self.joystick.handle_touch(event)
            else:
                self.keyboard.handle_event(event)
            
            if self.state == GameState.MENU:
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    self.state = GameState.INTRO
                    self.dialogue_system.start_dialogue(self.intro_dialogue, "Narrador")
            
            elif self.state == GameState.INTRO:
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    if self.dialogue_system.active:
                        if self.dialogue_system.next_line():
                            self.state = GameState.PLAYING
                    else:
                        self.state = GameState.PLAYING
            
            elif self.state == GameState.PLAYING:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    # Botão de pausa
                    if self.pause_button.is_pressed(pos):
                        self.state = GameState.PAUSED
                        return True
                    
                    # Botão de interação (apenas mobile)
                    if self.use_touch_controls and self.interact_button.is_pressed(pos) and self.player.can_interact():
                        self.try_interact()
                
                # Tecla de interação (computador)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.player.can_interact():
                    self.try_interact()
                
                # Tecla de pausa (computador)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = GameState.PAUSED
            
            elif self.state == GameState.DIALOGUE:
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    if self.dialogue_system.active:
                        if self.dialogue_system.next_line():
                            # Se o diálogo era com um mentor, inicia o desafio
                            if self.player.current_mentor:
                                self.current_challenge = MathChallenge(self.player.current_mentor)
                                self.state = GameState.MATH_CHALLENGE
                            else:
                                self.state = GameState.PLAYING
                    else:
                        self.state = GameState.PLAYING
            
            elif self.state == GameState.MATH_CHALLENGE:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    # Botão voltar
                    back_button = VirtualButton(50, 50, 100, 40, LIGHT_RED, "VOLTAR (ESC)")
                    if back_button.is_pressed(pos):
                        self.state = GameState.PLAYING
                        self.current_challenge = None
                        self.player.current_mentor = None
                        return True
                    
                    # Selecionar resposta
                    for button in self.current_challenge.answer_buttons:
                        if button.is_pressed(pos):
                            self.current_challenge.selected_answer = button.text
                
                # Controles de teclado para desafios
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.PLAYING
                        self.current_challenge = None
                        self.player.current_mentor = None
                        return True
                    elif event.key == pygame.K_SPACE and self.current_challenge.selected_answer:
                        self.process_challenge_answer()
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        index = event.key - pygame.K_1
                        if index < len(self.current_challenge.answer_buttons):
                            self.current_challenge.selected_answer = self.current_challenge.answer_buttons[index].text
            
            elif self.state == GameState.PAUSED:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    resume_button = VirtualButton(SCREEN_WIDTH//2 - 100, 300, 200, 60, GREEN, "CONTINUAR")
                    menu_button = VirtualButton(SCREEN_WIDTH//2 - 100, 400, 200, 60, LIGHT_RED, "MENU")
                    
                    if resume_button.is_pressed(pos):
                        self.state = GameState.PLAYING
                    elif menu_button.is_pressed(pos):
                        self.__init__()  # Reiniciar o jogo
                
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = GameState.PLAYING
            
            elif self.state == GameState.GAME_OVER:
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    self.__init__()  # Reiniciar o jogo
        
        return True

    def try_interact(self):
        """Tenta interagir com NPCs ou mentores próximos"""
        player_rect = self.player.get_rect()
        
        # Verificar mentores primeiro
        for mentor in self.mentors:
            if player_rect.colliderect(mentor.get_rect()):
                self.player.current_mentor = mentor
                self.dialogue_system.start_dialogue(mentor.dialogue, mentor.name)
                self.state = GameState.DIALOGUE
                self.player.start_interaction_cooldown()
                return
        
        # Verificar NPCs
        for npc in self.npcs:
            if player_rect.colliderect(npc.get_rect()):
                self.dialogue_system.start_dialogue(npc.dialogue, npc.name)
                self.state = GameState.DIALOGUE
                self.player.start_interaction_cooldown()
                return

    def process_challenge_answer(self):
        """Processa a resposta do desafio matemático"""
        correct = self.current_challenge.check_answer()
        if self.current_challenge.questions_answered >= 3:
            self.completed_challenges += 3
            self.fragments_collected += 1
            if self.player.current_mentor in self.mentors:
                self.mentors.remove(self.player.current_mentor)
            self.state = GameState.PLAYING
            self.current_challenge = None
            self.player.current_mentor = None
            
            # Verificar se o jogo foi completado
            if self.fragments_collected >= 6:
                self.state = GameState.GAME_OVER
        else:
            self.current_challenge.load_new_problem()

    def update(self):
        if self.state == GameState.PLAYING:
            # Obter direção dos controles
            if self.use_touch_controls:
                direction = self.joystick.direction
            else:
                direction = self.keyboard.get_direction()
            
            # Salvar posição anterior para colisão
            old_x, old_y = self.player.x, self.player.y
            
            # Mover jogador
            self.player.move(direction)
            
            # Verificar colisão com o mapa
            player_rect = self.player.get_rect()
            if self.game_map.check_collision(player_rect):
                # Reverter movimento em caso de colisão
                self.player.x, self.player.y = old_x, old_y
            
            # Atualizar cooldown de interação
            self.player.update()

    def draw(self):
        screen.fill(WHITE)
        
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.INTRO:
            self.draw_intro()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.DIALOGUE:
            self.draw_game()
            self.dialogue_system.draw(screen)
        elif self.state == GameState.MATH_CHALLENGE:
            self.draw_game()
            self.current_challenge.draw(screen)
        elif self.state == GameState.PAUSED:
            self.draw_game()
            self.draw_pause_menu()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()

    def draw_menu(self):
        # Fundo
        self.game_map.draw(screen)
        
        # Título
        title_font = pygame.font.SysFont("Arial", 64, bold=True)
        title = title_font.render("MATH QUEST RPG", True, BLUE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        subtitle_font = pygame.font.SysFont("Arial", 36)
        subtitle = subtitle_font.render("Aventura Matemática", True, BLACK)
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 180))
        
        # Botão iniciar
        start_button = VirtualButton(SCREEN_WIDTH//2 - 100, 400, 200, 60, GREEN, "INICIAR (Enter)")
        start_button.draw(screen)
        
        # Instruções
        instructions = [
            "• Use WASD/Setas para mover (PC)",
            "• Use joystick para mover (Mobile)", 
            "• Espaço para interagir (PC)",
            "• Toque no botão INTERAGIR (Mobile)",
            "• Resolva problemas matemáticos",
            "• Colete os 6 fragmentos do cristal!"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, BLACK)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 230 + i*25))

    def draw_intro(self):
        # Fundo
        screen.fill((0, 0, 50))
        
        # Título
        title_font = pygame.font.SysFont("Arial", 48, bold=True)
        title = title_font.render("MATH QUEST RPG", True, LIGHT_BLUE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
        
        # Desenhar cristal
        points = [
            (SCREEN_WIDTH//2, 150),
            (SCREEN_WIDTH//2 - 30, 200),
            (SCREEN_WIDTH//2, 250),
            (SCREEN_WIDTH//2 + 30, 200)
        ]
        pygame.draw.polygon(screen, LIGHT_BLUE, points)
        
        # Diálogo de introdução
        if self.dialogue_system.active:
            self.dialogue_system.draw(screen)
        else:
            start_font = pygame.font.SysFont("Arial", 36)
            start_text = start_font.render("Pressione Espaço para começar...", True, WHITE)
            screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 400))

    def draw_game(self):
        # Desenhar mapa
        self.game_map.draw(screen)
        
        # Desenhar NPCs
        for npc in self.npcs:
            npc.draw(screen)
            # Nome do NPC
            name_surface = self.small_font.render(npc.name, True, BLACK)
            screen.blit(name_surface, (npc.x - 15, npc.y - 25))
        
        # Desenhar mentores
        for mentor in self.mentors:
            mentor.draw(screen)
            # Nome do mentor
            name_surface = self.small_font.render(mentor.name, True, BLACK)
            screen.blit(name_surface, (mentor.x - 15, mentor.y - 25))
        
        # Desenhar jogador
        self.player.draw(screen)
        
        # Controles
        if self.use_touch_controls:
            # Joystick virtual e botão de interação
            self.joystick.draw(screen)
            self.interact_button.draw(screen)
        else:
            # Instruções para teclado
            controls_text = [
                "WASD/Setas: Mover",
                "Espaço: Interagir", 
                "ESC: Pausar"
            ]
            for i, text in enumerate(controls_text):
                control_surface = self.small_font.render(text, True, BLACK)
                screen.blit(control_surface, (20, 20 + i*25))
        
        # Botão de pausa
        self.pause_button.draw(screen)
        
        # Progresso
        progress_text = f"Fragmentos: {self.fragments_collected}/6"
        progress_surface = self.small_font.render(progress_text, True, BLACK)
        screen.blit(progress_surface, (SCREEN_WIDTH - 150, 20))
        
        # Dica de interação
        player_rect = self.player.get_rect()
        near_character = False
        for mentor in self.mentors:
            if player_rect.colliderect(mentor.get_rect()):
                near_character = True
                break
        for npc in self.npcs:
            if player_rect.colliderect(npc.get_rect()):
                near_character = True
                break
        
        if near_character and self.player.can_interact():
            if self.use_touch_controls:
                hint_text = "Toque em INTERAGIR!"
            else:
                hint_text = "Pressione ESPAÇO para interagir!"
            hint_surface = self.small_font.render(hint_text, True, GREEN)
            screen.blit(hint_surface, (SCREEN_WIDTH//2 - hint_surface.get_width()//2, SCREEN_HEIGHT - 40))

    def draw_pause_menu(self):
        # Overlay escuro
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        screen.blit(s, (0, 0))
        
        # Menu de pausa
        pygame.draw.rect(screen, WHITE, (150, 150, 500, 300), border_radius=20)
        pygame.draw.rect(screen, BLACK, (150, 150, 500, 300), 3, border_radius=20)
        
        title = self.font.render("JOGO PAUSADO", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 180))
        
        resume_button = VirtualButton(SCREEN_WIDTH//2 - 100, 300, 200, 60, GREEN, "CONTINUAR (ESC)")
        menu_button = VirtualButton(SCREEN_WIDTH//2 - 100, 400, 200, 60, LIGHT_RED, "MENU")
        
        resume_button.draw(screen)
        menu_button.draw(screen)

    def draw_game_over(self):
        # Fundo
        self.game_map.draw(screen)
        
        # Overlay
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        screen.blit(s, (0, 0))
        
        # Mensagem de vitória
        pygame.draw.rect(screen, WHITE, (100, 100, 600, 400), border_radius=20)
        pygame.draw.rect(screen, BLACK, (100, 100, 600, 400), 3, border_radius=20)
        
        title_font = pygame.font.SysFont("Arial", 48, bold=True)
        title = title_font.render("PARABÉNS!", True, BLUE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        
        message_font = pygame.font.SysFont("Arial", 32)
        messages = [
            "Você reuniu todos os fragmentos",
            "do Cristal da Sabedoria!",
            "O Reino da Matemágica está salvo!",
            "",
            f"Desafios completos: {self.completed_challenges}"
        ]
        
        for i, message in enumerate(messages):
            text = message_font.render(message, True, BLACK)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 220 + i*40))
        
        # Botão de menu
        menu_button = VirtualButton(SCREEN_WIDTH//2 - 100, 450, 200, 60, GREEN, "MENU (Enter)")
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
