import boto3
import re
import json


def extract_model_name_from_quota(quota_name):
    """
    Extract model name from QuotaName by removing common prefixes
    """
    # Remove common prefixes that might precede the model name
    prefixes = [
        r'^Batch inference job size \(in GB\) for ',
        r'^Maximum number of ',
        r'^Concurrent ',
        r'^Number of ',
        r'^Maximum '
    ]
    
    for prefix in prefixes:
        model_name = re.sub(prefix, '', quota_name, flags=re.IGNORECASE)
        if model_name != quota_name:
            return model_name.strip()
    
    return quota_name.strip()

def map_bedrock_quotas_to_models():
    """
    Map Bedrock service quotas to foundation models
    """
    # Initialize boto3 clients
    service_quotas_client = boto3.client('service-quotas')
    bedrock_client = boto3.client('bedrock')
    
    # Retrieve service quotas for Bedrock
    quotas_response = service_quotas_client.list_aws_default_service_quotas(
        ServiceCode='bedrock',
        MaxResults=100  # Adjust as needed to retrieve all quotas
    )
    #print(json.dumps(quotas_response, indent=2))


    # Retrieve foundation models
    models_response = bedrock_client.list_foundation_models()
    

    # Mapping results
    mapped_quotas = []
    
    # Iterate through quotas
    for quota in quotas_response.get('Quotas', []):
        # Extract model name from quota name
        quota_model_name = extract_model_name_from_quota(quota['QuotaName'])
        
        # Find matching model
        matching_models = [
            model for model in models_response.get('modelSummaries', [])
            if model['modelName'].lower() == quota_model_name.lower()
        ]
        
        # If a matching model is found
        for model in matching_models:
            mapped_quota = {
                'QuotaArn': quota['QuotaArn'],
                'QuotaCode': quota['QuotaCode'],
                'QuotaName': quota['QuotaName'],
                'QuotaValue': quota['Value'],
                'QuotaUnit': quota['Unit'],
                'ModelArn': model['modelArn'],
                'ModelId': model['modelId'],
                'ModelName': model['modelName']
            }
            mapped_quotas.append(mapped_quota)
    
    return mapped_quotas

def main():
    try:
        # Map quotas to models
        mapped_results = map_bedrock_quotas_to_models()
        
        # Print results
        import json
        print(json.dumps(mapped_results, indent=2))
    
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
