import cloudinary
from django.conf import settings
# Configuration    

def cloud_init():   
    cloudinary.config( 
        cloud_name = settings.CLOUD_NAME, 
        api_key = settings.API_KEY,
        api_secret = settings.API_SECRET, # Click 'View API Keys' above to copy your API secret
        secure=True
    )

