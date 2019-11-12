using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp1
{
    class Program
    {
        static int[] r1 = { 0, 1, 0, 0};
        static int[] r2 = { 0, 1, 0, 0, 0, 0 };


        static int[] row1 = { 0,1,0,0,1,0,0,0,1,1,0,0,0,1,0,1,1,1,0,0 };
        static void Main(string[] args)
        {
            // The code provided will print ‘Hello World’ to the console.
            // Press Ctrl+F5 (or go to Debug > Start Without Debugging) to run your app.
            Console.WriteLine("Let's go");

 
            Program p = new Program();
            int[] row1 = createArray(10);
            int[] ring = makeRing(row1);
            int cutPos = p.start(ring);
            //check, p1 = cut -> -row1.Length, p2 = cut -> +row1.Length
            int[] part1 = ring.Slice(cutPos - (row1.Length / 2), cutPos);
            //int[] part2 = ring.Slice(cutPos, cutPos + (row1.Length / 2));

            Console.WriteLine("part 1");
            foreach (int i in part1) {
                Console.WriteLine(i);
            }

            //måste klippas ihop från det som blir över...
            /*
            Console.WriteLine("part 2");
            foreach (int i in part2) {
                Console.WriteLine(i);
            }
            */

            Console.ReadKey();

            // Go to http://aka.ms/dotnet-get-started-console to continue learning how to build a console app!
        }

        static private int[] makeRing(int[] row)
        {
            int[] halfRow = row.Where((item, index) => index < row.Length / 2).ToArray();
            var list = new List<int>();
            list.AddRange(row);
            list.AddRange(halfRow);
            return list.ToArray();
        }

   

    static private int[] createArray(int size)
        {
            Random randNum = new Random();
            return Enumerable
                .Repeat(0, size)
                .Select(i => randNum.Next(0, 2))
                .ToArray();
            //return test2;
        }

        public int start(int[] ring)
        {
            Console.WriteLine("Length " + ring.Length);

            int tot = 0;
            int tot1 = 0;
            int maxTot1 = 0;
            int cutPos = 0;
            foreach (int i in ring) {
                if (i == 1) {
                    tot1++;
                    if (tot1 > maxTot1)
                        cutPos = tot;
                }
                if (tot >= ring.Length / 2) {
                    //dra bort i början ifall den var en 1'a
                    if (ring[tot] == 1) {
                        //first decrease, means we had a highest
                        if (ring[tot - 1] == 1) {
                            maxTot1 = tot1;
                        }
                        tot1--;
                    }
                }

                //Console.WriteLine(i);
                tot++;
            }
            Console.WriteLine("maxTot1 " + maxTot1);
            Console.WriteLine("cutPos " + cutPos);

            return cutPos;
        }

    }


    public static class Extensions
    {
        /// <summary>
        /// Get the array slice between the two indexes.
        /// ... Inclusive for start index, exclusive for end index.
        /// </summary>
        public static T[] Slice<T>(this T[] source, int start, int end)
        {
            // Handles negative ends.
            if (end < 0) {
                end = source.Length + end;
            }
            int len = end - start;

            // Return new array.
            T[] res = new T[len];
            for (int i = 0; i < len; i++) {
                res[i] = source[i + start];
            }
            return res;
        }
    }

}
