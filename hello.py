# from jupyter_core.paths import jupyter_config_dir
# jupyter_dir = jupyter_config_dir()
# import os
# custom_path = os.path.join(jupyter_dir, 'custom')
# try: 
#     os.mkdir(custom_path) 
# except OSError as error: 
#     pass 
    
# custom_js_path = os.path.join(jupyter_dir, 'custom', 'custom.js')
# write_me="$('#appmode-leave').hide();\n$('#appmode-busy').hide();\n$('#appmode-loader').append('<h2>Loading...</h2>')"
# if os.path.isfile(custom_js_path):
#     with open(custom_js_path,'a') as f:
#         f.write(write_me)
# else:
#     f=open(custom_js_path,'w+')
#     f.write(write_me)
#     f.close()



from IPython.core.display import HTML
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, Markdown, clear_output
import plotly.io as pio
from plotly.subplots import make_subplots
from ipywidgets import HBox,VBox
import numpy as np
import plotly.graph_objs as go
import plotly_express as px
################# Utility Variables ###########################################################################

## Collecting data from csv

raw_data = pd.read_csv("time_series_covid_19_confirmed.csv")
death_data = pd.read_csv("time_series_covid_19_deaths.csv")
population_data=pd.read_csv("pop_worldometer_data.csv")
over_data=pd.read_csv("population_above_age_65_percentage_long.csv")
recovery_data=pd.read_csv("time_series_covid_19_recovered.csv")

## Pre-processing data to prevent problems later on

raw_data=raw_data.groupby("Country/Region",as_index=False).sum()
death_data=death_data.groupby("Country/Region",as_index=False).sum()
recovery_data=recovery_data.groupby("Country/Region",as_index=False).sum()
over_data=over_data.loc[over_data['Year'] == 2017]

var=raw_data.keys().values[-1]
color_dat="burg_r"


################# Utility Functions ###########################################################################
"""

TODO--->
Create a single function substituting the bunch of functions.

"""

def call_me_for_recovery(country,label=0):
    
    df_store=pd.DataFrame()
    
    if label==0:
        for i,data in enumerate(recovery_data['Country/Region']):        
            if data==country:
                
                for z,k in enumerate(recovery_data.keys()):                    
                    if k=="1/22/20":
                        #getting the first date
                        break
                
                df_new = recovery_data.iloc[i][z:]
                df_new=df_new.T
                df_new = df_new.reset_index()
                df_new=df_new.rename(columns={df_new.keys()[0]: 'dates',df_new.keys()[1]:'recovered'})
                df_new['country']=data
                
                return df_new
    else:
        for i,data in enumerate(recovery_data['Country/Region']):
            if data in country:
                
                for z,k in enumerate(recovery_data.keys()):
                    if k=="1/22/20":
                        break
                
                df_new = recovery_data.iloc[i][z:]
                df_new=df_new.T
                df_new = df_new.reset_index()
                df_new=df_new.rename(columns={df_new.keys()[0]: 'dates',df_new.keys()[1]:'recovered'})
                df_new['country']=data
                if type(df_store) is int:
                    df_store=(df_new)
                else:
                    df_store = pd.concat([df_store, df_new])
                    
        return df_store            

def call_me_for_more(country,label=0):
    
    df_store=0
    if label==0:
        for i,data in enumerate(raw_data['Country/Region']):
            if data==country:
                
                for z,k in enumerate(raw_data.keys()):
                    if k=="1/22/20":
                        break
                
                df_new = raw_data.iloc[i][z:]
                df_new=df_new.T
                df_new = df_new.reset_index()
                df_new=df_new.rename(columns={df_new.keys()[0]: 'dates',df_new.keys()[1]:'cases'}) 
                df_new['country']=data
                return df_new
    else:
        for i,data in enumerate(raw_data['Country/Region']):
            if data in country:
                
                for z,k in enumerate(raw_data.keys()):
                    if k=="1/22/20":
                        break
                
                df_new = raw_data.iloc[i][z:]
                df_new=df_new.T
                df_new = df_new.reset_index()
                df_new=df_new.rename(columns={df_new.keys()[0]: 'dates',df_new.keys()[1]:'cases'})
                df_new['country']=data
                if type(df_store) is int:
                    df_store=(df_new)
                else:
                    df_store = pd.concat([df_store, df_new])
        return df_store


def call_me_for_deaths(country,label=0):
    df_store=0
    count=0
    if label==0:
        for i,data in enumerate(death_data['Country/Region']):
            if data==country:
                
                for z,k in enumerate(death_data.keys()):
                    if k=="1/22/20":
                        break
                
                df_new = death_data.iloc[i][z:]
                df_new=df_new.T
                df_new = df_new.reset_index()
                df_new=df_new.rename(columns={df_new.keys()[0]: 'dates',df_new.keys()[1]:'deaths'})
                df_new['country']=data
                return df_new
    else:
        for i,data in enumerate(death_data['Country/Region']):
            if data in country:
                
                for z,k in enumerate(death_data.keys()):
                    if k=="1/22/20":
                        break
                
                df_new = death_data.iloc[i][z:]
                df_new=df_new.T
                df_new = df_new.reset_index()
                df_new=df_new.rename(columns={df_new.keys()[0]: 'dates',df_new.keys()[1]:'deaths'})
                df_new['country']=data
                if type(df_store) is int:
                    df_store=(df_new)
                else:
                    df_store = pd.concat([df_store, df_new])          
        return df_store
    
################################# Event Handlers ##############################################################  

"""

TODO--->
Reduce the number of functions by reusing code. Reusability very poor currently...

"""    
p=[]
flag=0

def controller(points):
    
    global p,fk
    
    country=[]
    
    for i in points:
        ##get the selected countries
        
        count=raw_data.loc[[i]]['Country/Region']
        country.append(count.values[0])
    
    if len(country)==0:
        
        """
        
        If a selection is made but no country is selected in the selection, the following is done-->
        
        1) The original world-plot is re-drawn after clearning the screen
        
        2) A small message is displayed to tell the user that no country has been selected.
           The message might not appear in app-mode. Even without the message, selection of no country
           would land the user in the beggining plot and the order of things will still be viable.
           
           [TODO -- Make a plot that says "No data" through line-charts and label it as "No Country selected". 
           This would be a substitute of the message.]
           
           
        """
        
        clear_output(wait=True)
        
        print("Select Region with at least one Country")
        
        f=go.FigureWidget(px.choropleth(raw_data,scope="world",locationmode = 'country names',locations="Country/Region",
                    color=var,color_continuous_scale=color_dat,
                 hover_name="Country/Region",hover_data=[var],projection="natural earth"))
        f.update_layout(
            hoverlabel=dict(
                bgcolor="white", 
                font_size=14, 
                font_family="Rockwell"
            )
        )
    
        scatter=f.data[0]
        scatter.on_click(selected_point)
        scatter.on_selection(selection_fn)

        #f.update_traces(textposition='top center')

        f.update_layout(
            height=500,
            title_text='COVID 19 WORLD DATA'
        )
        fk=f
        display(VBox([fk]))
        return
    
    #print(country)    
    
    country_data=call_me_for_more(country,1)                          ###Functions to help align the data 
    country_deaths=call_me_for_deaths(country,1)                      ###Functions to help align the data 
    country_recovery=call_me_for_recovery(country,1)                  ###Functions to help align the data 
    
    
    #calculating the self-made metric "recovery-ratio"
    
    country_recovery["recovery-ratio"]=country_recovery["recovered"]/country_data["cases"]
    country_recovery.drop(['recovered'],axis=1)
    
    
    ###Clearing the screen for a better experience and to avoid too much clutter during series of interactions
    clear_output(wait=True)
    
    fig=go.FigureWidget(px.line(country_data,title="Country wise tally--Cases", x="dates", y="cases", color='country'))
    fig1=go.FigureWidget(px.line(country_deaths,title="Country wise tally--Deaths", x="dates", y="deaths", color='country'))
    fig2=go.FigureWidget(px.line(country_recovery,title="Country wise tally--Recovery-Ratio*", x="dates", y="recovery-ratio", color='country'))
    
    
    df_store=0
    df_store2=0
    
    
    for i,country in enumerate(population_data[population_data.keys()[0]]):
        
        if country in country_data["country"].values:
                temp = population_data.iloc[[i]]
                if type(df_store) is int:
                    
                    df_store=(temp)
                    
                else:
                    df_store = pd.concat([df_store, temp])
                    
                
    for i,country in enumerate(over_data[over_data.keys()[0]]):
        
        if country in country_data["country"].values:
                
                temp = over_data.iloc[[i]]     ##a temporary data storage 
                
                if type(df_store2) is int:
                    df_store2=temp             ##Creating the dataframe to access it later
                else:
                    df_store2 = pd.concat([df_store2, temp])
    
    
    """
    
    Getting the population statistics
    
    df_store---->Data on population density and total population
    df_store2--->Data on what percentage of the population has age over 65
    
    
    """
    
    fig_pop1 = go.FigureWidget(px.pie(df_store, values=df_store.keys()[4], names=df_store.keys()[0], title='Population Density',hole=0.3))
    fig_pop2 = go.FigureWidget(px.pie(df_store2, values=df_store2.keys()[2], names=df_store2.keys()[0], title='Over-65 Percentage',hole=0.3))
    fig_pop3 = go.FigureWidget(px.pie(df_store, values=df_store.keys()[1], names=df_store.keys()[0], title='Total Population',hole=0.3))
    
    pop=HBox([fig_pop1,fig_pop3])
    pop=VBox([pop,fig_pop2])
            
    fig=HBox([fig,fig1])
    fig=VBox([fig,fig2])
    """
    Updating the world-plot after selection is needed as selection would highlight specific areas of the plot
    """
    
    f=go.FigureWidget(px.choropleth(raw_data,scope="world",locationmode = 'country names',locations="Country/Region",
                    color=var,color_continuous_scale=color_dat,
                 hover_name="Country/Region",hover_data=[var],projection="natural earth"))
    f.update_layout(
    hoverlabel=dict(
                bgcolor="white", 
                font_size=14, 
                font_family="Rockwell"
            )
        )
    scatter=f.data[0]
    scatter.on_click(selected_point)
    scatter.on_selection(selection_fn)
    f.update_layout(
        height=500,
        title_text='COVID 19 WORLD DATA'
    )
    fk=f
    f1=VBox([fk,fig,pop])
    
    display(f1)

        

def selected_point(trace, points, selector):
    
    global flag,fk
     
    for i in points.point_inds:
       
        ### check if a list of points is being passed with ctrl pressed
        
        if (selector.ctrl==True):
            
            p.append(i)
            flag+=1
            return
        
        if flag>=1 and selector.ctrl==False:
            controller(p)
            flag=0
            return  
        
        ##if it reaches this part of the code, then ONLY ONE country is selected        
        
        country=raw_data.loc[[i]]['Country/Region']
        country=country.values[0]
        country_data=call_me_for_more(country)
        country_death=call_me_for_deaths(country)
        country_recovery=call_me_for_recovery(country)
        
        ## create animations for "Daywise Analysis" of Cases and Deaths 
        
        fig_drawing = go.Figure(
                data=[go.Scatter(x=[0], y=[0],mode="markers")],
                layout=go.Layout(
                yaxis=dict(range=[0, country_data['cases'].values[-1]], autorange=False),
                xaxis=dict(range=[0, 132], autorange=False),
                xaxis_title="Day",
                yaxis_title="Cases",
                title=country_data['country'].values[-1]+"- Daywise Analysis (Cases)",
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label=">>",
                                  method="animate",
                                  args=[None,{"frame": {"duration": 20, "redraw": False},}])])]
            ),
             frames=[go.Frame(
                data=[go.Scatter(
                    x=np.arange(i),
                    y=country_data["cases"][0:i],
                    mode="lines",
                    marker=dict(color="blue", size=10))])

                for i in range(len(country_data["cases"].values))]
        )
        fig_drawing.update_layout(transition_duration=0)
        
        fig_drawing_death=go.Figure(
                data=[go.Scatter(x=[0], y=[0],mode="markers")],
                layout=go.Layout(
                yaxis=dict(range=[0, country_death['deaths'].values[-1]], autorange=False),
                xaxis=dict(range=[0, 132], autorange=False),
                xaxis_title="Day",
                yaxis_title="Deaths",
                title=country_death['country'].values[-1]+"- Daywise Analysis (Deaths)",
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label=">>",
                                  method="animate",
                                  args=[None, {"frame": {"duration": 20, "redraw": False},}])])]
            ),
             frames=[go.Frame(
                data=[go.Scatter(
                    x=np.arange(i),
                    y=country_death["deaths"][0:i],
                    mode="lines",
                    marker=dict(color="red", size=10))])

                for i in range(len(country_death["deaths"].values))]
        )
        fig_drawing_death.update_layout(transition_duration=0)
        
        
        ### Create line charts
        
        country_data["deaths"]=country_death["deaths"]
        country_data["recovered"]=country_recovery["recovered"]
        
        fig_ = px.line(country_data, x="dates", y=["cases","deaths","recovered"])
        fig_.update_layout(title="Date Wise Analysis (Cases, Deaths, and Recovered)")
        fig1=go.FigureWidget(fig_)
        
        f=VBox([fk,fig1])
        clear_output(wait=True)
        
        fig_drawing.update_layout(
             autosize=False,
            width=800,
            height=500
            )
        fig_drawing_death.update_layout(
            autosize=False,
            width=800,
            height=500
            )
        fig_drawing.update_yaxes(automargin=True)
        fig_drawing_death.update_yaxes(automargin=True)
        fig_drawing.show()
        fig_drawing_death.show()
        
        display(f)
        
        ###   Get population and age statistics----might not work due to poor data
        
        fig_pop=go.Figure()
        count_pop=0
        for i,country in enumerate(population_data[population_data.keys()[0]]):
            if country in country_data["country"].values:
                count_pop=population_data.iloc[[i]][population_data.keys()[1]].values
                break
        
        
        recovery=recovery_data.loc[recovery_data["Country/Region"]==country_data["country"].values[-1]]
        recovery=recovery[recovery.keys().values[-1]]
        recovery=recovery.values[0]
        
        temp=over_data.loc[over_data["Country Name"]==country_data["country"].values[-1]]
        if count_pop!=0 and len(temp["Count"].values)!=0:
            over=temp["Count"].values[-1]
            
            over=int(over*count_pop[0]/100)

            deaths=country_death['deaths'].values[-1]
            cases=country_data['cases'].values[-1]
            labels=['Covid','Deaths from Covid','Recovered']
            
            values=[cases,deaths,recovery]
            colors=['blue','red','green']
            
            fig_pop = go.Figure(data=[go.Pie(labels=labels, values=values,hole=0.3,pull=[0,0.2,0])])
            fig_pop.update_traces(marker=dict(colors=colors))
            fig_pop.update_layout(title="Population statistics for "+country_data['country'].values[1])
            count=count_pop[0]-over
            labels=["Under 65","Over 65"]
            values=[count,over]
            colors=['blue','red']
            fig_pop_age = go.Figure(data=[go.Pie(labels=labels, values=values,hole=0.2)])
            fig_pop_age.update_traces(marker=dict(colors=colors))
            fig_pop_age.update_layout(title="Age statistics for "+country_data['country'].values[1])
            
            fig_pop=go.FigureWidget(fig_pop)
            fig_pop_age=go.FigureWidget(fig_pop_age)
            fig_pop_tot=HBox([fig_pop,fig_pop_age])
            display(fig_pop_tot)
          
        else:
            fig_pop.update_layout(title="Population report for "+country_data["country"].values[1]+"is unavailable at the moment!")
            fig_pop.show()
        
        
def selection_fn(trace,points,selector):
    country=[]
    
    global fk,scatter,f
    
    for i in points.point_inds:
        
        ##get the selected countries
        
        count=raw_data.loc[[i]]['Country/Region']
        country.append(count.values[0])
    
    if len(country)==0:
        
        """
        
        If a selection is made but no country is selected in the selection, the following is done-->
        
        1) The original world-plot is re-drawn after clearning the screen
        
        2) A small message is displayed to tell the user that no country has been selected.
           The message might not appear in app-mode. Even without the message, selection of no country
           would land the user in the beggining plot and the order of things will still be viable.
           
           [TODO -- Make a plot that says "No data" through line-charts and label it as "No Country selected". 
           This would be a substitute of the message.]
           
           
        """
        
        clear_output(wait=True)
        
        print("Select Region with at least one Country")
        
        f=go.FigureWidget(px.choropleth(raw_data,scope="world",locationmode = 'country names',locations="Country/Region",
                    color=var,color_continuous_scale=color_dat,
                 hover_name="Country/Region",hover_data=[var],projection="natural earth"))
        f.update_layout(
            hoverlabel=dict(
                bgcolor="white", 
                font_size=14, 
                font_family="Rockwell"
            )
        )
    
        scatter=f.data[0]
        scatter.on_click(selected_point)
        scatter.on_selection(selection_fn)

        #f.update_traces(textposition='top center')

        f.update_layout(
            height=500,
            title_text='COVID 19 WORLD DATA'
        )
        fk=f
        display(VBox([fk]))
        return
    
    #print(country)    
    
    country_data=call_me_for_more(country,1)                          ###Functions to help align the data 
    country_deaths=call_me_for_deaths(country,1)                      ###Functions to help align the data 
    country_recovery=call_me_for_recovery(country,1)                  ###Functions to help align the data 
    
    
    #calculating the self-made metric "recovery-ratio"
    
    country_recovery["recovery-ratio"]=country_recovery["recovered"]/country_data["cases"]
    country_recovery.drop(['recovered'],axis=1)
    
    
    ###Clearing the screen for a better experience and to avoid too much clutter during series of interactions
    clear_output(wait=True)
    
    fig=go.FigureWidget(px.line(country_data,title="Country wise tally--Cases", x="dates", y="cases", color='country'))
    fig1=go.FigureWidget(px.line(country_deaths,title="Country wise tally--Deaths", x="dates", y="deaths", color='country'))
    fig2=go.FigureWidget(px.line(country_recovery,title="Country wise tally--Recovery-Ratio*", x="dates", y="recovery-ratio", color='country'))
    
    
    df_store=0
    df_store2=0
    
    
    for i,country in enumerate(population_data[population_data.keys()[0]]):
        
        if country in country_data["country"].values:
                temp = population_data.iloc[[i]]
                if type(df_store) is int:
                    
                    df_store=(temp)
                    
                else:
                    df_store = pd.concat([df_store, temp])
                    
                
    for i,country in enumerate(over_data[over_data.keys()[0]]):
        
        if country in country_data["country"].values:
                
                temp = over_data.iloc[[i]]     ##a temporary data storage 
                
                if type(df_store2) is int:
                    df_store2=temp             ##Creating the dataframe to access it later
                else:
                    df_store2 = pd.concat([df_store2, temp])
    
    
    """
    
    Getting the population statistics
    
    df_store---->Data on population density and total population
    df_store2--->Data on what percentage of the population has age over 65
    
    
    """
    
    fig_pop1 = go.FigureWidget(px.pie(df_store, values=df_store.keys()[4], names=df_store.keys()[0], title='Population Density',hole=0.3))
    fig_pop2 = go.FigureWidget(px.pie(df_store2, values=df_store2.keys()[2], names=df_store2.keys()[0], title='Over-65 Percentage',hole=0.3))
    fig_pop3 = go.FigureWidget(px.pie(df_store, values=df_store.keys()[1], names=df_store.keys()[0], title='Total Population',hole=0.3))
    
    pop=HBox([fig_pop1,fig_pop3])
    pop=VBox([pop,fig_pop2])
            
    fig=HBox([fig,fig1])
    fig=VBox([fig,fig2])
    """
    Updating the world-plot after selection is needed as selection would highlight specific areas of the plot
    """
    
    f=go.FigureWidget(px.choropleth(raw_data,scope="world",locationmode = 'country names',locations="Country/Region",
                    color=var,color_continuous_scale=color_dat,
                 hover_name="Country/Region",hover_data=[var],projection="natural earth"))
    f.update_layout(
    hoverlabel=dict(
                bgcolor="white", 
                font_size=14, 
                font_family="Rockwell"
            )
        )
    scatter=f.data[0]
    scatter.on_click(selected_point)
    scatter.on_selection(selection_fn)
    f.update_layout(
        height=500,
        title_text='COVID 19 WORLD DATA'
    )
    fk=f
    f1=VBox([fk,fig,pop])
    
    display(f1)
    

    
##############################################################################################################
#####################STARTING TO PLOT ########################################################################
##############################################################################################################

f=go.FigureWidget(px.choropleth(raw_data,scope="world",locationmode = 'country names',locations="Country/Region",
                    color=var,color_continuous_scale=color_dat,
                 hover_name="Country/Region",hover_data=[var],projection="natural earth"))

f.update_layout(
    hoverlabel=dict(
        bgcolor="white", 
        font_size=14, 
        font_family="Rockwell"
    )
)
    
    
    
scatter=f.data[0]
scatter.on_click(selected_point)

scatter.on_selection(selection_fn)

f.update_layout(
    height=500,
    title_text='COVID 19 WORLD DATA'
)

fk=f
f=VBox([f])
display(f)
#display(f)
#import plotly
#plotly.offline.plot(f, filename='name.html')
