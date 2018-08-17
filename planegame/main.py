import pygame
import sys
import traceback
from pygame.locals import *
import myplane
import enemy
import bullet
import supply
from random import *
import dynamicmap

pygame.init()
pygame.mixer.init()

bg_size = width , height = 480 , 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战')

#background = pygame.image.load('images/background.png').convert()


#定义动态地图
bg1 = dynamicmap.MyMap(x = 0,y = 0)
bg2 = dynamicmap.MyMap(x = 0,y = 700)

BLACK = (0 , 0 , 0)
GREEN = (0 , 255 , 0)
RED = (255 , 0 , 0)
WHITE = (255 , 255 , 255)

#音乐
pygame.mixer.music.load('music/game_music.mp3')
pygame.mixer.music.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound('music/enemy3_out.wav')
enemy3_fly_sound.set_volume(0.4)
enemy3_down_sound = pygame.mixer.Sound('music/enemy3_down.wav')
enemy3_down_sound.set_volume(0.5)
enemy2_down_sound = pygame.mixer.Sound('music/enemy2_down.wav')
enemy2_down_sound.set_volume(0.5)
enemy1_down_sound = pygame.mixer.Sound('music/enemy1_down.wav')
enemy1_down_sound.set_volume(0.3)
me_down_sound = pygame.mixer.Sound('music/me_down.wav')
me_down_sound.set_volume(0.3)
up_level = pygame.mixer.Sound('music/up_level.wav')
up_level.set_volume(0.2)
bomb_sound = pygame.mixer.Sound('music/use_bomb.wav')
bomb_sound.set_volume(0.3)
get_bomb_sound = pygame.mixer.Sound('music/get_bomb.wav')
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound('music/get_bullet.wav')
get_bullet_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound('music/supply.wav')
supply_sound.set_volume(0.2)
bullet_sound = pygame.mixer.Sound('music/bullet.wav')
bullet_sound.set_volume(0.2)

def add_small_enemies(group1 , group2 , num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1 , group2 , num):
    for i in range(num):
        e1 = enemy.MidEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_big_enemies(group1 , group2 , num):
    for i in range(num):
        e1 = enemy.BigEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def increase_speed(group , num):
    for each in group:
        each.speed += num

def main():
    pygame.mixer.music.play(-1)
    
    #生成mylpane
    me  = myplane.Myplane(bg_size)

    enemies = pygame.sprite.Group()

    #smallenemy
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies , enemies , 15)

    #游戏结束画面
    gameover_font = pygame.font.Font('font/font_1.ttf' , 48)
    gameover_fontx = pygame.font.Font('font/font_3.ttf' , 28)
    
    #midenemy
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies , enemies , 5)
    
    #bigenemy
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies , enemies , 2)

    #限制重复打开最高分记录文件
    record_tag = 1

    #定义子弹列表
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 10
    for i in range(BULLET2_NUM // 2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 28 , me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 25 , me.rect.centery)))
    bullet1 = []
    bullet1_index = 0
    BULLET_NUM = 5
    for i in range(BULLET_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))
    
    #30秒一个补给
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME , 30 * 1000)

    #玩家飞机刷新间隔
    x = False

    #双发子弹定时器
    DOUBLE_BULLET_TIME = USEREVENT + 1

    INVINCIBLE = USEREVENT + 2
    
    #标记是否使用双子弹
    tag_double_bullet = False

    #生命数量
    life_image = pygame.image.load('images/life.png').convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3
    
    running = True

    board_image = pygame.image.load('images/board.png').convert_alpha()
    board_rect = board_image.get_rect()
    board_rect1 = board_rect
    board_rect2 = board_rect
    
    #暂停标志
    pause = False
    button_pa_1 = pygame.image.load('images/button_pa-1.png').convert_alpha()
    button_pa_2 = pygame.image.load('images/button_pa-2.png').convert_alpha()
    button_co_1 = pygame.image.load('images/button_co-1.png').convert_alpha()
    button_co_2 = pygame.image.load('images/button_co-2.png').convert_alpha()
    pause_rect = button_pa_1.get_rect()
    pause_rect.left , pause_rect.top = width - pause_rect.width - 10 , 10
    pause_image = button_pa_1

    #炸弹
    bomb_image = pygame.image.load('images/bomb.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font('font/font_1.ttf' , 48)
    bomb_num = 3

    
    clock = pygame.time.Clock()

    score = 0
    score_font = pygame.font.Font('font/font_1.ttf' , 36)

    #难度设置
    level = 1
    
    switch_image = True

    #中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0
    #延迟
    delay = 100
    
    while running:
        #screen.blit(background , (0 , 0))
        bg1.map_update(screen)
        bg2.map_update(screen)
        bg1.map_rolling()
        bg2.map_rolling()
    
        if level == 1 and score > 2000:
            level = 2
            up_level.play()
            add_small_enemies(small_enemies , enemies , 3)
            add_mid_enemies(mid_enemies , enemies , 2)
            add_big_enemies(big_enemies , enemies , 1)
        if level == 2 and score > 5000:
            level = 3
            up_level.play()
            add_small_enemies(small_enemies , enemies , 3)
            add_mid_enemies(mid_enemies , enemies , 2)
            add_big_enemies(big_enemies , enemies , 1)
            increase_speed(small_enemies , 1)
        if level == 3 and score > 10000:
            level = 4
            up_level.play()
            add_small_enemies(small_enemies , enemies , 5)
            add_mid_enemies(mid_enemies , enemies , 3)
            add_big_enemies(big_enemies , enemies , 2)
            increase_speed(small_enemies , 1)
            increase_speed(mid_enemies , 1)
        if level == 4 and score > 20000:
            level = 5
            up_level.play()
            add_small_enemies(small_enemies , enemies , 5)
            add_mid_enemies(mid_enemies , enemies , 3)
            add_big_enemies(big_enemies , enemies , 2)
            increase_speed(small_enemies , 1)
            increase_speed(mid_enemies , 1)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and pause_rect.collidepoint(event.pos):
                    if pause_image == button_co_2:
                        pause_image = button_pa_2
                    else:
                        pause_image = button_co_2
                    screen.blit(pause_image , pause_rect)
                    pause = not pause
                    if pause:
                        pygame.time.set_timer(SUPPLY_TIME , 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME , 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):
                    if pause:
                        pause_image = button_co_2
                    else:
                        pause_image = button_pa_2
                else:
                    if pause:
                        pause_image = button_co_1
                    else:
                        pause_image = button_pa_1

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            
            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if choice([True , False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == DOUBLE_BULLET_TIME:
                tag_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME , 0)

            elif event.type == INVINCIBLE:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE , 0)

        #画暂停符号
        if life_num != 0:
            screen.blit(pause_image , pause_rect)
        if pause == False and life_num:
            
            #检测键盘操作
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            #画补给
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image , bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply , me):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False
                
            if bullet_supply.active:
                    bullet_supply.move()
                    screen.blit(bullet_supply.image , bullet_supply.rect)
                    if pygame.sprite.collide_mask(bullet_supply , me):
                        get_bullet_sound.play()
                        tag_double_bullet = True
                        pygame.time.set_timer(DOUBLE_BULLET_TIME , 20 * 1000)
                        bullet_supply.active = False
                        
            #bullet
            if not(delay % 10):
                bullet_sound.play()
                if tag_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 28 , me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 25 , me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET_NUM



            #碰撞检测bullet
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image , b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b , enemies , False , pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.energy -= 1
                                e.hit = True
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False
                    
            #画大飞机
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit , each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1 , each.rect)
                        else:
                            screen.blit(each.image2 , each.rect)
                    #画血槽
                    pygame.draw.line(screen , BLACK , \
                                    (each.rect.left + 20 , each.rect.top - 5),\
                                    (each.rect.right - 20 , each.rect.top - 5),\
                                     2)
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen , energy_color , \
                                     (each.rect.left + 20 , each.rect.top - 5), \
                                     (each.rect.left + 20 + (each.rect.width - 40) * energy_remain , \
                                      each.rect.top - 5) , 2)   
                    #出场音效
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play()
                else:
                    #destroy
                    if not(delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index] , each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 1500
                            each.reset()
                            
            #画中飞机
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit , each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image , each.rect)
                    pygame.draw.line(screen , BLACK , \
                                    (each.rect.left + 20 , each.rect.top + 10),\
                                    (each.rect.right - 20 , each.rect.top + 10),\
                                     2)
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen , energy_color , \
                                   (each.rect.left + 20 , each.rect.top + 10), \
                                   (each.rect.left + 20 + (each.rect.width - 40) * energy_remain , \
                                    each.rect.top + 10) , 2)
                else:
                    if not(delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index] , each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 600
                            each.reset()
                
            #画小飞机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image , each.rect)
                else:
                    if not(delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index] , each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 100
                            each.reset()
                            
            #我方飞机碰撞检测
            enemies_down = pygame.sprite.spritecollide(me , enemies , False , pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False
            
            #画我方飞机
            if me.active:
                if me.invincible:
                    if x:                
                        if switch_image:
                            screen.blit(me.image1 , me.rect)
                        else:
                            screen.blit(me.image2 , me.rect)
                else:
                    if switch_image:
                        screen.blit(me.image1 , me.rect)
                    else:
                        screen.blit(me.image2 , me.rect)
            else:
                if not(delay % 3):
                    if me_destroy_index == 0:
                            me_down_sound.play()
                    screen.blit(each.destroy_images[me_destroy_index] , me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE , 3 * 1000)

            #画炸弹
            bomb_str = bomb_font.render('× %d' % bomb_num , True , WHITE)
            str_rect = bomb_str.get_rect()
            screen.blit(bomb_image , (10 , height - 10 - bomb_rect.height))
            screen.blit(bomb_str , (20 + bomb_rect.width , height - 5 - str_rect.height))

            #画生命数量
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image , \
                                (width - 10 - (i + 1) * life_rect.width,\
                                 height - 10 - life_rect.height))
            #画计分板
            score_str = score_font.render('Score : %s' % str(score) , True , WHITE)
            screen.blit(score_str , (5 , 5))
            
        #没有生命的时候游戏结束
        elif life_num == 0:
            #音乐停止
            pygame.mixer.music.stop()
            pygame.mixer.stop()

            #停止发补给
            pygame.time.set_timer(SUPPLY_TIME , 0)
     
            if record_tag == 1:
            #查看历史最高分
                with open('record.txt' , 'r') as f:
                    record_score = int(f.read())
                if score > record_score:
                    with open('record.txt' , 'w') as f:
                        f.write(str(score))
                    record_score = score
                    print(record_score)
                record_tag = 0
            best_score_str = score_font.render('Best Score : %d' % record_score , True , WHITE)
            screen.blit(best_score_str , (5 , 5))

            best_score_text = gameover_font.render('Your Score' , True , WHITE)
            best_score_text_rect = best_score_text.get_rect()
            best_score_text_rect.left = (width - best_score_text_rect.width) // 2
            best_score_text_rect.top = (height - best_score_text_rect.height - 150) // 2
            screen.blit(best_score_text , best_score_text_rect)
            
            best_score_vtext = gameover_font.render(str(score) , True , WHITE)
            best_score_vtext_rect = best_score_vtext.get_rect()
            best_score_vtext_rect.left = (width - best_score_vtext_rect.width) // 2
            best_score_vtext_rect.top = (height - best_score_vtext_rect.height - 30) // 2
            screen.blit(best_score_vtext , best_score_vtext_rect)
            
            board_rect1.left = (width - board_rect.width) // 2
            board_rect1.top = (height - board_rect.height + 150) // 2
            screen.blit(board_image , board_rect1)
            
            board_str1 = gameover_fontx.render('Start Again' , True , BLACK)
            board_str1_rect = board_str1.get_rect()
            board_str1_rect.left = (width - board_rect.width) // 2 +\
                                   board_rect.width // 2 - board_str1_rect.width // 2
            board_str1_rect.top = (height - board_rect.height + 150) // 2 + 13
            screen.blit(board_str1 , board_str1_rect)
                        
            board_rect2.left = (width - board_rect.width) // 2
            board_rect2.top = (height - board_rect.height + 280) // 2
            screen.blit(board_image , board_rect2)

            board_str2 = gameover_fontx.render('Quit Game' , True , BLACK)
            board_str2_rect = board_str2.get_rect()
            board_str2_rect.left = (width - board_rect.width) // 2 +\
                                   board_rect.width // 2 - board_str2_rect.width // 2
            board_str2_rect.top = (height - board_rect.height + 280) // 2 + 13
            screen.blit(board_str2 , board_str2_rect)

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                #重新开始游戏
                if board_rect1.right > pos[0] > board_rect1.left and \
                   397 < pos[1] < 55 + 397:
                    main()
                #结束游戏
                elif board_rect2.right > pos[0] > board_rect2.left and \
                   462 < pos[1] < 55 + 462:
                    pygame.quit()
                    sys.exit()
                
        pygame.display.flip()

        if not(delay % 5):
            switch_image = not switch_image

        if not(delay % 20):
            x = not x

        delay -= 1
        
        if not delay:
            delay = 100
            
        clock.tick(60)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
        
