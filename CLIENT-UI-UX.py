class ClientUI:
    def display_menu(self):
        print("1. Add Server")
        print("2. Exit")

    def add_server(self):
        server_address = input("Enter server address: ")
        server_port = int(input("Enter server port: "))
        return server_address, server_port

    def user_feedback(self, message):
        print(f"[INFO] {message}")
