from flask import Flask , render_template, flash, redirect, url_for, session, request, logging
from data import Products
import mysql.connector
import os



app = Flask(__name__)
app.secret_key="123"
app.config['SESSION_TYPE'] = 'filesystem'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="myflask"
)
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mycursor = mydb.cursor()

#sql = "INSERT INTO products (name,image,description) VALUES (%s,%s, %s)"
#val = ("Bootstrap","../static/assets/bootstarplogo.png","disc")
#mycursor.execute(sql,val)
#mydb.commit()

#val = "test_name"
#mycursor.execute("select * from users where username = %s", (val,))
#result = mycursor.fetchone()

#print(result[0] + result[1] + result[2] +result[3])



#Products = Products()
#f = open('templates/here2.html','w')



#image = "../static/assets/css.png"
#name  ="any name"
#dis = "this is dis"
#message = '<div class="media" style="width: 70%; margin: 5% auto"> <img class="mr-3" src="'+image+'" alt="Generic placeholder image"><div class="media-body"> <h5 class="mt-0">'+name+'</h5> <p class="lead">'+dis+'</p></div></div>'
#m = "{% extends 'layout.html'%}{% block body %}"+ message+ '{% endblock %}'


#f.write(m)
#f.close()


def addReadMorePage(name , image , dis):
     f = open('templates/'+name +'.html','w')
     print("ennnn")
     message = '<div class="media" style="width: 70%; margin: 5% auto"> <img class="mr-3" src="'+image+'" alt="Generic placeholder image"><div class="media-body"> <h5 class="mt-0">'+name+'</h5> <p class="lead">'+dis+'</p></div></div>'
     message = "{% extends 'layout.html'%}{% block body %}"+ message+ '{% endblock %}'
     f.write(message)
     f.close()

def getData(form):
    return form.get("name"),form.get("link"),form.get("dis")

@app.route("/goTo/<string:name>")
def any(name):
    return render_template(name+".html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/pepe")
def pepe():
        return render_template("pepe.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/dashboard")
def dashboard():
    mycursor.execute("select * from products")
    products = mycursor.fetchall()
    mycursor.execute("select * from users")
    users = mycursor.fetchall()
    return render_template("dashboard.html" , Products = products, Users = users)

@app.route("/delete_user/<string:username>")
def delete_user(username):
    print(username)
    mycursor.execute("delete FROM users where username = %s",(username,))
    mydb.commit()
    print("ennnnn")
    flash("A USer is been deleted!","success")
 
    return  redirect(url_for('dashboard'))

@app.route("/delete/<string:id>")
def delete(id):
     mycursor.execute("select name from products where product_ID = %s",(id,))
     oldName = mycursor.fetchone()
     os.remove("templates/"+oldName[0] +".html")
     mycursor.execute("delete FROM products  where product_ID = %s",(id,))
     mydb.commit()
     flash("A product is been deleted!","success")
     
     return  redirect(url_for('dashboard'))
     
    
     

@app.route("/edit_product/<string:id>/", methods=["GET", "POST"])
def edit(id):
       mycursor.execute("select * FROM products where product_ID = %s",(id,))
       product = mycursor.fetchone()
       oldName = product[1]
       request.form.name = product[1]
       request.form.link = product[2]
       request.form.dis = product[3]
       if request.method == "POST":
                    
                    pname,image,dis = getData(request.form)
                    mycursor.execute("select name FROM products where name = %s and product_ID <> %s",(pname,id))
                    product = mycursor.fetchone()
                    if product == None:
                      os.remove("templates/"+oldName +".html")
                      addReadMorePage(pname,image,dis)
                      mycursor.execute("update products set name = %s, image = %s, description = %s where product_ID = %s",(pname,image,dis,id))
                      mydb.commit()
                      flash("A Product is been Edited","success")
                      return render_template("editProduct.html")
                    else:
                          flash("There is a product with the same name, please change the name ","danger")
                          return render_template("editProduct.html")
              
              

       return render_template("editProduct.html")





@app.route("/edit_user/<string:username>/", methods=["GET", "POST"])
def edit_user(username):
       print(username)
       mycursor.execute("select email , address from users where username = %s" ,(username,))
       userData =mycursor.fetchone()
       request.form.email = userData[0]
       request.form.address= userData[1]
      
       if request.method == "POST":
                    
                    email = request.form.get("email")
                    password = request.form.get("password")
                    address = request.form.get("address")
                    confirm =  request.form.get("confirm")
                    #SELECT username from users where email = 'any@.com' and username not in (SELECT username FROM users where username = 'any12' and email='any@.com')
                    mycursor.execute("SELECT email from users where email = %s and username <> %s" , (email,username))
                    user = mycursor.fetchone()
                    if user == None:
                      mycursor.execute("update users set email = %s, password = %s, address = %s where username = %s",(email,password,address,username))
                      mydb.commit()
                      flash("A User is been Edited","success")
                      return render_template("editUser.html")
                    else:
                          flash("This email is alredy exists , please change the email ","danger")
                          return render_template("editUser.html")
              
              

       return render_template("editUser.html")


@app.route("/add_product", methods=["GET", "POST"])
def add():
    if request.method == "POST":
       # name = request.form.get("name")
        #image = request.form.get("link")
        #dis = request.form.get("dis")
        name,image,dis = getData(request.form)
        if(image == ""):
         image = "https://cdn.pixabay.com/photo/2018/01/14/23/12/nature-3082832_960_720.jpg"

        mycursor.execute("select * from products where name= %s",(name,))
        result = mycursor.fetchone()
        if result == None:
            #f = open('templates/'+name +'.html','w')
            #message = '<div class="media" style="width: 70%; margin: 5% auto"> <img class="mr-3" src="'+image+'" alt="Generic placeholder image"><div class="media-body"> <h5 class="mt-0">'+name+'</h5> <p class="lead">'+dis+'</p></div></div>'
            #message = "{% extends 'layout.html'%}{% block body %}"+ message+ '{% endblock %}'
            #f.write(message)
            #f.close()
            addReadMorePage(name,image,dis)
            mycursor.execute("insert into products(name , image , description) values(%s,%s,%s)",(name,image,dis))
            mydb.commit()
            flash("A Product is been insrted","success")
            return redirect(url_for('add'))
        else:
            flash("There is a product with the same name, please change the name ","danger")
            return render_template("addProduct.html")


    return render_template("addProduct.html")

@app.route("/products")
def products():

    mycursor.execute("select * from products")
    Products = mycursor.fetchall()
    return render_template("products.html",products= Products)

@app.route("/search", methods=["GET" , "POST"])
def search():
   if request.method == "POST":  
    name = request.form.get("name")
    name = '%' + name +'%'
    mycursor.execute("select * from products where name like %s" ,(name,))
    Products = mycursor.fetchall()
    print(Products)
    if Products != []:
      print("enn")
      return render_template("products.html",products= Products)
    else:
        flash("Cant find anything","danger")
        return 


   return render_template("search.html")

@app.route("/", methods =["GET","POST"])
def login(): 
    if request.method == "POST":
        username = request.form.get("name") # get the form by name
        password = request.form.get("password")
        mycursor.execute("select * from users where username = %s",(username,))
        result = mycursor.fetchone()
        if result != None:
            if(password == result[1]):
                flash("Loged in successfuly","success")
                return redirect(url_for('login'))
            else:
                  flash("the password is not correct !","danger")
                  return render_template("login.html")
        else:
             flash("the username is not correct !","danger")
             return render_template("login.html")


    return render_template("login.html")

@app.route("/signup", methods =["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        address = request.form.get("address")
        confirm = request.form.get("confirm")
        email = request.form.get("email")
        role = "user"
        mycursor.execute("select * from users where username = %s",(username,)) 
        usernameRes = mycursor.fetchone()
        mycursor.execute("select * from users where email = %s",(email,)) 
        emailRes = mycursor.fetchone()
        print(usernameRes)
        print(emailRes)
        if usernameRes == None and emailRes == None :
            if confirm == password:
                val = (username,password,email,role,address)
                mycursor.execute("insert into users(username,password,email,role,address) values(%s,%s,%s,%s,%s)",val)
                mydb.commit()
                flash("all Done !","success")
                return redirect(url_for("signup"))
            else:
                flash("You didn't enter the same password, what a shame :-)","danger")
                return render_template("signup.html")
        else:
             flash("The username or email is already exists","danger")
             return render_template("signup.html")



    return render_template("signup.html")



if __name__ == '__main__':
    app.run(debug=True)