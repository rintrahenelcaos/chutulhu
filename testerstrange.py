# Server Class with Log Register

class Server:
    def __init__(self):
        self.log = []

    def register_log(self, message):
        self.log.append(message)
        print(f"Log registered: {message}")

    def display_logs(self):
        for entry in self.log:
            print(entry)

# Example usage
if __name__ == "__main__":
    server = Server()
    server.register_log("Server started.")
    server.register_log("Client connected.")
    server.display_logs()
