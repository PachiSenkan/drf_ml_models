import pickle
import numpy as np
import pandas as pd


def load_model_file(ml_model):
    with open('media/' + str(ml_model), 'rb') as filestream:
        clf = pickle.load(filestream)
        return clf


def get_features_from_model(model):
    list_of_features = []

    for ind, __ in enumerate(model.domain.attributes):
        list_of_features.append(model.domain.attributes[ind].name)
    return list_of_features


def get_values_for_model(model, ml_model, model_inputs):
    list_of_features = get_features_from_model(model)
    dict_of_val_for_model = {}
    print(list_of_features)
    print(ml_model.inputs)
    #if len(model_inputs) < len(list_of_features):
    #    print('MALO')
    #    return None

    for i, colName in enumerate(list_of_features):
        #if colName in ml_model.inputs:
        dict_of_val_for_model[colName] = model_inputs[i]
    print(dict_of_val_for_model)
    return dict_of_val_for_model


def calculate_diagnose_disease(ml_model, model_inputs):
    clf = load_model_file(ml_model.ml_model)
    dict_of_val_for_model = get_values_for_model(clf, ml_model, model_inputs)
    df_for_model = pd.DataFrame.from_dict(dict_of_val_for_model, orient='index', dtype=np.float64).T
    target_clases_name = ['Здоров', 'Болен']
    y_probability = clf.predict_proba(df_for_model.values)[0]
    print(y_probability)
    return y_probability

