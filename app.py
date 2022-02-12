from flask import Flask,render_template,request
from flask_mysqldb import MySQL
import mpu

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'dealercrawlerv3m2-crawl232.vindb.org'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'S@ikrishnan1'
app.config['MYSQL_DB'] = 'cars_db'

mysql = MySQL(app)





@app.route('/', methods=['GET', 'POST'])

def index():

  def calculator(zipArr,lon1,lat1):
      for j in zipArr:
          lon2 = float(j["lon"])
          lat2 = float(j["lat"])
          coords_1 = (lon1,lat1)
          coords_2 = (lon2,lat2)
          #Calculating and converting to miles
          diffDistance = (mpu.haversine_distance(coords_1, coords_2))*0.621371

          if diffDistance <= int(distance):
              neighbourZip.append(j["zip"])
      return neighbourZip


  if request.method == "POST":
      details = request.form
      zipvalue = details['zip']
      distance = details['distance']
      cur = mysql.connection.cursor()
      a = cur.execute("SELECT * FROM zips")
      zipdb = cur.fetchall()

      zipArr = []
      zipArr.clear()
      flag = False

      #Storing zip , logitude and latitude in array of dictionaries
      for val in zipdb:
          zipDict = {"zip":val[0],"lon":val[2],"lat":val[3]}
          zipArr.append(zipDict)

      #Validating user input
      for i in zipArr:
          if i["zip"] == zipvalue and  flag !=True:
              flag = True
              lon1 = float(i["lon"])
              lat1 = float(i["lat"])


      neighbourZip = []
      if flag == True:
          #Function for distance
          neighbourZip = calculator(zipArr,lon1,lat1)
          #Getting result from final table
          l = tuple(neighbourZip)
          p = {'l':l}
          query = "SELECT * FROM final WHERE ZipCode IN %(l)s"
          result = cur.execute(query,p)
          latresult = cur.fetchall()
          return render_template('direct.html',a = latresult)



  return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True,host='192.206.41.161')