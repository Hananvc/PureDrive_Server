from celery import shared_task
from django.db.utils import IntegrityError  # Import IntegrityError
from .models import News
import requests
import logging


logger = logging.getLogger(__name__)

@shared_task
def fetch_and_store_news():
    try:
        logger.info("Entered the task")

        api_key = 'ca789e9ab879409488626410ac1186ad'
        api_url = f'https://newsapi.org/v2/everything?q=electric%20vehicle&apiKey={api_key}'
        response = requests.get(api_url)
        news_data = response.json().get('articles', [])
        logger.info(news_data)

        if not news_data:
            logger.info("API response does not contain news data. Skipping addition.")
            return {'message': 'API response does not contain news data.'}

        # Clear existing news data
        News.objects.all().delete()
        logger.info("Cleared existing news data")

        news_added = 0
        max_news_count = 100

        for article in news_data:
            if news_added >= max_news_count:
                logger.info("Maximum news limit reached. Stopping further addition.")
                break
            
            try:
                News.objects.create(
                    title=article['title'],
                    description=article['description'],
                    url=article['url'],
                    url_to_image=article['urlToImage'],
                )
                news_added += 1
            except IntegrityError as e:
                logger.error('Error adding news article:', exc_info=True)
                continue  # Skip this article and continue with the next
            
        logger.info(f"Added {news_added} new news articles")
        return {'message': f'Added {news_added} news articles.'}
    except Exception as e:
        logger.error('Error fetching and storing news data.', exc_info=True)
        return {'message': 'Error fetching and storing news data.', 'error': str(e)}
