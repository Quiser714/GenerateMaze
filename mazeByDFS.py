import sys
from PIL import Image
from random import randint


class Node:
    def __init__(self, _x=0, _y=0) -> None:
        self.x = _x
        self.y = _y
        self.parent = None
        self.neighbors = {}
        self.neighbors['top'] = self.neighbors['below'] = self.neighbors['left'] = self.neighbors['right'] = None
        self.checked = False

    def setParent(self, n):
        self.parent = n

    def isChecked(self):
        return self.checked

    def pos(self):
        return self.x, self.y

    def getRelativePosition(self, n):
        if self.x - 1 == n.x and self.y == n.y:
            return 'top'
        elif self.x + 1 == n.x and self.y == n.y:
            return 'below'
        elif self.x == n.x and self.y - 1 == n.y:
            return 'left'
        elif self.x == n.x and self.y + 1 == n.y:
            return 'right'
        else:
            print(self.pos(), n.pos(), 'are not neighbor!')
            return None


class Maze:
    def __init__(self, _w=30, _h=30):
        self.map_w = _w
        self.map_h = _h

        self._block_size = 20  # 20*20
        self._wall_size = 5

        self.img_w = (_w + 1) * self._wall_size + _w * self._block_size
        self.img_h = (_h + 1) * self._wall_size + _h * self._block_size

        self.image = Image.new('RGB',
                               (self.img_w, self.img_h),
                               (255, 255, 255))
        self.img_arr = self.image.load()

        #self.map_arr = [[0 for _ in range(_w)] for _ in range(_h)]
        self.map_arr = []
        for i in range(_h):
            self.map_arr.append([])
            for j in range(_w):
                self.map_arr[-1].append(Node(i, j))
        self.startNode: Node = self.map_arr[0][0]
        self.endNode: Node = self.map_arr[-1][-1]

        self.InitImage()
        self.DFS()
        self.drawMapImage()
        self.drawBlock(self.startNode.pos(), (255, 0, 0))
        self.drawBlock(self.endNode.pos(), (255, 0, 0))
        self.image.save('DFS_maze.jpg')

    def InitImage(self, _color=(100, 100, 100)):
        for i in range(self.map_h+1):
            for y in range(i*(self._wall_size+self._block_size), i*(self._wall_size+self._block_size)+self._wall_size):
                for x in range(self.img_w):
                    self.img_arr[x, y] = _color
        for i in range(self.map_w+1):
            for x in range(i*(self._wall_size+self._block_size), i*(self._wall_size+self._block_size)+self._wall_size):
                for y in range(self.img_h):
                    self.img_arr[x, y] = _color

    def getReachablePos(self, p: Node):
        # Returns a list of elements with tuples
        ans = []
        for i in [(p.x-1, p.y), (p.x+1, p.y), (p.x, p.y-1), (p.x, p.y+1)]:
            if -1 in i or self.map_h == i[0] or self.map_w == i[1] or self.map_arr[i[0]][i[1]].isChecked():
                pass
            else:
                ans.append(i)
        return ans

    def DFS(self):
        cur_node: Node = self.startNode
        # id(self.startNode)==id(cur_node) -> True
        cur_node.checked = True
        not_checked_node = self.map_w * self.map_h - 1
        tmp_stack = []
        while not_checked_node > 0:
            reachable = self.getReachablePos(cur_node)
            if len(reachable) != 0:
                print(cur_node.pos(), 'now can reach', reachable)
                nextpos = reachable[randint(0, len(reachable)-1)]
                nextnode: Node = self.map_arr[nextpos[0]][nextpos[1]]
                tmp_stack.append(cur_node)
                cur_node.neighbors[cur_node.getRelativePosition(
                    nextnode)] = nextnode
                nextnode.neighbors[nextnode.getRelativePosition(
                    cur_node)] = cur_node
                nextnode.checked = True
                not_checked_node -= 1
                cur_node = nextnode
            elif len(tmp_stack) != 0:
                cur_node = tmp_stack.pop()

    def setWallSize(self, n: int):
        if type(n) == type(1) and n > 0:
            self._wall_size = n
        else:
            print('请输入一个正整数！')

    def getWallSize(self):
        return self._wall_size

    def setBlockSize(self, n: int):
        if type(n) == type(1) and n > 0:
            self._block_size = n
        else:
            print('请输入一个正整数！')

    def getBlockSize(self):
        return self._block_size

    def drawMapImage(self):
        for i in range(self.map_h):
            for j in range(self.map_w):
                if self.map_arr[i][j].neighbors['right'] != None:
                    for x in range((i+1)*self._wall_size+i*self._block_size, (i+1)*(self._wall_size+self._block_size)):
                        for y in range((j+1)*(self._wall_size+self._block_size), (j+2)*self._wall_size+(j+1)*self._block_size):
                            self.img_arr[y, x] = (255, 255, 255)
                if self.map_arr[i][j].neighbors['below'] != None:
                    for x in range((i+1)*(self._wall_size+self._block_size), (i+2)*self._wall_size+(i+1)*self._block_size):
                        for y in range((j+1)*self._wall_size+j*self._block_size, (j+1)*(self._wall_size+self._block_size)):
                            self.img_arr[y, x] = (255, 255, 255)

    def show(self):
        self.image.show()

    def drawBlock(self, pos, color):
        i, j = pos
        for y in range(i*self._block_size+i*self._wall_size, (i+1)*(self._block_size+self._wall_size)+self._wall_size):
            for x in range(j*(self._block_size+self._wall_size), (j+1)*(self._block_size+self._wall_size)+self._wall_size):
                if self.img_arr[x, y] == (255, 255, 255):
                    self.img_arr[x, y] = color


def BFS(m: Maze):
    startnode = m.startNode
    endnode = m.endNode
    openlist = []
    closelist = []
    for i in startnode.neighbors.values():
        if i != None:
            i.setParent(startnode)
            print(i.pos(), '->', startnode.pos())
            openlist.append(i)
    closelist.append(startnode)
    while True:
        if endnode in openlist:
            print('寻路完成！')
            break
        if len(openlist) == 0:
            print('找不到从起点到终点的路径')
            return
        p = openlist.pop(0)
        for i in p.neighbors.values():
            if i == None:
                continue
            if i not in closelist and i not in openlist:
                i.setParent(p)
                print(i.pos(), '->', p.pos())
                openlist.append(i)
        closelist.append(p)
    p = endnode.parent

    while p != startnode:
        m.drawBlock(p.pos(), (0, 255, 0))
        p = p.parent


if __name__ == '__main__':
    m = Maze()
    BFS(m)
    m.image.save('DFS_answer_by_BFS.jpg')
    #m.show()
