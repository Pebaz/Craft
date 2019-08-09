pushd ..
pytest --cov=src src
#pytest --cov=src src --cov-report html
#pytest --cov=src src --cov-report html -n 2
popd
