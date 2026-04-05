import MapMaker as map
from typing import Tuple, Dict, List, Optional
import os
import Slam as slam

class GridAreaManager:
    # Area position starting coordinates (4×4 blocks separated by 0s)
    AREA_STARTS = [1, 6, 11, 16, 21]  # Rows and columns where areas start
    AREA_SIZE = 4  # Each area is 4×4
    AREA_SEPARATION = 1  # 1 cell of 0s between areas
    
    # Area type names
    AREA_TYPES = {
        0: "Free Space",
        1: "Hospital A",
        2: "Hospital B",
        3: "Checkpoint",
        4: "Medical Evacuation",
        5: "HDB Building",
        6: "Aerial Photography",
        7: "Restricted Area"
    }
    
    def __init__(self, grid: list):
        self.grid = grid
        self.grid_size = len(grid)
        self.drone_pos = (0, 0)  # Grid coordinates
        self.drone_altitude = 0
        
        # Area restrictions/requirements
        self.area_requirements = {}  # {area_start: {'min_alt': X, 'max_alt': Y, ...}}
    
    def get_area_at_coord(self, row: int, col: int) -> Tuple[str, Tuple[int, int], int]:
        """
        Get area info at grid coordinate
        
        Returns: (area_name, area_start_pos, area_type)
        """
        # Check if coordinate is valid
        if not (0 <= row < self.grid_size and 0 <= col < self.grid_size):
            return ("Out of Bounds", None, -1)
        
        # Check if on a pathway (0)
        cell_value = self.grid[row][col]
        if cell_value == 0:
            return ("Pathway (Free Space)", None, 0)
        
        # Find which 4×4 area this coordinate belongs to
        area_row = None
        area_col = None
        
        # Determine which area row
        for start_row in self.AREA_STARTS:
            if start_row <= row < start_row + self.AREA_SIZE:
                area_row = start_row
                break
        
        # Determine which area col
        for start_col in self.AREA_STARTS:
            if start_col <= col < start_col + self.AREA_SIZE:
                area_col = start_col
                break
        
        if area_row is None or area_col is None:
            return ("Pathway or Edge", None, cell_value)
        
        area_start = (area_row, area_col)
        area_type = cell_value
        area_name = self.AREA_TYPES.get(area_type, f"Unknown (Type {area_type})")
        
        return (area_name, area_start, area_type)
    
    def set_area_requirement(self, area_start: Tuple[int, int], **requirements):
        """
        Set drone requirements for an area
        
        Example:
            set_area_requirement((1, 6), min_altitude=200, max_altitude=240)
        """
        self.area_requirements[area_start] = requirements
        print(f"✓ Set requirements for area at {area_start}: {requirements}")
    
    def check_requirements(self, area_start: Tuple[int, int], altitude: int) -> Tuple[bool, str]:
        """
        Check if drone meets area requirements
        
        Returns: (is_valid, message)
        """
        if area_start not in self.area_requirements:
            return (True, "No special requirements")
        
        reqs = self.area_requirements[area_start]
        
        if 'min_altitude' in reqs:
            if altitude < reqs['min_altitude']:
                return (False, f"Altitude {altitude}cm below minimum {reqs['min_altitude']}cm")
        
        if 'max_altitude' in reqs:
            if altitude > reqs['max_altitude']:
                return (False, f"Altitude {altitude}cm above maximum {reqs['max_altitude']}cm")
        
        return (True, "Requirements met")
    
    def navigate_to(self, target_row: int, target_col: int, start_alt: int = 0) -> bool:
        """
        Navigate drone to target grid coordinate
        
        Returns: True if successful, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"NAVIGATING TO COORDINATE ({target_row}, {target_col})")
        print(f"{'='*60}")
        
        # Validate target
        if not (0 <= target_row < self.grid_size and 0 <= target_col < self.grid_size):
            print(f"✗ Invalid coordinate: ({target_row}, {target_col})")
            return False
        
        # Get area info at target
        area_name, area_start, area_type = self.get_area_at_coord(target_row, target_col)
        print(f"\nTarget Area: {area_name}")
        print(f"Area Type ID: {area_type}")
        if area_start:
            print(f"Area Start Position: {area_start}")
        
        # Calculate movement needed
        row_diff = target_row - self.drone_pos[0]
        col_diff = target_col - self.drone_pos[1]
        
        print(f"\nCurrent Position: {self.drone_pos}")
        print(f"Movements needed:")
        print(f"  Rows: {row_diff:+d} (forward/backward)")
        print(f"  Cols: {col_diff:+d} (left/right)")
        
        # Convert to cm (25cm per cell)
        row_cm = abs(row_diff) * 20
        col_cm = abs(col_diff) * 20
        
        try:
            # Execute movements (only if slam/drone is available)
            if slam is not None:
                if row_diff < 0:
                    print(f"→ Moving backward {row_cm}cm")
                    slam.drone.move_backward(row_cm)
                elif row_diff > 0:
                    print(f"→ Moving forward {row_cm}cm")
                    slam.drone.move_forward(row_cm)
                
                if col_diff < 0:
                    print(f"→ Moving left {col_cm}cm")
                    slam.drone.move_left(col_cm)
                elif col_diff > 0:
                    print(f"→ Moving right {col_cm}cm")
                    slam.drone.move_right(col_cm)
            else:
                print(f"\n→ [SIMULATION] Moving backward {row_cm}cm" if row_diff < 0 else f"→ [SIMULATION] Moving forward {row_cm}cm")
                print(f"→ [SIMULATION] Moving left {col_cm}cm" if col_diff < 0 else f"→ [SIMULATION] Moving right {col_cm}cm")
            
            # Update drone position
            self.drone_pos = (target_row, target_col)
            self.drone_altitude = start_alt
            
            print(f"\n✓ Arrived at ({target_row}, {target_col})")
            return True
            
        except Exception as e:
            print(f"\n✗ Navigation error: {e}")
            return False
    
    def print_area_info(self, row: int, col: int):
        area_name, area_start, area_type = self.get_area_at_coord(row, col)
        
        print(f"\n{'='*60}")
        print(f"AREA INFORMATION")
        print(f"{'='*60}")
        print(f"Coordinate: ({row}, {col})")
        print(f"Area Name: {area_name}")
        print(f"Area Type ID: {area_type}")
        
        if area_start:
            print(f"Area Block Start: {area_start}")
            print(f"Area Block Range: Rows {area_start[0]}-{area_start[0]+3}, Cols {area_start[1]}-{area_start[1]+3}")
            
            # Check requirements
            if area_start in self.area_requirements:
                print(f"Special Requirements:")
                for key, value in self.area_requirements[area_start].items():
                    print(f"  {key}: {value}")
        
        print(f"{'='*60}\n")
    
    def print_grid_with_drone(self):
        # Simple display - show area types
        for r in range(min(26, self.grid_size)):
            row_str = f"{r:2}┃ "
            for c in range(min(26, self.grid_size)):
                if (r, c) == self.drone_pos:
                    row_str += "x"
                else:
                    cell_val = self.grid[r][c]
                    if cell_val == 0:
                        row_str += ". "
                    else:
                        row_str += f"{cell_val} "
            print(row_str)
        
        print(f"\n{'='*60}\n")