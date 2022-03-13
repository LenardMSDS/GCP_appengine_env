from flask import Flask,render_template,request
from google.cloud import bigquery
app = Flask(__name__)
 
@app.route("/")
def form():
    return render_template('form.html')



@app.route("/")
def reg_pred(a,b,c,d):
    client = bigquery.Client()
    type2="'"+a+"'"
    bed2=b
    bath2=c
    sqft2=d
    query="""
select * 


from  ML.PREDICT(MODEL `week9-343320.housing.price_model_reg`,


(
    select
 %s as type
  ,%s as BEDS
  ,%s as BATHS
  ,%s as sqft

FROM `week9-343320.housing.redfin` where PRICE is not null  and sqft is not null and BEDS is not null and BATHS is not null ))
        
        """ % (type2,bed2,bath2,sqft2)
        # .format('Single Family Residential', 3, 2, 2000)
    
    query_job = client.query(query)

    results = query_job.result()  # Waits for job to complete.


    # return results 
    for row in results:
         return ("{}".format(row.predicted_PRICE))


@app.route("/", methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form.to_dict()
        
        a=form_data['Property Type']
        b=form_data['Beds']
        c=form_data['Baths']
        d=form_data['SQFT']
        predicted_value=reg_pred(a,b,c,d)
        form_data['Predicted Price']="$"+format(float(predicted_value),",.0f")

        return render_template('data.html',form_data = form_data)
# @app.route("/<int:num>")
# def blogs(num):
#     return render_template('blog.html',number=num)
   
if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host="127.0.0.1", port=8081, debug=True)