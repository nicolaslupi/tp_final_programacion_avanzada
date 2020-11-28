import pickle

class ModeloSpam(object):
    def __init__(self, transform_entrenado, pca_entrenado, svm_entrenado):
        self.tfidf = transform_entrenado
        self.pca = pca_entrenado
        self.svm = svm_entrenado
        
    def predict_email(self, text):
        transf_text = self.tfidf.transform([text])
        transf_dense = transf_text.todense()
        pca_text = self.pca.transform(transf_dense)
        return self.svm.best_estimator_.predict(pca_text)

    def save_spam_model(self, out_path='.', out_name='trained_spam_model'):
        """Save the full model object in a pickle.
        Args:
            out_path (str, optional): Path to save pickled model.
                Defaults to '.'.
            out_name (str, optional): Name to save pickled model.
                Defaults to 'stacked-ensemble'.
        """
        with open(f'{out_path}/{out_name}.pkl', 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_spam_model(in_path='.', in_name='trained_spam_model'):
        """Static method to load a previously-saved pickeld model.
        Usage for this is as follow:
        my_new_stacked = StackedEnsembleModel.load_stacker(...)
        Args:
            in_path (str, optional): Path for saved pickled model.
                Defaults to '.'.
            in_name (str, optional): Name for saved pickled model.
                Defaults to 'stacked-ensemble'.
        Returns:
            [type]: [description]
        """
        with open(f'{in_path}/{in_name}.pkl', 'rb') as f:
            return pickle.load(f)