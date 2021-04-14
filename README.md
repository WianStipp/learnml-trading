# LearnMLTrading

LearnMLTrading is a series where we build and deploy a machine learning trading algorithm to the cloud. Each week there is a new [video](https://youtu.be/NhcvShzRgE8) & [blog post](https://learnml.co.uk/blog/) released.

## Documentation

To link to the docs can be found [here](https://wianstipp.github.io/LearnMLTrading/).

## Environment Variables

You need to make an environment variable script to set the environment variables, such as usernames and API tokens. For example:

1.  Create a file env_vars.sh

         vim env_vars.sh

2.  Insert the following into the file:

        export PYTHONPATH="."

        export OANDA_ACCOUNT_NUMBER=""

        export OANDA_API_TOKEN=""

3. Then run:

    
        source env_vars.sh
