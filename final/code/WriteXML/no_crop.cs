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
        const string LABEL_FILE = "train.csv";
        const string OUTPUT_PATH = @"Annotations";
        const string OUTPUT_TRAINVAL = @"ImageSets\Main\trainval.txt";

        static StreamWriter trainval;
        static void Main(string[] args)
        {
            StreamReader labels_file = new StreamReader(LABEL_FILE);
            trainval = new StreamWriter(OUTPUT_TRAINVAL);
            string line, id = null;
            List<coordinate> coordinates = new List<coordinate>();
            while ((line = labels_file.ReadLine()) != null)
            {
                string[] fields = line.Split(',');
                string current_id = fields[0];
                if (id != current_id)
                {
                    if (id != null)
                    {
                        writeXML(id, coordinates);
                        coordinates = new List<coordinate>();
                    }
                    id = current_id;
                }
                coordinate new_coordinate = new coordinate();
                //边界处理，防止减一、加一出错
                int x1 = Convert.ToInt32(fields[1]);
                if (x1 == 0) x1 = 1;
                int y1 = Convert.ToInt32(fields[2]);
                if (y1 == 0) y1 = 1;
                int x2 = Convert.ToInt32(fields[3]);
                if (x2 == 1279) x2 = 1278;
                int y2 = Convert.ToInt32(fields[4]);
                if (y2 == 719) y2 = 718;
                new_coordinate.x1 = x1;
                new_coordinate.y1 = y1;
                new_coordinate.x2 = x2;
                new_coordinate.y2 = y2;
                coordinates.Add(new_coordinate);
            }
            writeXML(id, coordinates);
            trainval.Close();
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
            addXMLnode(xmldoc, _size, "width", Convert.ToString(1280));
            addXMLnode(xmldoc, _size, "height", Convert.ToString(720));
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