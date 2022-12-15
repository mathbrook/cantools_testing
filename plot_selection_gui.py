from tkinter import *

items = ['Time', 'tps', 'batt', 'afr1_old', 'afr2_old', 'warmcor', 'tpsaccel', 'tpsfuelcut', 'barocor', 'sensors1', 'sensors2', 'sensors3', 'sensors4', 'seconds', 'pw1', 'pw2', 'rpm', 'adv_deg', 'squirt', 'engine', 'afrtgt1', 
'afrtgt2', 'wbo2_en1', 'wbo2_en2', 'baro', 'map', 'mat', 'clt', 'AFR1', 'AFR2', 'AFR3', 'AFR4', 'AFR5', 'AFR6', 'AFR7', 'AFR8', 'fuel_press1', 'fuel_press2', 'fuel_temp1', 'fuel_temp2', 'sensors5', 'sensors6', 'sensors7', 'sensors8']
print(items)
# Create object
OPTIONS = items #etc
items_to_plot=[]
master = Tk()

variable = StringVar(master)
variable.set(OPTIONS[0]) # default value

w = OptionMenu(master, variable, *OPTIONS)
w.pack()

def ok():
    if(variable.get() not in items_to_plot):
        items_to_plot.append(variable.get())
    print ("Added to plot: " + variable.get())

def sendit():
    print("figure\nhold on")
    legend = []
    for i in items_to_plot:
        print("plot(S." + str(i) + "(:,1)/1000, S." + str(i) + "(:,2)/100);")
        legend.append("'"+i+"'")
    print("legend({"+",".join(legend)+"})")
    print("xlabel('Time (s)')")
    print('ylim("auto")')
    print("title("+str(",".join(items_to_plot))+")")
    print("h = zoom;\nset(h,'Motion','horizontal','Enable','on');")
# def gui_func(options):

button2 = Button(master,text="Send it!",command=sendit)
button = Button(master, text="OK", command=ok)
button.pack()
button2.pack()

mainloop()