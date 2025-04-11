from flask import Flask, render_template, request, jsonify
from sudoku_solver import SudokuSolver
import os

app = Flask(__name__)
solver = SudokuSolver()

# Sample puzzles
SAMPLE_PUZZLES = {
    "easy": [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],
    "medium": [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ],
    "hard": [
        [0, 0, 0, 6, 0, 0, 4, 0, 0],
        [7, 0, 0, 0, 0, 3, 6, 0, 0],
        [0, 0, 0, 0, 9, 1, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 1, 8, 0, 0, 0, 3],
        [0, 0, 0, 3, 0, 6, 0, 4, 5],
        [0, 4, 0, 2, 0, 0, 0, 6, 0],
        [9, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 1, 0, 0]
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    grid = data.get('grid')
    
    if not grid or len(grid) != 9 or any(len(row) != 9 for row in grid):
        return jsonify({"error": "Invalid Sudoku grid"}), 400
    
    solution = solver.solve(grid)
    
    if solution:
        return jsonify({
            "solved": True,
            "solution": solution,
            "time": solver.solving_time
        })
    else:
        return jsonify({"solved": False})

@app.route('/sample/<difficulty>')
def get_sample(difficulty):
    puzzle = SAMPLE_PUZZLES.get(difficulty.lower(), SAMPLE_PUZZLES["easy"])
    return jsonify({"puzzle": puzzle})

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        # Save temporarily
        temp_path = os.path.join('temp', file.filename)
        file.save(temp_path)
        
        # Process image
        grid = solver.read_from_image(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        if grid:
            return jsonify({"grid": grid})
        else:
            return jsonify({"error": "Could not read Sudoku from image"}), 400

if __name__ == '__main__':
    # Create temp directory if it doesn't exist
    if not os.path.exists('temp'):
        os.makedirs('temp')
    app.run(debug=True)