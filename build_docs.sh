poetry run pdoc --html --force --output-dir docs learnmltrading/
mv docs/learnmltrading/* docs/
rm -r docs/learnmltrading
