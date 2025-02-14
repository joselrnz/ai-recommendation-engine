import boto3
import sagemaker
from sagemaker.amazon.amazon_estimator import image_uris

# Initialize SageMaker session
sagemaker_session = sagemaker.Session()
role = "arn:aws:iam::123456789012:role/SageMakerRole"

# Get built-in factorization machine algorithm image
image_uri = image_uris.retrieve(region=sagemaker_session.boto_region_name, framework='factorization-machines')

# Define training parameters
estimator = sagemaker.estimator.Estimator(
    image_uri=image_uri,
    role=role,
    instance_count=1,
    instance_type='ml.m5.large',
    sagemaker_session=sagemaker_session
)

# Set hyperparameters
estimator.set_hyperparameters(feature_dim=10, predictor_type='binary_classifier', mini_batch_size=100)

# Train the model using S3 dataset
s3_input_train = sagemaker.inputs.TrainingInput("s3://your-bucket/train-data/", content_type="csv")
estimator.fit({'train': s3_input_train})

# Deploy model
predictor = estimator.deploy(instance_type='ml.m5.large', initial_instance_count=1)
