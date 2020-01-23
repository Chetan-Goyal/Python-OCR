import requests

def ocr_space_file(filename, overlay=False, api_key='get_it_from_"ocr.space"', language='eng'):
    '''
    Purpose: To read text from an image

    Variables Used:
            1. payload : It is the data sent to the api url to get response.
                         It contains some variables to be used to while recognizing text.

                         The data which can be passed to it is described below-
                            1. isOverlayRequired - do we need bounding boxes?
                                                   default- False
                            2. apikey - get from https://ocr.space
                                        ~MUST~
                            3. language - short form of language of text to be recognized
                                          default- 'en'
                            4. detectOrientation - could image bse rotated?
                                                   default- False
                            5. scale - Do image need some enhancements?
                                       default- False
                            6. OCREngine -  1. fast but less accuracy
                                            2. slow but good accuracy

    Return : string of response data in json format
    '''

    # making a dict of the data we need for our request
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'detectOrientation': True,
               'scale': True,
               'OCREngine': 2,
               }

    # Making request with data assigned above
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )

    # returning data received from the request
    # Format- json data as string
    return r.content.decode()



if __name__ == "__main__":

    # Initializing image path to temporary variables
    file_path = 'Sample_Images/test.png'

    # Calling Functions
    test_file = ocr_space_file(filename=file_path)

    # Loading Json data
    import json
    data_test_file = json.loads(test_file)

    # Printing Results
    print('\n----------------TEST FILE---------------\n')
    print(data_test_file['ParsedResults'][0]['ParsedText'])
