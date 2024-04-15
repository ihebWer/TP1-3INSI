import json
import socketserver

class Book:
    def __init__(self, name, tag, image):
        self.__name = name
        self.__tag = tag
        self.__image = image

    @property
    def name(self):
        return self.__name
    
    @property
    def image(self):
        return self.__image
    
    @property
    def tag(self):
        return self.__tag

    def __str__(self):
        return f'Book: {self.__name} ({self.__tag})'

class BookEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Book):
            return {
                'name': obj.name,
                'tag': obj.tag,
                'image': obj.image
            }
        return super().default(obj)

class Library:
    def __init__(self):
        self.__books = []

    def add_book(self, book):
        self.__books.append(book)

    def display_books(self):
        if not self.__books:
            return "La bibliothèque est vide."
        else:
            books_info = '\n'.join(str(book) for book in self.__books)
            return f'Livres dans la bibliothèque:\n{books_info}'

    def remove_book(self, name):
        for book in self.__books:
            if book.name == name:
                self.__books.remove(book)
                return f"Livre '{name}' supprimé de la bibliothèque."
        return f"Livre '{name}' non trouvé dans la bibliothèque."

    def save(self):
        with open('bib.json', 'w') as output:
            save_str = json.dumps(self.__books, cls=BookEncoder)
            output.write(save_str)

class Server(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        command = self.data.decode("utf-8")
        print("Received from {}:".format(self.client_address[0]))
        print(command)
        
        response = self.process_command(command)
        self.request.sendall(response.encode("utf-8"))

    def process_command(self, command):
        parts = command.split()
        if not parts:
            return "Commande invalide."

        action = parts[0]
        if action == "ADD":
            if len(parts) != 4:
                return "Usage: ADD <name> <tag> <image>"
            name, tag, image = parts[1], parts[2], parts[3]
            book = Book(name, tag, image)
            library.add_book(book)
            return f"Livre '{name}' ajouté à la bibliothèque."
        elif action == "REMOVE":
            if len(parts) != 2:
                return "Usage: REMOVE <name>"
            name = parts[1]
            return library.remove_book(name)
        elif action == "DISPLAY":
            return library.display_books()
        else:
            return "Commande inconnue."

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    library = Library()
    
    with socketserver.TCPServer((HOST, PORT), Server) as server:
        print(f"Serveur démarré sur {HOST}:{PORT}")
        server.serve_forever()
