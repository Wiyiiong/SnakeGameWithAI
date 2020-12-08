using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace snakegame
{
    public class Board
    {
        private static ConsoleColor Color = ConsoleColor.White;
        public int Width { get; set; }
        public int Height { get; set; }
        public int Margin { get; set; }

        public Board(int width, int height, int margin)
        {
            this.Width = width;
            this.Height = height;
            this.Margin = margin;
        }
        
        public void DrawBerry(int x, int y)
        {
            Console.SetCursorPosition(x, y);
            Console.ForegroundColor = ConsoleColor.Green;
            Console.Write("*");
        }

        public void DrawMapArea()
        {
            Console.ForegroundColor = Color;
            int space = this.Width - this.Margin * 2;

            // draw top border
            Console.SetCursorPosition(this.Margin, this.Margin);            
            for(int i = 0; i < space; i++)
            {
                Console.Write("#");
            }

            // draw bottom border
            Console.SetCursorPosition(this.Margin, this.Height-this.Margin);            
            for (int i = 0; i < space; i++)
            {
                Console.Write("#");
            }

            space = this.Height - this.Margin;

            // draw left border
            for (int i = this.Margin; i <= space; i++)
            {
                Console.SetCursorPosition(this.Margin, i);
                Console.Write("#");
            }

            // draw right border
            for (int i = this.Margin; i <= space; i++)
            {
                Console.SetCursorPosition(this.Width- this.Margin, i);
                Console.Write("#");
            }
        }

        public bool isOnWall(int x, int y)
        {        
            // left or top border
            if (x <= this.Margin || y <= this.Margin)
            {
                return true;
            }
            // right or bottom border
            else if (x >= this.Width - this.Margin || y >= this.Height - this.Margin)
            {
                return true;
            }

            return false;
        }
    }
}
