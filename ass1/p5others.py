# coding:utf8
import csv
import numpy as np
from sklearn.linear_model import LinearRegression
import prettytable as pt
from scipy.stats import chi2, norm, t
import pickle

with open('./ass1/files/hw1q5.csv') as f:
    f = csv.reader(f)
    data = list(f)


X1s = np.array([float(i[0]) for i in data[1:]])
X2s = np.array([float(i[1]) for i in data[1:]])
X3s = X1s * X2s
Ys = np.array([float(i[2]) for i in data[1:]])

# (a)
Xsmall = np.vstack([X1s, X2s])
Xsmall = np.transpose(Xsmall, (1, 0))
modela = LinearRegression()
modela.fit(Xsmall, Ys)
Yhata = modela.predict(Xsmall)

beta0 = modela.intercept_
beta1, beta2 = modela.coef_
sigma2hata = np.mean((Ys-Yhata)**2)

tb1 = pt.PrettyTable()
tb1.field_names = ['beta0', 'beta1', 'beta2', 'sigma2']
tb1.add_row(np.round([beta0, beta1, beta2, sigma2hata], 4))
print(tb1)

# (c)
Xbig= np.vstack([X1s, X2s, X3s])
Xbig= np.transpose(Xbig, (1, 0))
modelc = LinearRegression()
modelc.fit(Xbig, Ys)
Yhatc = modelc.predict(Xbig)

beta0 = modelc.intercept_
beta1, beta2, beta3 = modelc.coef_
sigma2hatc = np.mean((Ys-Yhatc)**2)

tb2 = pt.PrettyTable()
tb2.field_names = ['beta0', 'beta1', 'beta2','beta3',  'sigma2']
tb2.add_row(np.round([beta0, beta1, beta2, beta3,  sigma2hata], 4))
print(tb2)

# (e)
n = len(Ys)

Lsmall = (1/(2*np.pi*sigma2hata))*np.exp(-n/2) 
Lbig = (1/(2*np.pi*sigma2hatc))*np.exp(-n/2) 
LR = 2*np.log(Lbig/Lsmall)
# LR asymptotically conforms to chisq_1 distribution
chi2rv = chi2(1) 
pvalue_lr = chi2rv.sf(LR)
print(f'pvalue of likehood ratio test is {pvalue_lr:.4f}, the LR ratio is {LR:.4}')
Xbigmat = np.mat(np.concatenate([np.ones(n).reshape(-1, 1), Xbig], axis=1))
c = np.mat([0, 0, 0, 1])
sebeta3 = np.array(np.sqrt(c*(Xbigmat.T*Xbigmat).I*c.T*sigma2hatc))[0][0]
waldT = beta3/sebeta3
pvaluew = 2*norm().sf(waldT) 
print(f'pvalue of wald test is {pvaluew:.4f}, the wald statisticis {waldT:.4}')

# Pop
with open('./ass1/savedoc/p5d.pkl', 'rb') as f:
    params = pickle.load(f)
beta3hat = np.array([i[3] for i in params])
prg0 = (beta3hat>0).sum()/len(beta3hat)
prs0 = (beta3hat<0).sum()/len(beta3hat)
Pop = 2 * (1- np.max([prg0, prs0]))
print(f'the two-sided posterior probility is {Pop}')
