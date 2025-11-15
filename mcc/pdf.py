"""
from fpdf import FPDF #pip install fpdf 
 

@app.route('/download/report/pdf')
def download_report():
    try:
 
        pdf = FPDF()
        pdf.add_page()
         
        page_width = pdf.w - 2 * pdf.l_margin
         
        pdf.set_font('Times','B',14.0) 
        pdf.cell(page_width, 0.0, 'Employee Data', align='C')
        pdf.ln(10)
 
        pdf.set_font('Courier', '', 12)
         
        col_width = page_width/4
         
        pdf.ln(1)
         
        th = pdf.font_size
         
        pdf.ln(10)
         
        pdf.set_font('Times','',10.0) 
        pdf.cell(page_width, 0.0, '- end of report -', align='C')
         
        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'inline;filename=employee_report.pdf'})
    except Exception as e:
        print(e)
   
 """