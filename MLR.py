
import numpy as np


def center_and_scale(vectors):
    """ Subtract mean and devide by standard deviation.
    This is done for each (column?) of the vectors 2D numpy array.  This makes
    the vectors dimentionless so you can compare 2 very different independent
    variables, like fan speed and chaffer spacing

    Args:
        vectors (1 or 2 D numpy array):
            ...

    Returns:
        vectors: same as input, but centered and scaled

        means: numpy array of means (if vector then it is just 1 number)

        stds:  ditto.  with these values you can reconstruct things later if
            desired
    """

    means = np.mean(vectors,0)
    vectors = vectors - means

    stds = np.std(vectors, 0)
    vectors = vectors/stds

    return vectors, means, stds



def MLR( X0, Y0 ):
    """ Multiple Linear Regression
    Models the relationship between X and Y based on empiricle data

    Args:
        X0 (1 or 2D numpy array):
            These are the independent variable(s)

        Y0 (1D numpy array):
            Dependent variable

    Returns:
        Ypredicted (1D numpy array)
            This is what the model would predict given X0
        Beta (2D numpy array)
            This is the model.  multiply by X0 to get Y
        adjR2 (float):
            Always <= R2.  If you include an extra column of random numbers in
            X0, R2 will generally get better, but adjR2 will get worse.
    """

    X, _, _ = center_and_scale(X0)
    Y, mean, std = center_and_scale(Y0)

    Beta = X.T.dot(X);
    Beta = np.linalg.inv(Beta)
    Beta = Beta.dot(X.T.dot(Y))

    Ypredict = X.dot(Beta)
    # adjusted R2 should account for number of samples and number of explanitory variables
    adjR2 = 1-np.sum((Ypredict-Y)**2)/np.sum((Y - np.mean(Y))**2)


    return Ypredict*std+mean, Beta, adjR2


def importance(X0,Y):
    """ Leaves out 1 column of X0 at a time to see how much adjR2 depends on it

    Args:
        X0 (1 or 2D numpy array):
            These are the independent variable(s)

        Y0 (1D numpy array):
            Dependent variable

    Returns:
        importance (1D numpy array, length of the numbe of columns in X0)
            How much did adjR2 decrease when each variable was removed

    """
    Ypredict, Beta, adjR20 = MLR( X0, Y )
    importance = np.zeros(Beta.shape)

    for setting in range(X0.shape[1]):
        X = np.delete(X0,setting,1)
        Ypredict, Beta, adjR2 = MLR( X, Y )
        importance[setting] = adjR20 - adjR2

    return importance









def PLS(spectra, known_values, numcomps):
    
    WW=np.empty([spectra.shape[1],numcomps])
    PP=np.empty([spectra.shape[1],numcomps])
    qq=np.empty([1,numcomps])
    
    #initial weight guess
    ww = np.dot(np.transpose(spectra),known_values)
    ww = ww/np.linalg.norm(ww)

    # initial scores
    tt = np.dot(spectra,ww)
        
    
    for i in range(0,numcomps):
        # normalize scores
        ti = np.dot(np.transpose(tt),tt)
        tt = tt/ti
    
        # principle component vector
        pp = np.dot(np.transpose(spectra),tt)
        PP[:,i] = pp[:,0] # all PC vectors
    
        # principle vector of Y? Y-weights
        qi = np.dot(np.transpose(known_values),tt)
        qq[:,i]=qi
    
        WW[:,i] = ww[:,0] #all the weights
    
        # deflate X
        spectra = spectra-ti*tt*np.transpose(pp)
        ww = np.dot(np.transpose(spectra),known_values) # new weights
        tt = np.dot(spectra,ww) # new scores
        continue
        
    P=np.dot(np.transpose(PP),WW)#So that the opperations were successful    
    WWp = np.dot(WW,np.linalg.inv(P))
    BB = np.dot(WWp,np.transpose(qq))
    

    return BB







def meancenter(spectra):
    return spectra - np.mean(spectra,0)

def SNV(spectra):
    return spectra/np.std(spectra,0)

def MSC(spectra,refspec=None):
    if refspec == None:
        refspec = np.mean(spectra,1)
    fit = np.polyfit(refspec,spectra,1)
    return (spectra-fit[1,:])/fit[0,:]

def remove_outliers(spectra, known_values, stdsaway = 2):
    initialnumber = spectra.shape[1]
    fff = spectra.reshape([spectra.shape[0],5,-1])
    spectrameans = np.mean(fff,1)
    spectrastds = np.std(fff,1)
    outlier_matrix = (np.rollaxis(fff,1,0)>spectrameans+stdsaway*spectrastds) + \
            (np.rollaxis(fff,1,0)<spectrameans-stdsaway*spectrastds)

    nonoutliers = (np.sum(outlier_matrix,1)<5).ravel()

    known_values = known_values[nonoutliers]
    spectra = spectra[:,nonoutliers]


    print('removed ' + str(initialnumber - np.sum(nonoutliers)) + ' outliers' )

    return spectra, known_values