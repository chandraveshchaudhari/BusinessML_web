# BusinessML_web
- Consists of JupyterBOOK
- JupyterLite
- Colab
- Download Button
- 
## Steps to follow

jupyter-book build notebooks/
cp -r notebooks/_build/html/* docs/
python3  forced_jupyterlite_button.py
mkdir -p jupyterlite_things
cp notebooks/*.ipynb jupyterlite_things/
cd jupyterlite_things/
jupyter lite build
cp -r _output/* ../docs/jupyterlite/
cd ..
rm -r jupyterlite_things/