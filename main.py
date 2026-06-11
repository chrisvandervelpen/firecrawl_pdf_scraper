import os
import re
from firecrawl import Firecrawl
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file if it exists
load_dotenv()

def scrape_pdfs(pdf_urls, output_dir=r"C:\temp\scraped_pdfs"):
    # Initialize the FirecrawlApp with your API key
    # It will automatically look for the FIRECRAWL_API_KEY environment variable
    # but you can also pass it explicitly.
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print("Error: FIRECRAWL_API_KEY not found. Please set it in your environment or .env file.")
        return

    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Saving results to: {output_path.absolute()}")

    app = Firecrawl(api_key=api_key)

    results = []

    for url in pdf_urls:
        print(f"Scraping: {url}...")
        try:
            # scrape_url is the method to get content from a specific URL
            # For PDFs, it will return the markdown representation of the PDF content
            scrape_result = app.scrape(url)
            
            if scrape_result:
                markdown_content = scrape_result.markdown
                metadata = scrape_result.metadata
                
                results.append({
                    "url": url,
                    "markdown": markdown_content,
                    "metadata": metadata
                })

                # Generate a safe filename from the URL
                filename = re.sub(r'[^\w\s-]', '_', url.split('/')[-1])
                if not filename.endswith('.md'):
                    filename += '.md'
                
                file_path = output_path / filename
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"# Scraped from: {url}\n\n")
                    f.write(markdown_content)
                
                print(f"Successfully scraped and saved: {filename}")
            else:
                print(f"Failed to scrape {url}: No result returned.")
        
        except Exception as e:
            print(f"An error occurred while scraping {url}: {e}")

    return results

if __name__ == "__main__":
    # Example list of PDF URLs
    # Replace these with your actual PDF URLs
    urls_to_scrape = [
        "https://www.sfonds200.be/media/lagdhff2/2021-11-18-eindejaarspremie.pdf", "https://www.sfonds200.be/media/2lofrsjd/2021-11-18-koopkracht-aanvullend-pensioen.pdf", "https://www.sfonds200.be/media/kbcjylah/2021-11-18-koopkracht.pdf", "https://www.sfonds200.be/media/jvzcnzje/2021-11-18-vervoerskosten.pdf", "https://www.sfonds200.be/media/jaanif0r/20150401-statutensf.pdf", "https://www.sfonds200.be/media/is5o5b0w/20150709-cp-pc200-cct-cao-jaarlijskepremieannuelle.pdf", "https://www.sfonds200.be/media/h3qdu3uj/20160609-statuutsyndicaledelegatie.pdf", "https://www.sfonds200.be/media/kkhfpo0i/20160609-syndicalevorming.pdf", "https://www.sfonds200.be/media/lmvg1rpv/20160609-nieuwearbeidsregimes.pdf", "https://www.sfonds200.be/media/frxfk5tg/20160609-collectiefontslag.pdf"
    ]

    output_directory = r"C:\temp\scraped_pdfs"
    scraped_data = scrape_pdfs(urls_to_scrape, output_dir=output_directory)
