from dataclasses import dataclass
import boto3
import sagemaker
from sagemaker.amazon.amazon_estimator import image_uris
from typing import Optional, Dict

@dataclass
class SageMakerConfig:
    account_id: str
    region: str = boto3.Session().region_name
    role_name: str = "SageMakerRole"
    instance_type: str = "ml.m5.large"
    instance_count: int = 1

    @property
    def role_arn(self) -> str:
        return f"arn:aws:iam::{self.account_id}:role/{self.role_name}"

class FactorizationMachineModel:
    def __init__(self, config: SageMakerConfig):
        self.config = config
        self.session = sagemaker.Session()
        self.estimator = None
        self.predictor = None
        
        self._validate_aws_resources()
        
    def _validate_aws_resources(self):
        """Check for required AWS resources"""
        if not self.config.account_id.isdigit() or len(self.config.account_id) != 12:
            raise ValueError("Invalid AWS account ID format")
            
        # Add additional resource checks here if needed

    def _get_image_uri(self) -> str:
        """Retrieve algorithm container image URI"""
        return image_uris.retrieve(
            region=self.config.region,
            framework='factorization-machines'
        )

    def initialize_estimator(self, hyperparameters: Dict):
        """Create and configure the SageMaker estimator"""
        self.estimator = sagemaker.estimator.Estimator(
            image_uri=self._get_image_uri(),
            role=self.config.role_arn,
            instance_count=self.config.instance_count,
            instance_type=self.config.instance_type,
            sagemaker_session=self.session
        )
        self.estimator.set_hyperparameters(**hyperparameters)

    def train(self, train_data_path: str, content_type: str = "csv"):
        """Launch training job"""
        if not self.estimator:
            raise RuntimeError("Estimator not initialized. Call initialize_estimator() first")
            
        train_input = sagemaker.inputs.TrainingInput(
            train_data_path,
            content_type=content_type
        )
        self.estimator.fit({'train': train_input})

    def deploy(self) -> sagemaker.predictor.Predictor:
        """Deploy model to SageMaker endpoint"""
        if not self.estimator:
            raise RuntimeError("No trained model available. Train first.")
            
        self.predictor = self.estimator.deploy(
            initial_instance_count=self.config.instance_count,
            instance_type=self.config.instance_type
        )
        return self.predictor

    def delete_endpoint(self):
        """Clean up deployed endpoint"""
        if self.predictor:
            self.predictor.delete_endpoint()
            self.predictor = None

class ModelFactory:
    @staticmethod
    def create_factorization_machine(config: SageMakerConfig, feature_dim: int) -> FactorizationMachineModel:
        """Factory method for creating configured Factorization Machine model"""
        model = FactorizationMachineModel(config)
        model.initialize_estimator({
            'feature_dim': feature_dim,
            'predictor_type': 'binary_classifier',
            'mini_batch_size': 100
        })
        return model

# Example usage
if __name__ == "__main__":
    # Configuration
    config = SageMakerConfig(
        account_id="YOUR_AWS_ACCOUNT_ID",
        instance_type="ml.m5.xlarge"
    )

    try:
        # Create model using factory
        model = ModelFactory.create_factorization_machine(
            config=config,
            feature_dim=10
        )

        # Train and deploy
        model.train("s3://your-bucket/path/to/train-data/")
        predictor = model.deploy()

  
        
    finally:
        # Cleanup resources
        model.delete_endpoint()