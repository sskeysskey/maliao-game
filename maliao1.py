import pygame
import sys

# 初始化
pygame.init()
clock = pygame.time.Clock()

# 屏幕大小
screen_width = 1024
screen_height = 551

# 创建屏幕
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("简易马里奥")

# 加载背景图像
background = pygame.image.load("images/background.png").convert()

# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("images/character.png").convert_alpha(), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = screen_height - 100
        self.is_jumping = False
        self.velocity_y = 0
        self.on_pipe = False

    def collide_with_pipe(self, pipe):
        if self.rect.colliderect(pipe.rect):
            # 从上方碰撞
            if self.velocity_y > 0 and self.rect.bottom <= pipe.rect.top + 5:
                self.on_pipe = True
                self.is_jumping = False
                self.velocity_y = 0
                self.rect.bottom = pipe.rect.top
            # 从下方碰撞
            elif self.velocity_y < 0 and self.rect.top >= pipe.rect.bottom - 5:
                self.rect.top = pipe.rect.bottom
                self.velocity_y = 0
            # 从左侧碰撞
            elif self.rect.right >= pipe.rect.left and self.rect.left < pipe.rect.left:
                self.rect.right = pipe.rect.left
            # 从右侧碰撞
            elif self.rect.left <= pipe.rect.right and self.rect.right > pipe.rect.right:
                self.rect.left = pipe.rect.right
        else:
            self.on_pipe = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        if self.is_jumping or not self.on_pipe:
            self.rect.y += self.velocity_y
            self.velocity_y += 1
            if self.rect.y >= screen_height - 100:
                self.is_jumping = False
                self.rect.y = screen_height - 100
                self.velocity_y = 0

        if self.on_pipe:
            if self.rect.bottom <= pipe.rect.top:
                self.rect.bottom = pipe.rect.top
            else:
                self.on_pipe = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -15

# 水管类
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load('images/smallpipe.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.rect.width = width
        self.rect.height = height

# 创建玩家和水管
player = Player()
pipe = Pipe(561, 446, 50, 200)
all_sprites = pygame.sprite.Group()
all_sprites.add(player, pipe)

# 游戏循环
running = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    all_sprites.update()

    player.collide_with_pipe(pipe)

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)