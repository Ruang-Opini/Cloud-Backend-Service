# Using Google Cloud Platform as Backend

> This repository contains complete code for running Machine Learning (ML) models purpose and getting document policy from a website.

Following Components are used for each purposes.
* Twitter API key: GET Twitter data using Twitter API
* Cloud Storage: Store ML models
* Cloud Functions: 
  1. Run ML models
  2. GET document policy from a website
* API Gateway: Manage all the API calls to serverless backends (in this case Cloud Functions)

This is how the architecture look a like.

Architecture: Serverless API with API Gateway for Running Machine Learning Models
![Sentiment Analysis](https://user-images.githubusercontent.com/71552937/121258345-fc850800-c8d8-11eb-828c-266844987587.png)

Architecture: Serverless API with API Gateway for Getting Policies On Website
![Getting Policies](https://user-images.githubusercontent.com/71552937/121258376-0444ac80-c8d9-11eb-9262-4551bed78ad6.png)

# Run Machine Learning Models on Google Cloud Platform
These following steps guide you how to run ML models using Cloud Functions.
## [1] Store ML Models on Cloud Storage
1. Create a bucket for storing ML models
2. Upload all the models and tokenizers to the bucket. Remember the filename, or you can rename it after the upload has done. It would be used by Cloud Functions to call the files.

In this case, we have 3 models:
1. GET policy trending list
> The model and tokenizer could be found [here](https://github.com/Ruang-Opini/Sentiment_Analysis/tree/main/Policy_Model)
2. GET sentiment result of tweets based on positive and negative responses
> The model and tokenizer could be found [here](https://github.com/Ruang-Opini/Machine-Learning/tree/sentiment_analysis)
3. GET sentiment result to detect buzzer
> The model could be found [here](https://github.com/Ruang-Opini/Machine-Learning/tree/buzzer)

## [2] Running ML Models on Cloud Functions: GET Policy Trending List
1. Go to Cloud Function on GCP
2. Click **CREATE FUNCTION**
3. Name the function on **Function name**
4. Choose **Region** as asia-southeast2 or any region you wish
5. Choose **HTTP** as **Trigger type**
6. Copy the URL provided for later purpose
7. For Authentication, select **Require authentication**, click SAVE
8. Click **RUNTIME, BUILD AND CONNECTIONS SETTINGS**
9. In RUNTIME tab, for **Memory allocated** you could select 1 GiB, for **Timeout** you could write 120
10. Left the others as default until you reach **Runtime environment variables**
11. For **Name**, use all variables using for using Twitter API: *consumer_key, consumer_secret, access_token, access_secret* and fill the **Value** met by the Twitter API key you got.
12. Click Next
13. Select Python 3.9 as the **Runtime** and fill the **Entry point** as *policy_sentiment*
14. Use this python code for main.py and define the dependencies on Requirements.txt. The full code could be accessed [here](https://github.com/Ruang-Opini/Cloud-Backend-Service/tree/main/Sentiment-Analysis/Policy_Model)
15. Click **DEPLOY** to deploy the function and wait for the deployment succeed

## [3] Running ML Models on Cloud Functions: GET Sentiment Result of Tweets
1. Go to Cloud Function on GCP
2. Click **CREATE FUNCTION**
3. Name the function on **Function name**
4. Choose **Region** as asia-southeast2 or any region you wish
5. Choose **HTTP** as **Trigger type**
6. Copy the URL provided for later purpose
7. For Authentication, select **Require authentication**, click SAVE
8. Click **RUNTIME, BUILD AND CONNECTIONS SETTINGS**
9. In RUNTIME tab, for **Memory allocated** you could select 1 GiB, for **Timeout** you could write 120
10. Left the others as default until you reach **Runtime environment variables**
11. For **Name**, use all variables using for using Twitter API: *consumer_key, consumer_secret, access_token, access_secret* and fill the **Value** met by the Twitter API key you got.
12. Click Next
13. Select Python 3.9 as the **Runtime** and fill the **Entry point** as *offensive_sentiment*
14. Use this python code for main.py and define the dependencies on Requirements.txt. The full code could be accessed [here](https://github.com/Ruang-Opini/Cloud-Backend-Service/tree/main/Sentiment-Analysis/Offensive-Buzzer_Model/Offensive)
15. Click **DEPLOY** to deploy the function and wait for the deployment succeed

## [4] Running ML Models on Cloud Functions: GET Sentiment Result to Detect Buzzer
1. Go to Cloud Function on GCP
2. Click **CREATE FUNCTION**
3. Name the function on **Function name**
4. Choose **Region** as asia-southeast2 or any region you wish
5. Choose **HTTP** as **Trigger type**
6. Copy the URL provided for later purpose
7. For Authentication, select **Require authentication**, click SAVE
8. Click **RUNTIME, BUILD AND CONNECTIONS SETTINGS**
9. In RUNTIME tab, for **Memory allocated** you could select 1 GiB, for **Timeout** you could write 120
10. Left the others as default until you reach **Runtime environment variables**
11. For **Name**, use all variables using for using Twitter API: *consumer_key, consumer_secret, access_token, access_secret* and fill the **Value** met by the Twitter API key you got.
12. Click Next
13. Select Python 3.9 as the **Runtime** and fill the **Entry point** as *offensive_sentiment*
14. Use this python code for main.py and define the dependencies on Requirements.txt. The full code could be accessed [here](https://github.com/Ruang-Opini/Cloud-Backend-Service/tree/main/Sentiment-Analysis/Offensive-Buzzer_Model/Buzzer)
15. Click **DEPLOY** to deploy the function and wait for the deployment succeed

# Deploy Function to Get Document Policies
We did scraping from https://peraturan.go.id/ to get the document policies. The GET method then run on Cloud Function.
There are 4 functions that should be deployed:
1. GetAllPolicyCategory
2. GetPolicyByCategory
3. GetPolicyByType
4. GetDocumentPolicy

## Get Policy
> Deploy this in 4 separate functions based on [codes provided here](https://github.com/Ruang-Opini/Cloud-Backend-Service/tree/main/Get-Policy)
The steps below applied to 4 functions.
1. Go to Cloud Function on GCP
2. Click **CREATE FUNCTION**
3. Name the function on **Function name**
4. Choose **Region** as asia-southeast2 or any region you wish
5. Choose **HTTP** as **Trigger type**
6. Copy the URL provided for later purpose
7. For Authentication, select **Require authentication**, click SAVE
8. Click Next
9. Select Python 3.9 as the **Runtime** and fill the **Entry point** consecutively as *getAllPolicyCategory*, *getPolicyByCategory*, *getPolicyByType*, and *getDocumentPolicy*
10. Fill the main.py and define the dependencies on Requirements.txt based on link [above](https://github.com/Ruang-Opini/Cloud-Backend-Service/tree/main/Get-Policy)
11. Click **DEPLOY** to deploy the function and wait for the deployment succeed

# Create OpenAPI Rules to Define Endpoints and Backend Services
We use Swagger to define the rules with 2 different yaml files: 
1. For the sentiment analysis purpose. The file could be found on [openapi-sentiment.yaml](https://github.com/Ruang-Opini/Cloud-Backend-Service)
2. For the document policy purpose. The file could be found on [openapi-definition.yaml](https://github.com/Ruang-Opini/Cloud-Backend-Service)
> Use different filenames for both to differ them on the next steps.

# Deploy API on API Gateway
Two APIs are created here: one for sentiment analysis purpose and the other one for the document policy purpose.
Follow these steps below to create API using Cloud Shell. 

## API for Sentiment Analysis Purpose
1. Enable API for Cloud Build, Cloud Function, and three required services.
```
gcloud services enable apigateway.googleapis.com
gcloud services enable servicemanagement.googleapis.com
gcloud services enable servicecontrol.googleapis.com
```
2. Set environment for these three.

If you haven't had the service account email, create it on **APIs & Services** --> **Credentials**. Click **CREATE CREDENTIALS** --> **Service account**. 
Name your service account. In this case, I use backend-auth-service as the service account name. Click **CREATE AND CONTINUE**, select **Owner** as the role, 
and then **DONE**.
```
## specify the correct path for the yaml file, remove the {}
export API_DEFINITION="/{path}/openapi-sentiment.yaml"      
export PROJECT_ID="YOUR_PROJECT_ID"                        
export SERVICE_ACCOUNT_EMAIL="backend-auth-service@YOUR_PROJECT_ID.iam.gserviceaccount.com"    
```
3. Create API
```
## replace your-sentiment-api-name with the name you wish
gcloud beta api-gateway apis create your-sentiment-api-name --project=$PROJECT_ID     
```
4. Create API config using the yaml file we've created before
```
## replace your-sentiment-config with the config name you want
gcloud beta api-gateway api-configs create your-sentiment-config \                
--api=your-sentiment-api-name --openapi-spec=$API_DEFINITION \
--project=$PROJECT_ID --backend-auth-service-account=$SERVICE_ACCOUNT_EMAIL
```
5. Enable API
```
gcloud beta api-gateway apis describe your-sentiment-api-name --project=$PROJECT_ID
```
6. After enabled successfully, enable the API name from managedService field.
```
gcloud services enable your-sentiment-api-name-HASH.apigateway.PROJECT_ID.cloud.goog
```
## API for Get Policy Purpose
1. Set environment for these three.
```
## specify the correct path for the yaml file, remove the {}
export API_DEFINITION="/{path}/openapi-definition.yaml"      
export PROJECT_ID="YOUR_PROJECT_ID"                        
export SERVICE_ACCOUNT_EMAIL="backend-auth-service@YOUR_PROJECT_ID.iam.gserviceaccount.com"    
```
2. Create API
```
## replace your-policy-api-name with the name you wish
gcloud beta api-gateway apis create your-policy-api-name --project=$PROJECT_ID     
```
4. Create API config using the yaml file we've created before
```
## replace your-policy-config with the config name you want
gcloud beta api-gateway api-configs create your-policy-config \                
--api=your-policy-api-name --openapi-spec=$API_DEFINITION \
--project=$PROJECT_ID --backend-auth-service-account=$SERVICE_ACCOUNT_EMAIL
```
5. Enable API
```
gcloud beta api-gateway apis describe your-policy-api-name --project=$PROJECT_ID
```
6. After enabled successfully, enable the API name from managedService field.
```
gcloud services enable your-policy-api-name-HASH.apigateway.PROJECT_ID.cloud.goog
```
## Create Gateway
For the sentiment analysis purpose, we're gonna create 3 gateways to avoid crowded traffic and timeout.
1. Gateway to GET Trending list
   
For the region, API Gateway supports only [11 GCP regions](https://cloud.google.com/api-gateway/docs/deployment-model) for deployment.
```
## you could change the trending-gateway as the gateway name you wish
gcloud beta api-gateway gateways create trending-gateway \
--api=your-sentiment-api-name --api-config=your-sentiment-config \
--location=asia-east1 --project=$PROJECT_ID
        
gcloud beta api-gateway gateways describe trending-gateway \
--location=us-central1 --project=$PROJECT_ID
```
2. Gateway to GET Sentiment Result of Tweets
```
## you could change the offensive-gateway as the gateway name you wish
gcloud beta api-gateway gateways create offensive-gateway \
--api=your-sentiment-api-name --api-config=your-sentiment-config \
--location=us-central1 --project=$PROJECT_ID
        
gcloud beta api-gateway gateways describe offensive-gateway \
--location=us-central1 --project=$PROJECT_ID
```    
3. Gateway to GET Sentiment Result of Buzzer Detection
```
## you could change the buzzer-gateway as the gateway name you wish
gcloud beta api-gateway gateways create buzzer-gateway \
--api=your-sentiment-api-name --api-config=your-sentiment-config \
--location=us-central1 --project=$PROJECT_ID
        
gcloud beta api-gateway gateways describe buzzer-gateway \
--location=us-central1 --project=$PROJECT_ID
```    
4. Gateway to GET Policies
```
## you could change the policy-gateway as the gateway name you wish
gcloud beta api-gateway gateways create policy-gateway \
--api=your-policy-api-name --api-config=your-policy-config \
--location=asia-east1 --project=$PROJECT_ID
        
gcloud beta api-gateway gateways describe policy-gateway \
--location=asia-east1 --project=$PROJECT_ID
```    
9. Use the defaultHostname as the gateway link.

The gateway would look like this: trending-gateway-{HASH}.uc.gateway.dev/Trending

or if using query: buzzer-gateway-{HASH}.uc.gateway.dev/Buzzer?trending={input the trending here}

## API Gateway Authorization

This is to give authorization to API gateway so that that it will be able to access resources in services. Do this for total 7 functions you've built before by differ them on the function name.
```
## Replace BuzzerDetection with each your functions deployed
gcloud functions add-iam-policy-binding BuzzerDetection \
--region asia-southeast2 \
--member "serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
--role "roles/cloudfunctions.invoker" \
--project $PROJECT_ID
```

## Redeploy if there's any change in config file

Ex: if you made change in openapi-sentiment.yaml, then you should redeploy the config and the gateway linked to the config.

    gcloud beta api-gateway api-configs create your-new-sentiment-config \
    --api=your-sentiment-api-name --openapi-spec="/{path}/openapi-sentiment.yaml" \
    --project=$PROJECT_ID --backend-auth-service-account=$SERVICE_ACCOUNT_EMAIL

    gcloud beta api-gateway gateways update buzzer-gateway \
    --api=your-sentiment-api-name --api-config=your-new-sentiment-config \
    --location=us-central1 --project=$PROJECT_ID
    
### Last, the gateway links then used by Android app for getting the results and datas.
