import os
import sys

# Import expert service package
dir_expert_service = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../../expert-service/"
)
sys.path.append(dir_expert_service)
