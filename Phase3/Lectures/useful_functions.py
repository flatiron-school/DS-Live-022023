def train_lr_randomly(data, sample_pt=None, ntimes=100):
    '''
    Takes in features & targets from `data` to train a linear regression with a
    random sample `ntimes`. It then returns a list of R2 scores, RMSEs, and the 
    predictions from a provided data point of features `sample_pt`.
    '''
    
    import numpy as np
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error
    
    # To save all of our predictions
    r2 = []
    rmse = []
    # Only return predictions if there is something to predict (sample_pt given)
    point_preds = [] if (sample_pt is not None) else None

    # We'll repeat this little experiment to see how the model does
    for i in range(ntimes):
        # Creating a random sample of data to train on
        df_sample = data.sample(300, replace=True)
        y = df_sample.target
        X = df_sample.drop('target', axis=1)

        # Our linear regression model about to be trained
        lr = LinearRegression()
        lr.fit(X, y)

        # Making predictions & evaluating on the data we used to train the model
        y_hat = lr.predict(X)
        rmse.append(np.sqrt(mean_squared_error(y, y_hat)))
        r2.append(lr.score(X, y))

        # Making a prediction on the one point the model definitely never saw
        if sample_pt is not None:
            y_hat_pt = lr.predict(sample_pt)
            # Getting just the single point to add into list
            point_preds.append(y_hat_pt[0])
    
    return r2, rmse, point_preds

def plot_model_predictions(predictions, my_sample_target, second_predictions=None):
    '''
    This function will display our different models' predictions.
    '''
    
    from matplotlib import pyplot as plt
    import seaborn as sns
    
    if second_predictions == None:
        ax = sns.boxplot(x=predictions);
        ax = sns.swarmplot(x=predictions, color='orange', ax=ax)
        ax.set_title(f'Predicting Sample Pt Target: {my_sample_target:,.2f} (Simpler LR)');
    
    else:
        f, (ax1,ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(6, 4));

        # Simple model
        ax = sns.boxplot(x=predictions, ax=ax1);
        ax = sns.swarmplot(x=predictions, color='orange', ax=ax)
        ax.set_title(f'Predicting Sample Pt Target Value: {my_sample_target:,.2f} (Simpler LR)');

        # Complex model
        ax = sns.boxplot(x=second_predictions, ax=ax2);
        ax = sns.swarmplot(x=second_predictions, color='orange', ax=ax)
        ax.set_title(f'Predicting Sample Pt Target Value: {my_sample_target:,.2f} (More Complex LR)');

        # Makes spacing work better
        f.tight_layout()