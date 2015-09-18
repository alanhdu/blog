#!/bin/sh

find build/ -name *.html | xargs -L 1 sed --in-place s#=\"/static#=\"/~ahd2125/static#g
