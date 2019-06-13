from django.views.generic import View
from django.utils import timezone
from persona.models import Persona
from .render import Render
from django.shortcuts import render,redirect,get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden

from django.shortcuts import get_object_or_404
from django.contrib.staticfiles import finders
import os
from io import BytesIO
from reportlab.platypus.tables import Table, TableStyle, CellStyle, LongTable
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter, A4,  LETTER, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, BaseDocTemplate, Frame, PageTemplate, Image, TableStyle, Spacer, SimpleDocTemplate, PageBreak
from reportlab.lib.units import inch, cm, mm 
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from datetime import datetime
from persona.models import Persona
from django.db.models import Sum

from diezmos.models import Ingreso,Egreso



# Número de Página -----------------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
 
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
 
    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
 
    def draw_page_number(self, page_count):
        self.setFont("Helvetica-Bold", 7)
        self.drawRightString(25 * mm, 4 * mm + (0.3 * inch),"Página %d de %d" % (self._pageNumber, page_count))


# PDF de Persona -----------------------------------------------------------------------------
def HeaderFooterPersona(canvas,doc):
        canvas.saveState()
        title = "Reporte de Personas"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen = finders.find('assets/img/logo.jpg')
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 10,
                            fontName="Helvetica",
                            )   
        ta_l = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )
        ta_l7 = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 7,
                            fontName="Helvetica-Bold",
                            )
        ta_r = ParagraphStyle('parrafos', 
                            alignment = TA_RIGHT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )

        # Header
        header = Paragraph("REPORTE DE PERSONAS ",ta_l,)
        w,h = header.wrap(doc.width+250, doc.topMargin)
        header.drawOn(canvas, 215, doc.height -10 + doc.topMargin-80)

        #header1 = Paragraph("<u>DIRECCIÓN DE AGRICULTURA Y TIERRA</u> ",ta_r,)
        #w,h = header1.wrap(doc.width-115, doc.topMargin)
        #header1.drawOn(canvas, 140, doc.height -10 + doc.topMargin - 2)
        
        P1 = Paragraph('''N°''',ta_c)
        P2 = Paragraph('''CEDULA''',ta_c)
        P3 = Paragraph('''NOMBRE''',ta_c)
        P4 = Paragraph('''APELLIDO''',ta_c)
        P5 = Paragraph('''CORREO''',ta_c)
        P6 = Paragraph('''ROL''',ta_c)
        data = [[P1, P2, P3, P4, P5,P6]]
        header2 = Table(data, colWidths = [35,85,80,80,150,80])
        header2.setStyle(TableStyle( 
            [   
                ('GRID', (0, -1), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#50b7e6'),
                ('ALIGN', (0, 0), (-1, -3), "CENTER"),
            ]
            ))
        w,h = header2.wrap(doc.width-115, doc.topMargin)
        header2.drawOn(canvas, 42.5, doc.height -40 + doc.topMargin-93)

       

        # FOOTER

        footer4 = Paragraph("Fecha: "+str(fecha),ta_l7)
        w, h = footer4.wrap(doc.width -200, doc.bottomMargin) 
        footer4.drawOn(canvas,doc.height-105, doc.topMargin +620, h)

        canvas.restoreState()

def PersonaPDF(request):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    filtro = Persona.objects.all().exclude(nombre='Ofrenda').order_by('-id')
    if(request.GET['tipo']):
        tipo = request.GET['tipo']
        c = filtro.filter(roles=tipo)

    else:
        c =filtro
    if c:
        for i in c:
            count =count+1 
            data.append([count,i.cedula,i.nombre,i.apellido,i.correo,i.roles])
    else:
        return redirect('persona:personas')
    x = Table(data, colWidths = [35,85,80,80,150,80])
    x.setStyle(TableStyle(
        [   
            ('GRID', (0, 0), (12, -1), 1, colors.black),
            ('ALIGN',(0,0),(3,-1),'CENTER'),
            ('FONTSIZE', (0, 0), (4, -1), 8),   
        ]
    ))
    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterPersona,onLaterPages=HeaderFooterPersona,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response

# PDF de Persona -----------------------------------------------------------------------------
def HeaderFooterIngreso(canvas,doc):
        canvas.saveState()
        title = "Reporte de Ingresos"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen = finders.find('assets/img/logo.jpg')
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 10,
                            fontName="Helvetica",
                            )   
        ta_l = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )
        ta_l7 = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 7,
                            fontName="Helvetica-Bold",
                            )
        ta_r = ParagraphStyle('parrafos', 
                            alignment = TA_RIGHT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )

        # Header
        header = Paragraph("REPORTE DE INGRESOS ",ta_l,)
        w,h = header.wrap(doc.width+250, doc.topMargin)
        header.drawOn(canvas, 215, doc.height -10 + doc.topMargin-80)

        #header1 = Paragraph("<u>DIRECCIÓN DE AGRICULTURA Y TIERRA</u> ",ta_r,)
        #w,h = header1.wrap(doc.width-115, doc.topMargin)
        #header1.drawOn(canvas, 140, doc.height -10 + doc.topMargin - 2)
        
        P1 = Paragraph('''N°''',ta_c)
        P2 = Paragraph('''FECHA''',ta_c)
        P3 = Paragraph('''MONTO''',ta_c)
        P4 = Paragraph('''N° TRAN.''',ta_c)
        P5 = Paragraph('''TIPO DE PAGO''',ta_c)
        P6 = Paragraph('''PERSONA''',ta_c)
        data = [[P1, P2, P3, P4, P5,P6]]
        header2 = Table(data, colWidths = [35,85,80,80,150,80])
        header2.setStyle(TableStyle( 
            [   
                ('GRID', (0, -1), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#50b7e6'),
                ('ALIGN', (0, 0), (-1, -3), "CENTER"),
            ]
            ))
        w,h = header2.wrap(doc.width-115, doc.topMargin)
        header2.drawOn(canvas, 42.5, doc.height -40 + doc.topMargin-93)

       

        # FOOTER

        footer4 = Paragraph("Fecha: "+str(fecha),ta_l7)
        w, h = footer4.wrap(doc.width -200, doc.bottomMargin) 
        footer4.drawOn(canvas,doc.height-105, doc.topMargin +620, h)

        canvas.restoreState()

def IngresoPDF(request):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    filtro = Ingreso.objects.all().order_by('-fecha','-id')
    if(request.GET['tipo']):
        tipo = request.GET['tipo']
        c = filtro.filter(tipo_de_pago=tipo)

    else:
        c =filtro
    if c:
        for i in c:
            count =count+1 
            if int(i.tipo_de_pago_id) ==2:
                numero = 'No aplica'
            else:
                numero = i.numero_trans 
            data.append([count,i.fecha,str(i.monto)+' bs.',numero,str(i.tipo_de_pago.tipopago),i.persona.nombre])
    else:
        return redirect('diezmo:ingresos')
    x = Table(data, colWidths = [35,85,80,80,150,80])
    x.setStyle(TableStyle(
        [   
            ('GRID', (0, 0), (12, -1), 1, colors.black),
            ('ALIGN',(0,0),(3,-1),'CENTER'),
            ('FONTSIZE', (0, 0), (4, -1), 8),   
        ]
    ))
    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterIngreso,onLaterPages=HeaderFooterIngreso,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response

# PDF de Persona -----------------------------------------------------------------------------
def HeaderFooterEgreso(canvas,doc):
        canvas.saveState()
        title = "Reporte de Egresos"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen = finders.find('assets/img/logo.jpg')
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 10,
                            fontName="Helvetica",
                            )   
        ta_l = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )
        ta_l7 = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 7,
                            fontName="Helvetica-Bold",
                            )
        ta_r = ParagraphStyle('parrafos', 
                            alignment = TA_RIGHT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )

        # Header
        header = Paragraph("REPORTE DE EGRESOS ",ta_l,)
        w,h = header.wrap(doc.width+250, doc.topMargin)
        header.drawOn(canvas, 215, doc.height -10 + doc.topMargin-80)

        #header1 = Paragraph("<u>DIRECCIÓN DE AGRICULTURA Y TIERRA</u> ",ta_r,)
        #w,h = header1.wrap(doc.width-115, doc.topMargin)
        #header1.drawOn(canvas, 140, doc.height -10 + doc.topMargin - 2)
        
        P1 = Paragraph('''N°''',ta_c)
        P2 = Paragraph('''FECHA''',ta_c)
        P3 = Paragraph('''MONTO''',ta_c)
        P4 = Paragraph('''DESCRIPCIÓN''',ta_c)
        P5 = Paragraph('''CONCEPTO''',ta_c)
        data = [[P1, P2, P3, P4, P5]]
        header2 = Table(data, colWidths = [35,85,80,200,80])
        header2.setStyle(TableStyle( 
            [   
                ('GRID', (0, -1), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#50b7e6'),
                ('ALIGN', (0, 0), (-1, -3), "CENTER"),
            ]
            ))
        w,h = header2.wrap(doc.width-115, doc.topMargin)
        header2.drawOn(canvas, 57.5, doc.height -40 + doc.topMargin-93)

       

        # FOOTER

        footer4 = Paragraph("Fecha: "+str(fecha),ta_l7)
        w, h = footer4.wrap(doc.width -200, doc.bottomMargin) 
        footer4.drawOn(canvas,doc.height-105, doc.topMargin +620, h)

        canvas.restoreState()

def EgresoPDF(request):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    data = []
    filtro = Egreso.objects.all().order_by('-fecha','-id')
    if(request.GET['tipo']):
        tipo = request.GET['tipo']
        c = filtro.filter(concepto=tipo)

    else:
        c =filtro
    if c:
        for i in c:
            count =count+1 
            data.append([count,i.fecha,str(i.monto)+' bs.',i.descripcion,i.concepto])
    else:
        return redirect('diezmo:egresos')
    x = Table(data, colWidths = [35,85,80,200,80])
    x.setStyle(TableStyle(
        [   
            ('GRID', (0, 0), (12, -1), 1, colors.black),
            ('ALIGN',(0,0),(3,-1),'CENTER'),
            ('FONTSIZE', (0, 0), (4, -1), 8),   
        ]
    ))
    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterEgreso,onLaterPages=HeaderFooterEgreso,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response

# PDF de Persona -----------------------------------------------------------------------------
def HeaderFooterTrans(canvas,doc):
        canvas.saveState()
        title = "Reporte de Transacciones"
        canvas.setTitle(title)
        
        Story=[]
        styles = getSampleStyleSheet()
        
        archivo_imagen = finders.find('assets/img/logo.jpg')
        canvas.drawImage(archivo_imagen, 30, 720, width=540,height=100,preserveAspectRatio=True)

        fecha = datetime.now().strftime('%d/%m/%Y ')
        # Estilos de Párrafos
        ta_c = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 10,
                            fontName="Helvetica",
                            )   
        ta_l = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 13,
                            fontName="Helvetica-Bold",
                            )
        ta_l7 = ParagraphStyle('parrafos', 
                            alignment = TA_LEFT,
                            fontSize = 7,
                            fontName="Helvetica-Bold",
                            )
        ta_r = ParagraphStyle('parrafos', 
                            alignment = TA_CENTER,
                            fontSize = 11,
                            fontName="Helvetica-Bold",
                            )

        # Header
        header = Paragraph("REPORTE DE TRANSACCIONES ",ta_l,)
        w,h = header.wrap(doc.width+250, doc.topMargin)
        header.drawOn(canvas, 215, doc.height -10 + doc.topMargin-80)

        total1 = Paragraph("Total: "+str(total)+" bs.",ta_l,)
        w,h = total1.wrap(doc.width+250, doc.topMargin)
        total1.drawOn(canvas, 425, doc.height -10 + doc.topMargin-60)

        meses = Paragraph("Mes: "+str(mes1)+".",ta_l,)
        w,h = meses.wrap(doc.width+250, doc.topMargin)
        meses.drawOn(canvas, 75, doc.height -10 + doc.topMargin-60)

        #header1 = Paragraph("<u>DIRECCIÓN DE AGRICULTURA Y TIERRA</u> ",ta_r,)
        #w,h = header1.wrap(doc.width-115, doc.topMargin)
        #header1.drawOn(canvas, 140, doc.height -10 + doc.topMargin - 2)
        
        P1 = Paragraph('''N°''',ta_c)
        P2 = Paragraph('''FECHA''',ta_c)
        P3 = Paragraph('''TIPO''',ta_c)
        P4 = Paragraph('''MONTO''',ta_c)
        data = [[P1, P2, P3, P4]]
        header2 = Table(data, colWidths = [35,85,80,250])
        header2.setStyle(TableStyle( 
            [   
                ('GRID', (0, -1), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), '#50b7e6'),
                ('ALIGN', (0, 0), (-1, -3), "CENTER"),
            ]
            ))
        w,h = header2.wrap(doc.width-115, doc.topMargin)
        header2.drawOn(canvas, 72.5, doc.height -40 + doc.topMargin-93)

       

        # FOOTER

        footer4 = Paragraph("Fecha: "+str(fecha),ta_l7)
        w, h = footer4.wrap(doc.width -200, doc.bottomMargin) 
        footer4.drawOn(canvas,doc.height-105, doc.topMargin +620, h)

        canvas.restoreState()

def TranPDF(request):
    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    doc = SimpleDocTemplate(buffer,
        pagesizes=letter,
        rightMargin = 30,
        leftMargin= 30,
        topMargin=176.9,
        bottomMargin=50,
        paginate_by=0,
    )
    ta_r = ParagraphStyle('parrafos', 
        alignment = TA_RIGHT,
        fontSize = 13,
        fontName="Helvetica-Bold",
        )
    persona=[]
    styles = getSampleStyleSheet()
    # TABLA NUMERO 1
    count = 0
    meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septimbre","Octubre","Noviembre","Diciembre"]
    data = []
    if "year" in request.GET and "mes" in request.GET :
        mes = request.GET['mes']
        year = request.GET['year']
    
    else:
        mes = datetime.now().month
        print(mes)
        year = datetime.now().year
    ingreso = Ingreso.objects.filter(fecha__month=mes,fecha__year=year).values_list("fecha_t","monto","disponible","tipo","id")
    ingreso1 = Ingreso.objects.filter(fecha__month=mes,fecha__year=year).aggregate(Sum('monto'))
    egreso = Egreso.objects.filter(fecha__month=mes,fecha__year=year).values_list("fecha_t","monto","disponible","tipo","id")
    global total,mes1
    mes1 = meses[int(mes)-1]

    total = ingreso1['monto__sum']
    transaccion = ingreso.union(egreso).order_by('-fecha_t','-id')
    tran = []
    if transaccion:
        for i in transaccion:
            if i[3] == True:
                tipo = 'Ingreso'
                monto = "{:,}".format(int(i[1])).replace(',','.')
            else:
                tipo = 'Egreso'
                monto = "-{:,}".format(int(i[1])).replace(',','.')
            count =count+1 
            data.append([
            count,
            i[0].date(),
            tipo,
            monto]
            )
    else:
        return redirect('diezmo:transacciones')
    x = Table(data, colWidths = [35,85,80,250])
    x.setStyle(TableStyle(
        [   
            ('GRID', (0, 0), (8, -1), 1, colors.black),
            ('ALIGN',(0,0),(3,-1),'CENTER'),
            ('FONTSIZE', (0, 0), (3, -1), 8),   
        ]
    ))
    persona.append(x)

    doc.build(persona,onFirstPage=HeaderFooterTrans,onLaterPages=HeaderFooterTrans,canvasmaker=NumberedCanvas)
    response.write(buffer.getvalue())
    buffer.close()

    return response