import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from umap import UMAP

plt.close('all')
plt.ion()

url_confirmed_us = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
url_deaths_us = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
url_confirmed_global = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths_global = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered_global = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'


# Import urls as dataframes

confirmed_dat = pd.read_csv(url_confirmed_global)
deaths_dat = pd.read_csv(url_deaths_global)


deaths_dat.set_index("Country/Region", inplace = True)
deaths_dat = deaths_dat.loc[~deaths_dat.index.duplicated(keep='first')]



deaths_set = deaths_dat.iloc[:, 4:]




# Embed - Try other embeddings here
emb = UMAP(verbose = 1).fit_transform(deaths_set)
embed = pd.DataFrame(emb).set_index(deaths_set.index)





# Setup axes
fig, ax = plt.subplots(figsize = (9, 6), ncols = 2)
ax_emb = ax[0]
ax_show = ax[1]

# Plot embedding
scat_plot = ax_emb.scatter(emb[:, 0], emb[:, 1], cmap = 'plasma', c = np.log(deaths_set.iloc[:, -1]))


# Dummy plot for now. But it is the markers
colors = ['r', 'g', 'k', 'orange', 'purple']
marked_scat = ax_emb.scatter([], [], marker = 'x', s = 60)






def onclick(event):
	dist_x = emb[:, 0] - event.xdata
	dist_y = emb[:, 1] - event.ydata
	dist_sq = pd.Series(dist_x ** 2 + dist_y ** 2)
	dist_sq.index = deaths_set.index
	dist_sq.sort_values(inplace = True)

	marked_scat.set_offsets(embed.loc[dist_sq.index[:5], :])
	marked_scat.set_color(colors)

	ax_show.cla()
	for i in range(5):
		ax_show.plot(range(len(deaths_set.loc[dist_sq.index[i], :])), deaths_set.loc[dist_sq.index[i], :], ls = '--', label = dist_sq.index[i], color = colors[i])



	ax_show.legend()
	plt.draw()	


cid = fig.canvas.mpl_connect('button_press_event', onclick)
