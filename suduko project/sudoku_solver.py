import time
import cv2
import numpy as np
import pytesseract
from PIL import Image

class SudokuSolver:
    def __init__(self):
        self.solving_time = 0
        
    def solve(self, grid, algorithm='backtracking'):
        start_time = time.time()
        solution = None
        
        if algorithm == 'backtracking':
            solution = self._solve_backtracking([row[:] for row in grid])
        elif algorithm == 'bruteforce':
            solution = self._solve_bruteforce([row[:] for row in grid])
        
        self.solving_time = time.time() - start_time
        return solution
    
    def _solve_backtracking(self, grid):
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        if self._is_valid(grid, row, col, num):
                            grid[row][col] = num
                            if self._solve_backtracking(grid):
                                return grid
                            grid[row][col] = 0
                    return None
        return grid
    
    def _solve_bruteforce(self, grid, index=0):
        if index == 81:
            return grid
        
        row, col = index // 9, index % 9
        
        if grid[row][col] != 0:
            return self._solve_bruteforce(grid, index + 1)
        
        for num in range(1, 10):
            if self._is_valid(grid, row, col, num):
                grid[row][col] = num
                if self._solve_bruteforce(grid, index + 1):
                    return grid
                grid[row][col] = 0
        
        return None
    
    def _is_valid(self, grid, row, col, num):
        # Check row
        if num in grid[row]:
            return False
        
        # Check column
        for i in range(9):
            if grid[i][col] == num:
                return False
        
        # Check 3x3 box
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if grid[box_row + i][box_col + j] == num:
                    return False
        
        return True
    
    def read_from_image(self, image_path):
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not read image")
                
            # Preprocess image
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            thresh = cv2.adaptiveThreshold(
                blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV, 11, 2
            )
            
            # Find contours
            contours, _ = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            
            # Find Sudoku grid (largest square contour)
            sudoku_contour = None
            for contour in contours:
                peri = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
                if len(approx) == 4:
                    sudoku_contour = approx
                    break
            
            if sudoku_contour is None:
                raise ValueError("Could not find Sudoku grid in image")
            
            # Perspective transform
            pts = np.float32([sudoku_contour[0][0], sudoku_contour[1][0], 
                             sudoku_contour[2][0], sudoku_contour[3][0]])
            width, height = 450, 450
            dst = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
            M = cv2.getPerspectiveTransform(pts, dst)
            warped = cv2.warpPerspective(gray, M, (width, height))
            
            # Extract digits
            grid = [[0 for _ in range(9)] for _ in range(9)]
            cell_size = warped.shape[0] // 9
            
            for row in range(9):
                for col in range(9):
                    x1 = col * cell_size + 5
                    y1 = row * cell_size + 5
                    x2 = (col + 1) * cell_size - 5
                    y2 = (row + 1) * cell_size - 5
                    
                    cell = warped[y1:y2, x1:x2]
                    cell = cv2.resize(cell, (64, 64))
                    cell = cv2.threshold(cell, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                    
                    # Check if cell has content
                    if cv2.countNonZero(cell) > 50:
                        # Configure Tesseract for single digit
                        custom_config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=123456789'
                        digit = pytesseract.image_to_string(cell, config=custom_config).strip()
                        
                        if digit.isdigit():
                            grid[row][col] = int(digit)
            
            return grid
            
        except Exception as e:
            print(f"Image processing error: {str(e)}")
            return None