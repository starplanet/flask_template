import requests

from proj.extensions import celery
from proj.utils.mail import send_task_status_email


@celery.task
def download_result(download_url, email):
    result_file = 'result_file' + '.tar.gz'
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(result_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
    send_task_status_email(status='download success', email=email)
