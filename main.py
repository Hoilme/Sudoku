import pygame
import json
from pathlib import Path
import random

pygame.display.init()
pygame.font.init()
font = pygame.font.SysFont("arial", 32, bold=True)

cell_size = 50
offset = 10
board_size = 9 * cell_size
screen_width = 470
screen_height = 470
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sudoku Test")

# 1. JSON'dan tahtayı yükleme (çalışma dizininden bağımsız)
boards_path = Path(__file__).with_name("boards.json")
with boards_path.open(encoding="utf-8") as f:
	puzzles = json.load(f)

#Random sudoku seçimi
chosen_game = random.choice(puzzles)
puzzle_str = chosen_game.get("puzzle","")
solution_str = chosen_game.get("solution","")
game_won = False


if not puzzles or len(puzzle_str) != 81:
	raise ValueError("boards.json must contain a puzzle with exactly 81 digits")

if not puzzle_str.isdigit():
	raise ValueError("The puzzle must contain digits only")
original_board = []
board = []
for r in range(9):
	row_data = []
	for c in range(9):
		row_data.append(int(puzzle_str[r * 9 + c]))
	original_board.append(row_data)
board = [row.copy() for row in original_board]

selected = None
clock = pygame.time.Clock()
running = True

def control(board, solution_str):
	board_str = "".join(str(value) for row in board for value in row)
	return board_str == solution_str

while running:
	screen.fill((0, 0, 0))
	
	# 2. Hover (Mavi)
	mouse_x, mouse_y = pygame.mouse.get_pos()
	if (offset <= mouse_x < offset + board_size and
			offset <= mouse_y < offset + board_size):
		col = (mouse_x - offset) // cell_size
		row = (mouse_y - offset) // cell_size
		cell_rect = pygame.Rect(
			offset + col * cell_size,
			offset + row * cell_size,
			cell_size,
			cell_size,
		)
		pygame.draw.rect(screen, (45, 85, 125), cell_rect)

	# 3. Seçili Hücre (Sarı Çerçeve)
	if selected is not None:
		sel_row, sel_col = selected
		selected_rect = pygame.Rect(
			offset + sel_col * cell_size,
			offset + sel_row * cell_size,
			cell_size,
			cell_size
		)
		pygame.draw.rect(screen, (255, 255, 0), selected_rect, 4)

	# 4. Izgara Çizgileri
	for i in range(10):
		pos = offset + i * cell_size
		if i % 3 == 0 and i != 0 and i != 9:
			line_w = 7
		else:
			line_w = 3
		pygame.draw.line(screen, (255, 255, 255), (pos, offset), (pos, offset + board_size), line_w)
		pygame.draw.line(screen, (255, 255, 255), (offset, pos), (offset + board_size, pos), line_w)

	# 5. Sayıları Ekrana Basma
	for r in range(9):
		for c in range(9):
			val = board[r][c]
			if val != 0:
				center_x = offset + c * cell_size + cell_size // 2
				center_y = offset + r * cell_size + cell_size // 2
				if game_won:
					color = (0, 255, 0)
				else:
					color = (173, 216, 230) if original_board[r][c] != 0 else (255, 255, 255)
				text_surf = font.render(str(val), True, color)
				text_rect = text_surf.get_rect(center=(center_x, center_y))
				screen.blit(text_surf, text_rect)

	# 6. Event Kontrolleri
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if selected is not None:
				r, c = selected
				if original_board[r][c] == 0:
					if event.key in (pygame.K_1, pygame.K_KP1):
						board[r][c] = 1
						game_won = control(board, solution_str)
					elif event.key in (pygame.K_2, pygame.K_KP2):
						board[r][c] = 2
						game_won = control(board, solution_str)
					elif event.key in (pygame.K_3, pygame.K_KP3):
						board[r][c] = 3
						game_won = control(board, solution_str)
					elif event.key in (pygame.K_4, pygame.K_KP4):
						board[r][c] = 4
						game_won = control(board, solution_str)
					elif event.key in (pygame.K_5, pygame.K_KP5):
						board[r][c] = 5
						game_won = control(board, solution_str)
					elif event.key in (pygame.K_6, pygame.K_KP6):
						board[r][c] = 6
						game_won = control(board, solution_str)
					elif event.key in (pygame.K_7, pygame.K_KP7):
						board[r][c] = 7
						game_won = control(board, solution_str)
					elif event.key in (pygame.K_8, pygame.K_KP8):
						board[r][c] = 8
						game_won = control(board, solution_str)
					elif event.key in (pygame.K_9, pygame.K_KP9):
						board[r][c] = 9
						game_won = control(board, solution_str)
					elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE, pygame.K_0, pygame.K_KP0):
						board[r][c] = 0
						game_won = control(board, solution_str)
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				x, y = event.pos
				click_col = (x - offset) // cell_size
				click_row = (y - offset) // cell_size
				if 0 <= click_row < 9 and 0 <= click_col < 9:
					selected = (click_row, click_col)
				else:
					selected = None
		if game_won:
				pass
		if event.type == pygame.QUIT:
				running = False
	pygame.display.update()
	clock.tick(60)

pygame.quit()