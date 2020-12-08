using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static System.Console;

namespace snakegame
{
    public class Pixel
    {
        public int XPos { get; set; }
        public int YPos { get; set; }

        public Pixel(int xPos, int yPos)
        {
            this.XPos = xPos;
            this.YPos = yPos;
        }

        public void DrawPixel(string item)
        {
            SetCursorPosition(this.YPos, this.YPos);
            Write(item);
        }
    }
}
