#!/bin/bash
aws s3 sync pdcdump/ s3://viquity-database-import-us-east-1/Jobs/pdc/pdc_archive/pdcdump-"$(date +%d-%m-%y-%H-%M)"/
