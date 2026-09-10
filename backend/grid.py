class Grid:
    def __init__(self, width: int = 5, height: int = 5):
        self.width = width
        self.height = height
        self.x = 2
        self.y = 2

    def move_down(self) -> bool:
        if self.y > 0:
            self.y -= 1
            return True
        return False

    def move_up(self) -> bool:
        if self.y < self.height - 1:
            self.y += 1
            return True
        return False

    def move_left(self) -> bool:
        if self.x > 0:
            self.x -= 1
            return True
        return False

    def move_right(self) -> bool:
        if self.x < self.width - 1:
            self.x += 1
            return True
        return False

    def get_position(self) -> dict:
        return {"x": self.x, "y": self.y}