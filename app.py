<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Trò chơi Rắn Săn Mồi</title>
  <style>
    body {
      background-color: #1e1e2e;
      color: #ffffff;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
    }

    h1 {
      margin-bottom: 10px;
    }

    #score-board {
      font-size: 20px;
      margin-bottom: 15px;
    }

    canvas {
      border: 4px solid #89b4fa;
      background-color: #181825;
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
      border-radius: 8px;
    }

    .instructions {
      margin-top: 15px;
      font-size: 14px;
      color: #a6adc8;
    }
  </style>
</head>
<body>

  <h1>Rắn Săn Mồi</h1>
  <div id="score-board">Điểm: <span id="score">0</span></div>
  <canvas id="gameCanvas" width="400" height="400"></canvas>
  <div class="instructions">Sử dụng các phím mũi tên <b>↑ ↓ ← →</b> để di chuyển.</div>

  <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const scoreElement = document.getElementById("score");

    const gridSize = 20; // Kích thước mỗi ô vuông
    const tileCount = canvas.width / gridSize; // Số ô trên một hàng/cột (20x20)

    let snake = [
      { x: 10, y: 10 }
    ];
    let food = { x: 5, y: 5 };
    let dx = 0; // Hướng di chuyển X
    let dy = 0; // Hướng di chuyển Y
    let score = 0;
    let gameInterval;
    let gameStarted = false;

    // Vòng lặp chính của trò chơi
    function mainGameLoop() {
      if (hasGameEnded()) {
        alert(`Game Over! Điểm của bạn: ${score}`);
        resetGame();
        return;
      }

      clearCanvas();
      drawFood();
      moveSnake();
      drawSnake();
    }

    // Xóa khung vẽ cũ
    function clearCanvas() {
      ctx.fillStyle = "#181825";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    // Vẽ con rắn
    function drawSnake() {
      ctx.fillStyle = "#a6e3a1"; // Màu thân rắn
      snake.forEach((part, index) => {
        // Đầu rắn vẽ màu khác cho đẹp
        if (index === 0) ctx.fillStyle = "#94e2d5";
        else ctx.fillStyle = "#a6e3a1";

        ctx.fillRect(part.x * gridSize, part.y * gridSize, gridSize - 2, gridSize - 2);
      });
    }

    // Di chuyển rắn
    function moveSnake() {
      if (!gameStarted) return;

      const head = { x: snake[0].x + dx, y: snake[0].y + dy };
      snake.unshift(head);

      // Kiểm tra ăn mồi
      if (head.x === food.x && head.y === food.y) {
        score += 10;
        scoreElement.textContent = score;
        generateFood();
      } else {
        snake.pop(); // Xóa đuôi nếu không ăn mồi
      }
    }

    // Sinh mồi ngẫu nhiên
    function generateFood() {
      food.x = Math.floor(Math.random() * tileCount);
      food.y = Math.floor(Math.random() * tileCount);

      // Đảm bảo mồi không xuất hiện trên thân rắn
      snake.forEach(part => {
        if (part.x === food.x && part.y === food.y) {
          generateFood();
        }
      });
    }

    // Vẽ mồi
    function drawFood() {
      ctx.fillStyle = "#f38ba8"; // Màu thức ăn
      ctx.fillRect(food.x * gridSize, food.y * gridSize, gridSize - 2, gridSize - 2);
    }

    // Kiểm tra va chạm (thua game)
    function hasGameEnded() {
      if (!gameStarted) return false;

      // Đâm vào tường
      const hitLeft = snake[0].x < 0;
      const hitRight = snake[0].x >= tileCount;
      const hitTop = snake[0].y < 0;
      const hitBottom = snake[0].y >= tileCount;

      if (hitLeft || hitRight || hitTop || hitBottom) return true;

      // Cắn vào thân
      for (let i = 1; i < snake.length; i++) {
        if (snake[i].x === snake[0].x && snake[i].y === snake[0].y) {
          return true;
        }
      }

      return false;
    }

    // Lắng nghe sự kiện bàn phím
    document.addEventListener("keydown", changeDirection);

    function changeDirection(event) {
      const keyPressed = event.keyCode;
      const LEFT = 37, UP = 38, RIGHT = 39, DOWN = 40;

      // Ngăn rắn tự quay đầu 180 độ
      const goingUp = dy === -1;
      const goingDown = dy === 1;
      const goingRight = dx === 1;
      const goingLeft = dx === -1;

      if (keyPressed === LEFT && !goingRight) { dx = -1; dy = 0; gameStarted = true; }
      if (keyPressed === UP && !goingDown) { dx = 0; dy = -1; gameStarted = true; }
      if (keyPressed === RIGHT && !goingLeft) { dx = 1; dy = 0; gameStarted = true; }
      if (keyPressed === DOWN && !goingUp) { dx = 0; dy = 1; gameStarted = true; }
    }

    // Khởi động lại game
    function resetGame() {
      snake = [{ x: 10, y: 10 }];
      dx = 0;
      dy = 0;
      score = 0;
      gameStarted = false;
      scoreElement.textContent = score;
      generateFood();
    }

    // Bắt đầu chạy game với tốc độ 100ms mỗi khung hình (10 FPS)
    generateFood();
    setInterval(mainGameLoop, 100);
  </script>
</body>
</html>
