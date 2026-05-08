def render_grid(grid: list[list[int]]) -> str:
    lines = []
    for row in grid:
        line = " ".join(str(cell) if cell != 0 else "." for cell in row)
        lines.append(line)
    return "\n".join(lines)
