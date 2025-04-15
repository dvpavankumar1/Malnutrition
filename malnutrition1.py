

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt  
import seaborn as sns 
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import warnings
warnings.filterwarnings('ignore')
from pylab import rcParams




import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

malnutrition_df = pd.read_csv('/kaggle/input/world-malnutrition/world-malnutrition.csv')
malnutrition_df.head()

malnutrition_df.info()

malnutrition_df.describe()

malnutrition_df.columns

malnutrition_df.isnull().sum()

malnutrition_df.drop(['Code'],axis=1,inplace=True)
malnutrition_df.columns

malnutrition_df['Entity'].value_counts()

malnutrition_df = malnutrition_df.rename(columns={
    'Entity':'Country',
    'Prevalence of underweight, weight for age (% of children under 5)': 'Underweight',
    'Prevalence of stunting, height for age (% of children under 5)': 'Stunting',
    'Prevalence of wasting, weight for height (% of children under 5)': 'Wasting'
})

malnutrition_df.columns

malnutrition_df.corr()

plt.figure(figsize=(10,6))
sns.heatmap(malnutrition_df.corr(),annot=True,cmap='viridis')
plt.title('Correlation Heatmap')

malnutrition_df.groupby('Country').mean().sort_values(by='Underweight',ascending=False).head(10)

top_underweight = malnutrition_df.groupby('Country')['Underweight'].mean().sort_values(ascending=False).head(10)
top_stunting = malnutrition_df.groupby('Country')['Stunting'].mean().sort_values(ascending=False).head(10)
top_wasting = malnutrition_df.groupby('Country')['Wasting'].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(16,5))
plt.subplot(1,3,1)
sns.barplot(y=top_underweight.index,x=top_underweight.values)
plt.title('Top 10 Countries - Underweight')
plt.subplot(1,3,2)
sns.barplot(y=top_stunting.index,x=top_stunting.values)
plt.title('Top 10 Countries - Stunting')
plt.subplot(1,3,3)
sns.barplot(y=top_wasting.index,x=top_wasting.values)
plt.title('Top 10 Countries - Wasting')

countries = ['India','Bangladesh','Pakistan','Nigeria','Ethiopia']
rcParams['figure.figsize'] = 12,8
for country in countries:
    data = malnutrition_df[malnutrition_df['Country'] == country]
    plt.plot(data['Year'],data['Underweight'],label=country)
plt.legend()
plt.title('Underweight Comparison')
plt.xlabel('Year')
plt.ylabel('Underweight (%)')

country = 'India'
data = malnutrition_df[malnutrition_df['Country'] == country]
trace1 = go.Scatter(x=data['Year'], y=data['Underweight'], mode='lines+markers', name='Underweight')
trace2 = go.Scatter(x=data['Year'], y=data['Stunting'], mode='lines+markers', name='Stunting')
trace3 = go.Scatter(x=data['Year'], y=data['Wasting'], mode='lines+markers', name='Wasting')

layout = go.Layout(title='Malnutrition Trends in India', xaxis=dict(title='Year'), yaxis=dict(title='%'))

fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
py.iplot(fig)
