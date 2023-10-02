from flask import Flask,redirect,url_for,render_template,request,Response
import cv2

app = Flask(__name__)

# Mark calculation code

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/fail/<int:score>')
def fail(score):
    return "Student failed the exam by the mark of " + str(score)

@app.route('/success/<int:score>')
def success(score):
    res = ""
    if score >=50:
        res = "PASS"
    else:
        res = "FAIL"
    exp = {'score':score,'result':res}
    return render_template("result.html",result = exp)

@app.route('/result/<int:score>')
def res(score):
    result = ''
    if(score<35):
        result = 'fail'
    else:
        result = 'success'
    return redirect(url_for(result,score=score))

@app.route('/submit',methods = ['POST','GET'])
def submit():
    total_score = 0
    if request.method == 'POST':
        science = float(request.form['science'])
        maths = float(request.form['maths'])
        total_score = (science+maths)/2
        print(science)
        print(maths)
        print(total_score)
    return redirect(url_for('success',score=total_score))


### Live Streaming code using cv2
camera = cv2.VideoCapture(0)
@app.route('/live')
def live():
    return render_template('video.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    while True:
        success,frame = camera.read()
        if not success:
            break
        else:
            ## This converts the frames to jpg format and return the two values one is boolean and another is memory buffer
            ret,buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



if __name__ == "__main__":
    app.run(debug=True)