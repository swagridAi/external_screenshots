# Managing API Keys and Secrets

This document explains how to properly manage API keys and other sensitive information in the Screenshot to Table application.

## Why API Keys Should Be Protected

- **Security**: API keys provide access to services and should be kept private
- **Cost Management**: Exposed keys could be used by others, potentially incurring charges
- **Version Control**: API keys should never be committed to version control systems
- **Compliance**: Many organizations require proper handling of credentials

## Setup Options

The application supports two methods for providing API keys:

### Option 1: Using secrets.py (Preferred)

1. Copy the template file to create your own secrets file:
   ```bash
   cp secrets.py.example secrets.py
   ```

2. Edit `secrets.py` and add your actual OpenAI API key:
   ```python
   OPENAI_API_KEY = "sk-your_actual_openai_key_here"
   ```

3. The `.gitignore` file is configured to exclude `secrets.py` from git, so it won't be committed.

### Option 2: Using Environment Variables

1. Copy the template `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and set your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your_actual_openai_key_here
   ```

3. The `.gitignore` file excludes `.env` from git.

## Precedence Order

The application checks for API keys in this order:
1. First, it tries to load from `secrets.py` (if it exists)
2. If not found, it falls back to environment variables or `.env` file
3. If still not found, warnings will be logged

## Additional Notes

- Never share screenshots containing your API keys
- Rotate API keys periodically for better security
- Consider using API key management services for production environments
- You can check your configuration is valid by running:
  ```python
  python -c "from config import CONFIG_VALID; print('Configuration valid:', CONFIG_VALID)"
  ```

## Troubleshooting

If you encounter errors related to missing API keys:

1. Verify that you've created either `secrets.py` or `.env` with your API key
2. Check for any error messages in the application logs
3. Test your API key directly with the OpenAI API to ensure it's valid
4. Make sure the application has read permissions for your configuration files