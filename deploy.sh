#/bin/bash

source activate blog
python run.py build
scp -r build/* ahd2125@cunix.cc.columbia.edu:~/public_html/
