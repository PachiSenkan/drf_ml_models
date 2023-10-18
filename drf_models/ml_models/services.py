import pickle
import Orange


def get_input_data(ml_model):
    print(ml_model)
    with open('media/' + str(ml_model), 'rb') as filestream:
        clf = pickle.load(filestream)
    list_of_features = []

    for ind, __ in enumerate(clf.domain.attributes):
        list_of_features.append(clf.domain.attributes[ind].name)
    return list_of_features
