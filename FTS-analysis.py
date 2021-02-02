# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] slideshow={"slide_type": "slide"}
# # Analysis of FTS financial flows to the CCCM sector
#
# ### Limitations
# - FTS data comes from agency and donor reporting and can vary in quality.
# - Many FTS flows combine funds for CCCM with other sectors, meaning that some figures may overestimate CCCM specific funding. These limitations are documented in the accompanying notes.
# - 2020 flows may be incomplete, subject to reporting delays.

# %%
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import openpyxl
import matplotlib #imported for heatchart
import geopandas as gpd
import geoviews as gv
from cartopy import crs
import holoviews as hv

# style seaborn
sns.set_theme()
sns.set_context("talk")
sns.set_style("white")

# %%
# read and clean data
old = pd.read_excel('FTS2005-2019.xlsx', sheet_name='2005-201') 
new = pd.read_excel('FTS2020.xlsx', sheet_name='Results - Incoming') 
full = new.append(old, ignore_index=True)
def splitagencies(x):
    if x['Destination Organization']=='International Organization for Migration':
        return 'IOM'
    else:
        return 'Other agencies'
full['Agency'] = full.apply(splitagencies, axis=1)

# %% slideshow={"slide_type": "slide"}
# plot total funding per year
p = full.groupby(['Destination Usage year']).agg({'Amount (USD)':['sum']}).reset_index()
p.columns=['Year','Total']
fig, ax = plt.subplots(figsize = (18,9))

g = sns.barplot(data=p,x="Year", y="Total", color="#2a87c8").set_title("Total CCCM Funding")
ax.yaxis.set_major_formatter(tkr.FuncFormatter(lambda y, p: f'${y/1000000:,.0f}m'))
ax.set(xlabel='Year', ylabel='Funding (US$)')
sns.despine()
plt.savefig('outputs/one.svg')

# %% [markdown]
# On average, CCCM funding increased approximately 56% year-on-year since 2005  
# The CCCM sector has received approximately US$1,065m since 2005

# %%
# print funding
print(f"Total CCCM Funding: ${full['Amount (USD)'].sum():,d}")

# %% slideshow={"slide_type": "slide"}
#plot per country - 2005-2020
fig, ax = plt.subplots(figsize = (18,16))

df = full
df2 = df.groupby(['Destination Location']).agg({'Amount (USD)':['sum']})
df3 = df2.reset_index()
df3.columns=['Country','Funding']
df3 = df3.sort_values(['Funding']).reset_index(drop=True)
g = sns.barplot(data=df3, y="Country", x="Funding", color="#2a87c8").set_title("Funding per Country - 2005-2020")
ax.xaxis.set_major_formatter(tkr.FuncFormatter(lambda y, p: f'${y/1000000:,.0f}m'))
ax.set(xlabel='Funding (US$)', ylabel='Country')
sns.despine()
plt.savefig('outputs/four.svg')

# %% [markdown]
# ### Limitations:
# - Yemen funding in is misleading as it includes funding for all sectors by the government of Saudi Arabia
# - CAR data is inaccurate as many flows were mistakenly tagged as CCCM
# - Jordan data is inaccurate

# %% slideshow={"slide_type": "slide"}
# map countries funded between 2005-2020
mapdata = full.groupby(['Destination Location']).agg({'Amount (USD)':['sum']})
mapdata = mapdata.reset_index()
mapdata.columns=['Destination Location','Funding']

gv.extension('bokeh', 'matplotlib',logo=False)
gv.output(backend='bokeh', fig='png', logo=False, size=800)
geometries = gpd.read_file('./world.geojson')
geometries.rename(columns={"NAME":"Destination Location"}, inplace=True)
geometries['Destination Location'] = geometries['Destination Location'].replace('Democratic Republic of the Congo','Congo, The Democratic Republic of the')
mapdf = gpd.GeoDataFrame(pd.merge(geometries, mapdata))

basemap = gv.Polygons(geometries, crs=crs.GOOGLE_MERCATOR).opts(line_color='w', line_alpha=0.3, color='#A6A6A6', xaxis=None, yaxis=None, width=200, height=100)
map = gv.Polygons(mapdf,label='Trainings', crs=crs.GOOGLE_MERCATOR).opts(show_frame=False, width=200, height=100, xaxis=None, yaxis=None, color='#2a87c8', line_color='w', line_alpha=0.3, title="43 countries received CCCM funding between 2005-2020")

t = basemap * map
hv.save(t, 'outputs/mapall.png', fmt='png')
t
# todo: find a way to export the map as an svg. rendering as bokeh stopped working for some reason

# %% slideshow={"slide_type": "slide"}
#plot per country - 2019
fig, ax = plt.subplots(figsize = (18,9))

df = full[full['Destination Usage year']==2019]
df2 = df.groupby(['Destination Location']).agg({'Amount (USD)':['sum']})
df3 = df2.reset_index()
df3.columns=['Country','Funding']
df3 = df3.sort_values(['Funding']).reset_index(drop=True)
g = sns.barplot(data=df3, y="Country", x="Funding", color="#2a87c8").set_title("Funding per Country - 2019")
ax.xaxis.set_major_formatter(tkr.FuncFormatter(lambda y, p: f'${y/1000000:,.0f}m'))
ax.set(xlabel='Funding (US$)', ylabel='Country')
sns.despine()
plt.savefig('outputs/five.svg')

# %% [markdown]
# 16 countries received CCCM funding in 2020 compared to 14 in 2009  
# Funding ended for Cameroon and Haiti and started for Honduras, Mozambique, Niger and Philippines

# %% slideshow={"slide_type": "slide"}
#plot per country - 2020
fig, ax = plt.subplots(figsize = (18,9))

df = full[full['Destination Usage year']==2020]
df2 = df.groupby(['Destination Location']).agg({'Amount (USD)':['sum']})
df3 = df2.reset_index()
df3.columns=['Country','Funding']
df3 = df3.sort_values(['Funding']).reset_index(drop=True)
g = sns.barplot(data=df3, y="Country", x="Funding", color="#2a87c8").set_title("Funding per Country - 2020")
ax.xaxis.set_major_formatter(tkr.FuncFormatter(lambda y, p: f'${y/1000000:,.0f}m'))
ax.set(xlabel='Funding (US$)', ylabel='Country')
sns.despine()
plt.savefig('outputs/six.svg')

# %% slideshow={"slide_type": "slide"}
# map countries funded in 2020
mapdata2020 = full[full['Destination Usage year']==2020].groupby(['Destination Location']).agg({'Amount (USD)':['sum']})
mapdata2020 = mapdata2020.reset_index()
mapdata2020.columns=['Destination Location','Funding']



geometries['Destination Location'] = geometries['Destination Location'].replace('Democratic Republic of the Congo','Congo, The Democratic Republic of the')
mapdf2020 = gpd.GeoDataFrame(pd.merge(geometries, mapdata2020))
map2020 = gv.Polygons(mapdf2020,label='Trainings', crs=crs.GOOGLE_MERCATOR).opts(show_frame=False, width=200, height=100, xaxis=None, yaxis=None, color='#2a87c8', line_color='w', line_alpha=0.3, title="16 countries received CCCM funding in 2020")

t2 = basemap * map2020 
hv.save(t2, 'outputs/map2020.png', fmt='png')
t2

# %% slideshow={"slide_type": "slide"}
# full.groupby(['Destination Location']).agg({'Amount (USD)':['sum']})
hmdf = full[['Destination Usage year','Destination Location','Amount (USD)']].groupby(['Destination Usage year','Destination Location']).agg({'Amount (USD)':['sum']}).reset_index()
hmdf.columns=['Year','Country','Funding']
hmdf = hmdf.astype({'Funding': 'int64','Country': 'category','Year':'int64'})
hmdf = hmdf.pivot('Country','Year','Funding').fillna(0).astype('int64')

norm = matplotlib.colors.Normalize(0,20000000)
colors = [[norm(0), "white"],
          [norm(500000), "#eff3ff"],
          [norm(2500000), "#bdd7e7"],
          [norm(5000000), "#6baed6"],
          [norm(20000000), "#2171b5"]]
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
f, ax = plt.subplots(figsize=(27, 18))
s= sns.heatmap(hmdf, annot=False, cmap=cmap, fmt=".1f", linewidths=.5, ax=ax)
cbar = s.collections[0].colorbar
cbar.set_ticks([0, 25000000, 50000000, 75000000, 113593430])
cbar.set_ticklabels(['$0', '$25m','$50m','$75m','$113m'])
plt.savefig('outputs/seven.svg')

# %% [markdown]
# The longest consecutively funding countries for CCCM are South Sudan (9 years) and Yemen (12 years)

# %% slideshow={"slide_type": "slide"}
# plot the numbr of CCCM agencies per year
agencies = full.groupby(['Destination Usage year']).agg({'Destination Organization':['nunique']}).reset_index()
agencies.columns = ['Year','Number of organizations']

fig, ax = plt.subplots(figsize = (18,9))
g = sns.barplot(data=agencies,x="Year", y="Number of organizations", color="#2a87c8").set_title("Number of CCCM Organizations")
ax.set(xlabel='Year', ylabel='Number of organizations')
sns.despine()
plt.savefig('outputs/eight.svg')

# %% [markdown]
# Approximately 117 agencies have received CCCM funding since 2005

# %% [markdown]
# ### 

# %% slideshow={"slide_type": "slide"}
donors = full.groupby(['Destination Usage year']).agg({'Source Organization':['nunique']}).reset_index()
donors.columns = ['Year','Number of donors']

fig, ax = plt.subplots(figsize = (18,9))
g = sns.barplot(data=donors,x="Year", y="Number of donors", color="#2a87c8").set_title("Number of CCCM donors")
ax.set(xlabel='Year', ylabel='Number of donors')
sns.despine()
plt.savefig('outputs/nine.svg')

# %% [markdown]
# 2020 seen the largest increase in donors to CCCM since 2009

# %%
# number of orgs in 2020
f2020 = full[full['Destination Usage year'] == 2020]
len(f2020['Source Organization'].unique())

# %% slideshow={"slide_type": "slide"}
donorsall = full.groupby(['Source Organization']).agg({'Amount (USD)':['sum']}).reset_index()
donorsall.columns = ['Donor', 'Funding']
donorsall = donorsall.sort_values(['Funding']).reset_index(drop=True)

fig, ax = plt.subplots(figsize = (18,16))
g = sns.barplot(data=donorsall, y="Donor", x="Funding", color="#2a87c8").set_title("Funding per Donor - 2005-2020")
ax.xaxis.set_major_formatter(tkr.FuncFormatter(lambda y, p: f'${y/1000000:,.0f}m'))
ax.set(xlabel='Funding (US$)', ylabel='Donor')
sns.despine()
plt.savefig('outputs/ten.svg')
#how much funding was from ECHO and USA
#donorsall[donorsall['Donor']=='United States of America, Government of'].agg({'Funding':['sum']})
#donorsall[donorsall['Donor']=='European Commission\'s Humanitarian Aid and Civil Protection Department'].agg({'Funding':['sum']})

# %% [markdown]
# Since 2005, funding from the US government and ECHO account for over 42% of all funding received for CCCM

# %% slideshow={"slide_type": "slide"}
# 2019 donors
f2019 = full[full['Destination Usage year']==2019]
donors2019 = f2019.groupby(['Source Organization']).agg({'Amount (USD)':['sum']}).reset_index()
donors2019.columns = ['Donor', 'Funding']
donors2019 = donors2019.sort_values(['Funding']).reset_index(drop=True)

fig, ax = plt.subplots(figsize = (18,8))
g = sns.barplot(data=donors2019, y="Donor", x="Funding", color="#2a87c8").set_title("Funding per Donor - 2019")
ax.xaxis.set_major_formatter(tkr.FuncFormatter(lambda y, p: f'${y/1000000:,.0f}m'))
ax.set(xlabel='Funding (US$)', ylabel='Donor')
sns.despine()
plt.savefig('outputs/eleven.svg')

# %% slideshow={"slide_type": "slide"}
# 2020 donors
f2020 = full[full['Destination Usage year']==2020]
donors2020 = f2020.groupby(['Source Organization']).agg({'Amount (USD)':['sum']}).reset_index()
donors2020.columns = ['Donor', 'Funding']
donors2020 = donors2020.sort_values(['Funding']).reset_index(drop=True)

fig, ax = plt.subplots(figsize = (18,10))
g = sns.barplot(data=donors2020, y="Donor", x="Funding", color="#2a87c8").set_title("Funding per Donor - 2020")
ax.xaxis.set_major_formatter(tkr.FuncFormatter(lambda y, p: f'${y/1000000:,.0f}m'))
ax.set(xlabel='Funding (US$)', ylabel='Donor')
sns.despine()
plt.savefig('outputs/twelve.svg')

# %% [markdown]
# 6 additional donors funded CCCM in 2020 compared to 2019

# %%
#print the donor count
print(f"Number of donors in 2020: {len(donors2020['Donor'].unique())} \nNumber of donors in 2019: {len(donors2019['Donor'].unique())}")
