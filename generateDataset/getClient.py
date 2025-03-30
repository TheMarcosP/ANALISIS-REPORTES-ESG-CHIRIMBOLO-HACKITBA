from openai import OpenAI # pip install openai

# read key from file
# the key is how we authenticate with the openai api
def getClient(path):
    """
    Initializes and returns an OpenAI client using an API key stored in a local file.
    The function reads the API key from a file named "openai_key.txt" located in the 
    current working directory. It then uses this key to initialize an OpenAI client.
    Returns:
        OpenAI: An instance of the OpenAI client initialized with the API key.
    Raises:
        FileNotFoundError: If the "openai_key.txt" file is not found.
        IOError: If there is an issue reading the "openai_key.txt" file.
    """

    with open(path, "r") as file:
        key = file.read().replace('\n', '')

    # Initialize OpenAI client with the API key
    client = OpenAI(
        api_key=key
    )

    return client