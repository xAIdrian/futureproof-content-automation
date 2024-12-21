# Porygon Autonomous Chat VideoGenerator

 <img src="https://github.com/user-attachments/assets/3a1380fe-b7f7-45a2-be77-51bdf3b07909" align="right" width="100" height="100" alt="Porygon Logo">

### Table of Contents
  - [Project Description](#project-description)
  - [Using this app](#using-this-app)
  - [Quick Start Commands in Dev Mode](#quick-start-commands-in-dev-mode)
  - [Deployment Instructions](#deployment-instructions)
  - [Setting up the project](#setting-up-the-project)
  - [Setting Up Integrations](#setting-up-integrations)
  - [Additional Deployment Steps](#additional-deployment-steps)

### Project Description

We have built a flask server that the generates a vide of a chat conversation after entering brief description of the conversation, a caption, and the name of the viewer of the conversations and then posts automatically to TikTok and Instagram.

**Here's how we built it:
**
1. Generate scenarios
   - Create dynamic conversations between two people using the ChatGPT API [you can get your key here](https://platform.openai.com/api-keys) and will need to be set in secrets file.
   - Conversation is then passed within backend to our image generation tools.

2. Generate the video from images
   - We then use the Pillow library to generate images of the conversation.
   - We then use the moviepy library to sequence the images and add sound effects.

3. Upload to Instagram
   - We submit our instagram API key to the backend and then use the instagram API to upload the video to Instagram.
   - [Information needed for publishing reels using native IG](https://github.com/fbsamples/reels_publishing_apis/tree/main/insta_reels_publishing_api_sample?fbclid=IwZXh0bgNhZW0CMTEAAR1wf3OKOAHY3xp09E6USeHq7UJMblg9DK5oS0h31-_mYIx4qjGt4w1L9D4_aem_wWDShfiY8ppLdmrNlVMP9A)
   - [Publishing reels using graph.instagram.com not facebook](https://developers.facebook.com/docs/video-api/guides/reels-publishing)
   - [Handling error codes and expired tokens](https://developers.facebook.com/docs/facebook-login/guides/access-tokens#generating-an-app-access-token)

4. Upload to TikTok
   - We supply our client id and client secret in secret and use these to authenticate with TikTok through browser.
   - A redirect url is set in the TikTok developer portal and we use this to redirect to our backend.
   - It must be a production url to publish to TikTok.

### Using this app

**Authenticate with TikTok**
<img width="2537" alt="Screenshot 2024-11-19 at 6 37 15 PM" src="https://github.com/user-attachments/assets/0c79a66a-bb9e-4b41-88db-d478c9510226">

**Authenticate with Instagram**
<img width="2544" alt="Screenshot 2024-11-19 at 6 38 10 PM" src="https://github.com/user-attachments/assets/3840a7cb-a00b-4572-acca-80ac986c71f8">

**Generate a video**
<img width="2543" alt="Screenshot 2024-11-19 at 6 38 40 PM" src="https://github.com/user-attachments/assets/424011cc-e4af-48af-a8a9-ada7bb61f118">

**Done!**


 ### Quick Start Commands in Dev Mode

Run react app
```
cd frontend && npm install && npm start
```
Ensure daisyUI is running
```
cd frontend && npx tailwindcss -i ./src/index.css -o ./src/output.css --watch
```
Run flask backend
```
cd backend && python init.py
```

### Deployment Instructions

Let's start with deploying our backend to GCP Cloud Run Service.

Replace `porygon-video-generation` with your project id.  Replace `chat-image-generator` with the name of your service.

Here's what do do if you need permission for your service account:
```
gcloud config set project YOUR_PROJECT_ID

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:YOUR_SERVICE_ACCOUNT_EMAIL" \
    --role="roles/storage.objectAdmin"
```

```
cd backend

# Runnable Docker
docker build -t gcr.io/porygon-video-generation/chat-image-generator .
docker push gcr.io/porygon-video-generation/chat-image-generator

# Deploy to Cloud Run
gcloud builds submit --tag gcr.io/porygon-video-generation/chat-image-generator

gcloud run deploy chat-image-generator --image gcr.io/porygon-video-generation/chat-image-generator --platform managed --region us-central1 --allow-unauthenticated

# Get service url
gcloud run services describe chat-image-generator --platform managed --region us-central1 --format 'value(status.url)'

# Test deployment
curl -X GET \ 
-H "Content-Type: application/json" \
https://chat-image-generator-p22cordwkq-uc.a.run.app/tiktokauth
```

For the frontend, we use firebase.

```
cd frontend
npm install firebase-tools
npm run build:production
firebase login
firebase init 
# select project
# select only hosting NOT app hosting
firebase deploy --only hosting
```

### Setting up the project

Clone the project
```
git clone https://github.com/millionairemacmillionairemac/ai-generated-text-convo-video.git
```

Run the following command to install python dependencies in the backend folder
```
cd backend && pip install -r requirements.txt
```

### Setting Up Integrations

We'll be working with

- Google Cloud and Google Cloud Storage
- TikTok API
- Instagram API

#### Getting a service account json key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to the "IAM & Admin" section
3. Click on "Service Accounts"
4. Click on "Create Service Account"

#### Creating a Google Cloud Storage bucket

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to the "Storage" section
3. Click on "Create Bucket"
4. Fill out the required information and click on "Create"

#### Creating a developer account on TikTok

1. Go to the [TikTok Developer Portal](https://developers.tiktok.com/en) and log in with your TikTok account
2. Click on "Create App"
3. Fill out the required information and click on "Create"
4. In the sidebar on the left, click on "Settings"
5. In the "OAuth" tab, click on "Add"
6. Add `https://localhost:8000/redirect` as the "OAuth redirect URI"
7. Make sure "Access Token" is enabled
8. Click on "Save"

#### Verifying your domain property for production ready TikTok callback for Oauth

<img width="1657" alt="Screenshot 2024-11-12 at 5 36 16 PM" src="https://github.com/user-attachments/assets/f553f945-3567-4657-845e-957dca2d3894">

<img width="1659" alt="Screenshot 2024-11-12 at 6 00 24 PM" src="https://github.com/user-attachments/assets/a6bf8ff4-15c9-4724-9128-882bafa5c1bd">

<img width="1680" alt="Screenshot 2024-11-12 at 6 05 32 PM (2)" src="https://github.com/user-attachments/assets/1d8488a3-3485-408e-b52f-c7cf6cf613c8">


<img width="1644" alt="Screenshot 2024-11-12 at 6 05 38 PM" src="https://github.com/user-attachments/assets/424ca2c2-c6f5-4dd8-9557-8cbc842850e6">

<img width="1671" alt="Screenshot 2024-11-12 at 6 25 43 PM" src="https://github.com/user-attachments/assets/666cb892-abba-4011-8f6d-7740f66badf6">


#### Creating a developer app with your instagram account and getting an access token

1. Go to the [Instagram Developer Portal](https://developers.facebook.com/apps/) and log in with your Facebook account
2. Click on "Create"
3. Fill out the required information and click on "Create"
4. In the sidebar on the left, click on "Settings"
5. In the "Valid OAuth redirect URIs" field, add `https://localhost:8000/redirect`
6. In the sidebar on the left, click on "Products"
7. Click on "Add Product" and select "Instagram"
8. In the sidebar on the left, click on "Tools"

<img width="1680" alt="Screenshot 2024-11-11 at 2 07 10 PM" src="https://github.com/user-attachments/assets/7bcac868-0269-4e59-a892-087235ac51dd">

<img width="1680" alt="Screenshot 2024-11-11 at 2 07 27 PM" src="https://github.com/user-attachments/assets/72b8cbe9-19fd-47f3-8c54-d3d7c7405409">


#### We'll need to take all of the information you just created and put it in the `backend/.env` file 

In the root of the project with the following names (case sensitive):

- TIKTOK_CLIENT_KEY
- TIKTOK_CLIENT_SECRET
- TIKTOK_REDIRECT_URI
- OPENAI_API_KEY
- INSTAGRAM_TOKEN


![Roc - Upwork Agency Banner](https://github.com/user-attachments/assets/79467e15-71b8-44ed-be35-d69701179169)



### Additional Deployment Steps

For local testing:
```
# Build locally
docker build -t chat-image-generator ./backend

# Run locally
docker run -p 8080:8080 chat-image-generator
```

Add environment variables in Cloud Run (if needed):
```
gcloud run services update chat-image-generator \
  --platform managed \
  --region us-central1 \
  --set-env-vars "KEY=value"
```

Set up continuous deployment (optional):
Create a cloudbuild.yaml file:
```
steps:
  # Build the container image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/chat-image-generator', './backend']
  
  # Push the container image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/chat-image-generator']
  
  # Deploy to Cloud Run
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'chat-image-generator'
      - '--image'
      - 'gcr.io/$PROJECT_ID/chat-image-generator'
      - '--platform'
      - 'managed'
      - '--region'
      - 'us-central1'
      - '--allow-unauthenticated'
```

Monitor the build:
```
# View logs
gcloud beta logging tail

# View service details
gcloud run services describe chat-image-generator --platform managed --region us-**central1**
```
# futureproof-content-automation
