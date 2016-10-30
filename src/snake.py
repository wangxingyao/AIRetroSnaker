# -*- coding: utf-8 -*-

import pygame
import sys
import random
import traceback 
# import copy




class Diamond(pygame.sprite.Sprite):
    def __init__(self, snake_diamond_png):
        pygame.sprite.Sprite.__init__(self)
        
        # 定义每个方块的基本属性
        self.image = pygame.image.load(snake_diamond_png)
        self.rect = self.image.get_rect()

class Snake(Diamond, pygame.sprite.Sprite):
    def __init__(self, snakeHeadPng, snakeBodyPng, snakeFoodPng, snakeBodyAmount):
        # pygame.sprite.Sprite.__init__(self)
        
        # 贪吃蛇的蛇身
        self.bodyAmount = snakeBodyAmount
        self.bodys = []
        for i in range(self.bodyAmount):
            self.body = Diamond(snakeBodyPng)
            self.body.rect.left, self.body.rect.top = 67 + i*22, 67
            self.bodys.append(self.body)
        
        # 贪食蛇的蛇身的备胎:数字代表小键盘中相对5的位置,默认5向上
        self.headTemp  = Diamond(snakeHeadPng)
        self.bodyTemp4 = Diamond(snakeBodyPng)
        self.bodyTemp6 = Diamond(snakeBodyPng)
        
        # 贪吃蛇的食物
        self.food = Diamond(snakeFoodPng)
        self.food.rect.left = 67 + 22 * random.randint(1, 23-1)
        self.food.rect.top = 67 + 22 * random.randint(1, 11-1)
        
        # 贪吃蛇的蛇头
        self.head = Diamond(snakeHeadPng)
        self.head.rect.left = 67 + self.bodyAmount * 22
        self.head.rect.top = 67
        self.headUpImage = pygame.transform.rotate(self.head.image, 90)
        self.headLeftImage = pygame.transform.rotate(self.head.image, 180)
        self.headDownImage = pygame.transform.rotate(self.head.image, 270)
        self.headRightImage = self.head.image
        self.headImage = self.headRightImage
        
        # 贪吃蛇的速度
        self.speed = 22
        self.dir_x, self.dir_y = 1, 0
        
        self.eating = False
        self.control = True
        self.auto = False


    def move(self):
        # 更新蛇身位置
        if self.eating:
            self.body = self.bodys.pop(-1)
            self.body.rect = self.head.rect
            self.bodys.append(self.body)
            self.eating = False
        else:
            self.body = self.bodys.pop(0)
            self.body.rect = self.head.rect
            self.bodys.append(self.body)

        # 更新蛇头位置
        self.head.rect = self.head.rect.move(self.speed * self.dir_x,
                                             self.speed * self.dir_y)
        
        # 出边界后从另一边出来
        if self.head.rect.left < 67:
            self.head.rect.left = 551
        if self.head.rect.left > 551:
            self.head.rect.left = 67
        if self.head.rect.top < 67:
            self.head.rect.top = 287
        if self.head.rect.top > 287:
            self.head.rect.top = 67
        
    
    # 自动寻路函数
    def automove(self, bodyGroup):
        # 寻找食物的位置
        food_head_x = self.food.rect.left - self.head.rect.left
        food_head_y = self.food.rect.top  - self.head.rect.top
        # 向上
        if self.dir_x == 0 and self.dir_y == -1:
            if food_head_y >= 0 and food_head_x <= 0:
                self.dir_x, self.dir_y = -1,  0
                self.head.image = self.headLeftImage
            elif food_head_y >= 0 and food_head_x > 0:
                self.dir_x, self.dir_y =  1,  0
                self.head.image = self.headRightImage
        # 向下
        elif self.dir_x == 0 and self.dir_y == 1:
            if food_head_y <= 0 and food_head_x < 0:
                self.dir_x, self.dir_y = -1,  0
                self.head.image = self.headLeftImage
            elif food_head_y <= 0 and food_head_x >= 0:
                self.dir_x, self.dir_y =  1,  0
                self.head.image = self.headRightImage
        # 向左
        elif self.dir_x == -1 and self.dir_y == 0:
            if food_head_x >= 0 and food_head_y < 0:
                self.dir_x, self.dir_y =  0, -1
                self.head.image = self.headUpImage
            elif food_head_x >= 0 and food_head_y >= 0:
                self.dir_x, self.dir_y =  0,  1
                self.head.image = self.headDownImage
        # 向右
        elif self.dir_x == 1 and self.dir_y == 0:
            if food_head_x <= 0 and food_head_y <= 0:
                self.dir_x, self.dir_y =  0, -1
                self.head.image = self.headUpImage
            elif food_head_x <= 0 and food_head_y > 0:
                self.dir_x, self.dir_y =  0,  1
                self.head.image = self.headDownImage
            
        # 移动蛇头
        self.head.rect = self.head.rect.move(self.speed * self.dir_x,
                                             self.speed * self.dir_y)        
        
        # 碰撞身体
        if pygame.sprite.spritecollide(self.head, bodyGroup, False, None):
            self.head.rect = self.head.rect.move(self.speed * self.dir_x * -1,
                                                 self.speed * self.dir_y * -1)  
            
            # 寻找蛇尾的位置
            tail_head_x = self.bodys[0].rect.left - self.head.rect.left
            tail_head_y = self.bodys[0].rect.top  - self.head.rect.top
            # 向上
            if self.dir_x == 0 and self.dir_y == -1:
                if tail_head_x < 0:
                    self.dir_x, self.dir_y = -1,  0
                    self.head.image = self.headLeftImage
                elif tail_head_x > 0:
                    self.dir_x, self.dir_y =  1,  0
                    self.head.image = self.headRightImage
            # 向下
            elif self.dir_x == 0 and self.dir_y == 1:
                if tail_head_x < 0:
                    self.dir_x, self.dir_y = -1,  0
                    self.head.image = self.headLeftImage
                elif tail_head_x > 0:
                    self.dir_x, self.dir_y =  1,  0
                    self.head.image = self.headRightImage
            # 向左
            elif self.dir_x == -1 and self.dir_y == 0:
                if tail_head_y < 0:
                    self.dir_x, self.dir_y =  0, -1
                    self.head.image = self.headUpImage
                elif tail_head_y > 0:
                    self.dir_x, self.dir_y =  0,  1
                    self.head.image = self.headDownImage
            # 向右
            elif self.dir_x == 1 and self.dir_y == 0:
                if tail_head_y < 0:
                    self.dir_x, self.dir_y =  0, -1
                    self.head.image = self.headUpImage
                elif tail_head_y > 0:
                    self.dir_x, self.dir_y =  0,  1
                    self.head.image = self.headDownImage
            
            # 移动蛇头
            self.head.rect = self.head.rect.move(self.speed * self.dir_x,
                                                 self.speed * self.dir_y)        
        self.head.rect = self.head.rect.move(self.speed * self.dir_x * -1,
                                             self.speed * self.dir_y * -1)        
        self.move()
        
        

def search(snake2, bodyGroup):
    # 寻找食物的位置
    food_head_x = snake2.food.rect.left - snake2.head.rect.left
    food_head_y = snake2.food.rect.top  - snake2.head.rect.top
    # 向上
    if snake2.dir_x == 0 and snake2.dir_y == -1:
        if food_head_y >= 0 and food_head_x <= 0:
            snake2.dir_x, snake2.dir_y = -1,  0
            snake2.head.image = snake2.headLeftImage
        elif food_head_y >= 0 and food_head_x > 0:
            snake2.dir_x, snake2.dir_y =  1,  0
            snake2.head.image = snake2.headRightImage
    # 向下
    elif snake2.dir_x == 0 and snake2.dir_y == 1:
        if food_head_y <= 0 and food_head_x < 0:
            snake2.dir_x, snake2.dir_y = -1,  0
            snake2.head.image = snake2.headLeftImage
        elif food_head_y <= 0 and food_head_x >= 0:
            snake2.dir_x, snake2.dir_y =  1,  0
            snake2.head.image = snake2.headRightImage
    # 向左
    elif snake2.dir_x == -1 and snake2.dir_y == 0:
        if food_head_x >= 0 and food_head_y < 0:
            snake2.dir_x, snake2.dir_y =  0, -1
            snake2.head.image = snake2.headUpImage
        elif food_head_x >= 0 and food_head_y >= 0:
            snake2.dir_x, snake2.dir_y =  0,  1
            snake2.head.image = snake2.headDownImage
    # 向右
    elif snake2.dir_x == 1 and snake2.dir_y == 0:
        if food_head_x <= 0 and food_head_y <= 0:
            snake2.dir_x, snake2.dir_y =  0, -1
            snake2.head.image = snake2.headUpImage
        elif food_head_x <= 0 and food_head_y > 0:
            snake2.dir_x, snake2.dir_y =  0,  1
            snake2.head.image = snake2.headDownImage

    # 模拟移动
    snake2.move()
        
    if pygame.sprite.collide_rect(snake2.head, snake2.food):
        return True
    elif pygame.sprite.spritecollide(snake2.head, bodyGroup, False, None):
        return True
    else:
        return True


def main():
    background_png = r"..\pic\background.png"
    snakeHeadPng = r"..\pic\snake_head.png"
    snakeBodyPng = r"..\pic\snake_body.png"
    snakeFoodPng = r"..\pic\snake_food.png"
    gameoverPng = r"..\pic\gameover.png"
    
    # 初始化-----------------------------------------------------------------------------------
    # 初始化模块
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    # 初始化屏幕
    resolution = width, height = 638, 416
    screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
    pygame.display.set_caption("Snake")
    

    # 加载---------------------------------------------------------------------------------------
    # 加载图片
    backgroundImage = pygame.image.load(background_png)
    gameoverImage = pygame.image.load(gameoverPng)
    gameoverRect = gameoverImage.get_rect()
    gameoverRect.left = (width - gameoverRect.width) / 2
    gameoverRect.top = height / 2 - gameoverRect.height
    # 加载音乐
    pygame.mixer.music.load(r"..\music\wodehuabanxie.ogg")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops=5)
    # 加载音效
    laughSound = pygame.mixer.Sound(r"..\music\laugh.wav")
     
    
    # 初始化贪吃蛇------------------------------------------------------------------------------
    snakeBodyAmountInit = 4
    snake = Snake(snakeHeadPng, snakeBodyPng, snakeFoodPng, snakeBodyAmountInit)
    # 精灵组:蛇身
    bodyGroup = pygame.sprite.Group()
    for each_body in snake.bodys:
        bodyGroup.add(each_body)
    # 精灵组:食物
    ## foodGroup = pygame.sprite.Group()
    ## foodGroup.add(snake.food)
        
    # 文本
    font = pygame.font.FontType(r"..\font\minijianshaoer.ttf", 24)
    
    fullScreen = False
    gamePause = False
    gameDifficult = 2
    gameover = False
    running = True
    clock = pygame.time.Clock()
    while running:
        # 事件循环
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                    
            
            if event.type == pygame.KEYDOWN:
                # 方向选择
                if event.key == pygame.K_UP:
                    if snake.dir_x != 0 and snake.dir_y != 1 and snake.control:
                        snake.dir_x, snake.dir_y = 0, -1
                        snake.head.image = snake.headUpImage 
                        snake.control = False
                if event.key == pygame.K_DOWN:
                    if snake.dir_x != 0 and snake.dir_y != -1 and snake.control:
                        snake.dir_x, snake.dir_y = 0, 1
                        snake.head.image = snake.headDownImage
                        snake.control = False
                if event.key == pygame.K_LEFT:
                    if snake.dir_x != 1 and snake.dir_y != 0 and snake.control:
                        snake.dir_x, snake.dir_y = -1, 0
                        snake.head.image = snake.headLeftImage
                        snake.control = False
                if event.key == pygame.K_RIGHT:
                    if snake.dir_x != -1 and snake.dir_y != 0 and snake.control:
                        snake.dir_x, snake.dir_y = 1, 0
                        snake.head.image = snake.headRightImage
                        snake.control = False
                     
                # 重新开始   
                if event.key == pygame.K_r:
                    gameover = False
                    snake = Snake(snakeHeadPng, snakeBodyPng, snakeFoodPng, snakeBodyAmountInit)
                    bodyGroup = pygame.sprite.Group()
                    for each_body in snake.bodys:
                        bodyGroup.add(each_body)
                    ## foodGroup = pygame.sprite.Group()
                    ## foodGroup.add(snake.food)
                
                # 难度选择
                if event.key == pygame.K_d:
                    if gamePause:
                        if gameDifficult < 10:
                            gameDifficult += 1
                if event.key == pygame.K_a:
                    if gamePause:
                        if gameDifficult > 1:
                            gameDifficult -= 1
                    
                # 自动寻路
                if event.key == pygame.K_SPACE:
                    snake.auto = not snake.auto
                
                # 暂停
                if event.key == pygame.K_s:
                    gamePause = not gamePause
                
                # 退出
                if event.key == pygame.K_c and pygame.KMOD_CTRL:
                    pygame.quit()
                    sys.exit()
                    
                if event.key == pygame.K_F11:
                    fullScreen = not fullScreen
                    if fullScreen:
                        screen = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN | pygame.HWSURFACE)
                    else:
                        screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)

                
        
        # 贪吃蛇的移动
        if not gameover and not gamePause:
            if snake.auto:
                snake.automove(bodyGroup)
                # snake2 = copy.deepcopy(snake)
                # if search(snake2, bodyGroup):
                #     snake.move()
            else:
                snake.move()
        # 画背景        
        screen.blit(backgroundImage, (0, 0))
        # 画蛇身
        for i in range(snake.bodyAmount):
            screen.blit(snake.bodys[i].image, snake.bodys[i].rect)
        # 画食物
        screen.blit(snake.food.image, snake.food.rect)
        # 画蛇头
        screen.blit(snake.head.image, snake.head.rect)
        snake.control = True
        # 画 gameover
        if gameover:
            screen.blit(gameoverImage, gameoverRect)
        # 画底边说明
        gameDifficultText = "游戏难度:" + str(gameDifficult)
        underTextLeft = font.render(gameDifficultText, True, (0, 0, 0), (199, 237, 204))
        screen.blit(underTextLeft, (80, 338))
        
        snakeBodyAmountCurrentText = "蛇身长度:" + str(snake.bodyAmount)
        underTextRight = font.render(snakeBodyAmountCurrentText, True, (0, 0, 0), (199, 237, 204))
        screen.blit(underTextRight, (435, 338))
        
        if gamePause:
            playText = "Play"
            if snake.auto:
                underTextPlay = font.render(playText, True, (255, 0, 0), (199, 237, 204))
            else:
                underTextPlay = font.render(playText, True, (0, 0, 0), (199, 237, 204))
            screen.blit(underTextPlay, (293, 338))
        else:
            playText = "Pause"
            if snake.auto:
                underTextPause = font.render(playText, True, (255, 0, 0), (199, 237, 204))
            else:
                underTextPause = font.render(playText, True, (0, 0, 0), (199, 237, 204))
            screen.blit(underTextPause, (285, 338))
        
        
        # 碰撞检测
        # 蛇头与蛇身
        if pygame.sprite.spritecollide(snake.head, bodyGroup, False, None) and not gameover:
            laughSound.play()
            gameover = True
        # 蛇头与食物，食物与蛇身
        ## if pygame.sprite.spritecollide(snake.head, foodGroup, False, None):
        if pygame.sprite.collide_rect(snake.head, snake.food):
            snake.food.rect.left = 67 + 22 * random.randint(1, 23-1)
            snake.food.rect.top = 67 + 22 * random.randint(1, 11-1)
            snake.bodyAmount += 1
            snake.eating = True
            snake.body = Diamond(snakeBodyPng)                                                          
            snake.bodys.append(snake.body)    
            bodyGroup.add(snake.body)
            bodyGroup.add(snake.head)
            while pygame.sprite.spritecollide(snake.food, bodyGroup, False, None):
                snake.food.rect.left = 67 + 22 * random.randint(1, 23-1)
                snake.food.rect.top = 67 + 22 * random.randint(1, 11-1)
            bodyGroup.remove(snake.head)
            
    
        
        
        # 刷新画布
        pygame.display.flip()
        clock.tick(gameDifficult * 5 - 4)
        
                
             


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
