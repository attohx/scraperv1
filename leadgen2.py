import requests
import re
import os
import urllib.parse
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import ttkbootstrap as tb

class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Easy Web Scraper with Image Download")

        self.setup_ui()

    def setup_ui(self):
        # Theme
        self.style = tb.Style(theme="darkly")

        # URL Input
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.pack(fill="x")

        ttk.Label(input_frame, text="Enter URL:", font=("Arial", 12)).pack(side="left")
        self.url_entry = ttk.Entry(input_frame, width=50)
        self.url_entry.pack(side="left", padx=5)

        # Scrape Type
        self.scrape_type = ttk.Combobox(input_frame, values=["Emails", "Phone Numbers", "URLs", "Images"], state="readonly")
        self.scrape_type.pack(side="left", padx=5)
        self.scrape_type.current(0)

        # Scrape Button
        scrape_btn = ttk.Button(input_frame, text="Scrape", command=self.scrape)
        scrape_btn.pack(side="left", padx=5)

        # Output Area
        self.output = scrolledtext.ScrolledText(self.root, height=20, font=("Courier", 10))
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

    def scrape(self):
        url = self.url_entry.get()
        if not url.startswith("http"):
            url = "http://" + url

        try:
            response = requests.get(url, timeout=10)
            content = response.text

            scraped_data = []

            if self.scrape_type.get() == "Emails":
                scraped_data = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", content)
            elif self.scrape_type.get() == "Phone Numbers":
                scraped_data = re.findall(r"\b\d{10,15}\b", content)
            elif self.scrape_type.get() == "URLs":
                scraped_data = re.findall(r"https?://[^\s\"'>]+", content)
            elif self.scrape_type.get() == "Images":
                scraped_data = re.findall(r'<img[^>]+src="([^">]+)"', content)
                self.download_images(scraped_data, url)

            self.output.delete(1.0, tk.END)
            if scraped_data:
                for item in scraped_data:
                    self.output.insert(tk.END, item + "\n")
            else:
                self.output.insert(tk.END, "No data found.")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to scrape: {e}")

    def download_images(self, image_urls, base_url):
        if not os.path.exists("downloaded_images"):
            os.makedirs("downloaded_images")

        for idx, img_url in enumerate(image_urls):
            img_url = urllib.parse.urljoin(base_url, img_url)  # handle relative URLs
            try:
                img_data = requests.get(img_url, timeout=10).content
                ext = os.path.splitext(img_url)[-1]
                if not ext or len(ext) > 5:
                    ext = ".jpg"
                filename = f"downloaded_images/image_{idx+1}{ext}"
                with open(filename, "wb") as f:
                    f.write(img_data)
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = WebScraperApp(root)
    root.geometry("800x600")
    root.mainloop()
