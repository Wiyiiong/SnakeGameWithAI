using System;
using System.Threading;
using System.IO;
using System.Linq;

namespace snakegame
{
    public class Game
    {
        // Constant values
        private const int H = 22;
        private const int W = 44;
        private const int MARGIN = 2;

        // Instance variable
        public bool GameOver { get; set; }

        // Private Variable
        private ConsoleKey curKey;
        private ConsoleKey lastKey;
        private ConsoleKey lastDirectionKey;
        private int points;
        private int bestScores;
        private int speed;
        private Pixel berry;
        private Random random;
        private Pixel snakePos;

        // Object
        private Snake snake = new Snake(0, 0);
        private Board board = new Board(W, H, MARGIN);

        public Game()
        {
            this.curKey = ConsoleKey.Delete;
            this.lastKey = ConsoleKey.Delete;
            this.lastDirectionKey = ConsoleKey.Delete;
            this.points = 0;
            this.speed = 300;
            this.random = new Random();
            this.snakePos = new Pixel(0, 0);
        }

        public void StartGame()
        {
            Console.SetWindowSize(W + MARGIN * 4, H + MARGIN * 4);
            Console.CursorVisible = false;

            snake = Snake.initializeSnake(W / 2, H / 2);
            board = new Board(W, H, MARGIN);

            this.points = 0;
            this.GameOver = false;
            this.curKey = ConsoleKey.Delete;
            this.speed = 300;

            GenerateFood();

            while (!this.GameOver)
            {
                if (Console.KeyAvailable)
                {
                    this.curKey = Console.ReadKey(true).Key;
                    if (this.lastKey == this.curKey)
                    {
                        if (this.speed > 100)
                        {
                            this.speed -= 30;
                        }
                        else if (this.speed > 30)
                        {
                            this.speed -= 10;
                        }

                        continue;
                    }

                    this.speed = 300;
                }

                // drawing and updating 
                //Console.Clear();
                clearScreen();

                board.DrawMapArea();
                DrawPoints();
                board.DrawBerry(this.berry.XPos, this.berry.YPos);
                curKey = UpdateKey(curKey, lastDirectionKey);
                collisionOnWalls();
                snake.Draw();

                if (snake.collisionOnBody())
                {
                    this.GameOver = true;
                    break;
                }
                if (snake.eatBerry(this.berry.XPos, this.berry.YPos))
                {
                    this.points += 10;
                    GenerateFood();
                }

                Thread.Sleep(this.speed);
                this.lastKey = this.curKey;
                this.lastDirectionKey = this.curKey;
            }

            this.bestScores = int.Parse(ReadBestScore());

            Console.Clear();

            Console.SetCursorPosition(MARGIN + 5, (H - MARGIN) / 2);
            Console.WriteLine("######################");
            Console.SetCursorPosition(MARGIN + 5, ((H - MARGIN) / 2) + 1);
            Console.WriteLine("##### GAME OVER ######");
            Console.SetCursorPosition(MARGIN + 5, ((H - MARGIN) / 2) + 2);
            Console.WriteLine("######################");
            Console.SetCursorPosition(MARGIN + 5, ((H - MARGIN) / 2) + 3);
            Console.WriteLine();
            if(this.bestScores< this.points)
            {
                Console.SetCursorPosition(MARGIN + 5, ((H - MARGIN) / 2) + 5);
                Console.WriteLine("-- New Record --");
                Console.SetCursorPosition(MARGIN + 5, ((H - MARGIN) / 2) + 6);
                Console.WriteLine("New best score: " + points);
                Console.SetCursorPosition(MARGIN + 5, ((H - MARGIN) / 2) + 7);
                Console.WriteLine("Old best score: " + bestScores);
                SaveBestScore(points);
            }
            else
            {
                Console.SetCursorPosition(MARGIN + 5, ((H - MARGIN) / 2) + 5);
                Console.WriteLine("New Score: " + points);
                Console.SetCursorPosition(MARGIN + 5, ((H - MARGIN) / 2) + 6);
                Console.WriteLine("Best score: " + bestScores);
            }
            
            Thread.Sleep(2500);
            Console.Clear();
        }

        public void GenerateFood()
        {
            bool isInsideWall = false;
            bool isInBody = false;

            do
            {
                // generate berry
                berry = new Pixel(
                    this.random.Next(MARGIN + 1, W - MARGIN),
                    this.random.Next(MARGIN + 1, H - MARGIN)
                    );

                // if berry is in snake body, regenerate new berry
                foreach (var part in this.snake.Body)
                {
                    if (part.XPos == this.berry.XPos && part.YPos == this.berry.YPos)
                    {
                        isInBody = true;
                        break;
                    }
                }

                // if berry is inside wall, regenerate new berry
                isInsideWall = board.isOnWall(this.berry.XPos, this.berry.YPos);

            } while (isInsideWall && isInBody);

        }

        public void DrawPoints()
        {
            Console.SetCursorPosition(MARGIN, 1);
            Console.Write("Best: {0}", ReadBestScore());
            Console.SetCursorPosition(W - MARGIN * 2-8-this.points.ToString().Count(), 1);
            Console.Write("Points: {0}", this.points);
        }

        public ConsoleKey UpdateKey(ConsoleKey curKey, ConsoleKey lastDirection)
        {
            switch (curKey)
            {
                case ConsoleKey.RightArrow:
                case ConsoleKey.D:
                    if (lastDirection == ConsoleKey.LeftArrow || lastDirection == ConsoleKey.A)
                    {
                        curKey = lastDirection;
                        return curKey;
                    }
                    this.snake.moveRight();
                    break;
                case ConsoleKey.LeftArrow:
                case ConsoleKey.A:
                    if (lastDirection == ConsoleKey.RightArrow || lastDirection == ConsoleKey.D)
                    {
                        curKey = lastDirection;
                        return curKey;
                    }
                    this.snake.moveLeft();
                    break;
                case ConsoleKey.UpArrow:
                case ConsoleKey.W:
                    if (lastDirection == ConsoleKey.DownArrow || lastDirection == ConsoleKey.S)
                    {
                        curKey = lastDirection;
                        return curKey;
                    }
                    this.snake.moveUp();
                    break;
                case ConsoleKey.DownArrow:
                case ConsoleKey.S:
                    if (lastDirection == ConsoleKey.UpArrow || lastDirection == ConsoleKey.W)
                    {
                        curKey = lastDirection;
                        return curKey;
                    }
                    this.snake.moveDown();
                    break;
                default: break;
            }

            return curKey;

        }

        public void collisionOnWalls()
        {
            foreach (var parts in this.snake.Body)
            {
                if (board.isOnWall(parts.XPos, parts.YPos))
                {
                    if (parts.XPos == MARGIN)
                    {
                        parts.XPos = W - MARGIN - 1;
                    }
                    else if (parts.XPos == (W - MARGIN))
                    {
                        parts.XPos = MARGIN + 1;
                    }
                    if (parts.YPos == MARGIN)
                    {
                        parts.YPos = H - MARGIN - 1;
                    }
                    else if (parts.YPos == (H - MARGIN))
                    {
                        parts.YPos = MARGIN + 1;
                    }
                }
            }
        }

        public void clearScreen()
        {

            Console.SetCursorPosition(this.snake.Body[0].XPos, this.snake.Body[0].YPos);
            Console.Write(" ");

            Console.SetCursorPosition(this.berry.XPos, this.berry.YPos);
            Console.Write(" ");
        }

        public string ReadBestScore()
        {
            string directory = Directory.GetCurrentDirectory() + @"\Scores\";
            if (!Directory.Exists(directory))
            {
                Directory.CreateDirectory(directory);
            }
            string fileName = "score.txt";
            if (!File.Exists(directory + @"\" + fileName))
            {
                File.CreateText(directory + @"\" + fileName);
            }

            string score = File.ReadLines(directory + @"\" + fileName).FirstOrDefault();
            if (score != null)
            {
                return score;
            }
            return "0";
        }

        public void SaveBestScore(int score)
        {
            string directory = Directory.GetCurrentDirectory() + @"\Scores\" + "score.txt";
            File.WriteAllText(directory, score.ToString());
        }
    }
}
