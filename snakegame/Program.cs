using System;
using System.Diagnostics;
using System.Linq;
using static System.Console;

namespace snakegame
{
    
    class Program
    {        
        static void Main(string[] args)
        {
            Console.Title = "Snake Game";
            Console.CursorVisible = false;

            Game game = new Game();
            bool exit = false;
            do
            {
                game.StartGame();
                var key = Console.ReadKey(true).Key;
                if (key == ConsoleKey.Escape) { exit = true; }                

            } while (!exit);
            
        }

    }
}
