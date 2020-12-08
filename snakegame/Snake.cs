using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace snakegame
{   
    public class Snake
    {       

        public Pixel Head { get; set; }
        public List<Pixel> Body { get; set; }

        public Snake(int x, int y)
        {
            Head = new Pixel(x, y);
            Body = new List<Pixel>();
        }     
        
       public void moveLeft()
        {            
            this.Head = new Pixel(this.Body[this.Body.Count - 1].XPos, this.Body[this.Body.Count - 1].YPos);
            this.Head.XPos--;
            this.Body.RemoveAt(0);
            this.Body.Add(this.Head);
            
        }
        public void moveRight()
        {            
            this.Head = new Pixel(this.Body[this.Body.Count - 1].XPos, this.Body[this.Body.Count - 1].YPos);
            this.Head.XPos++;
            this.Body.RemoveAt(0);
            this.Body.Add(this.Head);

        }
        public void moveUp()
        {            
            this.Head = new Pixel(this.Body[this.Body.Count - 1].XPos, this.Body[this.Body.Count - 1].YPos);
            this.Head.YPos--;
            this.Body.RemoveAt(0);
            this.Body.Add(this.Head);

        }
        public void moveDown()
        {            
            this.Head = new Pixel(this.Body[this.Body.Count - 1].XPos, this.Body[this.Body.Count - 1].YPos);
            this.Head.YPos++;
            this.Body.RemoveAt(0);
            this.Body.Add(this.Head);
        }

        public bool eatBerry(int x, int y)
        {
            if(this.Head.XPos == x && this.Head.YPos == y)
            {
                this.Body.Insert(0, new Pixel(this.Body[0].XPos, this.Body[0].YPos));
                return true;
            }

            return false;
        }
        public void Draw()
        {
            int count = 0;
           
            foreach(var parts in this.Body)
            {
                if (count == this.Body.Count - 1)
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                }
                else
                {
                    Console.ForegroundColor = ConsoleColor.White;
                }
                Console.SetCursorPosition(parts.XPos, parts.YPos);
                Console.Write("*");
                count++;
            }
        }

        public bool collisionOnBody()
        {
            // skip on head, so count - 1
           for(int i = 0; i < this.Body.Count - 1; i++)
            {
                if(this.Head.XPos==this.Body[i].XPos && this.Head.YPos == this.Body[i].YPos)
                {
                    // game over
                    return true;
                }
                
            }
            return false;
        }

        public static Snake initializeSnake(int x, int y)
        {
            Snake newSnake = new Snake(x, y);
            newSnake.Body.Add(newSnake.Head);

            return newSnake;
        }

    }
}
