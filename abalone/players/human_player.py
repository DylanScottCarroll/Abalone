import pygame
import abalone
from abalone.players import Player

class HumanPlayer(Player):
    def setup(self):
        self.selected = []
    
    def get_move(self, game_state, screen, events, viewscreen_size, space_radius):
        
        #Detect player input
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #Modify the selected list based on where the key press was
                    coord = self._find_nearest_space(event.pos[0], event.pos[1], viewscreen_size, space_radius)
                    if coord is None:
                        self.selected = []
                    elif coord in self.selected:
                        self.selected.remove(coord)
                    else:
                        self.selected.append(coord)
                        if len(self.selected) > 3:
                            del self.selected[0]

            elif event.type == pygame.KEYDOWN:
                #If enter is pressed, return the selected as a tuple to make the move.
                if event.key == pygame.K_RETURN:
                    move = tuple(self.selected)
                    self.selected = []
                    return move
        
        #Draw the current state of the selection onto the board

        spacing_x = viewscreen_size[0] / 10
        spacing_y = (viewscreen_size[1]* 0.866025403784) / 10 #hardcoded sqrt(3)/2 aka sin(pi/3)
        offset_y = viewscreen_size[1] *  ((1-0.866025403784)/2)

        for i, selection in enumerate(self.selected):
            if selection is not None:
                x, y = selection
                offset_x = (5-y) * (spacing_x/2)
                draw_y = int(viewscreen_size[1] - (spacing_y * y)) - offset_y #hardcoded sqrt(3)/2 aka sin(pi/3)
                draw_x = int(spacing_x * x) + offset_x

                color = (0, 0, 255) if i==len(self.selected)-1>0 else (255, 0, 0)

                pygame.draw.circle(screen, color, (draw_x, draw_y), space_radius, int(space_radius*0.2))


        #No move was made. Wait until next frame
        return None

    def _find_nearest_space(self, m_x, m_y, viewscreen_size, space_radius):
        """Finds the nearest space to the given mouse coordinates"""
        #I know this isn't optimized, but it runs so infrequently that it would be a waste of time to optimize it at all.

        spacing_x = viewscreen_size[0] / 10
        spacing_y = (viewscreen_size[1]* 0.866025403784) / 10 #hardcoded sqrt(3)/2 aka sin(pi/3)
        offset_y = viewscreen_size[1] *  ((1-0.866025403784)/2)
        
        space = None
        for y in range(0, 11):
            for x in range(0, 11):
                
                if abalone.coord_in_board_or_edge((x, y)):
                
                    offset_x = (5-y) * (spacing_x/2)
                    draw_y = int(viewscreen_size[1] - (spacing_y * y)) - offset_y
                    draw_x = int(spacing_x * x) + offset_x

                    if (((draw_x - m_x)**2 + (draw_y - m_y)**2)**0.5) <= space_radius:
                        return (x, y)

        return None
  