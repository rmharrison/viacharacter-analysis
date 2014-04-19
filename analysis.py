################################################################################
# ViaCharacter analysis tool
# Ryan M Harrison
# ryan.m.harrison@gmail.com
################################################################################

import glob
import numpy as np
import pylab as P

#Dictionary from long-name to abbreviated-name
attribDict={}
attribDict["Appreciation of Beauty & Excellence"]="Appreciation"
attribDict["Bravery"]="Bravery"
attribDict["Creativity"]="Creativity"
attribDict["Curiosity"]="Curiosity"
attribDict["Fairness"]="Fairness"
attribDict["Forgiveness"]="Forgiveness"
attribDict["Gratitude"]="Gratitude"
attribDict["Honesty"]="Honesty"
attribDict["Hope"]="Hope"
attribDict["Humility"]="Humility"
attribDict["Humor"]="Humor"
attribDict["Judgment"]="Judgement"
attribDict["Kindness"]="Kindness"
attribDict["Leadership"]="Leadership"
attribDict["Love"]="Love"
attribDict["Love of learning"]="Learning"
attribDict["Perseverance"]="Perserverance"
attribDict["Perspective"]="Perspective"
attribDict["Prudence"]="Prudence"
attribDict["Self-Regulation"]="Self-Regulation"
attribDict["Social intelligence"]="Social Int"
attribDict["Spirituality"]="Spirituality"
attribDict["Teamwork"]="Team Work"
attribDict["Zest"]="Zest"
attribList=np.sort(attribDict.keys())
attribListAbrv=np.sort(attribDict.values())

# Outputs master data structure
# Input file structure...
##2000001 : <NAME>
#Attribute1 (e.g. Hope)
#...
#Attribute24 (e.g. Love of learning)
def get_data(crawl_location='sample_data/*.txt'):
    data=[]
    filelist = glob.glob(crawl_location)
    for file in filelist:
        try:
            data.append(np.genfromtxt(file,dtype='str',delimiter='\n'))
        except IOError:
            pass
    data=np.array(data)
    return data

# Output, for a given rank
# Attribute (e.g. Honesty, Love), Frequency
def get_byRank(data, rank=0):
    byRank=[]
    for attrib in attribList:
            byRank.append([attrib, np.sum(data[:,rank]==attrib)])
    byRank=np.array(byRank)
    return byRank

# Output, for a given attribute
# rank (e.g. 0,1,2), Frequency
def get_byAttrib(data, attrib='Love'):
    byAttrib=[]
    Nattrib=np.size(data,1)
    for rank in range(Nattrib):
            byAttrib.append([rank, np.sum(data[:,rank]==attrib)])
    byAttrib=np.array(byAttrib)
    return byAttrib

# Output bool array, one entry per record if the attribute was at a given position in the ranklist
def get_byAttribRankRange(data, attrib='Love', ranklist=[0]):
    rank=ranklist[0]
    byAttribRankRange=data[:,rank]==attrib
    for rank in ranklist[1:]:
        byAttribRankRange=reduce(lambda x, y: x+y,[byAttribRankRange,data[:,rank]==attrib])
    return byAttribRankRange

def plot_pairwise_corrcoef(data,ranklist=range(16,24),title="Correlation Coefficient"):
    array_byAttribRankRange=[]
    for attrib in attribList:
        array_byAttribRankRange.append(get_byAttribRankRange(data, attrib=attrib, ranklist=ranklist))
    Narray = len(array_byAttribRankRange)

    array_corrcoef=np.zeros((Narray,Narray),dtype='float')
    for i,elemi in enumerate(array_byAttribRankRange[::-1]):
        for j,elemj in enumerate(array_byAttribRankRange[::-1]):
            if i>j:
                    continue
            elif i==j:
                array_corrcoef[i,j]=1
            else:
                array_corrcoef[i,j]=np.corrcoef(elemi,elemj)[0,1]

    P.pcolor(np.transpose(array_corrcoef), cmap=P.cm.RdBu, alpha=0.8)
    P.title(title)
    P.xlim([0,23])
    P.ylim([0,23])
    P.clim([-1,1])
    P.xticks(range(len(attribList)), attribListAbrv[::-1],rotation='vertical')
    P.yticks(range(len(attribList)), attribListAbrv[::-1])
    P.subplots_adjust(bottom=0.35)
    P.subplots_adjust(left=0.25)
    P.colorbar()
    return array_corrcoef


def plot_multiplot_histogram(data):
    xcol=4
    ycol=6
    for index,attrib in enumerate(attribList):
        byAttrib=get_byAttrib(data,attrib)
        P.suptitle('Attribute Histograms')
        ax = P.subplot(xcol,ycol,index+1)
        plot_histogram(byAttrib,attrib=attribDict[attrib],bool_labels=False)
        for item in ax.get_xticklabels():
            item.set_fontsize(0)
        for item in ax.get_yticklabels():
            item.set_fontsize(0)
        if index % ycol == 0:
            P.ylabel('Probability')
            for item in ax.get_yticklabels():
                item.set_fontsize(8)
        if index > (xcol-1)*ycol-1:
            P.xlabel('Rank')
            for item in ax.get_xticklabels():
                item.set_fontsize(8)
        P.xlim([1,24])
        P.ylim([0,0.25])
        ax.yaxis.label.set_size(10)
        ax.xaxis.label.set_size(10)
        if np.sum(byAttrib[0:7,1])>2*np.sum(byAttrib[16:23,1]):
            P.text(20,0.20,'+')
        elif np.sum(byAttrib[16:23,1])>2*np.sum(byAttrib[0:7,1]):
            P.text(20,0.20,'-')
    P.subplots_adjust(hspace=.50)
    P.subplots_adjust(wspace=.50)
    P.subplots_adjust(bottom=0.1)

def plot_histogram(byAttrib,attrib="Love",bool_labels=True):
    P.plot(byAttrib[:,1]/float(np.sum(byAttrib[:,1])))
    P.title(attrib, fontsize=10)
    if bool_labels:
        P.xlabel('Rank',fontsize=10)
        P.ylabel('Probability',fontsize=10)

def plot_rankplot(byRank, rank=0):
    #Sort by rank
    int_byRank=np.array(byRank[:,1],dtype='int')
    aarg=np.argsort(int_byRank)[::-1]
    sorted_byRank = byRank[aarg]

    P.title('Whittaker-esque plot of Attributes (Rank=%s)' % (str(rank+1)))
    P.xlabel('Attribute Name')
    P.ylabel('Probability')
    x_values=range(len(sorted_byRank))
    x_labels=[]
    for attrib in sorted_byRank[:,0]:
        x_labels.append(attribDict[attrib])
    int_sorted_byRank=np.array(sorted_byRank[:,1],dtype='int')
    y_values=int_sorted_byRank/float(np.sum(int_sorted_byRank))
    P.plot(x_values,y_values)
    P.xticks(x_values, x_labels,rotation='vertical')
    P.ylim([0,0.25])
    fig = P.gcf()
    fig.subplots_adjust(bottom=0.35)

def plot_master():
    data=get_data()
    P.clf()
    dpi=300

    # Pairwise correlation plots
    plot_pairwise_corrcoef(data,ranklist=range(18,24),title="Correlation Coefficient (4th Quartile / Bottom)")
    P.savefig('corrcoef_Q4_bottom.png',dpi=dpi)
    P.clf()
    plot_pairwise_corrcoef(data,ranklist=range(12,18),title="Correlation Coefficient (3nd Quartile / Average)")
    P.savefig('corrcoef_Q3_average.png',dpi=dpi)
    P.clf()
    plot_pairwise_corrcoef(data,ranklist=range(6,12),title="Correlation Coefficient (2nd Quartile / Average)")
    P.savefig('corrcoef_Q2_average.png',dpi=dpi)
    P.clf()
    plot_pairwise_corrcoef(data,ranklist=range(6),title="Correlation Coefficient (1st Quartile / Top)")
    P.savefig('corrcoef_Q1_top.png',dpi=dpi)
    P.clf()

    # Histogram
    plot_multiplot_histogram(data)
    P.savefig('multiplot_histogram.png',dpi=dpi)
    P.clf()

    for rank in range(24):
        byRank=get_byRank(data,rank)
        plot_rankplot(byRank, rank=rank)
        filename="byRank_%s.png" % str(rank+1)
        P.savefig(filename,dpi=dpi)
        P.clf()
    return data

if __name__ == '__main__':
    data=plot_master()

