import bentoml
from sklearn import svm
from sklearn import datasets

# load dataset
iris = datasets.load_iris()
X, y = iris.data, iris.target

# train model
clf = svm.SVC(gamma='scale')
clf.fit(X, y)

# Save model to BentoML local model store
saved_model = bentoml.sklearn.save_model('iris_clf', clf)
print(f"Model saved: {saved_model}")

# Model saved: Model(tag="iris_clf:te666gxgsop5juud")
# $bentoml models list -> saved to bentoml model store