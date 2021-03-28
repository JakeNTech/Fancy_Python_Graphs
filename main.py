# TTDS - 2021
# JakeNTech
# main.py
import pandas
import numpy as np
import matplotlib.pyplot as plt
import argparse
import seaborn as sns

def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="input_file", help="Name of the csv file to use for points", metavar="<filename>",required=True)
    parser.add_argument("-t","--title",dest="graph_title",help="The graph will have a title...this is how to specify it",metavar="<integer>",default="A Amazing Graph")
    parser.add_argument("-a","--average",dest="average",help="Plot Average line",action="store_true")
    parser.add_argument("-b","--best_fit",dest="bestfit",help="Calculate and plot average",action="store_true")
    parser.add_argument("-m","--heat_map",dest="heatmap",help="Plot data onto a heat map",action="store_true")
    parser.add_argument("-p","--pair_plot",dest="pairplot",help="sns pairplot",action="store_true")
    return parser.parse_args()

def readCSV(filename):
    return pandas.read_csv(filename, delimiter=',')

def line_with_best_fit(data, title_text,x_axis_data,y_axis_data):
    f = plt.figure()
    f.subplots_adjust(right=0.8)
    plt.title(title_text, color='black')
    x = np.array(data[x_axis_data])
    y = np.array(data[y_axis_data])
    m, b = np.polyfit(x, y, 1) 
    plt.plot(x, y)
    plt.plot(x, m*x + b) # Plot line of best fit
    plt.savefig('./Graphs/output.png')

#This function is custom to the ./Data/cars.csv file!
def many_lines_with_best_fit(data):
    colum_names = list(data.columns)
    for i in range(1,len(colum_names)):
        #print(colum_names[i])
        f = plt.figure()
        f.subplots_adjust(right=0.8)
        text = "Cars in "+colum_names[i]+" since '94"
        plt.title(text, color='black')
        x = np.array(data["Year"])
        y = np.array(data[colum_names[i]])
        m, b = np.polyfit(x, y, 1) 
        plt.plot(x, m*x + b) # Plot line of best fit
        plt.savefig("./Graphs/"+colum_names[i]+".png")

def check_and_remove_Total_Average(data):
    colum_names = list(data.columns)
    for i in range(1,len(colum_names)):
        if colum_names[i].lower()=="total" or colum_names[i].lower()=="average":
            data = data.drop(colum_names[i],axis=1)
    return data
#Calculate and add an average column to given data
def add_average_col(data):
    average = []
    for i in range(0,len(data.loc[:,list(data.columns)[0]])):
        col = list(data.loc[i,:])
        total = 0
        for j in range(1,len(col)):
            total = total + col[j]
        average.append(total/(len(col)-1))
    data["Average"] = average
    return(data)

#Plot Graph
def test(data, title_text,best_fit, average):
    # Start Graph Plot
    f = plt.figure()
    f.subplots_adjust(right=0.8)
    f.subplots_adjust(right=0.8)
    colum_names = list(data.columns)
    for i in range(1,len(colum_names)):
        #print(colum_names[i])
        if colum_names[i]=="Total" or colum_names[i]=="Average":
            break
        plt.plot(np.array(data[colum_names[0]]), np.array(data[colum_names[i]]), label=colum_names[i])
    # Calculate the line of best fit from the average column.
    # This probably isn't the correct way to do it but the only way I can think of to do it over multiple lines/data
    # If you can't tell I am also rubbish at maths
    # It looks about right so....
    if best_fit==True:
        m, b = np.polyfit(np.array(data[colum_names[0]]), np.array(data[colum_names[len(colum_names)-1]]), 1)
        plt.plot(np.array(data[colum_names[0]]), m*np.array(data[colum_names[0]]) + b, label="Line of best fit",c="red")
    if average==True:
        plt.plot(np.array(data[colum_names[0]]), np.array(data[colum_names[len(colum_names)-1]]),label="Average", c="red")
    #Add lables, legend and save to file
    plt.xlabel(colum_names[0])
    plt.ylabel("Number")
    plt.title(title_text, color='black')
    plt.grid()
    plt.savefig('./Graphs/output.png',dpi=300, format='png', bbox_extra_artists=(plt.legend(title="Legend", loc='center right', bbox_to_anchor=(1.3, 0.5),fontsize='x-small'),),bbox_inches='tight')

#Plot heat map
def heat_map(data):
    plt.imshow(data.corr(), cmap='cool', interpolation='nearest')
    sns.heatmap(data.corr(),annot=True,cmap="coolwarm")
    #g = sns.pairplot(data, diag_kind="kde")
    #g.map_lower(sns.kdeplot, levels=4, color=".2")
    plt.savefig('./Graphs/heatmap.png', format='png')

#The other task that I dont understand
def pair_plot(data):
    sns.pairplot(data,kind="kde")
    plt.tight_layout()
    plt.savefig('./Graphs/pairplot.png', format='png')
if __name__ == "__main__":
    # Now use command line arguments to make it work
    args = getargs()
    data = readCSV(args.input_file)
    data = check_and_remove_Total_Average(data)
    # Add an average column to the data from the CSV file, dont need to work them out if the user doesn't want the bestfit or average
    if args.bestfit == True or args.average == True:
        data = add_average_col(data)
    if args.heatmap == True:
        heat_map(data)
    if args.pairplot == True:
        pair_plot(data)
    else:
        #line_with_best_fit(data,"Total Cars since '94","Year","Total")
        #many_lines_with_best_fit(data)
        test(data,args.graph_title,args.best_fit, args.average)