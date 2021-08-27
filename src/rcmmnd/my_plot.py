import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style('dark')

# plt.figure(figsize=(8,6))
plt.rcParams['patch.force_edgecolor'] = True


def plt_hist(data, bins, xlabel='', ylabel='', facecolor='blue', alpha=0.5):
    plt.clf()
    plt.hist(data, bins=bins, facecolor=facecolor, alpha=alpha)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def sns_jointplot(data, x, y, alpha=0.4):
    sns.jointplot(data=data, x=x, y=y, alpha=alpha)
