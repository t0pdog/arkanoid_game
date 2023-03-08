import pygame
from random import randrange as rnd


class Game:
    '''
    The player controls a small racket platform that can be moved horizontally
    from one wall to another, substituting it under the ball, preventing it from
    falling down. The impact of the ball on the brick leads to the destruction 
    of the brick. After all the bricks on a given level are destroyed, there 
    is a transition to the next level, with a new set of bricks.
    '''
    def __init__(self, width=1200, height=800, fps=60, paddle_w=630,
                 paddle_h=35, paddle_speed=20, ball_radius=20,
                 ball_speed=6, num_blocks=80):
        
        # game window settings
        self.width = width
        self.height = height
        self.fps = fps
        # Platform settings, dimensions, speed.
        # The platform is an instance of Python's built-in Rect class.
        self.paddle_w = paddle_w
        self.paddle_h = paddle_h
        self.paddle_speed = paddle_speed
        # ball settings
        self.ball_radius = ball_radius
        self.ball_speed = ball_speed
        # block settings
        self.num_blocks = num_blocks
        # calculated parameters
        self.paddle = pygame.Rect(
            self.width // 2 - self.paddle_w // 2,
            self.height - self.paddle_h - 10,
            self.paddle_w, self.paddle_h
        )
        self.ball_rect = int(self.ball_radius * 2 ** 0.5)
        self.ball = pygame.Rect(
            rnd(self.ball_rect, self.width - self.ball_rect),
            self.height // 2,
            self.ball_rect,
            self.ball_rect
        )
        self.dx, self.dy = 1, -1

        self.block_list = [
            pygame.Rect(10+60*i, 10+70 *j,40,20) for i in range(20) for j in range(4)
        ]
        self.color_list = [
            (rnd(150,256), rnd(1,2), rnd(159,256)) for i in range(20) for j in range(4)
        ]

        pygame.init()
        self.sc = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.img = pygame.image.load('2.jpg').convert()

    def detect_collision(self, dx, dy, ball, rect):
        """
        Detects and handles collisions between game objects.
        """
        if dx > 0:
            delta_x = ball.right - rect.left
        else:
            delta_x = rect.right - ball.left
        if dy > 0:
            delta_y = ball.bottom - rect.top
        else:
            delta_y = rect.bottom - ball.top

        if abs(delta_x - delta_y) < 10:
            dx, dy = -dx, -dy
        elif delta_x > delta_y:
            dy = -dy
        elif delta_y > delta_x:
            dx = -dx
        return dx, dy

    def main(self):
        """
        Initializes the game and runs it.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.sc.blit(self.img,(0,0))
            #drawing world
            [
                pygame.draw.rect(self.sc, self.color_list[color], block)
                for color, block in enumerate(self.block_list)
            ]
            pygame.draw.rect(
                self.sc,pygame.Color('lightblue'),self.paddle
            )
            pygame.draw.circle(
                self.sc, pygame.Color('white'),
                self.ball.center, self.ball_radius
            )
            # control
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.paddle.left > 0:
                self.paddle.left -= self.paddle_speed
            if key[pygame.K_RIGHT] and self.paddle.right < self.width:
                self.paddle.right += self.paddle_speed

            # ball movement
            self.ball.x += self.ball_speed * self.dx
            self.ball.y += self.ball_speed * self.dy

            # collision left right
            if (
                self.ball.centerx < self.ball_radius or
                self.ball.centerx > self.width - self.ball_radius
                ):
                self.dx = -self.dx

            # collision top
            if self.ball.centery < self.ball_radius:
                self.dy = -self.dy

            # collision paddle
            if self.ball.colliderect(self.paddle) and self.dy > 0:
                self.dx, self.dy = self.detect_collision(
                    self.dx, self.dy, self.ball, self.paddle
                )

            # collision blocks
            hit_index = self.ball.collidelist(self.block_list)
            if hit_index != -1:
                hit_rect = self.block_list.pop(hit_index)
                hit_color = self.color_list.pop(hit_index)
                self.dx,self.dy = self.detect_collision(
                    self.dx, self.dy, self.ball, hit_rect
                )
                # special effects
                hit_rect.inflate_ip(self.ball.width * 2, self.ball.height * 2)
                pygame.draw.rect(self.sc, hit_color, hit_rect)
                self.fps +=2

            # update screen
            pygame.display.flip()
            self.clock.tick(self.fps)

            #win, game over
            if self.ball.bottom > self.height:
                print('Game over!')
                exit()
            elif not len(self.block_list):
                print('Win!')
                exit()


if __name__ == '__main__':
    game_1 = Game()
    game_1.main()
