# -*- coding: latin-1 -*-
import pandas as pd
import numpy as np
import scipy.special

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file

def Weibull_Distribution(input_file,column):
	df = pd.read_csv(input_file)
	p1 = figure(title="Weibull Distribution (λ=1, k=1.25)", tools="save",
	            background_fill_color="#E8DDCB")

	lam, k = 1, 1.25

	measured = lam*(df[column])**(1/k)
	hist, edges = np.histogram(measured, density=True, bins=50)

	x = np.linspace(0, 8, 1000)
	pdf = (k/lam)*(x/lam)**(k-1) * np.exp(-(x/lam)**k)
	cdf = 1 - np.exp(-(x/lam)**k)

	p1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
	       fill_color="#036564", line_color="#033649")
	p1.line(x, pdf, line_color="#D95B43", line_width=8, alpha=0.7, legend="PDF")
	p1.line(x, cdf, line_color="white", line_width=2, alpha=0.7, legend="CDF")

	p1.legend.location = "top_left"
	p1.xaxis.axis_label = 'x'
	p1.yaxis.axis_label = 'Pr(x)'
	output_file('histogram.html', title="histogram.py example")

	show(gridplot(p1, ncols=2, plot_width=400, plot_height=400, toolbar_location=None))

if __name__ == '__main__':
	Weibull_Distribution('user_pair_common_keywords_freq.csv','Frequency')
