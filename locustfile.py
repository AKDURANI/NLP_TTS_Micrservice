from locust import HttpUser, task, between
import os

class TTSUser(HttpUser):
    wait_time = between(1, 3)  # Simulate user think time

    @task(2)
    def upload_pdf(self):
        """Uploads RichDadPoorDad.pdf to the /upload endpoint."""
        file_path = "RichDadPoorDad.pdf"
        if not os.path.exists(file_path):
            print("RichDadPoorDad.pdf not found in directory.")
            return

        with open(file_path, "rb") as f:
            response = self.client.post(
                "/upload",
                files={"file": ("RichDadPoorDad.pdf", f, "application/pdf")},
                data={"start_page": 1, "end_page": 2}
            )
            print(f"Upload status: {response.status_code}")

    @task(1)
    def check_audio_files(self):
        """Checks if audio files were generated."""
        self.client.get("/get_audio_files")