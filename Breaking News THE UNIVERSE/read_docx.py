import zipfile
import xml.etree.ElementTree as ET

docx_file = r"C:\Users\start\Downloads\Juego.docx"

def extract_text(docx_file):
    try:
        with zipfile.ZipFile(docx_file) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            paragraphs = []
            for p in tree.findall('.//w:p', ns):
                texts = [node.text for node in p.findall('.//w:t', ns) if node.text]
                if texts:
                    paragraphs.append(''.join(texts))
            return '\n'.join(paragraphs)
    except Exception as e:
        return str(e)

text = extract_text(docx_file)
with open(r"D:\Game jam\BREAK-THE-WORLD-unisabana-gamejam-2026\Breaking News THE UNIVERSE\gdd.txt", "w", encoding="utf-8") as f:
    f.write(text)
print("Dumped to gdd.txt")
