from django.shortcuts import render, HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
import pygal


# Create your views here.
def index(request):
   return render(request,'desktopapp/index.html')

def login(request):
   return render(request,'desktopapp/login.html')

def dashboard(request):
    return render(request,'desktopapp/dashboard.html')

def home(request):
    global df
    if request.method == 'POST':
        file = request.FILES["myFile"]
        df = pd.read_csv(file, encoding='unicode_escape')
        df.columns = df.columns.str.lower()
        check_text("Create a line graph of avg of totalBalance and day")
        print(f"hey {svg_path}")
        return render(request, 'index.html', {"something": True, "df": df, "svg_path": svg_path})
    else:
        return render(request, 'index.html')


def upload(request):
    return render(request, 'fileupload.html')


def check_text(text):
    global svg_path
    synonyms = ["create", "draw", "make", "generate", "produce"]
    text = text.lower()
    for word in synonyms:
        if word in text:
            match = check_columns(text)
            # print(match)
            if match:
                if "bar chart" in text:
                    svg_path = create_bar_chart(text, match)
                elif "line graph" or "line chart" in text:
                    svg_path = create_line_chart(text, match)
                else:
                    print("The text does not contain any valid chart command.")
            else:
                print("No valid column names or data field present in the command.")
        else:
            print(
                "The text does not contain any of the synonyms of the words 'create', 'draw', 'make'.")


def check_columns(text):
    # storing the column names or field names present in the data

    column_names = df.columns
    column_names = [col.lower() for col in column_names]
    # print(column_names)
    # match list will store all the column names that appear in the text in the same order
    match = []
    for col in column_names:
        if col in text:
            match.append(col)
    print(f' Printing line 50 {match}')
    return match


def create_line_chart(text, col):
    # import re
   # col[totalBalance,day]
    # Create a bar chart of sum of totalBalance and day
    operation = None
    y_col = col[0]
    x_col = col[1]
    operation_words = ["between","sum of", "avg of", "max of", "min of", "total of", "average of", "maximum of", "minimum of",
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
            y_col = text[operation_index +
                         len(operation):].strip().split(" ")[0]
            x_col = [c for c in col if c != y_col][0]
            print(f' Printing line 74 {y_col,x_col}')
    print(f'print line 75 {df[y_col].dtype}')
    if (df[x_col].dtype in ["int64", float] or df[y_col].dtype in ["int64", float]):
        if operation == "sum of" or operation == "total" or operation == "sum":
            chart = pygal.Line()
            chart.title = f"{operation} {y_col} by {x_col}"
            chart.x_labels = df[x_col].unique()
            chart.add(y_col, df.groupby(x_col)[y_col].sum())

        elif operation == "avg of" or operation == "average" or operation == "avg":
            chart = pygal.Line()
            chart.title = f"{operation} of {y_col} by {x_col}"
            chart.x_labels = df[x_col].unique()
            chart.add(y_col, df.groupby(x_col)[y_col].mean())
        elif operation == "min of" or operation == "minimum":
            chart = pygal.Line()
            chart.title = f"{operation} of {y_col} by {x_col}"
            chart.x_labels = df[x_col].unique()
            chart.add(y_col, df.groupby(x_col)[y_col].min())
        elif operation == "max" or operation == "maximum":
            chart = pygal.Line()
            chart.title = f"{operation} of {y_col} by {x_col}"
            chart.x_labels = df[x_col].unique()
            chart.add(y_col, df.groupby(x_col)[y_col].max())
        else:
            return "Invalid operation or column names not found."

        charttitle = chart.title+""
        charttitle = remove(charttitle)
        print(charttitle)
        chart.render_to_file(f'uploads/Files/{charttitle}.svg')
        print("uploads/Files/"+charttitle+".svg")
        return "uploads/Files/"+charttitle+".svg"
    else:
        print("At least one column must be numerical")


def create_bar_chart(text, col):
    operation = None
    y_col = col[0]
    x_col = col[1]
    operation_words = [ "sum of", "avg of", "max of", "min of", "total of", "average of", "maximum of", "minimum of",
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
                y_col = text[operation_index +
                             len(operation):].strip().split(" ")[0]
                x_col = [c for c in col if c != y_col][0]
                print(f' Printing line 74 {y_col,x_col}')
        print(f'print line 75 {df[y_col].dtype}')
        if (df[x_col].dtype in ["int64", float] or df[y_col].dtype in ["int64", float]):
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
            elif operation == "min of" or operation == "minimum":
                chart = pygal.Bar()
                chart.title = f"{operation} of {y_col} by {x_col}"
                chart.x_labels = df[x_col].unique()
                chart.add(y_col, df.groupby(x_col)[y_col].min())
            elif operation == "max" or operation == "maximum":
                chart = pygal.Bar()
                chart.title = f"{operation} of {y_col} by {x_col}"
                chart.x_labels = df[x_col].unique()
                chart.add(y_col, df.groupby(x_col)[y_col].max())
            else:
                return "Invalid operation or column names not found."

            charttitle = chart.title+""
            charttitle = remove(charttitle)
            print(charttitle)
            chart.render_to_file(f'uploads/Files/{charttitle}.svg')
            print("uploads/Files/"+charttitle+".svg")
            return "uploads/Files/"+charttitle+".svg"
        else:
            print("At least one column must be numerical")


def remove(string):
    return string.replace(" ", "_")
