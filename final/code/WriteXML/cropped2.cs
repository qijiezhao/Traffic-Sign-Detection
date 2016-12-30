using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Xml;

namespace Utilities
{
    struct coordinate
    {
        public int x1, y1, x2, y2;
    };
    class Program
    {
        const string LABEL_FILE = "train_cropped.csv";
        const string OUTPUT_PATH = @"D:\_PKU\Research\traffic_sign2\Annotations\cropped2\VOC2007\Annotations";
        const string OUTPUT_TRAINVAL = @"D:\_PKU\Research\traffic_sign2\Annotations\cropped2\VOC2007\ImageSets\Main\trainval.txt";
        const string OUTPUT_TEST = @"D:\_PKU\Research\traffic_sign2\Annotations\cropped2\VOC2007\ImageSets\Main\test.txt";

        static StreamWriter test;
        static StreamWriter trainval;
        static void Main(string[] args)
        {
            StreamReader labels_file = new StreamReader(LABEL_FILE);
            test = new StreamWriter(OUTPUT_TEST);
            trainval = new StreamWriter(OUTPUT_TRAINVAL);
            string line, id = null;
            List<coordinate> coordinates = new List<coordinate>();
            while ((line = labels_file.ReadLine()) != null)
            {
                string[] fields = line.Split(',');
                if (id != fields[0])
                {
                    if (id != null)
                    {
                        if (coordinates.Count != 0)
                            writeXML(id, coordinates);
                        coordinates = new List<coordinate>();
                    }
                    id = fields[0];
                }
                coordinate new_coordinate = new coordinate();
                int x1 = Convert.ToInt32(fields[1]);
                int y1 = Convert.ToInt32(fields[2]);
                int x2 = Convert.ToInt32(fields[3]);
                int y2 = Convert.ToInt32(fields[4]);
                if (y2 <= 533)
                {
                    if (x1 == 0) x1 = 1;
                    if (x2 >= 779) x2 = 778;
                    if (y1 == 0) y1 = 1;
                    if (y2 >= 529) y2 = 528;
                    new_coordinate.x1 = x1;
                    new_coordinate.y1 = y1;
                    new_coordinate.x2 = x2;
                    new_coordinate.y2 = y2;
                    coordinates.Add(new_coordinate);
                }
            }
            if (coordinates.Count != 0)
                writeXML(id, coordinates);
            trainval.Close();
            test.Close();
            labels_file.Close();
        }

        static XmlElement addXMLnode(XmlDocument xmldoc, XmlElement father_element, string name, string value = null)
        {
            XmlElement new_element = xmldoc.CreateElement(name);
            if (value != null)
                new_element.InnerText = value;
            father_element.AppendChild(new_element);
            return new_element;
        }

        static void writeXML(string id, List<coordinate> coordinates)
        {
            int _id = Convert.ToInt32(id.Substring(0, id.Length - 1));
            if (_id % 19 == 3)
                test.WriteLine(id);
            else
                trainval.WriteLine(id);
            string xml_filename = Path.ChangeExtension(id, "xml");
            string xml_fullfilename = Path.Combine(OUTPUT_PATH, xml_filename);
            XmlDocument xmldoc = new XmlDocument();
            XmlElement root_element = xmldoc.CreateElement("annotation");
            addXMLnode(xmldoc, root_element, "folder", "VOC2007");
            addXMLnode(xmldoc, root_element, "filename", Path.ChangeExtension(id, "jpg"));
            XmlElement _source = addXMLnode(xmldoc, root_element, "source");
            addXMLnode(xmldoc, _source, "database", "The VOC2007 Database");
            addXMLnode(xmldoc, _source, "annotation", "The TS Database");
            addXMLnode(xmldoc, _source, "image", "ccf-dataset");
            addXMLnode(xmldoc, _source, "flickrid", "null");
            XmlElement _owner = addXMLnode(xmldoc, root_element, "owner");
            addXMLnode(xmldoc, _owner, "flickrid", "null");
            addXMLnode(xmldoc, _owner, "name", "traffic-sign");
            XmlElement _size = addXMLnode(xmldoc, root_element, "size");
            addXMLnode(xmldoc, _size, "width", Convert.ToString(780));
            addXMLnode(xmldoc, _size, "height", Convert.ToString(530));
            addXMLnode(xmldoc, _size, "depth", Convert.ToString(3));
            addXMLnode(xmldoc, root_element, "segmented", Convert.ToString(0));
            foreach (coordinate each_coordinate in coordinates)
            {
                XmlElement _object = addXMLnode(xmldoc, root_element, "object");
                addXMLnode(xmldoc, _object, "name", "sign");
                addXMLnode(xmldoc, _object, "pose", "null");
                addXMLnode(xmldoc, _object, "truncated", Convert.ToString(0));
                addXMLnode(xmldoc, _object, "difficult", Convert.ToString(0));
                XmlElement _bndbox = addXMLnode(xmldoc, _object, "bndbox");
                addXMLnode(xmldoc, _bndbox, "xmin", Convert.ToString(each_coordinate.x1));
                addXMLnode(xmldoc, _bndbox, "ymin", Convert.ToString(each_coordinate.y1));
                addXMLnode(xmldoc, _bndbox, "xmax", Convert.ToString(each_coordinate.x2));
                addXMLnode(xmldoc, _bndbox, "ymax", Convert.ToString(each_coordinate.y2));
            }
            xmldoc.AppendChild(root_element);
            xmldoc.Save(xml_fullfilename);
        }
    }
}