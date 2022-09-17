import pygame
import sys
import noise # only import if using mountaineous terrain generation


class Player: # usually a class should be in another file for organisation, which is why it has parameters
    def __init__(self, pos, tile_size):
        self.display = pygame.display.get_surface()
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect(center=pos)
        self.moving_left = False
        self.moving_right = False
        self.speed = 3
        self.gravity = 0

    def tile_collision_test(self, tiles):
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, tiles):
        self.movement = pygame.math.Vector2(0, 0)
        if self.moving_left:
            self.movement.x -= self.speed
        if self.moving_right:
            self.movement.x += self.speed
        self.movement.y += self.gravity
        self.gravity += 0.5
        if self.gravity > 4:
            self.gravity = 4
        self.rect.x += self.movement.x
        hit_list = self.tile_collision_test(tiles)
        for tile in hit_list:
            if self.movement.x > 0:
                self.rect.right = tile.left
            elif self.movement.x < 0:
                self.rect.left = tile.right
        self.rect.y += self.movement.y
        hit_list = self.tile_collision_test(tiles)
        for tile in hit_list:
            if self.movement.y > 0:
                self.rect.bottom = tile.top
                self.gravity = 0
            elif self.movement.y < 0:
                self.rect.top = tile.bottom
                self.gravity = 0
        return self.rect

    def update(self, tiles, scroll):
        self.rect = self.move(tiles)
        self.display.blit(
            self.image, (self.rect.x - scroll.x, self.rect.y - scroll.y))


def draw_text(text, size, color, surface, pos):
    font = pygame.font.Font('assets/PressStart2P-Regular.ttf', size)
    text_render = font.render(text, True, color)
    text_rect = text_render.get_rect()
    text_rect.center = pos
    display.blit(text_render, text_rect)


def generate_chunk(x, y):
    chunk_data = []
    for y_pos in range(chunk_size):
        for x_pos in range(chunk_size):
            target_x = x * chunk_size + x_pos
            target_y = y * chunk_size + y_pos
            tile_type = 0
            # use this section for flat terrain
            if target_y > 10:
                tile_type = 2
                chunk_data.append([[target_x, target_y], tile_type])
            elif target_y == 10:
                tile_type = 1
                chunk_data.append([[target_x, target_y], tile_type])
            # use this section for mountaineous terrain (make sure to import noise)
            height = int(noise.pnoise1(target_x * 0.1, repeat=999999999) * 6) # change the * 6 to a higher or lower number to increase or reduce the terrain height
            if target_y > 8 - height:
                tile_type = 2
                chunk_data.append([[target_x, target_y], tile_type])
            elif target_y == 8 - height:
                tile_type = 1
                chunk_data.append([[target_x, target_y], tile_type])
    return chunk_data


def render_map(tiles):
    game_map = {}
    for y in range(3):
        for x in range(4):
            target_x = x + scroll.x // (chunk_size * tile_size)
            target_y = y + scroll.y // (chunk_size * tile_size)
            target_chunk = f'{str(target_x)};{str(target_y)}'
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x, target_y)
            for tile in game_map[target_chunk]:
                display.blit(tile_index[tile[1]], (tile[0][0] * tile_size -
                             scroll.x, tile[0][1] * tile_size - scroll.y))
                if tile[1] in [1, 2]:
                    tiles.append(pygame.Rect(
                        tile[0][0] * tile_size, tile[0][1] * tile_size, tile_size, tile_size))


def game():
    while True:
        tile_rects = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if player.air_timer < 2:
                        player.gravity = -8
                if event.key == pygame.K_a:
                    player.moving_left = True
                if event.key == pygame.K_d:
                    player.moving_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.moving_left = False
                if event.key == pygame.K_d:
                    player.moving_right = False

        display.fill((146, 244, 255))

        pygame.draw.rect(display, (5, 80, 75), pygame.Rect(
            0, (window_size.y // 2), window_size.x, (window_size.y // 2)))

        scroll.x += (player.rect.x - scroll.x -
                     (window_size.x // 2) + (player.rect.width // 2)) // 20
        scroll.y += (player.rect.y - scroll.y -
                     (window_size.y // 2) + (player.rect.width // 2)) // 20

        render_chunk(tile_rects)

        player.update(tile_rects, scroll)

        draw_text(f'FPS: {str(int(clock.get_fps()))}', 16, (255, 255,
                  255), display, (window_size.x // 2, (window_size.y - 25)))

        pygame.display.update()
        clock.tick(60)


pygame.init()
pygame.display.set_caption('Pygame Window')
window_size = pygame.math.Vector2(600, 400)
display = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

tile_size = 32
chunk_size = 8

dirt_image = pygame.Surface((tile_size, tile_size))
dirt_image.fill((100, 50, 50))
grass_image = pygame.Surface((tile_size, tile_size))
grass_image.fill((0, 255, 0))

tile_index = {1: grass_image, 2: dirt_image}

scroll = pygame.math.Vector2(0, 0)

player = Player(pygame.math.Vector2(100, 100), tile_size)

if __name__ == '__main__':
    game_state = game()
