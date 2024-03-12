import os
import platform
import torch
from torchvision import transforms
from PIL import ImageGrab, Image, ImageDraw, ImageFont
import pyautogui
import time
import psutil

print(platform.platform())


class Watcher:

    def __init__(self, model_path=None):
        self.model = None
        self.class_weights = {"reddit": 2, "facebook": 2, "settings": 0.5}
        if model_path:
            self.device = torch.device(
                "cuda:0" if torch.cuda.is_available() else "cpu")
            self.model = torch.hub.load("WongKinYiu/yolov7",
                                        "custom",
                                        f"{model_path}",
                                        trust_repo=True)
            # self.model = torch.hub.load("WongKinYiu/yolov7", "custom", model_path, force_reload=True, trust_repo=True)
            self.model.eval()
            print("model success")

    def get_running_programs(self):
        result = []
        for process in psutil.process_iter(["pid", "name"]):
            result.append(process.info["name"])
        return result

    def get_mac_application_list(self):
        applications_path = "/Applications"
        apps = os.listdir(applications_path)

        installed_programs = []
        for app in apps:
            if app.endswith(".app"):
                installed_programs.append(app)

        return sorted(installed_programs)

    def is_program_running(self, target):
        for process in psutil.process_iter(["pid", "name"]):
            if process.info["name"] == target:
                return True
        return False

    def kill_program(self, target):
        if self.is_program_running(target):
            if "Windows" in platform.platform():
                os.system(f"taskkill /f /im {target}")
            else:
                os.system(f"pkill -f {target}")
        else:
            print(f"The program {target} is not running.")

    def kill_focused_program(self):
        if "Windows" in platform.platform():
            pyautogui.hotkey('alt', 'f4')
        else:
            pyautogui.hotkey('command', 'q', interval=0.25)
            time.sleep(1)
            pyautogui.press('return')

    def _create_screenshot_directory(self):
        if not os.path.exists("screenshots"):
            os.mkdir("screenshots")

    def take_screenshot(self, filename, analyze=False):
        self._create_screenshot_directory()
        filename = f"screenshots/{filename}.png"

        time.sleep(3)

        # screenshot whole screen
        screenshot = ImageGrab.grab()

        print("Took a screenshot!")

        result = None

        # save file
        screenshot.save(filename)

        if analyze:
            result = self._analyze_image(filename, draw_results=True)

        return result

    def _analyze_image(self,
                       image_path,
                       draw_results=False,
                       confidence_threshold=0.8):
        if self.model:
            results = self.model(image_path)
            items = results.pandas().xyxy[0]
            print(items)

            result = set()

            try:
                if draw_results:
                    # Load Image
                    image = Image.open(image_path)
                    draw = ImageDraw.Draw(image)

                    # # Define font
                    # font_size = 20
                    # font = ImageFont.truetype("DejaVuSans.ttf", font_size)

                    # Draw boxes and labels
                    for idx, row in items.iterrows():
                        # Extract info
                        xmin, ymin, xmax, ymax = row["xmin"], row["ymin"], row[
                            "xmax"], row["ymax"]
                        label = row["name"]
                        confidence = row["confidence"]

                        # Draw rectangle
                        draw.rectangle([(xmin, ymin), (xmax, ymax)],
                                       outline="red",
                                       width=2)

                        # Draw label and confidence
                        text = f"{label} {confidence:.2f}"
                        draw.text((xmin, ymin), text, "red")

                        if confidence >= confidence_threshold:
                            result.add(label)

                    image.save("screenshots/detected_" +
                               os.path.basename(image_path))
                else:
                    for item in items:
                        if (item['confidence'].values[0]
                                >= confidence_threshold):
                            result.add(item['name'].values[0])
            except Exception as e:
                pass

            print(f"RESULTS: {list(result)}")
            return list(result)
        print("No model currently active.")
        return []

    # take_screenshot("screenshots/captureTest.png")


# watcher = Watcher()
# watcher.kill_program("Spotify")
# print("done")
