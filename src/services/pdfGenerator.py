from PyPDF2 import PdfReader, PdfWriter, Transformation
import io
from reportlab.pdfgen.canvas import Canvas
from src.constants import (templates, FONT_PATH, WORD_PER_LINE, DEFAULT_FONT_SIZE, LINE_HEIGHT, CONTENT_WRAP_WIDTH, SIGNATURE_FONT_PATH, SIGNATURE_FONT_SIZE)
import random
from operator import itemgetter
from src.utils import wrap_text
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from src.services.openai import getMedicalContent

DOCTOR_NAMES = ['Harmesh Aggarwal', 'Naresh Garg', 'Ankit Maiti', 'Payal Sharma', 'Preeti Chauhan', 'Nitu Singh']
HOSPITALS_NAMES = ['Saraswati', 'Park', 'Narayana', 'SCI', 'Sheetla', 'GEM']

class GenerateFromTemplate:
    def __init__(self, templateLocation, fontPath=None):
        self.SELECTED_TEMPLATE = templates[random.randint(0, len(templates)-1)]
        self.templatePdf = PdfReader(open(templateLocation, 'rb'))
        self.templatePage = self.templatePdf.pages[0]
        self.signature = {
            "x": 100,
            "y": 100,
            'name': ''
        }
        
        if fontPath is not None:
            pdfmetrics.registerFont(TTFont('CustomFont', fontPath))
            
        if SIGNATURE_FONT_PATH is not None:
            pdfmetrics.registerFont(TTFont('SignatureFont', SIGNATURE_FONT_PATH))
        
        
        self.packet = io.BytesIO()
        self.c = Canvas(self.packet)
        
    def addText(self, text, point, fontSize = None, color = None, font=None):
        if color is not None:
            self.c.setFillColor(color)
            
        # if fontWeight is not None:
        #     self.c.setFont(fontSize)
        
        if font is not None:
            self.c.setFont(font, DEFAULT_FONT_SIZE)
            
        if fontSize is not None:
            self.c.setFontSize(fontSize)
            
        self.c.drawString(x=point[0], y=point[1], text=text)

    def addImage(self, image_path, point, width, height):
        self.c.drawImage(image_path, x=point[0], y=point[1], width=width, height=height)
        
    def addParagraph(self, content, point, fontSize = None, color = None, font=None, lineHeight = None):
        lines = content.split("\n")

        # Define the line height
        line_height = LINE_HEIGHT if lineHeight is None else lineHeight
        x,y = point[0], point[1]
        
        if color is not None:
            self.c.setFillColor(color)
            
        # if fontWeight is not None:
        #     self.c.setFont(fontSize)
        
        if font is not None:
            self.c.setFont(font, DEFAULT_FONT_SIZE)
            
        if fontSize is not None:
            self.c.setFontSize(fontSize)
            
        accessLines = ""

        # Draw each line
        for i, line in enumerate(lines):
            printableLine = (accessLines + " " if len(accessLines) > 0 else "") + line
            lineLen = len(printableLine)
            
            if lineLen > WORD_PER_LINE:
                nextWhiteSpaceIdx = -1
                for j in range(WORD_PER_LINE, WORD_PER_LINE+100):
                    if j >= lineLen or printableLine[j] == ' ':
                        nextWhiteSpaceIdx = j
                        break
                print("nextWhiteSpaceIdx", nextWhiteSpaceIdx)
                
                printableLine = printableLine[:nextWhiteSpaceIdx]
                accessLines = printableLine[nextWhiteSpaceIdx+1:]
            
            self.c.drawString(x, y - i * line_height, printableLine)
            
        while len(accessLines) >= WORD_PER_LINE:
            nextWhiteSpaceIdx = -1
            lineLen = len(accessLines)
            for j in range(WORD_PER_LINE, WORD_PER_LINE+100):
                    if j >= lineLen or accessLines[j] == ' ':
                        nextWhiteSpaceIdx = j
                        break
                    
            printableLine, accessLines = accessLines[:nextWhiteSpaceIdx], accessLines[nextWhiteSpaceIdx+1:]
            self.c.drawString(x, y - i * line_height, printableLine)
        
        self.signature["y"] = y - (i *line_height) - (2.5*line_height)
        self.signature["x"] = x + 5
        
    def addSignature(self):
        self.c.setFont('SignatureFont', SIGNATURE_FONT_SIZE)
        x, y, name = itemgetter("x", "y", "name")(self.signature)
        print("signature", x,y,name)
        self.c.drawString(x, y, name)
        
    def merge(self):
        self.c.save()
        self.packet.seek(0)
        
        resultPdf = PdfReader(self.packet)
        result = resultPdf.pages[0]
        
        self.output = PdfWriter()
        
        op = Transformation().rotate(0).translate(0,0)
        result.add_transformation(op)
        self.templatePage.merge_page(result)
        self.output.add_page(self.templatePage)
        
        
    def generate(self) -> io.BytesIO:
        pdfByteSteam = io.BytesIO()
        self.output.write(pdfByteSteam)
        pdfByteSteam.seek(0)
        return pdfByteSteam
    
    def fillDoctorDetails(self, specification = None, name = None):
        doctorName = name or random.choice(DOCTOR_NAMES)
        self.signature["name"] = doctorName
        nameConfig = self.SELECTED_TEMPLATE['placement']['doctorName']
        x, y, fontSize, color = itemgetter('x', 'y', 'fontSize', 'color')(nameConfig)
        self.addText(f'Dr. {doctorName}', (x, y), fontSize, color)
        
        doctorSpecification = (specification or 'General Physician').upper()
        specificationConfig = self.SELECTED_TEMPLATE['placement']['doctorSpecification']
        x, y, fontSize, color = itemgetter('x', 'y', 'fontSize', 'color')(specificationConfig)
        self.addText(doctorSpecification, (x, y), fontSize, color)
        
    def fillHospitalDetails(self):
        hospitalName = random.choice(HOSPITALS_NAMES)
        hospitalInfoConfig = self.SELECTED_TEMPLATE['placement']['hospitalInfo']
        x, y, fontSize, color = itemgetter('x', 'y', 'fontSize', 'color')(hospitalInfoConfig)
        self.addText(f'reachus@{hospitalName.lower()}hospital.com   |   +91 124 4570111', (x, y), fontSize, color)
        
    def fillDate(self, dateString):
        dateConfig = self.SELECTED_TEMPLATE['placement']['date']
        # date = datetime.strptime(dateString, '%d%d-%d%d-%Y')
        x, y, fontSize, color = itemgetter('x', 'y', 'fontSize', 'color')(dateConfig)
        self.addText(dateString, (x, y), fontSize, color)
        
    def fillContent(self, content):
        contentConfig = self.SELECTED_TEMPLATE['placement']['content']
        output_path='content.png'
        x, y, fontSize, color, width, height = itemgetter('x', 'y', 'fontSize', 'color', 'width', 'height')(contentConfig)
        wrappedContent = wrap_text(content, CONTENT_WRAP_WIDTH)
        self.addParagraph(wrappedContent, (x, y), fontSize=fontSize, color=color, font='CustomFont')
        
        # string_to_handwriting(wrappedContent, fontPath, output_path, (width+100, height+100))
        # self.addImage(output_path, (x,y), width, height)
    
    @staticmethod
    def buildMedical(patientName, patientAge, illness, startDate, endDate) -> io.BytesIO:
        print(patientName, patientAge, illness, startDate, endDate)
        gen = GenerateFromTemplate("templates/doctor-template-1.pdf", FONT_PATH)
        gen.fillDoctorDetails()
        gen.fillHospitalDetails()
        gen.fillDate(startDate)
        content = getMedicalContent(patientName, patientAge, illness, startDate, endDate)
        gen.fillContent(content)
        gen.addSignature()
        gen.merge()
        return gen.generate()
        
        

