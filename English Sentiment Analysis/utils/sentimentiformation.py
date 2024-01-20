import matplotlib.pyplot as plt
import seaborn as sns

def sentiment_percentage(data, target, figsize):
    fig, ax = plt.subplots(figsize = figsize)
    ax.pie(data[target].value_counts(), 
            labels=data[target].unique(),
            colors=['tomato', 'cornflowerblue', 'gold', 'orchid', 'green'], 
            autopct='%1.1f%%',
            textprops = {'size': 'large'})
    plt.title('{} Percentage'.format(target))
    return plt.show()

def sentiment_counts(data, target, figsize):
    ax, fig = plt.subplots(figsize = figsize)
    ax =sns.countplot(x=target, data=data, dodge=False, hue=target,  order= data[target].value_counts().index, hue_order =data[target].value_counts().index,  palette=sns.color_palette("Set2", 5), legend='full');
    ax.set(xticklabels=[]) 
    ax.set(ylabel=None) 
    plt.title('{} Count'.format(target))
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    return plt.show()