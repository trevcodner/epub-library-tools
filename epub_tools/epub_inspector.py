import os
from ebooklib import epub
from pathlib import Path

class EpubInspector:
    def __init__(self, book_path):
        """Initialize with path to epub file"""
        self.book_path = Path(book_path)
        self.book = None
    
    def load_book(self):
        """Load the epub file and return basic info"""
        try:
            self.book = epub.read_epub(str(self.book_path))
            return {
                'filename': self.book_path.name,
                'title': self.get_metadata('title'),
                'author': self.get_metadata('creator'),
                'language': self.get_metadata('language'),
                'has_cover': self.has_cover_image()
            }
        except Exception as e:
            return f"Error loading {self.book_path.name}: {str(e)}"
    
    def get_metadata(self, field):
        """Safely extract metadata field"""
        if self.book:
            metadata = self.book.get_metadata('DC', field)
            return metadata[0][0] if metadata else "Not found"
        return None
    
    def has_cover_image(self):
        """Check if book has a cover image"""
        if self.book:
            for item in self.book.get_items():
                if item.get_type() == ebooklib.ITEM_COVER:
                    return True
        return False

def main():
    """Main function to demonstrate usage"""
    script_dir = Path(__file__).parent.parent
    sample_dir = script_dir / 'sample_books'
    
    if not any(sample_dir.iterdir()):
        print(f"\nPlease add some epub files to the {sample_dir} directory")
        return
    
    print("\nAnalyzing EPUB files...\n")
    
    for epub_path in sample_dir.glob('*.epub'):
        inspector = EpubInspector(epub_path)
        info = inspector.load_book()
        
        if isinstance(info, dict):
            print(f"\nFile: {info['filename']}")
            print(f"Title: {info['title']}")
            print(f"Author: {info['author']}")
            print(f"Language: {info['language']}")
            print(f"Has cover: {'Yes' if info['has_cover'] else 'No'}")
            print("-" * 50)
        else:
            print(info)

if __name__ == "__main__":
    main()
