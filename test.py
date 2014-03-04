from board import *

b = Board()
b.start()
b.display()
print b.score()
print b.can_move()
print
b.move(Board.UP)
b.display()
print
b.move(Board.UP)
b.display()
print
b.move(Board.UP)
b.display()
print
b.move(Board.RIGHT)
b.display()
print
b.move(Board.RIGHT)
b.display()
print
b.move(Board.RIGHT)
b.display()

