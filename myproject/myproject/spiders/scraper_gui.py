import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import json

class ScraperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Web Scraper GUI")

        self.url_label = tk.Label(master, text="Enter URL to scrape:")
        self.url_label.pack()

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        self.scrape_button = tk.Button(master, text="Scrape", command=self.scrape)
        self.scrape_button.pack()

        self.convert_button = tk.Button(master, text="Convert to Markdown", command=self.convert_to_markdown)
        self.convert_button.pack()

        self.view_button = tk.Button(master, text="View Results", command=self.view_results)
        self.view_button.pack()

    def scrape(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        try:
            subprocess.run(["scrapy", "crawl", "example", "-a", f"start_urls={url}", "-O", "output.json"], check=True)
            messagebox.showinfo("Success", "Scraping completed. Output saved to output.json")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Scraping failed. Check your Scrapy setup.")

    def convert_to_markdown(self):
        try:
            with open('output.json', 'r') as f:
                data = json.load(f)

            markdown_content = f"# {data[0]['title']}\n\n"
            for section in data[0]['content']:
                markdown_content += f"## {section['section']}\n\n{section['content']}\n\n"

            with open('output.md', 'w') as f:
                f.write(markdown_content)

            messagebox.showinfo("Success", "Converted to Markdown. Saved as output.md")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")

    def view_results(self):
        try:
            with open('output.json', 'r') as f:
                data = json.load(f)

            view_window = tk.Toplevel(self.master)
            view_window.title("Scraped Results")

            text_widget = tk.Text(view_window, wrap=tk.WORD)
            text_widget.pack(expand=True, fill='both')

            text_widget.insert(tk.END, json.dumps(data, indent=2))
            text_widget.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot view results: {str(e)}")

root = tk.Tk()
gui = ScraperGUI(root)
root.mainloop()