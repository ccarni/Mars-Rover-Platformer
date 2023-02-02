import pygame
import helper_functions
import block as block_file
import spring
import player as player_file
import background
import spike as spike_file
import ice as ice_file
import random
import checkpoint as checkpoint_file
import sand as sand_file
from coyote import Coyote


class Runner():


    def make_clouds(self, level_size, cloud, tilesize, objs):
        for i in range(20):
            x = random.randint(0, level_size[0] // tilesize)
            y = random.randint(0, level_size[1] // tilesize // 2)
            c = background.Background(cloud, x * tilesize, y * tilesize)
            c.depth = random.uniform(0.5, 1)
            objs.append(c)

            return x, y, c, objs

    def make_mountains(self, level_size, objs):
        for i in range(1000):
            x = random.randint(0, level_size[0])
            y = random.randint(10, 2 * level_size[1] // 3)
            w = random.randint(10, 100)
            mountain = helper_functions.draw_mountain(w, level_size[1] - y)
            m = background.Background(mountain, x, y)
            m.depth = random.uniform(0.25, 0.5)
            temp_surf = pygame.Surface(mountain.get_size()).convert_alpha()
            temp_surf.fill((0, 0, 0, 255 * m.depth))
            m.image.blit(temp_surf, (0, 0))
            m.image.set_colorkey((0, 0, 0))
            objs.append(m)

        return x, y, w, mountain, m, objs

    def make_stars(self, level_size, objs):
        for i in range(2000):
            star = helper_functions.draw_star()
            x = random.randint(0, level_size[0])
            y = random.randint(0, level_size[1])
            s = background.Background(star, x, y)
            s.depth = random.uniform(0, 0.01)
            objs.append(s)

        return star, x, y, s, objs

    def run(self):

        display = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        screen = pygame.Surface((300, 200))

        # Each tile is a square of pixels
        tilesize = 20

        dirt = helper_functions.draw_dirt()
        grass = helper_functions.draw_grass(dirt)
        cloud = helper_functions.draw_cloud()

# ------------------------------------------------------------ DRAW TILES --------------------------------------------
        # Make all the tiles the right size
        cloud = pygame.transform.scale(cloud, (tilesize, tilesize))
        dirt = pygame.transform.scale(dirt, (tilesize, tilesize))
        grass = pygame.transform.scale(grass, (tilesize, tilesize))
        drawn_spring = pygame.transform.scale(helper_functions.draw_spring(), (tilesize, tilesize / 2))
        drawn_spike = pygame.transform.scale(helper_functions.draw_spike(), (tilesize, tilesize))
        drawn_ice = pygame.transform.scale(helper_functions.draw_ice(), (tilesize, tilesize))
        checkpoint = pygame.transform.scale(helper_functions.draw_checkpoint(), (tilesize, tilesize))
        sand = pygame.transform.scale(helper_functions.draw_sand(), (tilesize, tilesize))


        # Read in the level.txt file to determine the placement of blocks
        with open('level.txt', 'r') as level:
            block_grid = level.read()
        block_grid = block_grid.split('\n')

        # How many blocks big the level will be
        level_size = (tilesize * len(block_grid[0]), tilesize * len(block_grid))
        objs = []

        #makes clouds
        x, y, c, objs = self.make_clouds(level_size, cloud, tilesize, objs)

        # Make the mountains (which look more like trees)
        x, y, w, mountain, m, objs = self.make_mountains(level_size, objs)

        #make moon
        moon = helper_functions.draw_moon()
        m = background.Background(moon, 200, 10)
        m.depth = 0.1  # This depth controls the parallax - smaller is slower
        objs.append(m)

        # Draw the stars
        star, x, y, s, objs = self.make_stars(level_size, objs)

        p = helper_functions.draw_player()
        player = player_file.Player(p, 0, 0)

# ----------------------------------------- BLOCKS ---------------------------------------------------------------------
        blocks = pygame.sprite.Group()
        for row in range(len(block_grid)):
            for col in range(len(block_grid[row])):
                if block_grid[row][col] == 'd':
                    d = block_file.Block(dirt, col * tilesize, row * tilesize)
                    blocks.add(d)
                if block_grid[row][col] == 'g':
                    g = block_file.Block(grass, col * tilesize, row * tilesize)
                    blocks.add(g)
                if block_grid[row][col] == 's':
                    s = spring.Spring(drawn_spring, col * tilesize, row * tilesize + tilesize / 2)
                    blocks.add(s)
                if block_grid[row][col] == 'k':
                    k = spike_file.Spike(drawn_spike, col * tilesize, row * tilesize)
                    blocks.add(k)
                if block_grid[row][col] == 'i':
                    i = ice_file.Ice(drawn_ice, col * tilesize, row * tilesize)
                    blocks.add(i)
                if block_grid[row][col] == 'c':
                    c = checkpoint_file.Checkpoint(checkpoint, col * tilesize, row * tilesize)
                    blocks.add(c)
                if block_grid[row][col] == 'n':
                    n = sand_file.Sand(sand, col * tilesize, row * tilesize)
                    blocks.add(n)

        # Draw the background objects so that further away objects are behind closer ones
        objs.sort(key=lambda x: x.depth)

        clock = pygame.time.Clock()
        fps = 30

        max_coyote_time = 2
        coyote_timer = max_coyote_time
        can_jump = False

        max_jump_buffer = 4
        jump_timer = max_jump_buffer
        jump_input = False

        running = True
        true_scroll = [0, 0]
        scroll = [0, 0]
        while running:
            clock.tick(fps)
            screen.fill((0, 0, 0))
            for obj in objs:
                screen.blit(obj.image, obj.rect)
            blocks.draw(screen)
            screen.blit(player.image, (player.rect.x - scroll[0], player.rect.y - scroll[1]))
            s = pygame.transform.smoothscale(screen, display.get_size())
            display.blit(s, (0, 0))
            pygame.display.update()
# ---------------------------------------------- INPUT ---------------------------------------------

            if jump_timer > 0:
                jump_timer -= 1
            if jump_timer <= 0:
                jump_input = False

            if player.on_ground:
                coyote_timer = max_coyote_time
                can_jump = True
            else:
                if coyote_timer > 0:
                    coyote_timer -= 1
                if coyote_timer <= 0:
                    can_jump = False


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if (event.key == pygame.K_w or event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                        jump_input = True
                        jump_timer = max_jump_buffer

            if jump_input and can_jump:
                player.v = -8.5

            keys = pygame.key.get_pressed()
            player.horizontal_dir = None
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                if player.on_ice:
                    player.a_x = -5
                player.horizontal_dir = 'left'
                if player.rect.x < 0:
                    player.rect.x = 0
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                if player.on_ice:
                    player.a_x = 5
                player.horizontal_dir = 'right'
                if player.rect.right - scroll[0] > screen.get_width():
                    player.rect.right = screen.get_width() + scroll[0]


            # Reset the player if they fall
            if player.rect.y > level_size[1]:
                player.respawn(scroll)

            # The camera magic :)
            # Every object moves based on the scroll variable
            # The scroll variable updates based on how far from the player the center of the screen is
            scroll_speed = 7

            true_scroll[0] += (player.rect.x - true_scroll[0] - screen.get_width() / 2) / scroll_speed
            true_scroll[1] += (player.rect.y - true_scroll[1] - screen.get_height() / 2) / scroll_speed

            # Casting to an integer when using the scroll improves the quality
            scroll[0] = int(true_scroll[0])
            scroll[1] = int(true_scroll[1])

            # Block scrolling on reaching level boundaries
            if scroll[0] < 0:
                scroll[0] = 0
            if scroll[0] + screen.get_width() > len(block_grid[0]) * tilesize:
                scroll[0] = len(block_grid[0]) * tilesize - screen.get_width()

            if scroll[1] < 0:
                scroll[1] = 0
            if scroll[1] + screen.get_height() > len(block_grid) * tilesize:
                scroll[1] = len(block_grid) * tilesize - screen.get_height()

            # Update block and background locations
            for obj in objs:
                obj.update(scroll)
            blocks.update(scroll)

            # Convert the player coordinates to world coordinates
            player.rect.x -= scroll[0]
            player.rect.y -= scroll[1]

            if player.on_ice:
                player.ice_x()
            else:
                speed = 5
                if player.on_sand:
                    speed = 2
                player.v_x = 0
                player.a_x = 0
                if player.horizontal_dir == 'left':
                    player.rect.x -= speed
                if player.horizontal_dir == 'right':
                    player.rect.x += speed

            # Check horizontal ball-et heck
            # Doing things this way avoids issues where the collision occurs on a corner of the block
            # so that there isn't confusion over whether to place the player above the block or to the side
            player.on_ice = False
            player.on_ground = False
            collides = pygame.sprite.spritecollide(player, blocks, dokill=False)
            for block in collides:
                block.collide_horizontal(player, scroll=scroll)




            # Update y position and check vertical ball-et heck
            player.update_y(scroll)
            collides = pygame.sprite.spritecollide(player, blocks, dokill=False)
            for block in collides:
                block.collide_vertical(player, scroll=scroll)



            # Convert the world coordinates back to player coordinates
            player.rect.x += scroll[0]
            player.rect.y += scroll[1]