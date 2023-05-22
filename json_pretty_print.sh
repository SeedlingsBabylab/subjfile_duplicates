#!/bin/bash

# usage: ./json_pretty_print.sh inline.json prettyprint_output.json

cat $1 | python -m json.tool > $2
