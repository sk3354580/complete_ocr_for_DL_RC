import os,cv2,pytesseract
import re
from flask import Flask, render_template, request,jsonify
from PIL import Image
app = Flask(__name__)
UPLOAD_FOLDER = os.path.basename('.')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/',methods=['GET'])
def home():
    return render_template('upload.html')
@app.route('/sugar', methods=['POST'])
def upload_file():
    if request.method == "POST":
        file = request.files['image']
        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(f)
        image = cv2.imread(UPLOAD_FOLDER+"/"+file.filename)

        text = pytesseract.image_to_string(image)
        dicc={"Registration_no":"Not Found","Engine_no":"Not Found","Chasis_no":"Not Found","Register_date":"Not Found","Name":"Not Found","Manufacturing_Date":"Not Found"}
        final_data1 = []
###engine numer
        if re.findall(r'\b([A-Z0-9]{5}[0-9]{7})\b',text):
            dicc['Engine_no'] =re.findall(r'\b([A-Z0-9]{5}[0-9]{7})\b',text)
        elif re.findall(r'\b([A-Z0-9]{5}[0-9]{6,7})\b',text):
            dicc['Engine_no']=re.findall(r'\b([A-Z0-9]{5}[0-9]{6,7})\b',text)
        elif re.findall(r'\b([A-Z0-9]{6}[0-9]{6})\b',text):
            dicc['Engine_no']=re.findall(r'\b([A-Z0-9]{6}[0-9]{6})\b',text)
        elif re.findall(r'[A-Z][0-9]\w{3,4}\s?\d{5,6}',text):
            dicc['Engine_no']=re.findall(r'[A-Z][0-9]\w{3,4}\s?\d{5,6}',text)
        elif re.findall(r'\b([0-9]{7,9})\b',text):
            dicc['Engine_no']=re.findall(r'\b([0-9]{7,9})\b',text)
        final_data1.append(dicc)
        print("Text in Image :\n",text)
        #####Registration number
        if re.findall(r'\b([A-Z]{2}[0-9A-Z]{4}[0-9]{4})\b',text):
            dicc["Registration_no"]=re.findall(r'\b([A-Z]{2}[0-9A-Z]{4}[0-9]{4})\b',text)
        elif re.findall(r'\b([A-Z]{2}[0-9A-Z]{3}[\s][0-9]{4}|[A-Z]{1}[0-9A-Z]{4,5}[\s][0-9]{4})\b',text):
            dicc["Registration_no"]=re.findall(r'\b([A-Z]{2}[0-9A-Z]{3}[\s][0-9]{4}|[A-Z]{1}[0-9A-Z]{4,5}[\s][0-9]{4})\b',text)
        elif re.findall(r'\b([A-Z]{2}[0-9A-Z]{2}[-][A-Z]{1}[-][0-9]{4})\b',text):
            dicc["Registration_no"]=re.findall(r'\b([A-Z]{2}[0-9A-Z]{2}[-][A-Z]{1}[-][0-9]{4})\b',text)
####chasis number
        if re.findall(r'\b([A-Z0-9]{14,})\b',text):
            dicc['Chasis_no']=re.findall(r'\b([A-Z0-9]{14,})\b',text)
## Registeration Date
        if re.findall(r"\d{1,2}[/-]\w{2,}[/-]\d{4}",text):
            dicc["Register_date"] = re.findall(r"\d{1,2}[/-]\w{2,}[/-]\d{4}",text)
        if re.findall(r"[^\/]\d{1,2}[/]\d{4}",text):
            dicc['Manufacturing_Date']=re.findall(r"[^\/]\d{1,2}[/]\d{4}",text)
        for wordlist in text.split('\n'):
            xx = wordlist.split()
            if [w for w in xx if re.search('(NAME|Name)$', w)]:
                    dicc['Name'] = wordlist

        return jsonify(dicc)

app.run("0.0.0.0",5000,threaded=True,debug=True)

