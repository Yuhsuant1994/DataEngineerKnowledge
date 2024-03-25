# yolov5_runnable.py
import bentoml

class Yolov5Runnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", "cpu")
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        import torch

        self.model = torch.hub.load("ultralytics/yolov5:v6.2", "yolov5s")

        if torch.cuda.is_available():
            self.model.cuda()
        else:
            self.model.cpu()

        self.inference_size = 320

    @bentoml.Runnable.method(batchable=True, batch_dim=0)
    def inference(self, input_imgs):
        results = self.model(input_imgs, size=self.inference_size)
        return results.pandas().xyxy

    @bentoml.Runnable.method(batchable=True, batch_dim=0)
    # def render(self, input_imgs):
    #     return self.model(input_imgs, size=self.inference_size).render()
    # Inside the Yolov5Runnable class, when you're about to render boxes and labels
    def render(self, input_imgs):
        # Assuming `input_imgs` is a list of images you want to process
        
        writable_imgs = [img.copy() for img in input_imgs]  # Create writable copies
        # Use writable_imgs with the model for rendering
        results = self.model(writable_imgs, size=self.inference_size)
        rendered_imgs = results.render()
        
        # Ensure rendered_imgs are writable if further modification is needed
        rendered_imgs = [img.copy() for img in rendered_imgs]
        return rendered_imgs

