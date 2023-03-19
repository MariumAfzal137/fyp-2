from django.shortcuts import render,redirect
import pandas as pd
import matplotlib.pyplot as plt
import pygal
from .models import createUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def registerPage(request):
    form=createUserForm()

    if request.method== 'POST':
      form=createUserForm(request.POST)
      if form.is_valid():
         form.save()
         user=form.cleaned_data.get('username')
         messages.success(request,'Account was created for '+user)
         return redirect('login')
    
    context={"form":form}        
    return render(request,'register.html',context)
def loginPage(request):
   if request.method== "POST":
      username=request.POST.get('username')
      password=request.POST.get('password')

      user=authenticate(request,username=username,password=password)

      if user is not None:
         login(request,user)
         return redirect('upload')
      else:
         messages.info(request,'Username or Password is incorrect')
         
   context={}
   return render(request,'login.html',context)

def logoutUser(request):
   logout(request)
   return redirect('login')

def home(request):
    global df
    if request.method=='POST':
        file=request.FILES["myFile"]
        df=pd.read_csv(file,encoding='unicode_escape')
        df.columns=df.columns.str.lower()
        check_text("Create a bar chart of avg of totalBalance and day")
        print(f"hey {svg_path}")
        return render(request,'index.html',{"something":True,"df":df,"svg_path":svg_path})
    else:
        return render(request,'index.html')

def upload(request):
    return render(request,'fileupload.html')

def check_text(text):
    global svg_path
    synonyms = ["create", "draw", "make", "generate", "produce"]
    text = text.lower()
    for word in synonyms:
        if word in text:
            if "bar chart" in text:
                match = check_columns(text)
                #print(match)
                if match:
                    svg_path=create_bar_chart(text,match)
                else:
                    print("No valid column names or data field present in the command.")
            else:
                print("The text does not contain any valid chart command.")
            break
    else:
        print("The text does not contain any of the synonyms of the words 'create', 'draw', 'make'.")

def check_columns(text):
    #storing the column names or field names present in the data

    column_names = df.columns
    column_names = [col.lower() for col in column_names]
    #print(column_names)
    #match list will store all the column names that appear in the text in the same order
    match = []
    for col in column_names:
        if col in text:
            match.append(col)
    print(f' Printing line 50 {match}')
    return match

def create_bar_chart(text,col):
    # import re
   #col[totalBalance,day]
    # Create a bar chart of sum of totalBalance and day
    operation = None
    y_col = col[0]
    x_col = col[1]
    operation_words = ["sum of", "avg of", "max of", "min of", "total of", "average of", "maximum of", "minimum of", 
                        "sum", "avg", "max", "min", "total", "average", "maximum", "minimum"]
    text = text.lower()
    for word in operation_words:
        if word in text:
            operation = word
            break
    if operation:
        operation_index = text.find(operation)
        # 5+1 text[6:].strip
        if operation_index != -1:
          y_col= text[operation_index + len(operation):].strip().split(" ")[0]
          x_col = [c for c in col if c != y_col][0]
          print(f' Printing line 74 {y_col,x_col}')
    print(f'print line 75 {df[y_col].dtype}')
    if (df[x_col].dtype in ["int64",float] or df[y_col].dtype in ["int64",float]):
        if operation == "sum of" or operation == "total":
         chart = pygal.Bar()
         chart.title = f"{operation} {y_col} by {x_col}"
         chart.x_labels = df[x_col].unique()
         chart.add(y_col, df.groupby(x_col)[y_col].sum())
     
        elif operation == "avg of" or operation == "average":
         chart = pygal.Bar()
         chart.title = f"{operation} of {y_col} by {x_col}"
         chart.x_labels = df[x_col].unique()
         chart.add(y_col, df.groupby(x_col)[y_col].mean())
        elif operation== "min of" or operation== "minimum":
         chart = pygal.Bar()
         chart.title = f"{operation} of {y_col} by {x_col}"
         chart.x_labels = df[x_col].unique()
         chart.add(y_col, df.groupby(x_col)[y_col].min())
        elif operation== "max" or operation== "maximum":
         chart = pygal.Bar()
         chart.title = f"{operation} of {y_col} by {x_col}"
         chart.x_labels = df[x_col].unique()
         chart.add(y_col, df.groupby(x_col)[y_col].max())
        else:
         return "Invalid operation or column names not found."

        charttitle=chart.title+""
        charttitle=remove(charttitle)
        print(charttitle)
        chart.render_to_file(f'uploads/Files/{charttitle}.svg')
        print("uploads/Files/"+charttitle+".svg")
        return "uploads/Files/"+charttitle+".svg"
    else:
        print("At least one column must be numerical")

def remove(string): 
    return string.replace(" ", "_")
