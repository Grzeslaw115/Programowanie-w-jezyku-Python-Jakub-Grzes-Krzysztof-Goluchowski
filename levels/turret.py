import pygame as pg
import constants as c
import math


class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheet, cost, damage, tile_x, tile_y):
        pg.sprite.Sprite.__init__(self)
        self.range = 150
        self.cooldown = 1500
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None

        self.cost = cost
        self.damage = damage

        self.tile_x = tile_x
        self.tile_y = tile_y

        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE

        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        self.angle = 90
        self.org_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Create range circle
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "gray100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def load_images(self):
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            tmp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(tmp_img)
        return animation_list

    def update(self, enemy_group):
        if self.target:
            self.play_animation()
        else:
            if pg.time.get_ticks() - self.last_shot > self.cooldown:
                self.pick_target(enemy_group)


    def play_animation(self):
        self.org_image = self.animation_list[self.frame_index]
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index = (self.frame_index + 1) % c.ANIMATION_STEPS
            if self.frame_index == 0:
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def draw(self, surface):
        self.image = pg.transform.rotate(self.org_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)

    def pick_target(self, enemy_group):
        for target in enemy_group:
            x_dist = target.rect.centerx - self.x
            y_dist = target.rect.centery - self.y
            dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
            if dist < self.range:
                self.target = target
                self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                target.health -= self.damage