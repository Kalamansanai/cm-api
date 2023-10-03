from cm_config import Logger
from google.cloud import vision


def detect_text(img_content, char_num):
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=img_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    result = None
    for text in texts:
        if text != None and (len(text.description) == char_num):
            result = text.description
        Logger.info(
            f"text found: {text.description} --- length: {len(text.description)}"
        )

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    Logger.info(f"detected text: {result}")
    return result
