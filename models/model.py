import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

class FoodClassifier:
    def __init__(self, model_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load the saved data (math + names)
        checkpoint = torch.load(model_path, self.device)
        self.class_names = checkpoint['classes']
        
        # Build the ResNet18 skeleton
        self.model = models.resnet18()
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, len(self.class_names))
        
        # Inject the knowledge and set to evaluation mode
        self.model.load_state_dict(checkpoint['state'])
        self.model.to(self.device)
        self.model.eval()
        
        # Set up the 'Eyes' (Preprocessing)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def predict(self, image_path):
        # Open and transform the JPEG
        img = Image.open(image_path).convert('RGB')
        img_tensor = self.transform(img).unsqueeze(0).to(self.device)
        
        # Run the math
        with torch.no_grad():
            outputs = self.model(img_tensor)
            # Convert scores to percentages (Softmax)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
            confidence, index = torch.max(probabilities, 0)
            
        return {
            "food": self.class_names[index.item()],
            "confidence": confidence.item() * 100.00
        }

if __name__ == "__main__":
    # Create the machine (only happens once)
    my_ai = FoodClassifier('food_model.pth')
    
    # Now you can use it on any image you want
    result = my_ai.predict('testimg.jpg')
    print(f"Result: {result['food']} ({result['confidence']})")
