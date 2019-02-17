rm -rf dist
python3 setup.py sdist bdist_wheel
twine upload -u just4test dist/*