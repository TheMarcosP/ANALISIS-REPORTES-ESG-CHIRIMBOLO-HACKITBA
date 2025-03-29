# AWS Textract PDF Module

import boto3
import time
import os


def upload_to_s3(pdf_file_path, bucket_name, s3_key):
    """
    Uploads a PDF file to an AWS S3 bucket.

    Args:
        pdf_file_path (str): The local file path of the PDF to be uploaded.
        bucket_name (str): The name of the S3 bucket where the file will be uploaded.
        s3_key (str): The key (path) within the S3 bucket where the file will be stored.

    Raises:
        botocore.exceptions.BotoCoreError: If there is an error during the upload process.
        botocore.exceptions.ClientError: If there is a client-side error during the upload process.
    """
    # Initialize aws S3
    s3 = boto3.client('s3')
    """Upload PDF file to S3"""
    with open(pdf_file_path, 'rb') as data:
        s3.upload_fileobj(data, bucket_name, s3_key)

def extract_text_from_pdf(pdf_file_path):
    """
    Extracts text from a PDF file using AWS Textract.
    This function uploads the specified PDF file to an S3 bucket, initiates a text detection job
    using AWS Textract, and retrieves the extracted text once the job is complete.
    Args:
        pdf_file_path (str): The local file path of the PDF to be processed.
    Returns:
        str: The extracted text from the PDF.
    Raises:
        Exception: If the text extraction job fails or encounters an error.
    Notes:
        - Ensure that AWS CLI is configured with the necessary permissions to access Textract and S3.
        - The function polls the job status every 20 seconds until the job is completed.
    """

    # Bucket name and S3 key from the file path
    bucket_name = 'hackitba2025chirimbucket'  # Specify your S3 bucket name
    s3_key = os.path.basename(pdf_file_path)  # Use the filename as the S3 key

    # Initialize AWS Textract client
    textract = boto3.client('textract', region_name='us-east-2')  # specify your region
    # Upload the PDF to S3 first
    upload_to_s3(pdf_file_path, bucket_name, s3_key)

    # Call Textract to start analyzing the document
    response = textract.start_document_text_detection(
        DocumentLocation={'S3Object': {'Bucket': bucket_name, 'Name': s3_key}}
    )

    # Extract the JobId from the response
    job_id = response['JobId']
    print(f"[*] Started job with ID: {job_id}...")

    # Poll for the job result until it's done
    while True:
        result = textract.get_document_text_detection(JobId=job_id)
        status = result['JobStatus']

        if status == 'SUCCEEDED':
            print("[+] Text extraction succeeded.")
            break
        elif status == 'FAILED':
            print("[x] Text extraction failed.")
            raise Exception("Text extraction failed: " + result['StatusMessage'])
        else:
            # Job still in progress, wait a few seconds before checking again
            print("[*] In progress, waiting...")
            time.sleep(40)

    # Now that the job is done, process the result
    pages = result['Blocks']
    extracted_text = ''
    
    # Iterate through the blocks and extract the text
    for page in pages:
        if page['BlockType'] == 'LINE':
            extracted_text += page['Text'] + '\n'

    return extracted_text



if __name__ == "__main__":
    # Path to your PDF file
    name = "testPdf"
    pdf_file_path = os.path.join("data", "reports", name + '.pdf')  # Replace with your PDF file path

    # Extract text from the PDF
    extracted_text = extract_text_from_pdf(pdf_file_path)

    # Print the extracted text
    print(extracted_text)

    # save to file 
    with open("outputTextract.txt", "w", encoding="utf-8") as f:
        f.write(extracted_text)
