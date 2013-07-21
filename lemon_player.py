#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import signal
import pygame
import time
import os
from pygame import mixer
from pygame.locals import *
from random import randint


class Player:
    def __init__(self):
        self.list = []
        self.play_flag = False
        self.pause_flag = False
        self.volume = 0.5
        self.curr_name = ''
        pygame.mixer.init()

    def add(self, item):
        self.list.append(item)

    def load(self, filename):
        with open(filename, 'r') as list_file:
            for line in list_file.readlines():
                line = line.strip('\n').strip()
                if len(line) > 0:
                    self.list.append(line.strip('\n').strip())

    def play(self):
        #print 'play', self.play_flag, self.pause_flag
        if self.play_flag is False:
            mixer.music.load(self.next_name())
            mixer.music.play()
            self.play_flag = True
            self.pause_flag = False
        else:
            if self.pause_flag is False:
                mixer.music.pause()
                self.pause_flag = True
            else:
                mixer.music.unpause()
                self.pause_flag = False

    def pause(self):
        mixer.music.pause()
        self.pause_flag = True

    def add_volume(self, volume):
        #print 'add_volume', volume
        if volume > 0:
            self.volume = min(self.volume + volume, 1.0)
        else:
            self.volume = max(self.volume + volume, 0.0)
        mixer.music.set_volume(self.volume)

    def stop(self):
        mixer.music.stop()
        self.play_flag = False
        self.pause_flag = False

    def next_name(self):
        self.curr_name = self.list[randint(0, len(self.list) - 1)]
        return self.curr_name

    def get_name(self):
        print self.curr_name.split('/')[-1].split('.')[0]
        return self.curr_name.split('/')[-1].split('.')[0]

    def get_busy(self):
        return mixer.music.get_busy()

    def quit(self):
        mixer.quit()

    def get_time(self):
        sound = mixer.Sound(self.get_name())
        return sound.get_length()


COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (128, 128, 128)
COLOR_LIGHTGREEN = (108, 202, 138)
COLOR_LIGHTGREEN_C = (171, 241, 194)
SCREEN_SIZE = [360, 200]

def _is_in_(position, rect):
    return position[0] >= rect[0] and position[0] <= rect[0] + rect[2] and position[1] >= rect[1] and position[1] <= rect[1] + rect[3]

class ControlPause:
    def __init__(self, manager):
        self.x = SCREEN_SIZE[0] - 40
        self.y = 6
        self.w = 30
        self.h = 30
        self.hide = False
        self.inflg = False
        self.name = 'ctl_pause'
        self.manager = manager
        self.color = COLOR_LIGHTGREEN

    def set_player(self, player):
        self.player = player

    def draw(self, screen):
        m_position = [self.x, self.y, self.w, self.h]
        l_position = [self.x+8, self.y+6, self.w/2-10, self.h-12]
        r_position = [self.x+self.w/2+2, self.y+6, self.w/2-10, self.h-12]
        pygame.draw.rect(screen, self.color, m_position)
        pygame.draw.rect(screen, COLOR_WHITE, l_position)
        pygame.draw.rect(screen, COLOR_WHITE, r_position)

    def on_click(self):
        print 'ControlPause on_click'
        self.manager.forward('show', name='ctl_play')
        self.player.pause()

    def move_in(self):
        if self.inflg: return
        self.inflg = True
        print 'ControlPause move_in'
        self.color = COLOR_LIGHTGREEN_C

    def move_out(self):
        self.inflg = False
        print 'ControlPause move_out'
        self.color = COLOR_LIGHTGREEN

    def is_in(self, position):
        if self.hide: return False
        return _is_in_(position, [self.x, self.y, self.w, self.h])

    def show(self):
        self.hide = False

class ControlPlay:
    def __init__(self, manager):
        self.x = 0
        self.y = 0
        self.w = SCREEN_SIZE[0]
        self.h = SCREEN_SIZE[1]
        self.hide = True
        self.inflg = False
        self.name = 'ctl_play'
        self.manager = manager

    def set_player(self, player):
        self.player = player

    def draw(self, screen):
        if self.hide: return
        pass

    def on_click(self):
        print 'ControlPlay on_click'
        self.player.play()
        self.manager.forward('set_content', name='ctl_txt_name', args=self.player.get_name())
        self.hide = True

    def move_in(self):
        if self.inflg: return
        self.inflg = True
        print 'ControlPlay move_in'

    def move_out(self):
        self.inflg = False
        print 'ControlPlay move_out'

    def is_in(self, position):
        if self.hide: return False
        return _is_in_(position, [self.x, self.y, self.w, self.h])

    def show(self):
        self.hide = False

class ControlNext:
    def __init__(self, manager):
        self.x = SCREEN_SIZE[0] - 40
        self.y = SCREEN_SIZE[1] - 60
        self.w = 30
        self.h = 30
        self.hide = False
        self.inflg = False
        self.name = 'ctl_next'
        self.manager = manager
        self.color = COLOR_BLACK

    def set_player(self, player):
        self.player = player

    def draw(self, screen):
        #m_position = [self.x, self.y, self.w, self.h]
        #pygame.draw.rect(screen, COLOR_BLACK, m_position, 1)
        l_pos_list = [(self.x, self.y), (self.x, self.y+self.h), (self.x+self.w/2+4,self.y+self.h/2)]
        r_pos_list = [(self.x+self.w/2, self.y), (self.x+self.w/2, self.y+self.h), (self.x+self.w,self.y+self.h/2)]
        pygame.draw.polygon(screen, self.color, l_pos_list)
        pygame.draw.polygon(screen, self.color, r_pos_list)

    def on_click(self):
        print 'ControlNext on_click'
        self.player.stop()
        self.manager.forward('on_click', name='ctl_play')

    def move_in(self):
        if self.inflg: return
        self.inflg = True
        print 'ControlNext move_in'
        print 'ControlNext move_out'
        self.color = COLOR_GRAY

    def move_out(self):
        self.inflg = False
        print 'ControlNext move_out'
        self.color = COLOR_BLACK

    def is_in(self, position):
        if self.hide: return False
        return _is_in_(position, [self.x, self.y, self.w, self.h])

    def show(self):
        self.hide = False

class ControlProgressBar:
    def __init__(self, manager):
        self.x = 20
        self.y = SCREEN_SIZE[1] / 2
        self.w = SCREEN_SIZE[0] - 40
        self.h = 2
        self.hide = False
        self.inflg = False
        self.name = 'ctl_prb'
        self.manager = manager

    def set_player(self, player):
        self.player = player

    def draw(self, screen):
        m_position = [self.x, self.y, self.w, self.h]
        pygame.draw.rect(screen, COLOR_GRAY, m_position, 1)

    def on_click(self):
        print 'ControlProgressBar on_click'

    def move_in(self):
        if self.inflg: return
        self.inflg = True
        print 'ControlProgressBar move_in'

    def move_out(self):
        self.inflg = False
        print 'ControlProgressBar move_out'

    def is_in(self, position):
        if self.hide: return False
        return _is_in_(position, [self.x, self.y, self.w, self.h])

    def show(self):
        self.hide = False

class ControlText:
    def __init__(self, manager):
        self.x = 20
        self.y = SCREEN_SIZE[1]/2 - 32
        self.w = SCREEN_SIZE[0] - 40
        self.h = 30
        self.hide = False
        self.inflg = False
        self.name = 'ctl_txt_name'
        self.manager = manager
        self.content = ''
        self.font = pygame.font.SysFont("arial", 20)

    def set_player(self, player):
        self.player = player

    def set_content(self, content):
        self.content = content

    def draw(self, screen):
        #m_position = [self.x, self.y, self.w, self.h]
        #pygame.draw.rect(screen, COLOR_BLACK, m_position, 1)
        text = self.font.render(self.content, True, COLOR_BLACK)
        screen.blit(text, (self.x, self.y+(self.h-18)/2))

    def on_click(self):
        print 'ControlText on_click'

    def move_in(self):
        if self.inflg: return
        self.inflg = True
        print 'ControlText move_in'

    def move_out(self):
        self.inflg = False
        print 'ControlText move_out'

    def is_in(self, position):
        if self.hide: return False
        return _is_in_(position, [self.x, self.y, self.w, self.h])

    def show(self):
        self.hide = False

    def set_content(self, content):
        self.content = content

class ControlManager:
    def __init__(self):
        self.controls = []

    def add(self, ctlclass, control):
        self.controls.append((ctlclass, control))

    def forward(self, function, args=None, position=None, name=None):
        for ctlclass,control in self.controls:
            if (position is not None):
                if control.inflg and not control.is_in(position):
                    control.move_out()
            if (position is not None and control.is_in(position)) or \
                (name is not None and control.name == name):
                if args is None:
                    ctlclass.__dict__[function](control)
                else:
                    ctlclass.__dict__[function](control, args)
                break

    def draw(self, screen):
        for ctlclass, control in self.controls:
            control.draw(screen)

    def set_player(self, player):
        for ctlclass, control in self.controls:
            control.set_player(player)

class Lemon:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.stop_flag = False
        self.ctlmanager = ControlManager()
        self.ctlmanager.add(ControlPlay, ControlPlay(self.ctlmanager))
        self.ctlmanager.add(ControlPause, ControlPause(self.ctlmanager))
        self.ctlmanager.add(ControlNext, ControlNext(self.ctlmanager))
        self.ctlmanager.add(ControlProgressBar, ControlProgressBar(self.ctlmanager))
        self.ctlmanager.add(ControlText, ControlText(self.ctlmanager))
        self.player = Player()

    def start(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Lemon")
        self.ctlmanager.set_player(self.player)
        #self.player.load('play.lst')
        self.draw()

        pygame.time.delay(1000)
        self.ctlmanager.forward('on_click', name='ctl_play')
        #print 'time:', self.player.get_time()

    def update(self):
        pygame.display.update()

    def draw(self):
        self.screen.fill(COLOR_WHITE)
        self.ctlmanager.draw(self.screen)
        self.update()

    def run(self):
        while not self.stop_flag:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.stop_flag = True
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.ctlmanager.forward('on_click', name='ctl_next')
                    elif event.key == K_RIGHT:
                        self.ctlmanager.forward('on_click', name='ctl_next')
                    elif event.key == K_UP:
                        self.player.stop()
                    elif event.key == K_DOWN:
                        self.ctlmanager.forward('on_click', name='ctl_play')
                    elif event.key == K_EQUALS:
                        self.player.add_volume(0.1)
                    elif event.key == K_MINUS:
                        self.player.add_volume(-0.1)
                elif event.type == MOUSEBUTTONUP:
                    self.ctlmanager.forward('on_click', position=pygame.mouse.get_pos())
                elif event.type == MOUSEMOTION:
                    self.ctlmanager.forward('move_in', position=pygame.mouse.get_pos())
            time.sleep(0.01)
            if not self.player.get_busy():
                self.ctlmanager.forward('on_click', name='ctl_next')

        self.quit()

    def quit(self):
        self.player.quit()
        pygame.quit()

    def load_mp3(self):
        with open('path.lst', 'r') as path_file:
            for line in path_file.readlines():
                self.load_mp3_with_path(line.strip('\n'))

    def load_mp3_with_path(self, path):
        if len(path) == 0: return
        for file_item in os.listdir(path):
            if file_item[-4:] == '.mp3':
                self.player.add(path.rstrip('/') + '/' + file_item)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    lemon = Lemon()
    lemon.load_mp3()
    lemon.start()
    lemon.run()


