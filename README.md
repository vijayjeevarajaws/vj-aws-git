
# Bedrock Quota Mapping
Maps AWS Bedrock service quotas to their associated foundation models, providing a way to understand the relationship between quotas and models.

## Overview

The `extract_model_name_from_quota` function takes a quota name and removes any common prefixes that might precede the model name. This helps to extract the actual model name from the quota name.

The `map_bedrock_quotas_to_models` function is the main functionality of the code. It:

1. Initializes boto3 clients for the Service Quotas and Bedrock services.
2. Retrieves the list of service quotas for the Bedrock service.
3. Retrieves the list of foundation models from the Bedrock service.
4. Iterates through the service quotas, extracts the model name from the quota name, and finds the matching foundation model.
5. Creates a dictionary mapping the quota information (ARN, code, name, value, unit) to the model information (ARN, ID, name).
6. Returns the list of mapped quota-model pairs.

The `main` function is the entry point that calls the `map_bedrock_quotas_to_models` function and prints the results as JSON.
