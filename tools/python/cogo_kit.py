import math

class CogoKit:
    """Coordinate Geometry (COGO) Kit for navigation and surveying."""

    @staticmethod
    def distance(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate the Euclidean distance between two points."""
        return math.hypot(x2 - x1, y2 - y1)

    @staticmethod
    def bearing(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate the bearing from point 1 to point 2 in degrees (0-360)."""
        angle = math.degrees(math.atan2(x2 - x1, y2 - y1))
        return (angle + 360) % 360

    @staticmethod
    def destination(x: float, y: float, bearing_deg: float, distance: float) -> tuple[float, float]:
        """Compute the destination point given a start point, bearing, and distance."""
        angle_rad = math.radians(bearing_deg)
        x2 = x + distance * math.sin(angle_rad)
        y2 = y + distance * math.cos(angle_rad)
        return (x2, y2)

    @staticmethod
    def midpoint(x1: float, y1: float, x2: float, y2: float) -> tuple[float, float]:
        """Calculate the midpoint between two points."""
        return ((x1 + x2) / 2, (y1 + y2) / 2)

if __name__ == "__main__":
    # Example usage
    p1 = (10.0, 20.0)
    p2 = (13.0, 24.0)
    
    print(f"Point 1: {p1}")
    print(f"Point 2: {p2}")
    print(f"Distance: {CogoKit.distance(*p1, *p2):.3f}")
    print(f"Bearing: {CogoKit.bearing(*p1, *p2):.3f}°")
    
    dest_x, dest_y = CogoKit.destination(p1[0], p1[1], 45.0, 10.0)
    print(f"Destination (45°, 10 units): ({dest_x:.3f}, {dest_y:.3f})")
