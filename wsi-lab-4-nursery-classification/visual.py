import pygame
from decisionTree import DecisionTreeNode

class VisualNode:
    def __init__(self, x, y, parent_pos, node):
        self.x = x
        self.y = y
        self.parent_pos = parent_pos
        self.node = node

class Visualization:
    """
    Class made purely for visualizing the tree
    """
    def __init__(self, WIDTH, HEIGHT, root, attributes):
        pygame.init()
        pygame.display.set_caption("Id3")
        self._width = WIDTH
        self._height = HEIGHT
        self.font = pygame.font.SysFont('Arial Black', 15)
        self._rootNode = root
        self._win = pygame.display.set_mode((WIDTH, HEIGHT))
        self._attributes = attributes
    
    def getAttribute(self, i:int) -> str:
        return self._attributes[i]
    
    def getLayers(self, node: DecisionTreeNode) -> list:
        height = 100
        layers = [[VisualNode(self._width/2, height, None, node)]]
        queue = [VisualNode(self._width/2, height, None, node)]
        i = 0
        while len(queue) != 0:
            height += 100
            layer = []

            spacing = self._width / len(layers[i])
            n = 0
            for element in queue:
                x_offset = spacing / (len(element.node.childs) + 1)
                for child in element.node.childs:
                    layer.append(VisualNode(n * spacing + x_offset, height, (element.x, element.y), child))
                    x_offset += spacing / (len(element.node.childs) + 1)
                n += 1

            layers.append(layer)
            queue = layer
            i += 1
        
        return layers    
    
    def draw(self, root: DecisionTreeNode):
        layers = self.getLayers(root)
        for layer in layers:
            for node in layer:
                # Red circle if node is Leaf
                if node.node.isLeaf:
                    pygame.draw.circle(self._win, (250, 50, 20), (node.x, node.y), 25)
                # Draw Lines
                if node.parent_pos:
                    pygame.draw.line(self._win, (80, 230, 140), (node.x, node.y - 22), (node.parent_pos[0], node.parent_pos[1] + 22))
                # Draw Green ring
                pygame.draw.circle(self._win, (80, 230, 140), (node.x, node.y), 22)
                pygame.draw.circle(self._win, (0, 0, 0), (node.x, node.y), 20)
                # If node is leaf, display the final class else display attribute that lead us to this node
                if node.node.isLeaf:
                    self.displayText(node.node.classValue, node.x, node.y, (255, 100, 100))
                else:
                    self.displayText(self.getAttribute(node.node.decidingAttr), node.x, node.y, (9, 67, 176))
                # Display the value of decisive attribute if not Leaf
                if node.node.value:
                    self.displayText(node.node.value, node.x, node.y - 30, (0, 0, 0))

    def displayText(self, my_text:str, x: int, y: int, color):
        text = self.font.render(my_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(x-1, y-1))
        self._win.blit(text, text_rect)

        text = self.font.render(my_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(x-1, y+1))
        self._win.blit(text, text_rect)

        text = self.font.render(my_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(x+1, y-1))
        self._win.blit(text, text_rect)

        text = self.font.render(my_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(x+1, y+1))
        self._win.blit(text, text_rect)

        text = self.font.render(my_text, True, color)
        text_rect = text.get_rect(center=(x, y))
        self._win.blit(text, text_rect)
    
    def show(self):
        run = True
        self.draw(self._rootNode)
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()
        pygame.quit()