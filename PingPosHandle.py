import config


class PingArea:
    def __init__(self, topLeft=None, height=None, width=None, ping=None):
        if ping is not None:
            self.create_square_from_ping(ping)
        else:
            self.topLeft = topLeft
            self.height = height
            self.width = width

    def create_square_from_ping(self, ping):
        self.topLeft = (
            ping[0] - config.HIDER_PING_RANGE,
            ping[1] - config.HIDER_PING_RANGE,
        )
        self.height = config.HIDER_PING_RANGE * 2 + 1
        self.width = config.HIDER_PING_RANGE * 2 + 1

    def find_intersect(self, pingArea):
        topLeft = (
            max(self.topLeft[0], pingArea.topLeft[0]),
            max(self.topLeft[1], pingArea.topLeft[1]),
        )
        height = abs(min(
            self.topLeft[0] + self.height, pingArea.topLeft[0] + pingArea.height
        ) - max(self.topLeft[0], pingArea.topLeft[0]))
        width = abs(min(
            self.topLeft[1] + self.width, pingArea.topLeft[1] + pingArea.width
        ) - max(self.topLeft[1], pingArea.topLeft[1]))
        return PingArea(topLeft, height, width)

    def __str__(self):
        return f"Top Left: {self.topLeft}, Height: {self.height}, Width: {self.width}"


def final_destination(ping_list,map_data,viewable_map):
    final_top_left = PingArea(ping=ping_list[0])

    for ping in ping_list[1:]:
        final_top_left = final_top_left.find_intersect(PingArea(ping=ping))
    print(final_top_left)
    positions = []
    for x in range(final_top_left.topLeft[0], final_top_left.topLeft[0] + final_top_left.height):
        for y in range(final_top_left.topLeft[1], final_top_left.topLeft[1] + final_top_left.width):
            if map_data[x][y] != 1 and viewable_map[x][y] != True:
                positions.append((x, y))
    
    return positions
