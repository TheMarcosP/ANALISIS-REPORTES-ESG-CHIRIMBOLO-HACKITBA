import boto3
import time
import os

# Initialize the boto3 clients for Textract and S3
textract = boto3.client('textract', region_name='us-east-2')  # specify your region
s3 = boto3.client('s3')

def upload_to_s3(pdf_file_path, bucket_name, s3_key):
    """Upload PDF file to S3"""
    with open(pdf_file_path, 'rb') as data:
        s3.upload_fileobj(data, bucket_name, s3_key)

def extract_text_from_pdf(pdf_file_path, bucket_name, s3_key):
    # Upload the PDF to S3 first
    upload_to_s3(pdf_file_path, bucket_name, s3_key)

    # Call Textract to start analyzing the document
    response = textract.start_document_text_detection(
        DocumentLocation={'S3Object': {'Bucket': bucket_name, 'Name': s3_key}}
    )

    # Extract the JobId from the response
    job_id = response['JobId']
    print(f"Started job with ID: {job_id}")

    # Poll for the job result until it's done
    while True:
        result = textract.get_document_text_detection(JobId=job_id)
        status = result['JobStatus']

        if status == 'SUCCEEDED':
            print("Text extraction succeeded.")
            break
        elif status == 'FAILED':
            print("Text extraction failed.")
            break
        else:
            # Job still in progress, wait a few seconds before checking again
            print("In progress, waiting...")
            time.sleep(5)

    # Now that the job is done, process the result
    pages = result['Blocks']
    extracted_text = ''
    
    # Iterate through the blocks and extract the text
    for page in pages:
        if page['BlockType'] == 'LINE':
            extracted_text += page['Text'] + '\n'

    return extracted_text

# Path to your PDF file
pdf_file_path = os.path.join("data", "reports", 'testPdf.pdf')  # Replace with your PDF file path
bucket_name = 'hackitba2025chirimbucket'  # Specify your S3 bucket name
s3_key = 'testPdf.pdf'  # Specify the S3 key (filename) for the uploaded PDF

# Extract text from the PDF
extracted_text = extract_text_from_pdf(pdf_file_path, bucket_name, s3_key)

# Print the extracted text
print(extracted_text)
