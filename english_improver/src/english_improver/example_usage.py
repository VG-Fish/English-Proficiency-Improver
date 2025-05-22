from gutenberg_scraper import GutenbergScraper
from markov_chain_generator import MarkovChainGenerator
from pdf_generator import PDFGenerator
from asyncio import run

async def main() -> None:
    scraper: GutenbergScraper = GutenbergScraper("data.txt")
    await scraper.save_book_texts(amount=200, overwrite_file=True)

    markov_chain_generator: MarkovChainGenerator = MarkovChainGenerator("data.txt", "generated.txt", 1000)
    markov_chain_generator.generate_text(overwrite_file=True)

    pdf_generator: PDFGenerator = PDFGenerator("generated.txt", "output.pdf")
    pdf_generator.generate_pdf()

if __name__ == "__main__":
    run(main())
