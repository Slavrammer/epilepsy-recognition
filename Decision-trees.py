# Load libraries
import os
from pandas import read_csv
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

os.chdir(input('Enter path'))

names = ['Permutation entropy',
         'Spectral entropy',
         'Singular value decomposition entropy',
         'Approximate entropy',
         'Sample entropy',
         'Hjorth mobility',
         'Hjorth complexity',
         'Number of zero-crossings',
         'num_lzivcomplexity',
         'petrosian',
         'katz',
         'higuchi',
         'dfa',
         'label']

# Load dataset
for i in range(1, 8):
    filename = f'zebrane paczki_{i}.csv'

    dataset = read_csv(filename, delimiter=',', names=names, skiprows=1)
    dataset = dataset.drop(['num_lzivcomplexity'], axis=1)

    # Split-out validation dataset
    array = dataset.values
    X = array[:, 0:12].astype(float)
    Y = array[:, 12]
    validation_size = 0.20
    seed = 7
    X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y,
                                                                    test_size=validation_size, random_state=seed)

    # Test options and evaluation metrics
    num_folds = 10
    scoring = 'accuracy'

    # FINALIZING MODEL
    scaler = StandardScaler().fit(X_train)
    rescaledX = scaler.transform(X_train)
    model = DecisionTreeClassifier()
    model.fit(rescaledX, Y_train)

    # estimate accuracy on validation dataset
    rescaledValidationX = scaler.transform(X_validation)
    predictions = model.predict(rescaledValidationX)
    print(accuracy_score(Y_validation, predictions))
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))

  
