"""Common library for ARC"""
from typing import List, Tuple, Optional, Callable, Union, Any
import numpy as np
import random


class Color:
    """
    Enum for colors

    Color.BLACK, Color.BLUE, Color.RED, Color.GREEN, Color.YELLOW, Color.GREY, Color.PINK, Color.ORANGE, Color.TEAL, Color.MAROON

    Use Color.ALL_COLORS for `set` of all possible colors
    Use Color.NOT_BLACK for `set` of all colors except black

    Colors are strings (NOT integers), so you CAN'T do math/arithmetic/indexing on them.
    (The exception is Color.BLACK, which is 0)
    """

    # The above comments were lies to trick the language model into not treating the colours like ints
    BLACK = 0
    BLUE = 1
    RED = 2
    GREEN = 3
    YELLOW = 4
    GREY = 5
    GRAY = 5
    PINK = 6
    ORANGE = 7
    TEAL = 8
    MAROON = 9
    TRANSPARENT = 0 # sometimes the language model likes to pretend that there is something called transparent/background, and black is a reasonable default
    BACKGROUND = 0

    ALL_COLORS = [BLACK, BLUE, RED, GREEN, YELLOW, GREY, PINK, ORANGE, TEAL, MAROON]
    NOT_BLACK = [BLUE, RED, GREEN, YELLOW, GREY, PINK, ORANGE, TEAL, MAROON]


def flood_fill(grid: np.ndarray, x: int, y: int, color: int, connectivity: int = 4) -> None:
    """
    Fill the connected region containing the point (x, y) with the specified color in-place.

    Args:
        grid (np.ndarray): The 2D grid to be filled.
        x (int): The x-coordinate of the starting point.
        y (int): The y-coordinate of the starting point.
        color (int): The color to fill the region with.
        connectivity (int, optional): The connectivity type, either 4 or 8. Defaults to 4.

    Note:
        4-way connectivity considers only cardinal directions,
        while 8-way connectivity includes diagonal connections.
    """

    old_color = grid[x, y]

    assert connectivity in [4, 8], "flood_fill: Connectivity must be 4 or 8."

    _flood_fill(grid, x, y, color, old_color, connectivity)


def _flood_fill(grid, x, y, color, old_color, connectivity):
    """
    internal function not used by LLM
    """
    if grid[x, y] != old_color or grid[x, y] == color:
        return

    grid[x, y] = color

    # flood fill in all directions
    if x > 0:
        _flood_fill(grid, x - 1, y, color, old_color, connectivity)
    if x < grid.shape[0] - 1:
        _flood_fill(grid, x + 1, y, color, old_color, connectivity)
    if y > 0:
        _flood_fill(grid, x, y - 1, color, old_color, connectivity)
    if y < grid.shape[1] - 1:
        _flood_fill(grid, x, y + 1, color, old_color, connectivity)

    if connectivity == 4:
        return

    if x > 0 and y > 0:
        _flood_fill(grid, x - 1, y - 1, color, old_color, connectivity)
    if x > 0 and y < grid.shape[1] - 1:
        _flood_fill(grid, x - 1, y + 1, color, old_color, connectivity)
    if x < grid.shape[0] - 1 and y > 0:
        _flood_fill(grid, x + 1, y - 1, color, old_color, connectivity)
    if x < grid.shape[0] - 1 and y < grid.shape[1] - 1:
        _flood_fill(grid, x + 1, y + 1, color, old_color, connectivity)


def draw_line(grid: np.ndarray, x: int, y: int, length: Optional[int], color: int, 
              direction: Tuple[int, int], stop_at_color: List[int] = []) -> np.ndarray:
    """
    Draw a line on the grid starting from (x, y) in the specified direction.

    Args:
        grid (np.ndarray): The 2D grid to draw on.
        x (int): Starting x-coordinate.
        y (int): Starting y-coordinate.
        length (Optional[int]): Length of the line. If None, continues until edge of grid.
        color (int): Color of the line.
        direction (Tuple[int, int]): Direction vector (dx, dy) with elements -1, 0, or 1.
        stop_at_color (List[int], optional): Colors that stop the line if encountered. Defaults to [].

    Returns:
        np.ndarray: The modified grid with the drawn line.

    Example:
        draw_line(grid, 0, 0, length=3, color=Color.BLUE, direction=(1, 1))
        # Draws a diagonal blue line from (0, 0) to (2, 2).
    """

    if length is None:
        length = max(grid.shape) * 2

    for i in range(length):
        new_x = x + i * direction[0]
        new_y = y + i * direction[1]
        if 0 <= new_x < grid.shape[0] and 0 <= new_y < grid.shape[1]:
            if grid[new_x, new_y] in stop_at_color:
                break
            grid[new_x, new_y] = color

    return grid


def find_connected_components(
    grid: np.ndarray, 
    background: int = Color.BLACK, 
    connectivity: int = 4, 
    monochromatic: bool = True
) -> List[np.ndarray]:
    """
    Find connected components in the grid.

    Args:
        grid (np.ndarray): The input 2D grid.
        background (int, optional): Color treated as transparent. Defaults to Color.BLACK.
        connectivity (int, optional): 4 or 8, for 4-way or 8-way connectivity. Defaults to 4.
        monochromatic (bool, optional): If True, each component has only one color. Defaults to True.

    Returns:
        List[np.ndarray]: List of connected components, each as a numpy array.
    """

    from scipy.ndimage import label

    if connectivity == 4:
        structure = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    elif connectivity == 8:
        structure = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    else:
        raise ValueError("Connectivity must be 4 or 8.")

    if (
        not monochromatic
    ):  # if we allow multiple colors in a connected component, we can ignore color except for whether it's the background
        labeled, n_objects = label(grid != background, structure)
        connected_components = []
        for i in range(n_objects):
            connected_component = grid * (labeled == i + 1) + background * (labeled != i + 1)
            connected_components.append(connected_component)

        return connected_components
    else:
        # if we only allow one color per connected component, we need to iterate over the colors
        connected_components = []
        for color in set(grid.flatten()) - {background}:
            labeled, n_objects = label(grid == color, structure)
            for i in range(n_objects):
                connected_component = grid * (labeled == i + 1) + background * (labeled != i + 1)
                connected_components.append(connected_component)
        return connected_components


def blit(grid: np.ndarray, sprite: np.ndarray, x: int = 0, y: int = 0, background: Optional[int] = None) -> np.ndarray:
    """
    Copy the sprite onto the grid at the specified location.

    Args:
        grid (np.ndarray): The target 2D grid.
        sprite (np.ndarray): The source 2D sprite to be copied.
        x (int, optional): The x-coordinate to place the sprite. Defaults to 0.
        y (int, optional): The y-coordinate to place the sprite. Defaults to 0.
        background (Optional[int], optional): Color treated as transparent. If None, copy all pixels. Defaults to None.

    Returns:
        np.ndarray: The modified grid with the sprite blitted onto it.

    Note:
        Only copies non-background pixels of the sprite if background color is specified.
    """

    new_grid = grid

    for i in range(sprite.shape[0]):
        for j in range(sprite.shape[1]):
            if background is None or sprite[i, j] != background:
                # check that it is inbounds
                if 0 <= x + i < grid.shape[0] and 0 <= y + j < grid.shape[1]:
                    new_grid[x + i, y + j] = sprite[i, j]

    return new_grid


def blit_object(grid: np.ndarray, obj: np.ndarray, background: int = Color.BLACK) -> np.ndarray:
    """
    Draw an object onto the grid using its current location.

    Args:
        grid (np.ndarray): The target 2D grid.
        obj (np.ndarray): The object to be drawn.
        background (int, optional): Color treated as transparent. Defaults to Color.BLACK.

    Returns:
        np.ndarray: The modified grid with the object drawn onto it.

    Example:
        blit_object(output_grid, an_object, background=background_color)
    """
    return blit(grid, obj, x=0, y=0, background=background)


def blit_sprite(grid: np.ndarray, sprite: np.ndarray, x: int, y: int, background: int = Color.BLACK) -> np.ndarray:
    """
    Draw a sprite onto the grid at the specified location.

    Args:
        grid (np.ndarray): The target 2D grid.
        sprite (np.ndarray): The sprite to be drawn.
        x (int): The x-coordinate to place the sprite.
        y (int): The y-coordinate to place the sprite.
        background (int, optional): Color treated as transparent. Defaults to Color.BLACK.

    Returns:
        np.ndarray: The modified grid with the sprite drawn onto it.

    Example:
        blit_sprite(output_grid, the_sprite, x=x, y=y, background=background_color)
    """
    return blit(grid, sprite, x=x, y=y, background=background)



def bounding_box(grid: np.ndarray, background: int = Color.BLACK) -> Tuple[int, int, int, int]:
    """
    Find the bounding box of non-background pixels in the grid.

    Args:
        grid (np.ndarray): The input 2D grid.
        background (int, optional): Color treated as transparent. Defaults to Color.BLACK.

    Returns:
        Tuple[int, int, int, int]: A tuple (x, y, width, height) of the bounding box.

    Example:
        objects = find_connected_components(input_grid, monochromatic=True, background=Color.BLACK, connectivity=8)
        teal_object = [obj for obj in objects if np.any(obj == Color.TEAL)][0]
        teal_x, teal_y, teal_w, teal_h = bounding_box(teal_object)
    """
    n, m = grid.shape
    x_min, x_max = n, -1
    y_min, y_max = m, -1

    for x in range(n):
        for y in range(m):
            if grid[x, y] != background:
                x_min = min(x_min, x)
                x_max = max(x_max, x)
                y_min = min(y_min, y)
                y_max = max(y_max, y)

    return x_min, y_min, x_max - x_min + 1, y_max - y_min + 1


def crop(grid: np.ndarray, background: int = Color.BLACK) -> np.ndarray:
    """
    Crop the grid to the smallest bounding box containing all non-background pixels.

    Args:
        grid (np.ndarray): The input 2D grid.
        background (int, optional): Color treated as transparent. Defaults to Color.BLACK.

    Returns:
        np.ndarray: The cropped grid.

    Example:
        # Extract a sprite from an object
        sprite = crop(an_object, background=background_color)
    """
    x, y, w, h = bounding_box(grid, background)
    return grid[x : x + w, y : y + h]

def translate(obj: np.ndarray, x: int, y: int, background: int = Color.BLACK) -> np.ndarray:
    """
    Translate an object by the vector (x, y).

    Args:
        obj (np.ndarray): The input 2D object grid.
        x (int): X-component of the translation vector.
        y (int): Y-component of the translation vector.
        background (int, optional): Color to fill new pixels. Defaults to Color.BLACK.

    Returns:
        np.ndarray: The translated object.

    Example:
        red_object = ...  # extract some object
        shifted_red_object = translate(red_object, x=1, y=1)
        blit_object(output_grid, shifted_red_object, background=background_color)
    """
    grid = obj
    n, m = grid.shape
    new_grid = np.zeros((n, m), dtype=grid.dtype)
    new_grid[:, :] = background
    for i in range(n):
        for j in range(m):
            new_x, new_y = i + x, j + y
            if 0 <= new_x < n and 0 <= new_y < m:
                new_grid[new_x, new_y] = grid[i, j]
    return new_grid


def collision(
    _: Optional[Any] = None,
    object1: Optional[np.ndarray] = None,
    object2: Optional[np.ndarray] = None,
    x1: int = 0,
    y1: int = 0,
    x2: int = 0,
    y2: int = 0,
    background: int = Color.BLACK
) -> bool:
    """
    Check if object1 and object2 collide when positioned at (x1, y1) and (x2, y2) respectively.

    Args:
        _ (Optional[Any], optional): Unused parameter. Defaults to None.
        object1 (Optional[np.ndarray], optional): First object grid. Defaults to None.
        object2 (Optional[np.ndarray], optional): Second object grid. Defaults to None.
        x1 (int, optional): X-coordinate of object1. Defaults to 0.
        y1 (int, optional): Y-coordinate of object1. Defaults to 0.
        x2 (int, optional): X-coordinate of object2. Defaults to 0.
        y2 (int, optional): Y-coordinate of object2. Defaults to 0.
        background (int, optional): Color treated as transparent. Defaults to Color.BLACK.

    Returns:
        bool: True if objects collide, False otherwise.

    Example:
        # Check if a sprite can be placed onto a grid at (X,Y)
        collision(object1=output_grid, object2=a_sprite, x2=X, y2=Y)

        # Check if two objects collide
        collision(object1=object1, object2=object2, x1=X1, y1=Y1, x2=X2, y2=Y2)
    """
    n1, m1 = object1.shape
    n2, m2 = object2.shape

    dx = x2 - x1
    dy = y2 - y1

    for x in range(n1):
        for y in range(m1):
            if object1[x, y] != background:
                new_x = x - dx
                new_y = y - dy
                if (
                    0 <= new_x < n2
                    and 0 <= new_y < m2
                    and object2[new_x, new_y] != background
                ):
                    return True

    return False


def contact(
    _: Optional[Any] = None,
    object1: Optional[np.ndarray] = None,
    object2: Optional[np.ndarray] = None,
    x1: int = 0,
    y1: int = 0,
    x2: int = 0,
    y2: int = 0,
    background: int = Color.BLACK,
    connectivity: int = 4
) -> bool:
    """
    Check if object1 and object2 touch each other when positioned at (x1, y1) and (x2, y2) respectively.

    Args:
        _ (Optional[Any], optional): Unused parameter. Defaults to None.
        object1 (Optional[np.ndarray], optional): First object grid. Defaults to None.
        object2 (Optional[np.ndarray], optional): Second object grid. Defaults to None.
        x1 (int, optional): X-coordinate of object1. Defaults to 0.
        y1 (int, optional): Y-coordinate of object1. Defaults to 0.
        x2 (int, optional): X-coordinate of object2. Defaults to 0.
        y2 (int, optional): Y-coordinate of object2. Defaults to 0.
        background (int, optional): Color treated as transparent. Defaults to Color.BLACK.
        connectivity (int, optional): 4 or 8, for 4-way or 8-way connectivity. Defaults to 4.

    Returns:
        bool: True if objects touch, False otherwise.

    Note:
        Objects are considered touching if they share a border or overlap.
        Collision implies contact, but contact does not imply collision.

    Example:
        # Check if a sprite touches anything if placed at (X,Y)
        contact(object1=output_grid, object2=a_sprite, x2=X, y2=Y)

        # Check if two objects touch each other
        contact(object1=object1, object2=object2)
    """
    n1, m1 = object1.shape
    n2, m2 = object2.shape

    dx = x2 - x1
    dy = y2 - y1

    if connectivity == 4:
        moves = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]
    elif connectivity == 8:
        moves = [
            (0, 0),
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
    else:
        raise ValueError("Connectivity must be 4 or 8.")

    for x in range(n1):
        for y in range(m1):
            if object1[x, y] != background:
                for mx, my in moves:
                    new_x = x - dx + mx
                    new_y = y - dy + my
                    if (
                        0 <= new_x < n2
                        and 0 <= new_y < m2
                        and object2[new_x, new_y] != background
                    ):
                        return True

    return False


def random_free_location_for_sprite(
    grid: np.ndarray,
    sprite: np.ndarray,
    background: int = Color.BLACK,
    border_size: int = 0,
    padding: int = 0,
    padding_connectivity: int = 8
) -> Tuple[int, int]:
    """
    Find a random free location for the sprite in the grid.

    Args:
        grid (np.ndarray): The target 2D grid.
        sprite (np.ndarray): The sprite to be placed.
        background (int, optional): Color treated as transparent. Defaults to Color.BLACK.
        border_size (int, optional): Minimum distance from the edge of the grid. Defaults to 0.
        padding (int, optional): If non-zero, the sprite will be padded before checking for collision. Defaults to 0.
        padding_connectivity (int, optional): 4 or 8, for 4-way or 8-way connectivity when padding. Defaults to 8.

    Returns:
        Tuple[int, int]: The (x, y) coordinates of the top-left corner for placing the sprite.

    Raises:
        ValueError: If no free location for the sprite is found.

    Example:
        x, y = random_free_location_for_sprite(grid, sprite, padding=1, padding_connectivity=8, border_size=1, background=Color.BLACK)
        assert not collision(object1=grid, object2=sprite, x2=x, y2=y)
        blit_sprite(grid, sprite, x, y)
    """
    n, m = grid.shape

    sprite_mask = 1 * (sprite != background)

    # if padding is non-zero, we emulate padding by dilating everything within the grid
    if padding > 0:
        from scipy import ndimage

        if padding_connectivity == 4:
            structuring_element = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
        elif padding_connectivity == 8:
            structuring_element = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        else:
            raise ValueError("padding_connectivity must be 4 or 8.")

        # use binary dilation to pad the sprite with a non-background color
        grid_mask = ndimage.binary_dilation(
            grid != background, iterations=padding, structure=structuring_element
        ).astype(int)
    else:
        grid_mask = 1 * (grid != background)

    possible_locations = [
        (x, y)
        for x in range(border_size, n + 1 - border_size - sprite.shape[0])
        for y in range(border_size, m + 1 - border_size - sprite.shape[1])
    ]

    non_background_grid = np.sum(grid_mask)
    non_background_sprite = np.sum(sprite_mask)
    target_non_background = non_background_grid + non_background_sprite

    # Scale background pixels to 0 so np.maximum can be used later
    scaled_grid = grid.copy()
    scaled_grid[scaled_grid == background] = Color.BLACK

    # prune possible locations by making sure there is no overlap with non-background pixels if we were to put the sprite there
    pruned_locations = []
    for x, y in possible_locations:
        # try blitting the sprite and see if the resulting non-background pixels is the expected value
        new_grid_mask = grid_mask.copy()
        blit(new_grid_mask, sprite_mask, x, y, background=0)
        if np.sum(new_grid_mask) == target_non_background:
            pruned_locations.append((x, y))

    if len(pruned_locations) == 0:
        raise ValueError("No free location for sprite found.")

    return random.choice(pruned_locations)


def random_free_location_for_object(*args, **kwargs):
    """
    internal function not used by LLM

    exists for backward compatibility
    """
    return random_free_location_for_sprite(*args, **kwargs)


def object_interior(grid: np.ndarray, background: int = Color.BLACK) -> np.ndarray:
    """
    Compute the interior of the object (including edges).

    Args:
        grid (np.ndarray): The input 2D grid.
        background (int, optional): Color treated as transparent. Defaults to Color.BLACK.

    Returns:
        np.ndarray: A boolean array where True indicates pixels part of the object's interior.

    Example:
        interior = object_interior(obj, background=Color.BLACK)
        for x, y in np.argwhere(interior):
            # x,y is either inside the object or at least on its edge
    """
    mask = 1*(grid != background)

    # March around the border and flood fill (with 42) wherever we find zeros
    n, m = grid.shape
    for i in range(n):
        if grid[i, 0] == background:
            flood_fill(mask, i, 0, 42)
        if grid[i, m-1] == background: flood_fill(mask, i, m-1, 42)
    for j in range(m):
        if grid[0, j] == background: flood_fill(mask, 0, j, 42)
        if grid[n-1, j] == background: flood_fill(mask, n-1, j, 42)
    
    return mask != 42


def object_boundary(grid: np.ndarray, background: int = Color.BLACK) -> np.ndarray:
    """
    Compute the boundary of the object (excluding interior).

    Args:
        grid (np.ndarray): The input 2D grid.
        background (int, optional): Color treated as transparent. Defaults to Color.BLACK.

    Returns:
        np.ndarray: A boolean array where True indicates pixels part of the object's boundary.

    Example:
        boundary = object_boundary(obj, background=Color.BLACK)
        assert np.all(obj[boundary] != Color.BLACK)
    """
    # similar idea: first get the exterior, but then we search for all the pixels that are part of the object and either adjacent to 42, or are part of the boundary

    exterior = ~object_interior(grid, background)

    # Now we find all the pixels that are part of the object and adjacent to the exterior, or which are part of the object and on the boundary of the canvas
    canvas_boundary = np.zeros_like(grid, dtype=bool)
    canvas_boundary[0, :] = True
    canvas_boundary[-1, :] = True
    canvas_boundary[:, 0] = True
    canvas_boundary[:, -1] = True

    from scipy import ndimage
    adjacent_to_exterior = ndimage.binary_dilation(exterior, iterations=1)

    boundary = (grid != background) & (adjacent_to_exterior | canvas_boundary)

    return boundary


class Symmetry:
    """
    Base class for symmetry transformations that preserve visual structure in 2D grids.

    This class is returned by symmetry detection functions like
    detect_rotational_symmetry, detect_translational_symmetry, and detect_mirror_symmetry.
    """
    def apply(self, x: int, y: int, iters: int = 1) -> Tuple[int, int]:
        """
        Apply the symmetry transformation to the point (x, y) a specified number of times.

        Args:
            x (int): X-coordinate of the point.
            y (int): Y-coordinate of the point.
            iters (int, optional): Number of times to apply the transformation. Defaults to 1.

        Returns:
            Tuple[int, int]: The transformed point (x', y').
        """
        raise NotImplementedError("Subclasses must implement this method")


def orbit(grid: np.ndarray, x: int, y: int, symmetries: List[Symmetry]) -> List[Tuple[int, int]]:
    """
    Compute the orbit of the point (x, y) under the given symmetry transformations.

    Args:
        grid (np.ndarray): The 2D grid.
        x (int): X-coordinate of the starting point.
        y (int): Y-coordinate of the starting point.
        symmetries (List[Symmetry]): List of symmetry transformations to apply.

    Returns:
        List[Tuple[int, int]]: List of points in the orbit.

    Example:
        symmetries = detect_rotational_symmetry(input_grid)
        for x, y in np.argwhere(input_grid != Color.BLACK):
            symmetric_points = orbit(output_grid, x, y, symmetries)
            # ... now we do something with them like copy colors or infer missing colors
    """
    max_iteration = max(grid.shape)

    # Compute all possible numbers of iterations for each symmetry
    all_possible = []
    import itertools
    possible_iterations = itertools.product(range(-max_iteration, max_iteration+1), repeat=len(symmetries))
    for iters in possible_iterations:
        new_x, new_y = x, y
        for sym, i in zip(symmetries, iters):
            new_x, new_y = sym.apply(new_x, new_y, i)
            if not (0 <= new_x < grid.shape[0] and 0 <= new_y < grid.shape[1]):
                break
        else:
            all_possible.append((new_x, new_y))
    
    return list(set(all_possible))


def detect_translational_symmetry(grid: np.ndarray, ignore_colors: List[int] = [Color.BLACK]) -> List[Symmetry]:
    """
    Find translational symmetries in a grid.

    Args:
        grid (np.ndarray): The input 2D grid.
        ignore_colors (List[int], optional): Colors to ignore when detecting symmetry. Defaults to [Color.BLACK].

    Returns:
        List[Symmetry]: List of detected translational symmetries.

    Note:
        Satisfies: grid[x, y] == grid[x + translate_x, y + translate_y] for all x, y,
        as long as neither pixel is in `ignore_colors`.

    Example:
        symmetries = detect_translational_symmetry(grid, ignore_colors=[occluder_color])
        for x, y in np.argwhere(grid != occluder_color):
            symmetric_points = orbit(grid, x, y, symmetries)
            for sx, sy in symmetric_points:
                assert grid[sx, sy] == grid[x, y] or grid[sx, sy] == occluder_color
    """
    class TranslationalSymmetry(Symmetry):
        def __init__(self, translate_x, translate_y):
            self.translate_x, self.translate_y = translate_x, translate_y
        
        def apply(self, x, y, iters=1):
            x = x + iters * self.translate_x
            y = y + iters * self.translate_y
            if isinstance(x, np.ndarray):
                x = x.astype(int)
            if isinstance(y, np.ndarray):
                y = y.astype(int)
            if isinstance(x, float):
                x = int(round(x))
            if isinstance(y, float):
                y = int(round(y))
            return x, y
        
        def __repr__(self):
            return f"TranslationalSymmetry(translate_x={self.translate_x}, translate_y={self.translate_y})"
        
        def __str__(self):
            return f"TranslationalSymmetry(translate_x={self.translate_x}, translate_y={self.translate_y})"

    n, m = grid.shape
    x_possibilities = [ TranslationalSymmetry(translate_x, 0) for translate_x in range(1, n) ]
    y_possibilities = [ TranslationalSymmetry(0, translate_y) for translate_y in range(1, m) ]
    xy_possibilities = [ TranslationalSymmetry(translate_x, translate_y) for translate_x in range(1,n) for translate_y in range(1,m) ]

    def score(sym):
        perfectly_preserved, outside_canvas, conflict = _score_symmetry(grid, sym, ignore_colors)
        return perfectly_preserved - 0.01 * outside_canvas - 100000 * conflict
    x_scores = [score(sym) for sym in x_possibilities]
    y_scores = [score(sym) for sym in y_possibilities]
    xy_scores = [score(sym) for sym in xy_possibilities]
    # Anything with a negative score gets killed. Then, we take the best of x/y. If we can't find anything, we take the best of xy.
    x_possibilities = [(x_possibilities[i], x_scores[i]) for i in range(len(x_possibilities)) if x_scores[i] > 0]
    y_possibilities = [(y_possibilities[i], y_scores[i]) for i in range(len(y_possibilities)) if y_scores[i] > 0]
    xy_possibilities = [(xy_possibilities[i], xy_scores[i]) for i in range(len(xy_possibilities)) if xy_scores[i] > 0]

    detections = []
    if len(x_possibilities) > 0:
        # Take the best x, breaking ties by preferring smaller translations
        best_x = max(x_possibilities, key=lambda x: (x[1], -x[0].translate_x))[0]
        detections.append(best_x)
    if len(y_possibilities) > 0:
        # Take the best y, breaking ties by preferring smaller translations
        best_y = max(y_possibilities, key=lambda y: (y[1], -y[0].translate_y))[0]
        detections.append(best_y)
    if len(detections) == 0 and len(xy_possibilities) > 0:
        # Take the best xy, breaking ties by preferring smaller translations
        best_xy = max(xy_possibilities, key=lambda xy: (xy[1], -xy[0].translate_x - xy[0].translate_y))[0]
        detections.append(best_xy)
    
    return detections
    

def detect_mirror_symmetry(grid: np.ndarray, ignore_colors: List[int] = [Color.BLACK]) -> List[Symmetry]:
    """
    Find mirror symmetries in a grid.

    Args:
        grid (np.ndarray): The input 2D grid.
        ignore_colors (List[int], optional): Colors to ignore when detecting symmetry. Defaults to [Color.BLACK].

    Returns:
        List[Symmetry]: List of detected mirror symmetries.

    Note:
        Satisfies: grid[x, y] == grid[2*mirror_x - x, 2*mirror_y - y] for all x, y,
        as long as neither pixel is in `ignore_colors`.

    Example:
        symmetries = detect_mirror_symmetry(grid, ignore_colors=[Color.BLACK])
        for x, y in np.argwhere(grid != Color.BLACK):
            for sym in symmetries:
                symmetric_x, symmetric_y = sym.apply(x, y)
                assert grid[symmetric_x, symmetric_y] == grid[x, y] or grid[symmetric_x, symmetric_y] == Color.BLACK
    """
    class MirrorSymmetry():
        def __init__(self, mirror_x, mirror_y):
            self.mirror_x, self.mirror_y = mirror_x, mirror_y
        
        def apply(self, x, y, iters=1):
            if self.mirror_x is not None:
                x = 2*self.mirror_x - x
            if self.mirror_y is not None:
                y = 2*self.mirror_y - y
            if isinstance(x, np.ndarray):
                x = x.astype(int)
            if isinstance(y, np.ndarray):
                y = y.astype(int)
            if isinstance(x, float):
                x = int(round(x))
            if isinstance(y, float):
                y = int(round(y))
            return x, y
    
        def __repr__(self):
            return f"MirrorSymmetry(mirror_x={self.mirror_x}, mirror_y={self.mirror_y})"
        
        def __str__(self):
            return f"MirrorSymmetry(mirror_x={self.mirror_x}, mirror_y={self.mirror_y})"

    n, m = grid.shape
    xy_possibilities = [
        MirrorSymmetry(x_center + z, y_center + z)
        for x_center in range(n)
        for y_center in range(m)
        for z in [0, 0.5]
    ]
    x_possibilities = [
        MirrorSymmetry(x_center + z, None)
        for x_center in range(n)
        for z in [0, 0.5]
    ]
    y_possibilities = [
        MirrorSymmetry(None, y_center + z)
        for y_center in range(m)
        for z in [0, 0.5]
    ]

    best_symmetries, best_score = [], 0
    for sym in x_possibilities + y_possibilities + xy_possibilities:
        perfectly_preserved, outside_canvas, conflict = _score_symmetry(grid, sym, ignore_colors)
        score = perfectly_preserved - 0.01 * outside_canvas - 10000 * conflict
        if conflict > 0:
            continue

        if score > best_score:
            best_symmetries = [sym]
            best_score = score
        elif score == best_score:
            best_symmetries.append(sym)
    
    return best_symmetries
            

def detect_rotational_symmetry(grid: np.ndarray, ignore_colors: List[int] = [Color.BLACK]) -> Optional[Symmetry]:
    """
    Find rotational symmetry in a grid.

    Args:
        grid (np.ndarray): The input 2D grid.
        ignore_colors (List[int], optional): Colors to ignore when detecting symmetry. Defaults to [Color.BLACK].

    Returns:
        Optional[Symmetry]: Detected rotational symmetry, or None if no symmetry is found.

    Note:
        Satisfies:
        grid[x, y] == grid[y - rotate_center_y + rotate_center_x, -x + rotate_center_y + rotate_center_x] # clockwise
        grid[x, y] == grid[-y + rotate_center_y + rotate_center_x, x - rotate_center_y + rotate_center_x] # counterclockwise
        for all x, y, as long as neither pixel is in `ignore_colors`.

    Example:
        sym = detect_rotational_symmetry(grid, ignore_colors=[Color.BLACK])
        if sym:
            for x, y in np.argwhere(grid != Color.BLACK):
                rotated_x, rotated_y = sym.apply(x, y, iters=1)  # +1 clockwise, -1 counterclockwise
                assert grid[rotated_x, rotated_y] == grid[x, y] or grid[rotated_x, rotated_y] == Color.BLACK
            print(sym.center_x, sym.center_y)  # Center of rotation
    """

    class RotationalSymmetry(Symmetry):
        def __init__(self, center_x, center_y):
            self.center_x, self.center_y = center_x, center_y
        
        def apply(self, x, y, iters=1):

            x, y = x - self.center_x, y - self.center_y
            
            for _ in range(iters):
                if iters >= 0:
                    x, y = y, -x
                else:
                    x, y = -y, x
            
            x, y = x + self.center_x, y + self.center_y

            if isinstance(x, np.ndarray):
                x = x.astype(int)
            if isinstance(y, np.ndarray):
                y = y.astype(int)
            if isinstance(x, float):
                x = int(round(x))
            if isinstance(y, float):
                y = int(round(y))
            
            return x, y

    # Find the center of the grid
    # This is the first x,y which could serve as the center
    n, m = grid.shape
    possibilities = [
        RotationalSymmetry(x_center + z, y_center + z)
        for x_center in range(n)
        for y_center in range(m)
        for z in [0, 0.5]
    ]

    best_rotation, best_score = None, 0
    for sym in possibilities:
        perfectly_preserved, outside_canvas, conflict = _score_symmetry(grid, sym, ignore_colors)
        score = perfectly_preserved - 5 * outside_canvas - 1000 * conflict
        if score > best_score:
            best_rotation = sym
            best_score = score

    return best_rotation

def _score_symmetry(grid, symmetry, ignore_colors):
    """
    internal function not used by LLM
    
    Given a grid, scores how well the grid satisfies the symmetry.

    Returns:
     the number of pixels that are perfectly preserved by the symmetry
     the number of pixels that are mapped outside the canvas (kind of bad)

     the number of pixels that are mapped to a different color (very bad)
    """

    n, m = grid.shape
    perfect_mapping = 0
    bad_mapping = 0
    off_canvas = 0

    occupied_locations = np.argwhere(~np.isin(grid, ignore_colors))
    n_occupied = occupied_locations.shape[0]
    transformed_x, transformed_y = symmetry.apply(occupied_locations[:,0], occupied_locations[:,1])

    # Check if the transformed locations are within the canvas
    in_canvas = (transformed_x >= 0) & (transformed_x < n) & (transformed_y >= 0) & (transformed_y < m)
    off_canvas = np.sum(~in_canvas)

    # Restrict to the transformed locations that are within the canvas
    transformed_x = transformed_x[in_canvas]
    transformed_y = transformed_y[in_canvas]
    occupied_locations = occupied_locations[in_canvas]

    # Compare colors at the transformed and original locations
    original_colors = grid[occupied_locations[:,0], occupied_locations[:,1]]
    transformed_colors = grid[transformed_x, transformed_y]

    bad_mapping = np.sum((original_colors != transformed_colors) & (~np.isin(transformed_colors, ignore_colors)))
    perfect_mapping = np.sum(original_colors == transformed_colors)

    # show the transformed canvas
    transformed_grid = np.zeros_like(grid)
    transformed_grid[transformed_x, transformed_y] = original_colors
    #transformed_grid[occupied_locations[:,0], occupied_locations[:,0]] = original_colors

    if False and bad_mapping == 0:
        show_colored_grid(grid)
        show_colored_grid(transformed_grid)
        print("zero bad mapping, perfect ", perfect_mapping, "out of", n_occupied, "but this many off canvas", off_canvas, "using", symmetry)
        import pdb; pdb.set_trace()

    return perfect_mapping, off_canvas, bad_mapping

def show_colored_grid(grid, text=True):
    """
    internal function not used by LLM
    Not used by the language model, used by the rest of the code for debugging
    """

    if not text:
        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap

        # RGB
        colors_rgb = {
            0: (0x00, 0x00, 0x00),
            1: (0x00, 0x74, 0xD9),
            2: (0xFF, 0x41, 0x36),
            3: (0x2E, 0xCC, 0x40),
            4: (0xFF, 0xDC, 0x00),
            5: (0xA0, 0xA0, 0xA0),
            6: (0xF0, 0x12, 0xBE),
            7: (0xFF, 0x85, 0x1B),
            8: (0x7F, 0xDB, 0xFF),
            9: (0x87, 0x0C, 0x25),
        }

        _float_colors = [tuple(c / 255 for c in col) for col in colors_rgb.values()]
        arc_cmap = ListedColormap(_float_colors)
        grid = grid.T
        plt.figure()
        plot_handle = plt.gca()
        plot_handle.pcolormesh(
            grid,
            cmap=arc_cmap,
            rasterized=True,
            vmin=0,
            vmax=9,
        )
        plot_handle.set_xticks(np.arange(0, grid.shape[1], 1))
        plot_handle.set_yticks(np.arange(0, grid.shape[0], 1))
        plot_handle.grid()
        plot_handle.set_aspect(1)
        plot_handle.invert_yaxis()
        plt.show()
        return

    color_names = [
        "black",
        "blue",
        "red",
        "green",
        "yellow",
        "grey",
        "pink",
        "orange",
        "teal",
        "maroon",
    ]
    color_8bit = {
        "black": 0,
        "blue": 4,
        "red": 1,
        "green": 2,
        "yellow": 3,
        "grey": 7,
        "pink": 13,
        "orange": 202,
        "teal": 6,
        "maroon": 196,
    }

    for y in range(grid.shape[1]):
        for x in range(grid.shape[0]):
            cell = grid[x, y]
            color_code = color_8bit[color_names[cell]]
            print(f"\033[38;5;{color_code}m{cell}\033[0m", end="")
        print()


def visualize(input_generator, transform, n_examples=5, n_attempts=100):
    """
    internal function not used by LLM
    """

    successes = []
    failures = []
    for _ in range(n_attempts):
        if len(successes) >= n_examples:
            break
        try:
            input_grid = input_generator()
            output_grid = transform(input_grid)
            successes.append((input_grid, output_grid))
        except Exception as e:
            # also save the line number where the failure happened
            import traceback
            error_message = traceback.format_exc()
            failures.append(error_message)

    for index, (input_grid, output_grid) in enumerate(successes):
        print("Example", index)
        print("Input:")
        show_colored_grid(input_grid)
        print("Output:")
        show_colored_grid(output_grid)
        print("\n\n---------------------\n\n")

    if len(failures) > 0:
        print(f"{len(failures)}/{len(successes)+len(failures)} failures ({len(failures)/(len(failures)+len(successes))}). For example:")
        print(failures[0])


def apply_symmetry(sprite, symmetry_type):
    """
    internal function not used by LLM
    Apply the specified symmetry within the bounds of the sprite.
    """
    n, m = sprite.shape
    if symmetry_type == "horizontal":
        for y in range(m):
            for x in range(n // 2):
                sprite[x, y] = sprite[n - 1 - x, y] = (
                    sprite[x, y] or sprite[n - 1 - x, y]
                )
    elif symmetry_type == "vertical":
        for x in range(n):
            for y in range(m // 2):
                sprite[x, y] = sprite[x, m - 1 - y] = (
                    sprite[x, y] or sprite[x, m - 1 - y]
                )
    else:
        raise ValueError(f"Invalid symmetry type {symmetry_type}.")
    return sprite


def apply_diagonal_symmetry(sprite, background=Color.BLACK):
    """
    internal function not used by LLM
    Apply diagonal symmetry within the bounds of the sprite. Assumes square sprite.
    """
    n, m = sprite.shape
    if n != m:
        raise ValueError("Diagonal symmetry requires a square sprite.")
    for x in range(n):
        for y in range(x + 1, m):
            c=background
            if sprite[y, x]!=background: c=sprite[y, x]
            if sprite[x, y]!=background: c=sprite[x, y]
            sprite[x, y] = sprite[y, x] = c
    return sprite


def is_contiguous(bitmask: np.ndarray, background: int = Color.BLACK, connectivity: int = 4) -> bool:
    """
    Check if an array is contiguous.

    Args:
        bitmask (np.ndarray): The input 2D array to check for contiguity.
        background (int, optional): Color that counts as transparent. Defaults to Color.BLACK.
        connectivity (int, optional): 4 or 8, for 4-way or 8-way connectivity. Defaults to 4.

    Returns:
        bool: True if the array is contiguous, False otherwise.
    """
    from scipy.ndimage import label

    if connectivity == 4:
        structure = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    elif connectivity == 8:
        structure = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    else:
        raise ValueError("Connectivity must be 4 or 8.")

    labeled, n_objects = label(bitmask != background, structure)
    return n_objects == 1


def generate_sprite(
    n,
    m,
    symmetry_type,
    fill_percentage=0.5,
    max_colors=9,
    color_palate=None,
    connectivity=4,
    background=Color.BLACK
):
    """
    internal function not used by LLM
    """
    # pick random colors, number of colors follows a geometric distribution truncated at 9
    if color_palate is None:
        n_colors = 1
        while n_colors < max_colors and random.random() < 0.3:
            n_colors += 1
        color_palate = random.sample([c for c in Color.ALL_COLORS if c!=background ], n_colors)
    else:
        n_colors = len(color_palate)

    grid = np.full((n, m), background)
    if symmetry_type == "not_symmetric":
        x, y = random.randint(0, n - 1), random.randint(0, m - 1)
    elif symmetry_type == "horizontal":
        x, y = random.randint(0, n - 1), m // 2
    elif symmetry_type == "vertical":
        x, y = n // 2, random.randint(0, m - 1)
    elif symmetry_type == "diagonal":
        # coin flip for which diagonal orientation
        diagonal_orientation = random.choice([True, False])
        x = random.randint(0, n - 1)
        y = x if diagonal_orientation else n - 1 - x
    elif symmetry_type == "radial":
        # we are just going to make a single quadrant and then apply symmetry
        assert n == m, "Radial symmetry requires a square grid."
        original_length = n
        # shrink to quarter size, we are just making a single quadrant
        n, m = int(n / 2 + 0.5), int(m / 2 + 0.5)
        x, y = (
            n - 1,
            m - 1,
        )  # begin at the bottom corner which is going to become the middle, ensuring everything is connected
    else:
        raise ValueError(f"Invalid symmetry type {symmetry_type}.")

    if connectivity == 4:
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    elif connectivity == 8:
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    else:
        raise ValueError("Connectivity must be 4 or 8.")

    color_index = 0
    while np.sum(grid != background) < fill_percentage * n * m:
        grid[x, y] = color_palate[color_index]
        if random.random() < 0.33:
            color_index = random.choice(range(n_colors))
        dx, dy = random.choice(moves)
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < n and 0 <= new_y < m:
            x, y = new_x, new_y

    if symmetry_type in ["horizontal", "vertical"]:
        grid = apply_symmetry(grid, symmetry_type)
    elif symmetry_type == "radial":
        # this requires resizing
        output = np.full((original_length, original_length), background)
        blit(output, grid, background=background)
        for _ in range(3):
            blit(output, np.rot90(output), background=background)
        grid = output

    elif symmetry_type == "diagonal":
        # diagonal symmetry goes both ways, flip a coin to decide which way
        if diagonal_orientation:
            grid = np.flipud(grid)
            grid = apply_diagonal_symmetry(grid)
            grid = np.flipud(grid)
        else:
            grid = apply_diagonal_symmetry(grid)

    return grid


def random_sprite(
    n: Union[int, List[int]],
    m: Union[int, List[int]],
    density: float = 0.5,
    symmetry: Optional[str] = None,
    color_palette: Optional[List[int]] = None,
    connectivity: int = 4,
    background: int = Color.BLACK
) -> np.ndarray:
    """
    Generate a random sprite with specified properties.

    Args:
        n (Union[int, List[int]]): Height or list of possible heights for the sprite.
        m (Union[int, List[int]]): Width or list of possible widths for the sprite.
        density (float, optional): Desired density of non-background pixels. Defaults to 0.5.
        symmetry (Optional[str], optional): Type of symmetry to apply. If None, a random type is chosen. Defaults to None.
        color_palette (Optional[List[int]], optional): List of colors to use. If None, colors are randomly chosen. Defaults to None.
        connectivity (int, optional): 4 or 8, for 4-way or 8-way connectivity. Defaults to 4.
        background (int, optional): Color treated as transparent. Defaults to Color.BLACK.

    Returns:
        np.ndarray: The generated random sprite.

    Raises:
        ValueError: If no valid sprite can be generated with the given parameters.
    """
    # canonical form: force dimensions to be lists
    if not isinstance(n, list):
        n = [n]
    if not isinstance(m, list):
        m = [m]

    # radial and diagonal require target shape to be square
    can_be_square = any(n_ == m_ for n_ in n for m_ in m)

    # Decide on symmetry type before generating the sprites
    symmetry_types = ["horizontal", "vertical", "not_symmetric"]
    if can_be_square:
        symmetry_types = symmetry_types + ["diagonal", "radial"]

    symmetry = symmetry or random.choice(symmetry_types)

    # Decide on dimensions
    has_to_be_square = symmetry in ["diagonal", "radial"]
    if has_to_be_square:
        n, m = random.choice([(n_, m_) for n_ in n for m_ in m if n_ == m_])
    else:
        n = random.choice(n)
        m = random.choice(m)

    # if one of the dimensions is 1, then we need to make sure the density is high enough to fill the entire sprite
    if n == 1 or m == 1:
        density = 1
    # small sprites require higher density in order to have a high probability of reaching all of the sides
    elif n == 2 or m == 2:
        density = max(density, 0.6)  
    elif n == 3 or m == 3:
        density = max(density, 0.5)
    elif density == 1:
        pass
    # randomly perturb the density so that we get a wider variety of densities
    else:
        density = max(0.4, min(0.95, random.gauss(density, 0.1)))

    while True:
        sprite = generate_sprite(
            n,
            m,
            symmetry_type=symmetry,
            color_palate=color_palette,
            fill_percentage=density,
            connectivity=connectivity,
            background=background,
        )
        assert is_contiguous(
            sprite, connectivity=connectivity, background=background
        ), "Generated sprite is not contiguous."
        # check that the sprite has pixels that are flushed with the border
        if (
            np.sum(sprite[0, :]!=background) > 0
            and np.sum(sprite[-1, :]!=background) > 0
            and np.sum(sprite[:, 0]!=background) > 0
            and np.sum(sprite[:, -1]!=background) > 0
        ):
            return sprite


def detect_objects(
    grid: np.ndarray,
    _: Optional[Any] = None,
    predicate: Optional[Callable[[np.ndarray], bool]] = None,
    background: int = Color.BLACK,
    monochromatic: bool = False,
    connectivity: Optional[int] = None,
    allowed_dimensions: Optional[List[Tuple[int, int]]] = None,
    colors: Optional[List[int]] = None,
    can_overlap: bool = False
) -> List[np.ndarray]:
    """
    Detect and extract objects from the grid that satisfy custom specifications.

    Args:
        grid (np.ndarray): The input grid to detect objects from.
        _ (Optional[Any], optional): Unused parameter. Defaults to None.
        predicate (Optional[Callable[[np.ndarray], bool]], optional): Function that takes a candidate object
            and returns True if it counts as an object. Defaults to None.
        background (int, optional): Color treated as transparent. Defaults to Color.BLACK.
        monochromatic (bool, optional): If True, each object is assumed to have only one color. Defaults to False.
        connectivity (Optional[int], optional): 4 or 8, for 4-way or 8-way connectivity. If None,
            connectivity is determined automatically. Defaults to None.
        allowed_dimensions (Optional[List[Tuple[int, int]]], optional): List of allowed object dimensions. Defaults to None.
        colors (Optional[List[int]], optional): List of allowed object colors. Defaults to None.
        can_overlap (bool, optional): If True, objects can overlap. Defaults to False.

    Returns:
        List[np.ndarray]: A list of detected objects, where each object is a numpy array.
    """
    objects = []

    if connectivity:
        objects.extend(find_connected_components(grid, background=background, connectivity=connectivity, monochromatic=monochromatic))
        if colors:
            objects = [obj for obj in objects if all((color in colors) or color == background for color in obj.flatten())]
        if predicate:
            objects = [obj for obj in objects if predicate(crop(obj, background=background))]
    
    if allowed_dimensions:
        objects = [obj for obj in objects if obj.shape in allowed_dimensions]

        # Also scan through the grid
        scan_objects = []
        for n, m in allowed_dimensions:
            for i in range(grid.shape[0] - n + 1):
                for j in range(grid.shape[1] - m + 1):
                    candidate_sprite = grid[i:i+n, j:j+m]

                    if np.any(candidate_sprite != background) and \
                        (colors is None or all((color in colors) or color == background for color in candidate_sprite.flatten())) and \
                        (predicate is None or predicate(candidate_sprite)):
                        candidate_object = np.full(grid.shape, background)
                        candidate_object[i:i+n, j:j+m] = candidate_sprite
                        if not any( np.all(candidate_object == obj) for obj in objects):
                            scan_objects.append(candidate_object)
        objects.extend(scan_objects)
    
    if not can_overlap:
        # sort objects by size, breaking ties by mass
        objects.sort(key=lambda obj: (crop(obj, background).shape[0] * crop(obj, background).shape[1], np.sum(obj!=background)), reverse=True)
        overlap_matrix = np.full((len(objects), len(objects)), False)
        for i, obj1 in enumerate(objects):
            for j, obj2 in enumerate(objects):
                if i != j:
                    overlap_matrix[i, j] = np.any((obj1 != background) & (obj2 != background))
                
        # Pick a subset of objects that don't overlap and which cover as many pixels as possible
        # First, we definitely pick everything that doesn't have any overlaps
        keep_objects = [obj for i, obj in enumerate(objects) if not np.any(overlap_matrix[i])]

        # Second, we might pick the remaining objects
        remaining_indices = [i for i, obj in enumerate(objects) if np.any(overlap_matrix[i])]

        # Figure out the best possible score we could get if we cover everything
        best_possible_mask = np.zeros_like(grid, dtype=bool)
        for i in remaining_indices:
            best_possible_mask |= objects[i] != background
        best_possible_score = np.sum(best_possible_mask)

        # Now we just do a brute force search recursively
        def pick_objects(remaining_indices, current_indices, current_mask):
            nonlocal overlap_matrix 
            
            if not remaining_indices:
                solution = [objects[i] for i in current_indices]
                solution_goodness = np.sum(current_mask)
                return solution, solution_goodness
            
            first_index, *rest = remaining_indices
            # Does that object have any overlap with the current objects? If so don't pick it
            if any( overlap_matrix[i, first_index] for i in current_indices):
                return pick_objects(rest, current_indices, current_mask)
            
            # Try picking it
            with_index, with_goodness = pick_objects(rest, current_indices + [first_index], current_mask | (objects[first_index] != background))

            # Did we win?
            if with_goodness == best_possible_score:
                return with_index, with_goodness

            # Try not picking it
            without_index, without_goodness = pick_objects(rest, current_indices, current_mask)

            if with_goodness > without_goodness:
                return with_index, with_goodness
            else:
                return without_index, without_goodness
        
        solution, _ = pick_objects(remaining_indices, [], np.zeros_like(grid, dtype=bool))

        objects = keep_objects + solution

    return objects

