using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace Utilities
{
    struct coordinate
    {
        public string x1, y1, x2, y2;
    };
    public partial class Form1 : Form
    {
        const string GROUNDTRUTH_FILENAME = @"D:\_PKU\Research\traffic_sign\test\migrate_test\VOC2007\train.txt";

        static Dictionary<string, List<coordinate>> ground_truth = new Dictionary<string, List<coordinate>>();
        static List<string> keys = new List<string>();

        static int index = 0;

        public Form1()
        {
            InitializeComponent();
        }

        private void load(string filename, Dictionary<string, List<coordinate>> database)
        {
            StreamReader labels_file = new StreamReader(filename);
            string line, id = null;
            List<coordinate> coordinates = new List<coordinate>();
            while ((line = labels_file.ReadLine()) != null)
            {
                string[] fields = line.Split(' ');
                if (id != fields[0])
                {
                    if (id != null)
                    {
                        database.Add(Path.ChangeExtension(id, "jpg"), coordinates);
                        coordinates = new List<coordinate>();
                    }
                    id = fields[0];
                }
                coordinate new_coordinate = new coordinate();
                new_coordinate.x1 = fields[1];
                new_coordinate.y1 = fields[2];
                new_coordinate.x2 = fields[3];
                new_coordinate.y2 = fields[4];
                coordinates.Add(new_coordinate);
            }
            database.Add(Path.ChangeExtension(id, "jpg"), coordinates);
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            load(GROUNDTRUTH_FILENAME, ground_truth);
            foreach (string s in ground_truth.Keys)
            {
                keys.Add(s);
            }
            textBox1.Text = keys[index];
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (pictureBox1.Image != null)
                pictureBox1.Image.Dispose();

            string image_filename = textBox1.Text;
            string image_fullfilename = Path.Combine(@"D:\_PKU\Research\traffic_sign\test\migrate_test\VOC2007\JPEGImages", image_filename);
            if (File.Exists(image_fullfilename) == false)
                return;

            string s = image_filename;
            Image i = Image.FromFile(image_fullfilename);
            Graphics g = Graphics.FromImage(i);

            if (ground_truth.ContainsKey(image_filename))
            {
                foreach (coordinate each_coordinate in ground_truth[image_filename])
                {
                    g.DrawRectangle(new Pen(Color.Blue, 2.0f), new Rectangle(Convert.ToInt32(Convert.ToDouble(each_coordinate.x1)),
                        Convert.ToInt32(Convert.ToDouble(each_coordinate.y1)),
                        Convert.ToInt32(Convert.ToDouble(each_coordinate.x2)) - Convert.ToInt32(Convert.ToDouble(each_coordinate.x1)),
                        Convert.ToInt32(Convert.ToDouble(each_coordinate.y2)) - Convert.ToInt32(Convert.ToDouble(each_coordinate.y1))));
                }
            }
            pictureBox1.Image = i;
            label1.Text = s;
        }

        private void button2_Click(object sender, EventArgs e)
        {
            ++index;
            textBox1.Text = keys[index];
            button1_Click(sender, e);
        }

        private void button3_Click(object sender, EventArgs e)
        {
            --index;
            textBox1.Text = keys[index];
            button1_Click(sender, e);
        }
    }
}