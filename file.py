import json

class Book:
    def __init__(self, name, tag, image):
        self.__name = name
        self.__tag = tag
        self.__image = image
    
    @property
    def name(self):
      return self.__name
    
    
        
    
    def __str__(self):
        return f'Book: {self.__name} ({self.__tag})'
      
      
class BookEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Book):
      return{
        'name': obj.name,
        'tag': obj.tag,
        'image' : obj.image
      }   
    return super().default(obj) 
      

    
    
class Library:
    def __init__(self):
        self.__books = []
        
    def add_book(self, book):
        self.__books.append(book)
        
    def display_books(self):
        for book in self.__books:
            print(book)
            
    def remove_book(self, name):
      book_to_delete = None
      for book in self.__books:
        if(book.name == name):
          book_to_delete = book
      self.__books.remove(book_to_delete)
      
    def save(self):
      with open('lib.json', 'w') as output:
        save_str = json.dumps(self.__books)
        output.write(save_str)    
    
          
        
        
if __name__ == '__main__':
    lib=Library()
    lib.display_books()
    lib.add_book(Book('fondation', 'sf', 'path/to/image'))
    lib.add_book(Book('swan song', 'sf', 'path/to/image'))
    lib.display_books()
    lib.remove_book('swan song')
    lib.display_books()