# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# from datetime import datetime
# import logging
# import os

from flask import Flask, redirect, render_template, request

# from google.cloud import datastore
# from google.cloud import storage
# from google.cloud import vision
from google.cloud import bigquery

# CLOUD_STORAGE_BUCKET = os.environ.get("CLOUD_STORAGE_BUCKET")


app = Flask(__name__)


@app.route("/")

def reg_pred():
    client = bigquery.Client()
    query_job = client.query(
        """
select * 


from  ML.PREDICT(MODEL `week9-343320.housing.price_model_reg`,


(
    select
'Single Family Residential' as type
,3 as BEDS
,3 as BATHS
,1400 as sqft
# type
# ,BEDS
# ,BATHS
# ,sqft
# ,PRICE
FROM `week9-343320.housing.redfin` where PRICE is not null  and sqft is not null and BEDS is not null and BATHS is not null ))
        
        """
    )

    results = query_job.result()  # Waits for job to complete.

    # return ("{}, {} Beds, {} Baths, Predicted Prices:{}".format(results.type, results.BEDS, results.BATHS, results.predicted_PRICE))
    # return results 
    for row in results:
         return ("{}, {} Beds, {} Baths, Predicted Prices:{}".format(row.type, row.BEDS, row.BATHS, row.predicted_PRICE))


if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host="127.0.0.1", port=8081, debug=True)
