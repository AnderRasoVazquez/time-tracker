#!/bin/bash

pygettext3.6 -d base -o locales/base.pot . 
msgcat locales/base.pot locales/es/LC_MESSAGES/base.po -o locales/es/LC_MESSAGES/base.po
