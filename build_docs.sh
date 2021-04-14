poetry run pdoc --html --force --output-dir docs learnmltrading/src/ 
mv docs/src/* docs/
rmdir docs/src/


